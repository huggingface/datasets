# coding=utf-8
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
import os
from datetime import datetime
from functools import partial
from typing import Dict, Union

from .file_utils import HF_DATASETS_CACHE, DownloadConfig, cached_path, get_from_cache, hash_url_to_filename
from .info_utils import get_size_checksum_dict
from .logging import get_logger
from .py_utils import flatten_nested, map_nested, size_str


logger = get_logger(__name__)


class GenerateMode(enum.Enum):
    """`Enum` for how to treat pre-existing downloads and data.

    The default mode is `REUSE_DATASET_IF_EXISTS`, which will reuse both
    raw downloads and the prepared dataset if they exist.

    The generations modes:

    |                                    | Downloads | Dataset |
    | -----------------------------------|-----------|---------|
    | `REUSE_DATASET_IF_EXISTS` (default)| Reuse     | Reuse   |
    | `REUSE_CACHE_IF_EXISTS`            | Reuse     | Fresh   |
    | `FORCE_REDOWNLOAD`                 | Fresh     | Fresh   |
    """

    REUSE_DATASET_IF_EXISTS = "reuse_dataset_if_exists"
    REUSE_CACHE_IF_EXISTS = "reuse_cache_if_exists"
    FORCE_REDOWNLOAD = "force_redownload"


class DownloadManager(object):
    def __init__(
        self,
        dataset_name=None,
        data_dir=None,
        download_config=None,
    ):
        """Download manager constructor.

        Args:
            data_dir: can be used to specify a manual directory to get the files from.
            dataset_name: `str`, name of dataset this instance will be used for. If
                provided, downloads will contain which datasets they were used for.
            download_config: `DownloadConfig` to specify the cache directory and other
                download options
        """
        self._dataset_name = dataset_name
        self._data_dir = data_dir
        self._download_config = download_config or DownloadConfig()
        # To record what is being used: {url: {num_bytes: int, checksum: str}}
        self._recorded_sizes_checksums: Dict[str, Dict[str, Union[int, str]]] = {}

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
            remote_file_path = os.path.join(remote_dir, "downloads", os.path.basename(local_file_path))
            logger.info(
                "Uploading {} ({}) to {}.".format(
                    local_file_path, size_str(os.path.getsize(local_file_path)), remote_file_path
                )
            )
            upload_local_to_remote(local_file_path, remote_file_path)
            return remote_file_path

        uploaded_path_or_paths = map_nested(
            lambda local_file_path: upload(local_file_path),
            downloaded_path_or_paths,
        )
        return uploaded_path_or_paths

    def _record_sizes_checksums(self, url_or_urls, downloaded_path_or_paths):
        """Record size/checksum of downloaded files."""
        flattened_urls_or_urls = flatten_nested(url_or_urls)
        flattened_downloaded_path_or_paths = flatten_nested(downloaded_path_or_paths)
        for url, path in zip(flattened_urls_or_urls, flattened_downloaded_path_or_paths):
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
        cache_dir = self._download_config.cache_dir or os.path.join(HF_DATASETS_CACHE, "downloads")

        def url_to_downloaded_path(url):
            return os.path.join(cache_dir, hash_url_to_filename(url))

        downloaded_path_or_paths = map_nested(url_to_downloaded_path, url_or_urls)
        flattened_urls_or_urls = flatten_nested(url_or_urls)
        flattened_downloaded_path_or_paths = flatten_nested(downloaded_path_or_paths)
        for url, path in zip(flattened_urls_or_urls, flattened_downloaded_path_or_paths):
            try:
                get_from_cache(url, cache_dir=cache_dir, local_files_only=True, use_etag=False)
                cached = True
            except FileNotFoundError:
                cached = False
            if not cached or self._download_config.force_download:
                custom_download(url, path)
                get_from_cache(url, cache_dir=cache_dir, local_files_only=True, use_etag=False)
        self._record_sizes_checksums(url_or_urls, downloaded_path_or_paths)
        return downloaded_path_or_paths

    def download(self, url_or_urls):
        """Download given url(s).

        Args:
            url_or_urls: url or `list`/`dict` of urls to download and extract. Each
                url is a `str`.

        Returns:
            downloaded_path(s): `str`, The downloaded paths matching the given input
                url_or_urls.
        """
        download_config = self._download_config.copy()
        download_config.extract_compressed_file = False
        # Default to using 16 parallel thread for downloading
        # Note that if we have less than 16 files, multi-processing is not activated
        if download_config.num_proc is None:
            download_config.num_proc = 16

        download_func = partial(cached_path, download_config=download_config)

        start_time = datetime.now()
        downloaded_path_or_paths = map_nested(
            download_func,
            url_or_urls,
            map_tuple=True,
            num_proc=download_config.num_proc,
        )
        duration = datetime.now() - start_time
        logger.info("Downloading took {} min".format(duration.total_seconds() // 60))

        start_time = datetime.now()
        self._record_sizes_checksums(url_or_urls, downloaded_path_or_paths)
        duration = datetime.now() - start_time
        logger.info("Checksum Computation took {} min".format(duration.total_seconds() // 60))

        return downloaded_path_or_paths

    def iter_archive(self, path):
        """Returns iterator over files within archive.

        Args:
            path: path to archive.

        Returns:
            Generator yielding tuple (path_within_archive, file_obj).
            File-Obj are opened in byte mode (io.BufferedReader)
        """
        logger.info("Extracting archive at %s", str(path))
        extracted_path = self.extract(path)
        if os.path.isfile(extracted_path):
            with open(extracted_path, "rb") as file_obj:
                yield (extracted_path, file_obj)

        # We do this complex absolute/relative scheme to reproduce the API of iter_tar of tfds
        for root, dirs, files in os.walk(extracted_path, topdown=False):
            relative_dir_path = root.replace(os.path.abspath(extracted_path) + os.sep, "")
            for name in files:
                relative_file_path = os.path.join(relative_dir_path, name)
                absolute_file_path = os.path.join(root, name)
                with open(absolute_file_path, "rb") as file_obj:
                    yield (relative_file_path, file_obj)

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
        download_config = self._download_config.copy()
        download_config.extract_compressed_file = True
        download_config.force_extract = False
        return map_nested(
            partial(cached_path, download_config=download_config),
            path_or_paths,
            num_proc=num_proc,
        )

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
