# Copyright 2020 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Download manager interface."""

import enum
import io
import os
import posixpath
import tarfile
import warnings
import zipfile
from datetime import datetime
from functools import partial
from itertools import chain
from typing import Callable, Dict, Generator, Iterable, List, Optional, Tuple, Union

from .. import config
from ..utils.deprecation_utils import DeprecatedEnum
from ..utils.file_utils import cached_path, get_from_cache, hash_url_to_filename, is_relative_path, url_or_path_join
from ..utils.info_utils import get_size_checksum_dict
from ..utils.logging import get_logger, is_progress_bar_enabled, tqdm
from ..utils.py_utils import NestedDataStructure, map_nested, size_str
from .download_config import DownloadConfig


logger = get_logger(__name__)


BASE_KNOWN_EXTENSIONS = [
    "txt",
    "csv",
    "json",
    "jsonl",
    "tsv",
    "conll",
    "conllu",
    "orig",
    "parquet",
    "pkl",
    "pickle",
    "rel",
    "xml",
]
MAGIC_NUMBER_TO_COMPRESSION_PROTOCOL = {
    bytes.fromhex("504B0304"): "zip",
    bytes.fromhex("504B0506"): "zip",  # empty archive
    bytes.fromhex("504B0708"): "zip",  # spanned archive
    bytes.fromhex("425A68"): "bz2",
    bytes.fromhex("1F8B"): "gzip",
    bytes.fromhex("FD377A585A00"): "xz",
    bytes.fromhex("04224D18"): "lz4",
    bytes.fromhex("28B52FFD"): "zstd",
}
MAGIC_NUMBER_TO_UNSUPPORTED_COMPRESSION_PROTOCOL = {
    b"Rar!": "rar",
}
MAGIC_NUMBER_MAX_LENGTH = max(
    len(magic_number)
    for magic_number in chain(MAGIC_NUMBER_TO_COMPRESSION_PROTOCOL, MAGIC_NUMBER_TO_UNSUPPORTED_COMPRESSION_PROTOCOL)
)


class DownloadMode(enum.Enum):
    """`Enum` for how to treat pre-existing downloads and data.

    The default mode is `REUSE_DATASET_IF_EXISTS`, which will reuse both
    raw downloads and the prepared dataset if they exist.

    The generations modes:

    |                                     | Downloads | Dataset |
    |-------------------------------------|-----------|---------|
    | `REUSE_DATASET_IF_EXISTS` (default) | Reuse     | Reuse   |
    | `REUSE_CACHE_IF_EXISTS`             | Reuse     | Fresh   |
    | `FORCE_REDOWNLOAD`                  | Fresh     | Fresh   |

    """

    REUSE_DATASET_IF_EXISTS = "reuse_dataset_if_exists"
    REUSE_CACHE_IF_EXISTS = "reuse_cache_if_exists"
    FORCE_REDOWNLOAD = "force_redownload"


class GenerateMode(DeprecatedEnum):
    REUSE_DATASET_IF_EXISTS = "reuse_dataset_if_exists"
    REUSE_CACHE_IF_EXISTS = "reuse_cache_if_exists"
    FORCE_REDOWNLOAD = "force_redownload"

    @property
    def help_message(self):
        return "Use 'DownloadMode' instead."


def _get_path_extension(path: str) -> str:
    # Get extension: train.json.gz -> gz
    extension = path.split(".")[-1]
    # Remove query params ("dl=1", "raw=true"): gz?dl=1 -> gz
    # Remove shards infos (".txt_1", ".txt-00000-of-00100"): txt_1 -> txt
    for symb in "?-_":
        extension = extension.split(symb)[0]
    return extension


def _get_extraction_protocol_with_magic_number(f) -> Optional[str]:
    """read the magic number from a file-like object and return the compression protocol"""
    # Check if the file object is seekable even before reading the magic number (to avoid https://bugs.python.org/issue26440)
    try:
        f.seek(0)
    except (AttributeError, io.UnsupportedOperation):
        return None
    magic_number = f.read(MAGIC_NUMBER_MAX_LENGTH)
    f.seek(0)
    for i in range(MAGIC_NUMBER_MAX_LENGTH):
        compression = MAGIC_NUMBER_TO_COMPRESSION_PROTOCOL.get(magic_number[: MAGIC_NUMBER_MAX_LENGTH - i])
        if compression is not None:
            return compression
        compression = MAGIC_NUMBER_TO_UNSUPPORTED_COMPRESSION_PROTOCOL.get(magic_number[: MAGIC_NUMBER_MAX_LENGTH - i])
        if compression is not None:
            raise NotImplementedError(f"Compression protocol '{compression}' not implemented.")


def _get_extraction_protocol(path: str) -> Optional[str]:
    path = str(path)
    extension = _get_path_extension(path)
    # TODO(mariosasko): The below check will be useful once we can preserve the original extension in the new cache layout (use the `filename` parameter of `hf_hub_download`)
    if (
        extension in BASE_KNOWN_EXTENSIONS
        or extension in ["tgz", "tar"]
        or path.endswith((".tar.gz", ".tar.bz2", ".tar.xz"))
    ):
        return None
    with open(path, "rb") as f:
        return _get_extraction_protocol_with_magic_number(f)


class _IterableFromGenerator(Iterable):
    """Utility class to create an iterable from a generator function, in order to reset the generator when needed."""

    def __init__(self, generator: Callable, *args, **kwargs):
        self.generator = generator
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        yield from self.generator(*self.args, **self.kwargs)


class ArchiveIterable(_IterableFromGenerator):
    """An iterable of (path, fileobj) from a TAR archive, used by `iter_archive`"""

    @staticmethod
    def _iter_tar(f):
        stream = tarfile.open(fileobj=f, mode="r|*")
        for tarinfo in stream:
            file_path = tarinfo.name
            if not tarinfo.isreg():
                continue
            if file_path is None:
                continue
            if os.path.basename(file_path).startswith((".", "__")):
                # skipping hidden files
                continue
            file_obj = stream.extractfile(tarinfo)
            yield file_path, file_obj
            stream.members = []
        del stream

    @staticmethod
    def _iter_zip(f):
        zipf = zipfile.ZipFile(f)
        for member in zipf.infolist():
            file_path = member.filename
            if member.is_dir():
                continue
            if file_path is None:
                continue
            if os.path.basename(file_path).startswith((".", "__")):
                # skipping hidden files
                continue
            file_obj = zipf.open(member)
            yield file_path, file_obj

    @classmethod
    def _iter_from_fileobj(cls, f) -> Generator[Tuple, None, None]:
        compression = _get_extraction_protocol_with_magic_number(f)
        if compression == "zip":
            yield from cls._iter_zip(f)
        else:
            yield from cls._iter_tar(f)

    @classmethod
    def _iter_from_path(cls, urlpath: str) -> Generator[Tuple, None, None]:
        compression = _get_extraction_protocol(urlpath)
        with open(urlpath, "rb") as f:
            if compression == "zip":
                yield from cls._iter_zip(f)
            else:
                yield from cls._iter_tar(f)

    @classmethod
    def from_buf(cls, fileobj) -> "ArchiveIterable":
        return cls(cls._iter_from_fileobj, fileobj)

    @classmethod
    def from_path(cls, urlpath_or_buf) -> "ArchiveIterable":
        return cls(cls._iter_from_path, urlpath_or_buf)


class FilesIterable(_IterableFromGenerator):
    """An iterable of paths from a list of directories or files"""

    @classmethod
    def _iter_from_paths(cls, urlpaths: Union[str, List[str]]) -> Generator[str, None, None]:
        if not isinstance(urlpaths, list):
            urlpaths = [urlpaths]
        for urlpath in urlpaths:
            if os.path.isfile(urlpath):
                if os.path.basename(urlpath).startswith((".", "__")):
                    # skipping hidden files
                    return
                yield urlpath
            else:
                for dirpath, dirnames, filenames in os.walk(urlpath):
                    # skipping hidden directories; prune the search
                    # [:] for the in-place list modification required by os.walk
                    dirnames[:] = sorted([dirname for dirname in dirnames if not dirname.startswith((".", "__"))])
                    if os.path.basename(dirpath).startswith((".", "__")):
                        # skipping hidden directories
                        continue
                    for filename in sorted(filenames):
                        if filename.startswith((".", "__")):
                            # skipping hidden files
                            continue
                        yield os.path.join(dirpath, filename)

    @classmethod
    def from_paths(cls, urlpaths) -> "FilesIterable":
        return cls(cls._iter_from_paths, urlpaths)


class DownloadManager:
    is_streaming = False

    def __init__(
        self,
        dataset_name: Optional[str] = None,
        data_dir: Optional[str] = None,
        download_config: Optional[DownloadConfig] = None,
        base_path: Optional[str] = None,
        record_checksums=True,
    ):
        """Download manager constructor.

        Args:
            data_dir:
                can be used to specify a manual directory to get the files from.
            dataset_name (`str`):
                name of dataset this instance will be used for. If
                provided, downloads will contain which datasets they were used for.
            download_config (`DownloadConfig`):
                to specify the cache directory and other
                download options
            base_path (`str`):
                base path that is used when relative paths are used to
                download files. This can be a remote url.
            record_checksums (`bool`, defaults to `True`):
                Whether to record the checksums of the downloaded files. If None, the value is inferred from the builder.
        """
        self._dataset_name = dataset_name
        self._data_dir = data_dir
        self._base_path = base_path or os.path.abspath(".")
        # To record what is being used: {url: {num_bytes: int, checksum: str}}
        self._recorded_sizes_checksums: Dict[str, Dict[str, Optional[Union[int, str]]]] = {}
        self.record_checksums = record_checksums
        self.download_config = download_config or DownloadConfig()
        self.downloaded_paths = {}
        self.extracted_paths = {}

    @property
    def manual_dir(self):
        return self._data_dir

    @property
    def downloaded_size(self):
        """Returns the total size of downloaded files."""
        return sum(checksums_dict["num_bytes"] for checksums_dict in self._recorded_sizes_checksums.values())

    @staticmethod
    def ship_files_with_pipeline(downloaded_path_or_paths, pipeline):
        """Ship the files using Beam FileSystems to the pipeline temp dir.

        Args:
            downloaded_path_or_paths (`str` or `list[str]` or `dict[str, str]`):
                Nested structure containing the
                downloaded path(s).
            pipeline ([`utils.beam_utils.BeamPipeline`]):
                Apache Beam Pipeline.

        Returns:
            `str` or `list[str]` or `dict[str, str]`
        """
        from ..utils.beam_utils import upload_local_to_remote

        remote_dir = pipeline._options.get_all_options().get("temp_location")
        if remote_dir is None:
            raise ValueError("You need to specify 'temp_location' in PipelineOptions to upload files")

        def upload(local_file_path):
            remote_file_path = posixpath.join(
                remote_dir, config.DOWNLOADED_DATASETS_DIR, os.path.basename(local_file_path)
            )
            logger.info(
                f"Uploading {local_file_path} ({size_str(os.path.getsize(local_file_path))}) to {remote_file_path}."
            )
            upload_local_to_remote(local_file_path, remote_file_path)
            return remote_file_path

        uploaded_path_or_paths = map_nested(
            lambda local_file_path: upload(local_file_path),
            downloaded_path_or_paths,
            disable_tqdm=not is_progress_bar_enabled(),
        )
        return uploaded_path_or_paths

    def _record_sizes_checksums(self, url_or_urls: NestedDataStructure, downloaded_path_or_paths: NestedDataStructure):
        """Record size/checksum of downloaded files."""
        delay = 5
        for url, path in tqdm(
            list(zip(url_or_urls.flatten(), downloaded_path_or_paths.flatten())),
            delay=delay,
            desc="Computing checksums",
            disable=not is_progress_bar_enabled(),
        ):
            # call str to support PathLike objects
            self._recorded_sizes_checksums[str(url)] = get_size_checksum_dict(
                path, record_checksum=self.record_checksums
            )

    def download_custom(self, url_or_urls, custom_download):
        """
        Download given urls(s) by calling `custom_download`.

        Args:
            url_or_urls (`str` or `list` or `dict`):
                URL or `list` or `dict` of URLs to download and extract. Each URL is a `str`.
            custom_download (`Callable[src_url, dst_path]`):
                The source URL and destination path. For example
                `tf.io.gfile.copy`, that lets you download from  Google storage.

        Returns:
            downloaded_path(s): `str`, The downloaded paths matching the given input
                `url_or_urls`.

        Example:

        ```py
        >>> downloaded_files = dl_manager.download_custom('s3://my-bucket/data.zip', custom_download_for_my_private_bucket)
        ```
        """
        cache_dir = self.download_config.cache_dir or config.DOWNLOADED_DATASETS_PATH
        max_retries = self.download_config.max_retries

        def url_to_downloaded_path(url):
            return os.path.join(cache_dir, hash_url_to_filename(url))

        downloaded_path_or_paths = map_nested(
            url_to_downloaded_path, url_or_urls, disable_tqdm=not is_progress_bar_enabled()
        )
        url_or_urls = NestedDataStructure(url_or_urls)
        downloaded_path_or_paths = NestedDataStructure(downloaded_path_or_paths)
        for url, path in zip(url_or_urls.flatten(), downloaded_path_or_paths.flatten()):
            try:
                get_from_cache(
                    url, cache_dir=cache_dir, local_files_only=True, use_etag=False, max_retries=max_retries
                )
                cached = True
            except FileNotFoundError:
                cached = False
            if not cached or self.download_config.force_download:
                custom_download(url, path)
                get_from_cache(
                    url, cache_dir=cache_dir, local_files_only=True, use_etag=False, max_retries=max_retries
                )
        self._record_sizes_checksums(url_or_urls, downloaded_path_or_paths)
        return downloaded_path_or_paths.data

    def download(self, url_or_urls):
        """Download given URL(s).

        By default, only one process is used for download. Pass customized `download_config.num_proc` to change this behavior.

        Args:
            url_or_urls (`str` or `list` or `dict`):
                URL or `list` or `dict` of URLs to download. Each URL is a `str`.

        Returns:
            `str` or `list` or `dict`:
                The downloaded paths matching the given input `url_or_urls`.

        Example:

        ```py
        >>> downloaded_files = dl_manager.download('https://storage.googleapis.com/seldon-datasets/sentence_polarity_v1/rt-polaritydata.tar.gz')
        ```
        """
        download_config = self.download_config.copy()
        download_config.extract_compressed_file = False
        if download_config.download_desc is None:
            download_config.download_desc = "Downloading data"

        download_func = partial(self._download, download_config=download_config)

        start_time = datetime.now()
        downloaded_path_or_paths = map_nested(
            download_func,
            url_or_urls,
            map_tuple=True,
            num_proc=download_config.num_proc,
            disable_tqdm=not is_progress_bar_enabled(),
            desc="Downloading data files",
        )
        duration = datetime.now() - start_time
        logger.info(f"Downloading took {duration.total_seconds() // 60} min")
        url_or_urls = NestedDataStructure(url_or_urls)
        downloaded_path_or_paths = NestedDataStructure(downloaded_path_or_paths)
        self.downloaded_paths.update(dict(zip(url_or_urls.flatten(), downloaded_path_or_paths.flatten())))

        start_time = datetime.now()
        self._record_sizes_checksums(url_or_urls, downloaded_path_or_paths)
        duration = datetime.now() - start_time
        logger.info(f"Checksum Computation took {duration.total_seconds() // 60} min")

        return downloaded_path_or_paths.data

    def _download(self, url_or_filename: str, download_config: DownloadConfig) -> str:
        url_or_filename = str(url_or_filename)
        if is_relative_path(url_or_filename):
            # append the relative path to the base_path
            url_or_filename = url_or_path_join(self._base_path, url_or_filename)
        return cached_path(url_or_filename, download_config=download_config)

    def iter_archive(self, path_or_buf: Union[str, io.BufferedReader]):
        """Iterate over files within an archive.

        Args:
            path_or_buf (`str` or `io.BufferedReader`):
                Archive path or archive binary file object.

        Yields:
            `tuple[str, io.BufferedReader]`:
                2-tuple (path_within_archive, file_object).
                File object is opened in binary mode.

        Example:

        ```py
        >>> archive = dl_manager.download('https://storage.googleapis.com/seldon-datasets/sentence_polarity_v1/rt-polaritydata.tar.gz')
        >>> files = dl_manager.iter_archive(archive)
        ```
        """

        if hasattr(path_or_buf, "read"):
            return ArchiveIterable.from_buf(path_or_buf)
        else:
            return ArchiveIterable.from_path(path_or_buf)

    def iter_files(self, paths: Union[str, List[str]]):
        """Iterate over file paths.

        Args:
            paths (`str` or `list` of `str`):
                Root paths.

        Yields:
            `str`: File path.

        Example:

        ```py
        >>> files = dl_manager.download_and_extract('https://huggingface.co/datasets/beans/resolve/main/data/train.zip')
        >>> files = dl_manager.iter_files(files)
        ```
        """
        return FilesIterable.from_paths(paths)

    def extract(self, path_or_paths, num_proc="deprecated"):
        """Extract given path(s).

        Args:
            path_or_paths (path or `list` or `dict`):
                Path of file to extract. Each path is a `str`.
            num_proc (`int`):
                Use multi-processing if `num_proc` > 1 and the length of
                `path_or_paths` is larger than `num_proc`.

                <Deprecated version="2.6.2">

                Pass `DownloadConfig(num_proc=<num_proc>)` to the initializer instead.

                </Deprecated>

        Returns:
            extracted_path(s): `str`, The extracted paths matching the given input
            path_or_paths.

        Example:

        ```py
        >>> downloaded_files = dl_manager.download('https://storage.googleapis.com/seldon-datasets/sentence_polarity_v1/rt-polaritydata.tar.gz')
        >>> extracted_files = dl_manager.extract(downloaded_files)
        ```
        """
        if num_proc != "deprecated":
            warnings.warn(
                "'num_proc' was deprecated in version 2.6.2 and will be removed in 3.0.0. Pass `DownloadConfig(num_proc=<num_proc>)` to the initializer instead.",
                FutureWarning,
            )
        download_config = self.download_config.copy()
        download_config.extract_compressed_file = True
        # Extract downloads the file first if it is not already downloaded
        if download_config.download_desc is None:
            download_config.download_desc = "Downloading data"
        extracted_paths = map_nested(
            partial(cached_path, download_config=download_config),
            path_or_paths,
            num_proc=download_config.num_proc,
            disable_tqdm=not is_progress_bar_enabled(),
            desc="Extracting data files",
        )
        path_or_paths = NestedDataStructure(path_or_paths)
        extracted_paths = NestedDataStructure(extracted_paths)
        self.extracted_paths.update(dict(zip(path_or_paths.flatten(), extracted_paths.flatten())))
        return extracted_paths.data

    def download_and_extract(self, url_or_urls):
        """Download and extract given `url_or_urls`.

        Is roughly equivalent to:

        ```
        extracted_paths = dl_manager.extract(dl_manager.download(url_or_urls))
        ```

        Args:
            url_or_urls (`str` or `list` or `dict`):
                URL or `list` or `dict` of URLs to download and extract. Each URL is a `str`.

        Returns:
            extracted_path(s): `str`, extracted paths of given URL(s).
        """
        return self.extract(self.download(url_or_urls))

    def get_recorded_sizes_checksums(self):
        return self._recorded_sizes_checksums.copy()

    def delete_extracted_files(self):
        paths_to_delete = set(self.extracted_paths.values()) - set(self.downloaded_paths.values())
        for key, path in list(self.extracted_paths.items()):
            if path in paths_to_delete and os.path.isfile(path):
                os.remove(path)
                del self.extracted_paths[key]

    def manage_extracted_files(self):
        if self.download_config.delete_extracted:
            self.delete_extracted_files()
