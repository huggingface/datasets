# coding=utf-8
# Copyright 2020 HuggingFace Inc.
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

import logging
import os
import tempfile

import requests
from absl.testing import parameterized

from nlp import (
    BuilderConfig,
    DatasetBuilder,
    DownloadConfig,
    GenerateMode,
    cached_path,
    hf_api,
    hf_bucket_url,
    load,
    load_dataset_module,
)

from .utils import slow


logging.basicConfig(level=logging.INFO)


class MockDataLoaderManager(object):

    dummy_data_folder_name = "dummy"
    dummy_data_file_name = "dummy_data.zip"
    dummy_data_extracted_folder_name = "dummy_data"

    def __init__(self, dataset_name, config, version_name, cache_dir):
        self.downloaded_size = 0
        self.dataset_name = dataset_name
        self.config = config
        self.version_name = version_name
        self.cache_dir = cache_dir

    def download_dummy_data(self, dataset_name, config_name, version_name, cache_dir):
        # dowloads dummy data
        filename = os.path.join(
            self.dummy_data_folder_name, config_name, version_name, self.dummy_data_file_name
        )

        # get url to dummy data on AWS S3 bucket
        url_to_dummy_data_dir = hf_bucket_url(dataset_name, filename=filename)

        # this function will download the dummy data and return the path
        local_path = cached_path(
            url_to_dummy_data_dir, cache_dir=cache_dir, extract_compressed_file=True, force_extract=True
        )
        return os.path.join(local_path, self.dummy_data_extracted_folder_name)

    def download_and_extract(self, data_url, *args):
        # this function has to be in the manager under this name to work
        # if data_url is a dict then return a dict with the correct file names

        # get config name
        config_name = self.config.name if self.config is not None else ""

        path_to_dummy_data = self.download_dummy_data(dataset_name=self.dataset_name, config_name=config_name, version_name=self.version_name, cache_dir=self.cache_dir)

        if isinstance(data_url, dict):
            dummy_data_dict = {}
            for key, abs_path in data_url.items():
                rel_path = abs_path.split('/')[-1]
                dummy_data_dict[key] = os.path.join(path_to_dummy_data, rel_path)
            return dummy_data_dict
        return path_to_dummy_data

    def check_or_save_checksums(self, *args):
        pass


class DatasetTester(object):
    def __init__(self, parent):
        self.parent = parent

    def load_builder(self, dataset_name, config=None, data_dir=None):
        builder_cls = load_dataset_module(dataset_name, force_reload=True)
        builder = builder_cls(config=config, data_dir=data_dir)
        return builder

    def load_all_configs(self, dataset_name):
        builder_cls = load_dataset_module(dataset_name, force_reload=True)
        builder = builder_cls()
        if len(builder.BUILDER_CONFIGS) == 0:
            return [None]
        return builder.BUILDER_CONFIGS

    def check_load_dataset(self, dataset_name, configs):
        # test only first config to speed up testing
        for config in configs:
            with tempfile.TemporaryDirectory() as processed_temp_dir, tempfile.TemporaryDirectory() as raw_temp_dir:
                # create config and dataset
                dataset_builder = self.load_builder(dataset_name, config, data_dir=processed_temp_dir)
                # get version
                version = dataset_builder.version
                version_name = str(version.major) + "." + str(version.minor) + "." + str(version.patch)

                # create mock data loader manager
                mock_dl_manager = MockDataLoaderManager(dataset_name=dataset_name, config=config, version_name=version_name, cache_dir=raw_temp_dir)

                # inject our fake download manager to the dataset_builder._make_download_manager fn
                dataset_builder._make_download_manager = lambda **kwargs: mock_dl_manager

                # build dataset from dummy data
                dataset_builder.download_and_prepare()

                # get dataset
                dataset = dataset_builder.as_dataset()

                # check that dataset is not empty
                for split in dataset_builder.info.splits.keys():
                    # check that loaded datset is not empty
                    self.parent.assertTrue(len(dataset[split]) > 0)


def get_dataset_names():
    # fetch all dataset names
    api = hf_api.HfApi()
    datasets = [x.datasetId for x in api.dataset_list()]
    dataset_names_parametrized = [{"testcase_name": x, "dataset_name": x} for x in datasets]
    return dataset_names_parametrized


@parameterized.named_parameters(get_dataset_names())
class DatasetTest(parameterized.TestCase):

    dataset_name = None

    def setUp(self):
        self.dataset_tester = DatasetTester(self)

    def test_dataset_has_valid_etag(self, dataset_name):
        py_script_path = list(filter(lambda x: x, dataset_name.split("/")))[-1] + ".py"
        dataset_url = hf_bucket_url(dataset_name, filename=py_script_path)
        etag = None
        try:
            response = requests.head(dataset_url, allow_redirects=True, proxies=None, timeout=10)

            if response.status_code == 200:
                etag = response.headers.get("Etag")
        except (EnvironmentError, requests.exceptions.Timeout):
            pass

        self.assertIsNotNone(etag)

    def test_builder_class(self, dataset_name):
        builder = self.dataset_tester.load_builder(dataset_name)
        self.assertTrue(isinstance(builder, DatasetBuilder))

    def test_builder_configs(self, dataset_name):
        builder_configs = self.dataset_tester.load_all_configs(dataset_name)
        self.assertTrue(len(builder_configs) > 0)

        if builder_configs[0] is not None:
            all(self.assertTrue(isinstance(config, BuilderConfig)) for config in builder_configs)

    def test_load_dataset(self, dataset_name):
        # test only first config
        configs = self.dataset_tester.load_all_configs(dataset_name)[:1]
        self.dataset_tester.check_load_dataset(dataset_name, configs)

    @slow
    def test_load_dataset_all_configs(self, dataset_name):
        configs = self.dataset_tester.load_all_configs(dataset_name)
        self.dataset_tester.check_load_dataset(dataset_name, configs)

    @slow
    def test_load_real_dataset(self, dataset_name):
        with tempfile.TemporaryDirectory() as temp_data_dir:
            download_config = DownloadConfig()
            download_config.download_mode = GenerateMode.FORCE_REDOWNLOAD
            download_and_prepare_kwargs = {"download_config": download_config}

            dataset = load(
                dataset_name, data_dir=temp_data_dir, download_and_prepare_kwargs=download_and_prepare_kwargs
            )
            for split in dataset.keys():
                self.assertTrue(len(dataset[split]) > 0)
