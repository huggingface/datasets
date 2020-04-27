# coding=utf-8
# Copyright 2019 HuggingFace Inc.
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

from nlp import load_dataset, hf_bucket_url

from parameterized import parameterized_class

import unittest


class DatasetTesterMixin:

    dataset_tester = None
    dataset_name = None

    def test_dataset_bucket_url(self):
        if self.dataset_name is None:
            return

        dataset_file = hf_bucket_url(self.dataset_name)

    def test_dataset_builder(self):
        if self.dataset_name is None:
            return

        dataset_builder = self.dataset_tester.load_builder_cls()

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
    return [{"dataset_name": "crime_and_punish"}, {"dataset_name": "sentiment140"}]


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

        def load_builder_cls(self):
            return load_dataset(self.dataset_name)

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
