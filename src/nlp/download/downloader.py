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
"""Async download API with checksum verification. No business logic."""

import concurrent.futures
import contextlib
import hashlib
import io
import os
import shutil
import re
import ssl
import sys
import logging
import promise
import requests
from requests.utils import extract_zipped_paths
import urllib

from .. import utils
from . import kaggle
from . import util as download_util

_DRIVE_URL = re.compile(r'^https://drive\.google\.com/')

logger = logging.getLogger(__name__)

@utils.memoize()
def get_downloader(*args, **kwargs):
    return _Downloader(*args, **kwargs)


def _get_filename(response):
    content_disposition = response.headers.get('content-disposition', None)
    if content_disposition:
        match = re.findall('filename="(.+?)"', content_disposition)
        if match:
            return match[0]
    return download_util.get_file_name(response.url)


class DownloadError(Exception):
    pass


class _Downloader(object):
    """Class providing async download API with checksum validation.

    Do not instantiate this class directly. Instead, call `get_downloader()`.
    """

    def __init__(self, max_simultaneous_downloads=50, checksumer=None):
        """Init _Downloader instance.

        Args:
            max_simultaneous_downloads: `int`, max number of simultaneous downloads.
            checksumer: `hashlib.HASH`. Defaults to `hashlib.sha256`.
        """
        self._executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=max_simultaneous_downloads)
        self._checksumer = checksumer or hashlib.sha256
        self._pbar_url = None
        self._pbar_dl_size = None

    @utils.memoize()
    def kaggle_downloader(self, competition_name):
        return kaggle.KaggleCompetitionDownloader(competition_name)

    @contextlib.contextmanager
    def tqdm(self):
        """Add a progression bar for the current download."""
        async_tqdm = utils.async_tqdm
        with async_tqdm(total=0, desc='Dl Completed...', unit=' url') as pbar_url:
            with async_tqdm(total=0, desc='Dl Size...', unit=' MiB') as pbar_dl_size:
                self._pbar_url = pbar_url
                self._pbar_dl_size = pbar_dl_size
                yield

    def download(self, url, destination_path):
        """Download url to given path.

        Returns Promise -> sha256 of downloaded file.

        Args:
            url: address of resource to download.
            destination_path: `str`, path to directory where to download the resource.

        Returns:
            Promise obj -> (`str`, int): (downloaded object checksum, size in bytes).
        """
        self._pbar_url.update_total(1)
        future = self._executor.submit(self._sync_download, url, destination_path)
        return promise.Promise.resolve(future)

    def _sync_kaggle_download(self, kaggle_url, destination_path):
        """Download with Kaggle API."""
        kaggle_file = kaggle.KaggleFile.from_url(kaggle_url)
        downloader = self.kaggle_downloader(kaggle_file.competition)
        filepath = downloader.download_file(kaggle_file.filename, destination_path)

        # dl_size = tf . io . gfile . stat(filepath).length  # TODO thom deprecating this
        checksum = self._checksumer()
        with open(filepath, 'rb') as f:
            while True:
                block = f.read(io.DEFAULT_BUFFER_SIZE)
                if not block:
                    break
                checksum.update(block)
        return checksum.hexdigest(), 0  # dl_size

    def _get_drive_url(self, url, session):
        """Returns url, possibly with confirmation token."""
        response = session.get(url, stream=True)
        if response.status_code != 200:
            raise DownloadError(
                    'Failed to get url %s. HTTP code: %d.' % (url, response.status_code))
        for k, v in response.cookies.items():
            if k.startswith('download_warning'):
                return url + '&confirm=' + v  # v is the confirm token
        # No token found, let's try with original URL:
        return url

    def _sync_file_copy(self, filepath, destination_path):
        out_path = os.path.join(destination_path, os.path.basename(filepath))
        shutil.copyfile(filepath, out_path)
        hexdigest, size = utils.read_checksum_digest(
                out_path, checksum_cls=self._checksumer)
        return hexdigest, size

    def _sync_download(self, url, destination_path):
        """Synchronous version of `download` method.

        Args:
            url: url to download
            destination_path: path where to write it
        Returns:
            None

        Raises:
            DownloadError: when download fails.

        Environment Variables:
                TFDS_HTTP_PROXY  : Configure Proxy Servers for HTTP Requests
                TFDS_HTTPS_PROXY : Configure Proxy Servers for HTTPS Requests
                TFDS_FTP_PROXY   : Configure Proxy Servers for FTP Requests
                TFDS_CA_BUNDLE   : Configure Custom Client Side SSL Certificates
                                                     (If REQUESTS_CA_BUNDLE is set, it would use that
                                                     path)

            Note: FTPS Custom Certificate verification doesn't work for python version
            <= 2.7.8
        """
        proxies = {
                'http': os.environ.get('TFDS_HTTP_PROXY', None),
                'https': os.environ.get('TFDS_HTTPS_PROXY', None),
                'ftp': os.environ.get('TFDS_FTP_PROXY', None)
        }
        ca_bundle = os.environ.get('TFDS_CA_BUNDLE', None)
        if not ca_bundle:
            ca_bundle = os.environ.get('REQUESTS_CA_BUNDLE', None)
        if ca_bundle:
            ca_bundle = extract_zipped_paths(ca_bundle)

        ca_verify = {
                'urllib':
                        ssl._create_unverified_context()  # pylint: disable=W0212
                        if not ca_bundle else ssl.create_default_context(capath=ca_bundle),
                'requests':
                        False if not ca_bundle else ca_bundle
        }

        if kaggle.KaggleFile.is_kaggle_url(url):
            if proxies['http']:
                os.environ['KAGGLE_PROXY'] = proxies['http']
            return self._sync_kaggle_download(url, destination_path)

        # If url is on a filesystem that gfile understands, use copy. Otherwise,
        # use requests (http) or urllib (ftp).
        if not url.startswith('http'):
            return self._sync_file_copy(url, destination_path)

        session = requests.Session()
        session.proxies = proxies
        session.verify = ca_verify['requests']
        if _DRIVE_URL.match(url):
            url = self._get_drive_url(url, session)
        use_urllib = url.startswith('ftp')
        if use_urllib:
            if proxies['ftp']:
                proxy = urllib.request.ProxyHandler({'ftp': proxies['ftp']})
                opener = urllib.request.build_opener(proxy)
                urllib.request.install_opener(opener)   # pylint: disable=too-many-function-args
            request = urllib.request.Request(url)

            # disable ssl context check for FTPS for python version <= 2.7.8
            if ca_verify['urllib'] is None:
                response = urllib.request.urlopen(request)
            else:
                response = urllib.request.urlopen(request, context=ca_verify['urllib'])
        else:
            response = session.get(url, stream=True)
            if response.status_code != 200:
                raise DownloadError('Failed to get url %s. HTTP code: %d.' %
                                                        (url, response.status_code))
        fname = _get_filename(response)
        path = os.path.join(destination_path, fname)
        size = 0

        size_mb = 0
        unit_mb = 2**20  # MB
        self._pbar_dl_size.update_total(
                int(response.headers.get('Content-length', 0)) // unit_mb)
        with open(path, 'wb') as file_:
            checksum = self._checksumer()
            if use_urllib:
                iterator = iter(lambda: response.read(io.DEFAULT_BUFFER_SIZE), b'')
            else:
                iterator = response.iter_content(chunk_size=io.DEFAULT_BUFFER_SIZE)

            for block in iterator:
                size += len(block)

                # Update the progress bar
                size_mb += len(block)
                if size_mb > unit_mb:
                    self._pbar_dl_size.update(size_mb // unit_mb)
                    size_mb %= unit_mb

                checksum.update(block)
                file_.write(block)
        self._pbar_url.update(1)
        return checksum.hexdigest(), size
