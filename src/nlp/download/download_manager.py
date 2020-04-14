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

import os
import shutil
import sys
import uuid

import logging
import promise

from .. import utils
from . import checksums
from . import downloader
from . import extractor
from . import resource as resource_lib
from . import util

logger = logging.getLogger(__name__)

class NonMatchingChecksumError(Exception):
    """The downloaded file doesn't have expected checksum."""

    def __init__(self, url, tmp_path):
        msg = 'Artifact %s, downloaded to %s, has wrong checksum.' % (url, tmp_path)
        Exception.__init__(self, msg)


class DownloadConfig(object):
    """Configuration for `nlp.DatasetBuilder.download_and_prepare`."""

    def __init__(self,
                             extract_dir=None,
                             manual_dir=None,
                             download_mode=None,
                             compute_stats=None,
                             max_examples_per_split=None,
                             register_checksums=False,
                             beam_runner=None,
                             beam_options=None):
        """Constructs a `DownloadConfig`.

        Args:
            extract_dir: `str`, directory where extracted files are stored.
                Defaults to "<download_dir>/extracted".
            manual_dir: `str`, read-only directory where manually downloaded/extracted
                data is stored. Defaults to
                "<download_dir>/manual".
            download_mode: `nlp.GenerateMode`, how to deal with downloads or data
                that already exists. Defaults to `REUSE_DATASET_IF_EXISTS`, which will
                reuse both downloads and data if it already exists.
            compute_stats: `nlp.download.ComputeStats`, whether to compute
                statistics over the generated data. Defaults to `AUTO`.
            max_examples_per_split: `int`, optional max number of examples to write
                into each split (used for testing).
            register_checksums: `bool`, defaults to False. If True, checksum of
                downloaded files are recorded.
            beam_runner: Runner to pass to `beam.Pipeline`, only used for datasets
                based on Beam for the generation.
            beam_options: `PipelineOptions` to pass to `beam.Pipeline`, only used for
                datasets based on Beam for the generation.
        """
        self.extract_dir = extract_dir
        self.manual_dir = manual_dir
        self.download_mode = util.GenerateMode(
                download_mode or util.GenerateMode.REUSE_DATASET_IF_EXISTS)
        self.compute_stats = util.ComputeStatsMode(
                compute_stats or util.ComputeStatsMode.AUTO)
        self.max_examples_per_split = max_examples_per_split
        self.register_checksums = register_checksums
        self.beam_runner = beam_runner
        self.beam_options = beam_options


class DownloadManager(object):
    """Manages the download and extraction of files, as well as caching.

    Downloaded files are cached under `download_dir`. The file name of downloaded
     files follows pattern "{sanitized_url}{content_checksum}.{ext}". Eg:
     'cs.toronto.edu_kriz_cifar-100-pythonJDF[...]I.tar.gz'.

    While a file is being downloaded, it is placed into a directory following a
    similar but different pattern:
    "{sanitized_url}{url_checksum}.tmp.{uuid}".

    When a file is downloaded, a "{fname}.INFO.json" file is created next to it.
    This INFO file contains the following information:
    {"dataset_names": ["name1", "name2"],
     "urls": ["http://url.of/downloaded_file"]}

    Extracted files/dirs are stored under `extract_dir`. The file name or
    directory name is the same as the original name, prefixed with the extraction
    method. E.g.
     "{extract_dir}/TAR_GZ.cs.toronto.edu_kriz_cifar-100-pythonJDF[...]I.tar.gz".

    The function members accept either plain value, or values wrapped into list
    or dict. Giving a data structure will parallelize the downloads.

    Example of usage:

    ```
    # Sequential download: str -> str
    train_dir = dl_manager.download_and_extract('https://abc.org/train.tar.gz')
    test_dir = dl_manager.download_and_extract('https://abc.org/test.tar.gz')

    # Parallel download: list -> list
    image_files = dl_manager.download(
            ['https://a.org/1.jpg', 'https://a.org/2.jpg', ...])

    # Parallel download: dict -> dict
    data_dirs = dl_manager.download_and_extract({
         'train': 'https://abc.org/train.zip',
         'test': 'https://abc.org/test.zip',
    })
    data_dirs['train']
    data_dirs['test']
    ```

    For more customization on the download/extraction (ex: passwords, output_name,
    ...), you can pass a `nlp.download.Resource` as argument.
    """

    def __init__(self,
                             download_dir,
                             extract_dir=None,
                             manual_dir=None,
                             manual_dir_instructions=None,
                             dataset_name=None,
                             force_download=False,
                             force_extraction=False,
                             register_checksums=False):
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
            force_extraction: `bool`, default to False. If True, always [re]extract.
            register_checksums: `bool`, default to False. If True, dl checksums aren't
                checked, but stored into file.
        """
        self._dataset_name = dataset_name
        self._download_dir = os.path.expanduser(download_dir)
        self._extract_dir = os.path.expanduser(
                extract_dir or os.path.join(download_dir, 'extracted'))
        self._manual_dir = manual_dir and os.path.expanduser(manual_dir)
        self._manual_dir_instructions = manual_dir_instructions
        os.makedirs(self._download_dir, exist_ok=True)
        os.makedirs(self._extract_dir, exist_ok=True)
        self._force_download = force_download
        self._force_extraction = force_extraction
        self._extractor = extractor.get_extractor()
        self._downloader = downloader.get_downloader()
        self._register_checksums = register_checksums
        # All known URLs: {url: (size, checksum)}
        self._sizes_checksums = {}  # checksums.get_all_sizes_checksums()
        # To record what is being used: {url: (size, checksum)}
        self._recorded_sizes_checksums = {}

    @property
    def downloaded_size(self):
        """Returns the total size of downloaded files."""
        return sum(size for size, sha256 in self._recorded_sizes_checksums.values())

    def _get_final_dl_path(self, url, sha256):
        return os.path.join(self._download_dir,
                                                resource_lib.get_dl_fname(url, sha256))

    @util.build_synchronize_decorator()
    def _record_sizes_checksums(self):
        """Store in file when recorded size/checksum of downloaded files."""
        checksums.store_checksums(self._dataset_name,self._recorded_sizes_checksums)

    def _handle_download_result(self, resource, tmp_dir_path, sha256, dl_size):
        """Store dled file to definitive place, write INFO file, return path."""
        fnames = os.listdir(tmp_dir_path)
        if len(fnames) > 1:
            raise AssertionError('More than one file in %s.' % tmp_dir_path)
        original_fname = fnames[0]
        tmp_path = os.path.join(tmp_dir_path, original_fname)
        self._recorded_sizes_checksums[resource.url] = (dl_size, sha256)
        if self._register_checksums:
            self._record_sizes_checksums()
        # TODO: add checksum checking back
        # elif (dl_size, sha256) != self._sizes_checksums.get(resource.url, None):
        #     raise NonMatchingChecksumError(resource.url, tmp_path)
        download_path = self._get_final_dl_path(resource.url, sha256)
        resource_lib.write_info_file(resource, download_path, self._dataset_name,
                                                                 original_fname)
        # Unconditionally overwrite because either file doesn't exist or
        # FORCE_DOWNLOAD=true
        os.rename(tmp_path, download_path)
        shutil.rmtree(tmp_dir_path)
        return download_path

    def download_checksums(self, checksums_url):
        """Downloads checksum file from the given URL and adds it to registry."""
        checksums_path = self.download(checksums_url)
        with open(checksums_path) as f:
            self._sizes_checksums.update(checksums.parse_sizes_checksums(f))

    # synchronize and memoize decorators ensure same resource will only be
    # processed once, even if passed twice to download_manager.
    @util.build_synchronize_decorator()
    @utils.memoize()
    def _download(self, resource):
        """Download resource, returns Promise->path to downloaded file."""
        if isinstance(resource, str):
            resource = resource_lib.Resource(url=resource)
        url = resource.url
        if url in self._sizes_checksums:
            expected_sha256 = self._sizes_checksums[url][1]
            download_path = self._get_final_dl_path(url, expected_sha256)
            if not self._force_download and resource.exists_locally(download_path):
                logger.info('URL %s already downloaded: reusing %s.',
                                         url, download_path)
                self._recorded_sizes_checksums[url] = self._sizes_checksums[url]
                return promise.Promise.resolve(download_path)
        # There is a slight difference between downloader and extractor here:
        # the extractor manages its own temp directory, while the DownloadManager
        # manages the temp directory of downloader.
        download_dir_path = os.path.join(
                self._download_dir,
                '%s.tmp.%s' % (resource_lib.get_dl_dirname(url), uuid.uuid4().hex))
        os.makedirs(download_dir_path)
        logger.info('Downloading %s into %s...', url, download_dir_path)

        def callback(val):
            checksum, dl_size = val
            return self._handle_download_result(
                    resource, download_dir_path, checksum, dl_size)
        return self._downloader.download(url, download_dir_path).then(callback)

    @util.build_synchronize_decorator()
    @utils.memoize()
    def _extract(self, resource):
        """Extract a single archive, returns Promise->path to extraction result."""
        if isinstance(resource, str):
            resource = resource_lib.Resource(path=resource)
        path = resource.path
        extract_method = resource.extract_method
        if extract_method == resource_lib.ExtractMethod.NO_EXTRACT:
            logger.info('Skipping extraction for %s (method=NO_EXTRACT).', path)
            return promise.Promise.resolve(path)
        method_name = resource_lib.ExtractMethod(extract_method).name
        extract_path = os.path.join(self._extract_dir,
                                                                '%s.%s' % (method_name, os.path.basename(path)))
        if not self._force_extraction and os.path.exists(extract_path):
            logger.info('Reusing extraction of %s at %s.', path, extract_path)
            return promise.Promise.resolve(extract_path)
        return self._extractor.extract(path, extract_method, extract_path)

    @util.build_synchronize_decorator()
    @utils.memoize()
    def _download_extract(self, resource):
        """Download-extract `Resource` or url, returns Promise->path."""
        if isinstance(resource, str):
            resource = resource_lib.Resource(url=resource)
        def callback(path):
            resource.path = path
            return self._extract(resource)
        return self._download(resource).then(callback)

    def download_kaggle_data(self, competition_name):
        """Download data for a given Kaggle competition."""
        with self._downloader.tqdm():
            kaggle_downloader = self._downloader.kaggle_downloader(competition_name)
            urls = kaggle_downloader.competition_urls
            files = kaggle_downloader.competition_files
            return _map_promise(self._download,
                                                    dict((f, u) for (f, u) in zip(files, urls)))

    def download(self, url_or_urls):
        """Download given url(s).

        Args:
            url_or_urls: url or `list`/`dict` of urls to download and extract. Each
                url can be a `str` or `nlp.download.Resource`.

        Returns:
            downloaded_path(s): `str`, The downloaded paths matching the given input
                url_or_urls.
        """
        # Add progress bar to follow the download state
        with self._downloader.tqdm():
            return _map_promise(self._download, url_or_urls)

    def iter_archive(self, resource):
        """Returns iterator over files within archive.

        **Important Note**: caller should read files as they are yielded.
        Reading out of order is slow.

        Args:
            resource: path to archive or `nlp.download.Resource`.

        Returns:
            Generator yielding tuple (path_within_archive, file_obj).
        """
        if isinstance(resource, str):
            resource = resource_lib.Resource(path=resource)
        return extractor.iter_archive(resource.path, resource.extract_method)

    def extract(self, path_or_paths):
        """Extract given path(s).

        Args:
            path_or_paths: path or `list`/`dict` of path of file to extract. Each
                path can be a `str` or `nlp.download.Resource`.

        If not explicitly specified in `Resource`, the extraction method is deduced
        from downloaded file name.

        Returns:
            extracted_path(s): `str`, The extracted paths matching the given input
                path_or_paths.
        """
        # Add progress bar to follow the download state
        with self._extractor.tqdm():
            return _map_promise(self._extract, path_or_paths)

    def download_and_extract(self, url_or_urls):
        """Download and extract given url_or_urls.

        Is roughly equivalent to:

        ```
        extracted_paths = dl_manager.extract(dl_manager.download(url_or_urls))
        ```

        Args:
            url_or_urls: url or `list`/`dict` of urls to download and extract. Each
                url can be a `str` or `nlp.download.Resource`.

        If not explicitly specified in `Resource`, the extraction method will
        automatically be deduced from downloaded file name.

        Returns:
            extracted_path(s): `str`, extracted paths of given URL(s).
        """
        # Add progress bar to follow the download state
        with self._downloader.tqdm():
            with self._extractor.tqdm():
                return _map_promise(self._download_extract, url_or_urls)

    @property
    def manual_dir(self):
        """Returns the directory containing the manually extracted data."""
        if not self._manual_dir:
            raise AssertionError(
                    'Manual directory was enabled. '
                    'Did you set MANUAL_DOWNLOAD_INSTRUCTIONS in your dataset?')
        if not os.path.exists(self._manual_dir):
            raise AssertionError(
                    'Manual directory {} does not exist. Create it and download/extract '
                    'dataset artifacts in there. Additional instructions: {}'.format(
                            self._manual_dir, self._manual_dir_instructions))
        return self._manual_dir


# ============================================================================
# In Python 2.X, threading.Condition.wait() cannot be interrupted by SIGINT,
# unless it's given a timeout. Here we artificially give a long timeout to
# allow ctrl+C.
# This code should be deleted once python2 is no longer supported.
if sys.version_info[0] > 2:

    def _wait_on_promise(p):
        return p.get()

else:

    def _wait_on_promise(p):
        while True:
            result = p.get(sys.maxint)  # pylint: disable=g-deprecated-member-used
            if p.is_fulfilled:
                return result

# ============================================================================


def _map_promise(map_fn, all_inputs):
    """Map the function into each element and resolve the promise."""
    all_promises = utils.map_nested(map_fn, all_inputs)  # Apply the function
    res = utils.map_nested(_wait_on_promise, all_promises)
    return res
