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

from .checksums_utils import CHECKSUMS_FILE_NAME, get_size_checksum, load_sizes_checksums, store_sizes_checksum
from .file_utils import cached_path, get_from_cache, url_to_filename
from .py_utils import flatten_nested, map_nested


logger = logging.getLogger(__name__)


class MissingFileError(Exception):
    """A dataset file is missing."""


class MissingChecksumError(Exception):
    """The expected checksum of the download file is missing."""


class NonMatchingChecksumError(Exception):
    """The downloaded file doesn't have expected checksum."""


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
        self, dataset_name=None, data_dir=None, ignore_checksums=False, save_checksums=False, download_config=None,
    ):
        """Download manager constructor.

        Args:
            data_dir: can be used to specify a manual directory to get the files from.
            cache_dir: `str`, path to directory where downloads are stored.
            extract_dir: `str`, path to directory where artifacts are extracted.
            dataset_name: `str`, name of dataset this instance will be used for. If
                provided, downloads will contain which datasets they were used for.
            force_download: `bool`, default to False. If True, always [re]download.
            ignore_checksums: `bool`, defaults to False. If True, wrong or missing checksums
                will be ignored.
            save_checksums: `bool`, defaults to False. If True, the checksums of the
                downloaded files will be saved in the `urls_checksums` folder
            beam_runner: Runner to pass to `beam.Pipeline`, only used for datasets
                based on Beam for the generation.
            beam_options: `PipelineOptions` to pass to `beam.Pipeline`, only used for
                datasets based on Beam for the generation.
        """
        self._dataset_name = dataset_name
        self._data_dir = data_dir
        self._download_config = download_config
        self._ignore_checksums = ignore_checksums
        self._save_checksums = save_checksums
        if ignore_checksums and save_checksums:
            raise ValueError(
                "Parameters `ignore_checksums` and `save_checksums` " "shouldn't be True at the same time."
            )
        # To record what is being used: {url: (size, checksum)}
        self._recorded_sizes_checksums = {}

    @property
    def manual_dir(self):
        return self._data_dir

    @property
    def downloaded_size(self):
        """Returns the total size of downloaded files."""
        return sum(size for size, sha256 in self._recorded_sizes_checksums.values())

    def _record_sizes_checksums(self, url_or_urls, downloaded_path_or_paths):
        """Record size/checksum of downloaded files."""
        flattened_urls_or_urls = flatten_nested(url_or_urls)
        flattened_downloaded_path_or_paths = flatten_nested(downloaded_path_or_paths)
        for url, path in zip(flattened_urls_or_urls, flattened_downloaded_path_or_paths):
            self._recorded_sizes_checksums[url] = get_size_checksum(path)

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

        def url_to_downloaded_path(url):
            return os.path.join(self._download_dir, url_to_filename(url))

        downloaded_path_or_paths = map_nested(url_to_downloaded_path, url_or_urls)
        flattened_urls_or_urls = flatten_nested(url_or_urls)
        flattened_downloaded_path_or_paths = flatten_nested(downloaded_path_or_paths)
        for url, path in zip(flattened_urls_or_urls, flattened_downloaded_path_or_paths):
            try:
                get_from_cache(url, cache_dir=self._download_dir, local_files_only=True)
                cached = True
            except FileNotFoundError:
                cached = False
            if not cached or self._force_download:
                custom_download(url, path)
                get_from_cache(url, cache_dir=self._download_dir, local_files_only=True)
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
            lambda url_or_urls: cached_path(url_or_urls, download_config=self._download_config,), url_or_urls,
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
            lambda path_or_paths: cached_path(path_or_paths, extract_compressed_file=True, force_extract=True),
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

    def check_or_save_checksums(self, urls_checksums_dir):
        if not self._ignore_checksums:
            checksums_file_path = os.path.join(urls_checksums_dir, CHECKSUMS_FILE_NAME)
            if self._save_checksums:
                os.makedirs(urls_checksums_dir, exist_ok=True)
                self._store_sizes_checksums(checksums_file_path)
                logger.info("Stored the recorded checksums in {}.".format(urls_checksums_dir))
            elif os.path.exists(checksums_file_path):
                expected_sizes_checksums = load_sizes_checksums(checksums_file_path)
                for url, rec_size_checksum in self._recorded_sizes_checksums.items():
                    exp_size_checksum = expected_sizes_checksums.get(url)
                    if exp_size_checksum is None:
                        raise MissingChecksumError(url)
                    if exp_size_checksum != rec_size_checksum:
                        raise NonMatchingChecksumError(url)
                logger.info("All checksums matched successfully.")
            else:
                logger.info("Checksum file not found.")
        else:
            logger.info("Checksums tests were ignored.")

    def _store_sizes_checksums(self, path):
        store_sizes_checksum(self.get_recorded_sizes_checksums(), path)

    def get_recorded_sizes_checksums(self):
        return self._recorded_sizes_checksums.copy()
