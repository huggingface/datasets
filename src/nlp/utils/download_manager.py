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

from .checksums_utils import load_sizes_checksums, store_sizes_checksum
from .file_utils import HF_DATASETS_CACHE, cached_path, get_size_checksum
from .py_utils import flatten_nest_dict, map_nested
from .checksums_utils import URLS_CHECKSUMS_FOLDER_NAME, CHECKSUMS_FILE_NAME

logger = logging.getLogger(__name__)


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


class DownloadConfig(object):
    """Configuration for `nlp.DatasetBuilder.download_and_prepare`."""

    def __init__(
        self,
        manual_dir=None,
        download_mode=None,
        max_examples_per_split=None,
        ignore_checksums=False,
        register_checksums=False,
        sizes_checksums=None,
        beam_runner=None,
        beam_options=None,
    ):
        """Constructs a `DownloadConfig`.

        Args:
            manual_dir: `str`, read-only directory where manually downloaded/extracted
                data is stored. Defaults to
                "<download_dir>/manual".
            download_mode: `nlp.GenerateMode`, how to deal with downloads or data
                that already exists. Defaults to `REUSE_DATASET_IF_EXISTS`, which will
                reuse both downloads and data if it already exists.
            max_examples_per_split: `int`, optional max number of examples to write
                into each split (used for testing).
            ignore_checksums: `bool`, defaults to False. If True, wrong or missing checksums
                will be ignored.
            register_checkums: `bool`, defaults to False. If True, the checksums of the
                downloaded files will be saved in the `urls_checksums` folder
            beam_runner: Runner to pass to `beam.Pipeline`, only used for datasets
                based on Beam for the generation.
            beam_options: `PipelineOptions` to pass to `beam.Pipeline`, only used for
                datasets based on Beam for the generation.
        """
        self.manual_dir = manual_dir
        self.download_mode = GenerateMode(download_mode or GenerateMode.REUSE_DATASET_IF_EXISTS)
        self.max_examples_per_split = max_examples_per_split
        self.ignore_checksums = ignore_checksums
        self.register_checksums = register_checksums
        self.sizes_checksums = sizes_checksums
        self.beam_runner = beam_runner
        self.beam_options = beam_options


class DownloadManager(object):
    def __init__(
        self,
        download_dir=None,
        manual_dir=None,
        manual_dir_instructions=None,
        dataset_name=None,
        force_download=False,
        ignore_checksums=False,
        register_checksums=False,
    ):
        """Download manager constructor.

        Args:
            download_dir: `str`, path to directory where downloads are stored.
            extract_dir: `str`, path to directory where artifacts are extracted.
            manual_dir: `str`, path to manually downloaded/extracted data directory.
            manual_dir_instructions: `str`, human readable instructions on how to
                                                 prepare contents of the manual_dir for this dataset.
            dataset_name: `str`, name of dataset this instance will be used for. If
                provided, downloads will contain which datasets they were used for.
            force_download: `bool`, default to False. If True, always [re]download.
            ignore_checksums: `bool`, defaults to False. If True, wrong or missing checksums
                will be ignored.
            register_checkums: `bool`, defaults to False. If True, the checksums of the
                downloaded files will be saved in the `urls_checksums` folder
        """
        self._dataset_name = dataset_name
        if download_dir is None:
            download_dir = HF_DATASETS_CACHE
        self._download_dir = download_dir
        self._manual_dir = manual_dir and os.path.expanduser(manual_dir)
        self._manual_dir_instructions = manual_dir_instructions
        os.makedirs(self._download_dir, exist_ok=True)
        self._force_download = force_download
        self._ignore_checksums = ignore_checksums
        self._register_checksums = register_checksums
        if ignore_checksums and register_checksums:
            raise ValueError("Parameters `ignore_checksums` and `register_checksums` "
            "shouldn't be True at the same time.")
        # To record what is being used: {url: (size, checksum)}
        self._recorded_sizes_checksums = {}
    
    @property
    def downloaded_size(self):
        """Returns the total size of downloaded files."""
        return sum(size for size, sha256 in self._recorded_sizes_checksums.values())

    def _record_sizes_checksums(self, url_or_urls, downloaded_path_or_paths):
        """Record size/checksum of downloaded files."""
        if isinstance(url_or_urls, str):
            url, path = url_or_urls, downloaded_path_or_paths
            self._recorded_sizes_checksums[url] = get_size_checksum(path)
            return
        elif isinstance(url_or_urls, dict):
            url_or_urls = list(flatten_nest_dict(url_or_urls).values())
            downloaded_path_or_paths = list(flatten_nest_dict(downloaded_path_or_paths).values())
        assert isinstance(url_or_urls, (list, tuple))
        for url, path in zip(url_or_urls, downloaded_path_or_paths):
            self._recorded_sizes_checksums[url] = get_size_checksum(path) 

    def download(self, url_or_urls):
        """Download given url(s).

        Args:
            url_or_urls: url or `list`/`dict` of urls to download and extract. Each
                url is a `str`.

        Returns:
            downloaded_path(s): `str`, The downloaded paths matching the given input
                url_or_urls.
        """
        downloaded_path_or_paths = map_nested(lambda url_or_urls: cached_path(
            url_or_urls,
            cache_dir=self._download_dir,
            force_download=self._force_download,
        ), url_or_urls)
        self._record_sizes_checksums(url_or_urls, downloaded_path_or_paths)
        return downloaded_path_or_paths

    def iter_archive(self, path):
        """Returns iterator over files within archive.

        Args:
            path: path to archive.

        Returns:
            Generator yielding tuple (path_within_archive, file_obj).
        """
        extracted_path = self.extract(path)
        if os.path.isfile(extracted_path):
            with open(extracted_path, "rb") as file_obj:
                yield (extracted_path, file_obj)
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    with open(entry.path, "rb") as file_obj:
                        yield (entry.path, file_obj)

    def extract(self, path_or_paths):
        """Extract given path(s).

        Args:
            path_or_paths: path or `list`/`dict` of path of file to extract. Each
                path is a `str`.

        Returns:
            extracted_path(s): `str`, The extracted paths matching the given input
                path_or_paths.
        """
        return map_nested(lambda path_or_paths: cached_path(
            path_or_paths,
            extract_compressed_file=True,
            force_extract=True
        ), path_or_paths)

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

    @property
    def manual_dir(self):
        """Returns the directory containing the manually extracted data."""
        if not self._manual_dir:
            raise AssertionError(
                "Manual directory was enabled. " "Did you set MANUAL_DOWNLOAD_INSTRUCTIONS in your dataset?"
            )
        if not os.path.exists(self._manual_dir):
            raise AssertionError(
                "Manual directory {} does not exist. Create it and download/extract "
                "dataset artifacts in there. Additional instructions: {}".format(
                    self._manual_dir, self._manual_dir_instructions
                )
            )
        return self._manual_dir
    
    def check_or_register_checksums(self, urls_checksums_dir):
        if not self._ignore_checksums:
            checksums_path = os.path.join(urls_checksums_dir, CHECKSUMS_FILE_NAME)
            if self._register_checksums:
                os.makedirs(urls_checksums_dir, exist_ok=True)
                self._store_sizes_checksums(checksums_path)
                logger.info("Stored the recorded checksums in {}.".format(urls_checksums_dir))
            else:
                expected_sizes_checksums = load_sizes_checksums(checksums_path)
                for url, rec_size_checksum in self._recorded_sizes_checksums.items():
                    exp_size_checksum = expected_sizes_checksums.get(url)
                    if exp_size_checksum is None:
                        raise MissingChecksumError(url)
                    if exp_size_checksum != rec_size_checksum:
                        raise NonMatchingChecksumError(url)
                logger.info("All checksums matched successfully.")
        else:
            logger.info("Checksums tests were ignored.")
    
    def _store_sizes_checksums(self, path):
        store_sizes_checksum(self.get_recorded_sizes_checksums(), path)
    
    def get_recorded_sizes_checksums(self):
        return self._recorded_sizes_checksums.copy()
