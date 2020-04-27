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

from nlp import load_dataset_module, hf_bucket_url, path_to_py_script_name, DatasetBuilder, BuilderConfig, get_builder_cls_from_module
import requests

from parameterized import parameterized_class

from types import ModuleType
import unittest


class DatasetTesterMixin:

    dataset_tester = None
    dataset_name = None

    def test_dataset_has_valid_etag(self):
        if self.dataset_name is None:
            return

        dataset_url = hf_bucket_url(self.dataset_name, postfix=path_to_py_script_name(self.dataset_name))
        etag = None
        try:
            response = requests.head(dataset_url, allow_redirects=True, proxies=None, timeout=10)

            if response.status_code == 200:
                etag = response.headers.get("Etag")
        except (EnvironmentError, requests.exceptions.Timeout):
            pass

        self.assertIsNotNone(etag)

    def test_load_module(self):
        if self.dataset_name is None:
            return

        module = load_dataset_module(self.dataset_name, force_reload=True)
        self.assertTrue(isinstance(module, ModuleType))

    def test_builder_class(self):
        if self.dataset_name is None:
            return

        builder = self.dataset_tester.load_builder()
        self.assertTrue(isinstance(builder, DatasetBuilder))

    def test_builder_configs(self):
        if self.dataset_name is None:
            return

        builder = self.dataset_tester.load_builder()
        builder_configs = builder.BUILDER_CONFIGS
        self.assertTrue(len(builder_configs) > 0)
        all(self.assertTrue(isinstance(config, BuilderConfig)) for config in builder_configs)

    def test_load_dataset(self):
        if self.dataset_name is None:
            return

        config_names = self.dataset_tester.prepare_config_names()
        dataset_builder_class_cls = self.dataset_tester.load_builder_cls()

        for config_name in config_names:
            # create config and dataset
            dataset_builder = dataset_builder_class_cls(config_name)

            path_to_dummy_data = self.dataset_tester.download_dummy_data(config_name)

            # create mock data loader manager with test specific mock_folder_strucutre_fn
            mock_dl_manager = DatasetTesterMixin.MockDataLoaderManager(path_to_dummy_data)

            # use the mock_dl_manager to create mock data and get split generators from there
            split_generators = dataset_builder._split_generators(mock_dl_manager)

            # ...


def get_dataset_names():
    # this function will call the dataset API and get the current names
    datasets = ["crime_and_punish", "sentiment140", "squad"]
    dataset_names_parametrized = [{"dataset_name": x} for x in datasets]
    return dataset_names_parametrized


@parameterized_class(get_dataset_names())
class DatasetTest(unittest.TestCase, DatasetTesterMixin):

    dataset_name = None

    class MockDataLoaderManager(object):
        # this can actually be defined here and is the data_dir used to
        data_dir = None

        def __init__(self, path_to_dummy_data):
            self.path_to_dummy_data = path_to_dummy_data

        def download_and_extract(self, *args):
            # this function has to be in the manager under this name to work
            return self.path_to_dummy_data

    class DatasetTester(object):

        def __init__(self, parent):
            self.parent = parent
            self.dataset_name = parent.dataset_name

        def load_builder(self, config_name=None):
            module = load_dataset_module(self.dataset_name, force_reload=True)
            builder_cls = get_builder_cls_from_module(module)
            builder = builder_cls(config=config_name)
            return builder

        def prepare_config_names(self):
            # this function will return all configs
            pass

        def download_dummy_data(self, config_name):
            # this function will download the dummy data
            # and return the path
            pass

        def create_mock_data_loader(self, path_to_dummy_data):
            return DatasetTest.MockDataLoaderManager(path_to_dummy_data)

    def setUp(self):
        self.dataset_tester = DatasetTest.DatasetTester(self)
