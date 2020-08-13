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
import logging
import os

from .file_utils import HF_DATASETS_CACHE, cached_path, get_from_cache, hash_url_to_filename
from .info_utils import get_size_checksum_dict
from .py_utils import flatten_nested, map_nested, size_str


logger = logging.getLogger(__name__)


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
        self, dataset_name=None, data_dir=None, download_config=None,
    ):
        """Download manager constructor.

        Args:
            data_dir: can be used to specify a manual directory to get the files from.
            cache_dir: `str`, path to directory where downloads are stored.
            extract_dir: `str`, path to directory where artifacts are extracted.
            dataset_name: `str`, name of dataset this instance will be used for. If
                provided, downloads will contain which datasets they were used for.
            force_download: `bool`, default to False. If True, always [re]download.
        """
        self._dataset_name = dataset_name
        self._data_dir = data_dir
        self._download_config = download_config
        # To record what is being used: {url: {num_bytes: int, checksum: str}}
        self._recorded_sizes_checksums = {}

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
        from nlp.utils.beam_utils import upload_local_to_remote

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

        uploaded_path_or_paths = map_nested(lambda local_file_path: upload(local_file_path), downloaded_path_or_paths,)
        return uploaded_path_or_paths

    def _record_sizes_checksums(self, url_or_urls, downloaded_path_or_paths):
        """Record size/checksum of downloaded files."""
        flattened_urls_or_urls = flatten_nested(url_or_urls)
        flattened_downloaded_path_or_paths = flatten_nested(downloaded_path_or_paths)
        for url, path in zip(flattened_urls_or_urls, flattened_downloaded_path_or_paths):
            self._recorded_sizes_checksums[url] = get_size_checksum_dict(path)

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
                get_from_cache(url, cache_dir=cache_dir, local_files_only=True)
                cached = True
            except FileNotFoundError:
                cached = False
            if not cached or self._download_config.force_download:
                custom_download(url, path)
                get_from_cache(url, cache_dir=cache_dir, local_files_only=True)
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
        downloaded_path_or_paths = map_nested(
            lambda url: cached_path(url, download_config=self._download_config,), url_or_urls,
        )
        self._record_sizes_checksums(url_or_urls, downloaded_path_or_paths)
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
            relative_dir_path = root.replace(os.path.abspath(extracted_path) + "/", "")
            for name in files:
                relative_file_path = os.path.join(relative_dir_path, name)
                absolute_file_path = os.path.join(root, name)
                with open(absolute_file_path, "rb") as file_obj:
                    yield (relative_file_path, file_obj)

    def extract(self, path_or_paths):
        """Extract given path(s).

        Args:
            path_or_paths: path or `list`/`dict` of path of file to extract. Each
                path is a `str`.

        Returns:
            extracted_path(s): `str`, The extracted paths matching the given input
                path_or_paths.
        """
        return map_nested(
            lambda path: cached_path(
                path, cache_dir=self._download_config.cache_dir, extract_compressed_file=True, force_extract=False
            ),
            path_or_paths,
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
