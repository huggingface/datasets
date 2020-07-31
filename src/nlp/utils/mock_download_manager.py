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
"""Mock download manager interface."""

import logging
import os
import urllib.parse

from .file_utils import cached_path, hf_bucket_url


logger = logging.getLogger(__name__)


class MockDownloadManager(object):
    dummy_file_name = "dummy_data"

    def __init__(self, dataset_name, config, version, cache_dir=None, is_local=False):
        self.downloaded_size = 0
        self.dataset_name = dataset_name
        self.cache_dir = cache_dir
        self.is_local = is_local
        self.config = config

        # TODO(PVP, QL) might need to make this more general
        self.version_name = str(version.major) + "." + str(version.minor) + "." + str(version.patch)
        # to be downloaded
        self._dummy_file = None
        self._bucket_url = None

    @property
    def dummy_file(self):
        if self._dummy_file is None:
            self._dummy_file = self.download_dummy_data()
        return self._dummy_file

    @property
    def dummy_data_folder(self):
        if self.config is not None:
            # structure is dummy / config_name / version_name
            return os.path.join("dummy", self.config.name, self.version_name)
        # structure is dummy / version_name
        return os.path.join("dummy", self.version_name)

    @property
    def dummy_zip_file(self):
        return os.path.join(self.dummy_data_folder, "dummy_data.zip")

    def download_dummy_data(self):
        path_to_dummy_data_dir = (
            self.local_path_to_dummy_data if self.is_local is True else self.aws_path_to_dummy_data
        )

        local_path = cached_path(
            path_to_dummy_data_dir, cache_dir=self.cache_dir, extract_compressed_file=True, force_extract=True
        )

        return os.path.join(local_path, self.dummy_file_name)

    @property
    def local_path_to_dummy_data(self):
        return os.path.join("datasets", self.dataset_name, self.dummy_zip_file)

    @property
    def aws_path_to_dummy_data(self):
        if self._bucket_url is None:
            self._bucket_url = hf_bucket_url(self.dataset_name, filename=self.dummy_zip_file)
        return self._bucket_url

    @property
    def manual_dir(self):
        # return full path if its a dir
        if os.path.isdir(self.dummy_file):
            return self.dummy_file
        # else cut off path to file -> example `xsum`.
        return "/".join(self.dummy_file.split("/")[:-1])

    # this function has to be in the manager under this name so that testing works
    def download_and_extract(self, data_url, *args):
        if self.cache_dir is not None:
            # dummy data is downloaded and tested
            dummy_file = self.dummy_file
        else:
            # dummy data cannot be downloaded and only the path to dummy file is returned
            dummy_file = self.dummy_file_name

        # special case when data_url is a dict
        if isinstance(data_url, dict):
            return self.create_dummy_data_dict(dummy_file, data_url)
        elif isinstance(data_url, (list, tuple)):
            return self.create_dummy_data_list(dummy_file, data_url)
        return dummy_file

    # this function has to be in the manager under this name so that testing works
    def download(self, data_url, *args):
        return self.download_and_extract(data_url)

    # this function has to be in the manager under this name so that testing works
    def download_custom(self, data_url, custom_download):
        return self.download_and_extract(data_url)

    # this function has to be in the manager under this name so that testing works
    def extract(self, path):
        return path

    # this function has to be in the manager under this name so that testing works
    def get_recorded_sizes_checksums(self):
        return {}

    def create_dummy_data_dict(self, path_to_dummy_data, data_url):
        dummy_data_dict = {}
        for key, abs_path in data_url.items():
            # we force the name of each key to be the last file / folder name of the url path
            # if the url has arguments, we need to encode them with urllib.parse.quote_plus
            if isinstance(abs_path, list):
                value = [os.path.join(path_to_dummy_data, urllib.parse.quote_plus(x.split("/")[-1])) for x in abs_path]
            else:
                value = os.path.join(path_to_dummy_data, urllib.parse.quote_plus(abs_path.split("/")[-1]))
            dummy_data_dict[key] = value

        # make sure that values are unique
        first_value = next(iter(dummy_data_dict.values()))
        if isinstance(first_value, str) and len(set(dummy_data_dict.values())) < len(dummy_data_dict.values()):
            # append key to value to make its name unique
            dummy_data_dict = {key: value + key for key, value in dummy_data_dict.items()}

        return dummy_data_dict

    def create_dummy_data_list(self, path_to_dummy_data, data_url):
        dummy_data_list = []
        for abs_path in data_url:
            # we force the name of each key to be the last file / folder name of the url path
            # if the url has arguments, we need to encode them with urllib.parse.quote_plus
            value = os.path.join(path_to_dummy_data, urllib.parse.quote_plus(abs_path.split("/")[-1]))
            dummy_data_list.append(value)
        return dummy_data_list
