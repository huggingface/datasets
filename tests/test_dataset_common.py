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
    def __init__(self, path_to_dummy_data):
        self.path_to_dummy_data = path_to_dummy_data
        self.downloaded_size = 0

    def download_and_extract(self, data_url, *args):
        # this function has to be in the manager under this name to work
        # if data_url is a dict then return a dict with the correct file names
        if isinstance(data_url, dict):
            dummy_data_dict = {}
            for key in data_url.keys():
                dummy_data_dict[key] = os.path.join(self.path_to_dummy_data, key)
            return dummy_data_dict
        return self.path_to_dummy_data

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
        return builder.BUILDER_CONFIGS

    def download_dummy_data(self, dataset_name, config_name, version_name, cache_dir):
        filename = os.path.join(
            self.parent.dummy_folder_name, config_name, version_name, self.parent.extracted_dummy_folder_name + ".zip"
        )
        url_to_dummy_data_dir = hf_bucket_url(dataset_name, filename=filename)
        # this function will download the dummy data and return the path
        local_path = cached_path(
            url_to_dummy_data_dir, cache_dir=cache_dir, extract_compressed_file=True, force_extract=True
        )
        return os.path.join(local_path, self.parent.extracted_dummy_folder_name)

    def create_mock_data_loader(self, path_to_dummy_data):
        mock_dl_manager = MockDataLoaderManager(path_to_dummy_data)
        return mock_dl_manager


def get_dataset_names():
    # fetch all dataset names
    api = hf_api.HfApi()
    datasets = [x.datasetId for x in api.dataset_list()]
    dataset_names_parametrized = [{"testcase_name": x, "dataset_name": x} for x in datasets]
    return dataset_names_parametrized


@parameterized.named_parameters(get_dataset_names())
class DatasetTest(parameterized.TestCase):

    dataset_name = None
    dummy_folder_name = "dummy"
    extracted_dummy_folder_name = "dummy_data"

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
        all(self.assertTrue(isinstance(config, BuilderConfig)) for config in builder_configs)

    def test_load_dataset(self, dataset_name):
        builder_configs = self.dataset_tester.load_all_configs(dataset_name)

        for config in builder_configs:
            with tempfile.TemporaryDirectory() as processed_temp_dir, tempfile.TemporaryDirectory() as raw_temp_dir:
                # create config and dataset
                dataset_builder = self.dataset_tester.load_builder(dataset_name, config, data_dir=processed_temp_dir)
                # get version
                version = dataset_builder.version
                version_name = str(version.major) + "." + str(version.minor) + "." + str(version.patch)

                # dowloads dummy data
                path_to_dummy_data = self.dataset_tester.download_dummy_data(
                    dataset_name, config_name=config.name, version_name=version_name, cache_dir=raw_temp_dir
                )

                # create mock data loader manager with test specific mock_folder_strucutre_fn
                mock_dl_manager = self.dataset_tester.create_mock_data_loader(path_to_dummy_data)

                # inject our fake download manager to the dataset_builder._make_download_manager fn
                dataset_builder._make_download_manager = lambda **kwargs: mock_dl_manager

                # build dataset from dummy data
                dataset_builder.download_and_prepare()

                # get dataset
                dataset = dataset_builder.as_dataset()

                # check that dataset is not empty
                for split in dataset_builder.info.splits.keys():
                    # check that loaded datset is not empty
                    self.assertTrue(len(dataset[split]) > 0)

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
