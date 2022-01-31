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
import tarfile
from datetime import datetime
from functools import partial
from typing import Dict, Optional, Union

from .. import config
from .file_utils import (
    DownloadConfig,
    cached_path,
    get_from_cache,
    hash_url_to_filename,
    is_relative_path,
    url_or_path_join,
)
from .info_utils import get_size_checksum_dict
from .logging import get_logger
from .py_utils import NestedDataStructure, map_nested, size_str


logger = get_logger(__name__)


class GenerateMode(enum.Enum):
    """`Enum` for how to treat pre-existing downloads and data.

    The default mode is `REUSE_DATASET_IF_EXISTS`, which will reuse both
    raw downloads and the prepared dataset if they exist.

    The generations modes:

    +------------------------------------+-----------+---------+
    |                                    | Downloads | Dataset |
    +====================================+===========+=========+
    | `REUSE_DATASET_IF_EXISTS` (default)| Reuse     | Reuse   |
    +------------------------------------+-----------+---------+
    | `REUSE_CACHE_IF_EXISTS`            | Reuse     | Fresh   |
    +------------------------------------+-----------+---------+
    | `FORCE_REDOWNLOAD`                 | Fresh     | Fresh   |
    +------------------------------------+-----------+---------+
    """

    REUSE_DATASET_IF_EXISTS = "reuse_dataset_if_exists"
    REUSE_CACHE_IF_EXISTS = "reuse_cache_if_exists"
    FORCE_REDOWNLOAD = "force_redownload"


class DownloadManager:
    def __init__(
        self,
        dataset_name: Optional[str] = None,
        data_dir: Optional[str] = None,
        download_config: Optional[DownloadConfig] = None,
        base_path: Optional[str] = None,
    ):
        """Download manager constructor.

        Args:
            data_dir: can be used to specify a manual directory to get the files from.
            dataset_name: `str`, name of dataset this instance will be used for. If
                provided, downloads will contain which datasets they were used for.
            download_config: `DownloadConfig` to specify the cache directory and other
                download options
            base_path: `str`, base path that is used when relative paths are used to
                download files. This can be a remote url.
        """
        self._dataset_name = dataset_name
        self._data_dir = data_dir
        self._base_path = base_path or os.path.abspath(".")
        # To record what is being used: {url: {num_bytes: int, checksum: str}}
        self._recorded_sizes_checksums: Dict[str, Dict[str, Union[int, str]]] = {}
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

    def ship_files_with_pipeline(self, downloaded_path_or_paths, pipeline):
        """
        Ship the files using Beam FileSystems to the pipeline temp dir.
        """
        from datasets.utils.beam_utils import upload_local_to_remote

        remote_dir = pipeline._options.get_all_options().get("temp_location")
        if remote_dir is None:
            raise ValueError("You need to specify 'temp_location' in PipelineOptions to upload files")

        def upload(local_file_path):
            remote_file_path = os.path.join(
                remote_dir, config.DOWNLOADED_DATASETS_DIR, os.path.basename(local_file_path)
            )
            logger.info(
                f"Uploading {local_file_path} ({size_str(os.path.getsize(local_file_path))}) to {remote_file_path}."
            )
            upload_local_to_remote(local_file_path, remote_file_path)
            return remote_file_path

        uploaded_path_or_paths = map_nested(
            lambda local_file_path: upload(local_file_path), downloaded_path_or_paths, disable_tqdm=False
        )
        return uploaded_path_or_paths

    def _record_sizes_checksums(self, url_or_urls: NestedDataStructure, downloaded_path_or_paths: NestedDataStructure):
        """Record size/checksum of downloaded files."""
        for url, path in zip(url_or_urls.flatten(), downloaded_path_or_paths.flatten()):
            # call str to support PathLike objects
            self._recorded_sizes_checksums[str(url)] = get_size_checksum_dict(path)

    def download_custom(self, url_or_urls, custom_download):
        """
        Download given urls(s) by calling `custom_download`.

        Args:
            url_or_urls: url or `list`/`dict` of urls to download and extract. Each
                url is a `str`.
            custom_download: Callable with signature (src_url: str, dst_path: str) -> Any
                as for example `tf.io.gfile.copy`, that lets you download from google storage

        Returns:
            downloaded_path(s): `str`, The downloaded paths matching the given input
                url_or_urls.
        """
        cache_dir = self.download_config.cache_dir or config.DOWNLOADED_DATASETS_PATH
        max_retries = self.download_config.max_retries

        def url_to_downloaded_path(url):
            return os.path.join(cache_dir, hash_url_to_filename(url))

        downloaded_path_or_paths = map_nested(url_to_downloaded_path, url_or_urls, disable_tqdm=False)
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
        """Download given url(s).

        Args:
            url_or_urls: url or `list`/`dict` of urls to download and extract. Each
                url is a `str`.

        Returns:
            downloaded_path(s): `str`, The downloaded paths matching the given input
                url_or_urls.
        """
        download_config = self.download_config.copy()
        download_config.extract_compressed_file = False
        # Default to using 16 parallel thread for downloading
        # Note that if we have less than 16 files, multi-processing is not activated
        if download_config.num_proc is None:
            download_config.num_proc = 16

        download_func = partial(self._download, download_config=download_config)

        start_time = datetime.now()
        downloaded_path_or_paths = map_nested(
            download_func, url_or_urls, map_tuple=True, num_proc=download_config.num_proc, disable_tqdm=False
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
            path_or_buf (:obj:`str` or :obj:`io.BufferedReader`): Archive path or archive binary file object.

        Yields:
            :obj:`tuple`[:obj:`str`, :obj:`io.BufferedReader`]: 2-tuple (path_within_archive, file_object).
                File object is opened in binary mode.
        """

        def _iter_archive(f):
            stream = tarfile.open(fileobj=f, mode="r|*")
            for tarinfo in stream:
                file_path = tarinfo.name
                if not tarinfo.isreg():
                    continue
                if file_path is None:
                    continue
                if os.path.basename(file_path).startswith(".") or os.path.basename(file_path).startswith("__"):
                    # skipping hidden files
                    continue
                file_obj = stream.extractfile(tarinfo)
                yield file_path, file_obj
                stream.members = []
            del stream

        if hasattr(path_or_buf, "read"):
            yield from _iter_archive(path_or_buf)
        else:
            with open(path_or_buf, "rb") as f:
                yield from _iter_archive(f)

    def iter_files(self, paths):
        """Iterate over file paths.

        Args:
            paths (list): Root paths.

        Yields:
            str: File path.
        """
        for path in paths:
            if os.path.isfile(path):
                yield path
            else:
                for dirpath, _, filenames in os.walk(path):
                    for filename in filenames:
                        yield os.path.join(dirpath, filename)

    def extract(self, path_or_paths, num_proc=None):
        """Extract given path(s).

        Args:
            path_or_paths: path or `list`/`dict` of path of file to extract. Each
                path is a `str`.
            num_proc: Use multi-processing if `num_proc` > 1 and the length of
                `path_or_paths` is larger than `num_proc`

        Returns:
            extracted_path(s): `str`, The extracted paths matching the given input
                path_or_paths.
        """
        download_config = self.download_config.copy()
        download_config.extract_compressed_file = True
        extracted_paths = map_nested(
            partial(cached_path, download_config=download_config), path_or_paths, num_proc=num_proc, disable_tqdm=False
        )
        path_or_paths = NestedDataStructure(path_or_paths)
        extracted_paths = NestedDataStructure(extracted_paths)
        self.extracted_paths.update(dict(zip(path_or_paths.flatten(), extracted_paths.flatten())))
        return extracted_paths.data

    def download_and_extract(self, url_or_urls):
        """Download and extract given url_or_urls.

        Is roughly equivalent to:

        ```
        extracted_paths = dl_manager.extract(dl_manager.download(url_or_urls))
        ```

        Args:
            url_or_urls: url or `list`/`dict` of urls to download and extract. Each
                url is a `str`.

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
