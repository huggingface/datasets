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

from nlp import load_dataset_module, hf_bucket_url, DatasetBuilder, BuilderConfig, cached_path, hf_api

import os
import requests
import tempfile

from absl.testing import parameterized


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
        postfix = os.path.join(self.parent.dummy_folder_name, config_name, version_name, self.parent.extracted_dummy_folder_name + '.zip')
        url_to_dummy_data_dir = hf_bucket_url(dataset_name, postfix=postfix)
        # this function will download the dummy data and return the path
        local_path = cached_path(url_to_dummy_data_dir, cache_dir=cache_dir, extract_compressed_file=True, force_extract=True)
        return os.path.join(local_path, self.parent.extracted_dummy_folder_name)

    def create_mock_data_loader(self, path_to_dummy_data):
        mock_dl_manager = MockDataLoaderManager(path_to_dummy_data)
        return mock_dl_manager


def get_dataset_names():
    # This function will soon work after Julien's PR.
#    api = hf_api.HfApi()
#    datasets = [x.datasetId for x in api.dataset_list()]
    datasets = ['aeslc', 'amazon_us_reviews', 'big_patent', 'billsum', 'blimp', 'c4', 'cfq', 'civil_comments', 'cnn_dailymail', 'cos_e', 'crime_and_punish', 'definite_pronoun_resolution', 'eraser_multi_rc', 'esnli', 'flores', 'forest_fires', 'gap', 'german_credit_numeric', 'gigaword', 'glue', 'higgs', 'imdb', 'iris', 'julien-c/squad', 'librispeech_lm', 'lm1b', 'math_dataset', 'movie_rationales', 'multi_news', 'multi_nli', 'multi_nli_mismatch', 'natural_questions', 'newsroom', 'opinosis', 'para_crawl', 'qa4mre', 'reddit_tifu', 'rock_you', 'scan', 'scicite', 'scientific_papers', 'sentiment140', 'snli', 'squad', 'super_glue', 'ted_hrlr', 'ted_multi', 'tiny_shakespeare', 'titanic', 'trivia_qa', 'wiki40b', 'wikihow', 'wikipedia', 'wmt', 'xnli', 'xsum', 'yelp_polarity']
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
        name = list(filter(lambda x: x, self.dataset_name.split("/")))[-1] + ".py"
        dataset_url = hf_bucket_url(self.dataset_name, filename=name)
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
                path_to_dummy_data = self.dataset_tester.download_dummy_data(dataset_name, config_name=config.name, version_name=version_name, cache_dir=raw_temp_dir)

                # create mock data loader manager with test specific mock_folder_strucutre_fn
                mock_dl_manager = self.dataset_tester.create_mock_data_loader(path_to_dummy_data)

                # inject our fake download manager to the dataset_builder._make_download_manager fn
                dataset_builder._make_download_manager = (lambda **kwargs: mock_dl_manager)

                # build dataset from dummy data
                dataset_builder.download_and_prepare()

                # get dataset
                dataset = dataset_builder.as_dataset()

                # check that dataset is not empty
                for split in dataset_builder.info.splits.keys():
                    # check that loaded datset is not empty
                    self.assertTrue(len(dataset[split]) > 0)


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

        def check_or_save_checksums(self, urls_checksums_dir):
            # we can edit this if we want to mock the checksum checks or registrations
            pass

    class DatasetTester(object):

        def __init__(self, parent):
            self.parent = parent
            self.dataset_name = parent.dataset_name

        def load_builder(self, config=None, data_dir=None):
            module = load_dataset_module(self.dataset_name, force_reload=True)
            builder_cls = get_builder_cls_from_module(module)
            builder = builder_cls(config=config, data_dir=data_dir)
            return builder

        def load_all_configs(self):
            module = load_dataset_module(self.dataset_name, force_reload=True)
            builder_cls = get_builder_cls_from_module(module)
            builder = builder_cls()
            return builder.BUILDER_CONFIGS

        def download_dummy_data(self, config_name, version_name, cache_dir):
            postfix = os.path.join(self.parent.dummy_folder_name, config_name, version_name, self.parent.extracted_dummy_folder_name + '.zip')
            url_to_dummy_data_dir = hf_bucket_url(self.dataset_name, postfix=postfix)
            # this function will download the dummy data and return the path
            local_path = cached_path(url_to_dummy_data_dir, cache_dir=cache_dir, extract_compressed_file=True, force_extract=True)
            return os.path.join(local_path, self.parent.extracted_dummy_folder_name)

        def create_mock_data_loader(self, path_to_dummy_data):
            mock_dl_manager = DatasetTest.MockDataLoaderManager(path_to_dummy_data)
            return mock_dl_manager

    def setUp(self):
        self.dataset_tester = DatasetTest.DatasetTester(self)
=======
>>>>>>> improve tests
