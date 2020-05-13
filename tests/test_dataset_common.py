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

import glob
import logging
import tempfile

import requests
from absl.testing import parameterized

from nlp import (
    BeamBasedBuilder,
    BuilderConfig,
    DatasetBuilder,
    DownloadConfig,
    GenerateMode,
    hf_api,
    hf_bucket_url,
    import_main_class,
    load_dataset,
    prepare_module,
)

from .utils import MockDataLoaderManager, aws, is_local_mode, local, slow


logging.basicConfig(level=logging.INFO)


class DatasetTester(object):
    def __init__(self, parent):
        self.parent = parent

    def load_builder_class(self, dataset_name, is_local=False):
        # Download/copy dataset script
        if is_local is True:
            module_path = prepare_module("./datasets/" + dataset_name)
        else:
            module_path = prepare_module(dataset_name, download_config=DownloadConfig(force_download=True))
        # Get dataset builder class
        builder_cls = import_main_class(module_path)
        # Instantiate dataset builder
        return builder_cls

    def load_all_configs(self, dataset_name, is_local=False):
        # get builder class
        builder_cls = self.load_builder_class(dataset_name, is_local=is_local)
        builder = builder_cls

        if len(builder.BUILDER_CONFIGS) == 0:
            return [None]
        return builder.BUILDER_CONFIGS

    def check_load_dataset(self, dataset_name, configs, is_local=False):
        # test only first config to speed up testing
        for config in configs:
            with tempfile.TemporaryDirectory() as processed_temp_dir, tempfile.TemporaryDirectory() as raw_temp_dir:
                # create config and dataset
                dataset_builder_cls = self.load_builder_class(dataset_name, is_local=is_local)
                dataset_builder = dataset_builder_cls(config=config, cache_dir=processed_temp_dir)

                # TODO: skip Beam datasets for now
                if isinstance(dataset_builder, BeamBasedBuilder):
                    logging.info("Skip tests for Beam datasets for now")
                    return

                # create mock data loader manager that has a special download_and_extract() method to download dummy data instead of real data

                if config is not None:
                    version = config.version
                else:
                    version = dataset_builder.VERSION

                mock_dl_manager = MockDataLoaderManager(
                    dataset_name=dataset_name,
                    config=config,
                    version=version,
                    cache_dir=raw_temp_dir,
                    is_local=is_local,
                )

                # build dataset from dummy data
                dataset_builder.download_and_prepare(
                    dl_manager=mock_dl_manager, download_mode=GenerateMode.FORCE_REDOWNLOAD, ignore_verifications=True
                )

                # get dataset
                dataset = dataset_builder.as_dataset()

                # check that dataset is not empty
                for split in dataset_builder.info.splits.keys():
                    # check that loaded datset is not empty
                    self.parent.assertTrue(len(dataset[split]) > 0)


def get_dataset_names():
    if is_local_mode() is True:
        # fetch all dirs in "./datasets/"
        datasets = [dataset_dir.split("/")[-2] for dataset_dir in glob.glob("./datasets/*/")]
    else:
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

    @aws
    def test_dataset_has_valid_etag(self, dataset_name):
        py_script_path = list(filter(lambda x: x, dataset_name.split("/")))[-1] + ".py"
        dataset_url = hf_bucket_url(dataset_name, filename=py_script_path, dataset=True)
        etag = None
        try:
            response = requests.head(dataset_url, allow_redirects=True, proxies=None, timeout=10)

            if response.status_code == 200:
                etag = response.headers.get("Etag")
        except (EnvironmentError, requests.exceptions.Timeout):
            pass

        self.assertIsNotNone(etag)

    @aws
    def test_builder_class(self, dataset_name):
        builder_cls = self.dataset_tester.load_builder_class(dataset_name)
        builder = builder_cls()
        self.assertTrue(isinstance(builder, DatasetBuilder))

    @aws
    def test_builder_configs(self, dataset_name):
        builder_configs = self.dataset_tester.load_all_configs(dataset_name)
        self.assertTrue(len(builder_configs) > 0)

        if builder_configs[0] is not None:
            all(self.assertTrue(isinstance(config, BuilderConfig)) for config in builder_configs)

    @aws
    def test_load_dataset(self, dataset_name):
        # test only first config
        configs = self.dataset_tester.load_all_configs(dataset_name)[:1]
        self.dataset_tester.check_load_dataset(dataset_name, configs)

    @local
    def test_load_dataset_local(self, dataset_name):
        configs = self.dataset_tester.load_all_configs(dataset_name, is_local=True)[:1]
        self.dataset_tester.check_load_dataset(dataset_name, configs, is_local=True)

    @slow
    @aws
    def test_load_dataset_all_configs(self, dataset_name):
        configs = self.dataset_tester.load_all_configs(dataset_name)
        self.dataset_tester.check_load_dataset(dataset_name, configs)

    @slow
    @local
    def test_load_dataset_all_configs_local(self, dataset_name):
        configs = self.dataset_tester.load_all_configs(dataset_name, is_local=True)
        self.dataset_tester.check_load_dataset(dataset_name, configs, is_local=True)

    @slow
    @aws
    def test_load_real_dataset(self, dataset_name):
        with tempfile.TemporaryDirectory() as temp_data_dir:
            download_config = DownloadConfig()
            download_config.download_mode = GenerateMode.FORCE_REDOWNLOAD
            download_and_prepare_kwargs = {"download_config": download_config}

            dataset = load_dataset(
                dataset_name, data_dir=temp_data_dir, download_and_prepare_kwargs=download_and_prepare_kwargs
            )
            for split in dataset.keys():
                self.assertTrue(len(dataset[split]) > 0)

    @slow
    @local
    def test_load_real_dataset_local(self, dataset_name):
        with tempfile.TemporaryDirectory() as temp_data_dir:
            download_config = DownloadConfig()
            download_config.download_mode = GenerateMode.FORCE_REDOWNLOAD
            download_and_prepare_kwargs = {"download_config": download_config}

            dataset = load_dataset(
                "./datasets/" + dataset_name,
                data_dir=temp_data_dir,
                download_and_prepare_kwargs=download_and_prepare_kwargs,
            )
            for split in dataset.keys():
                self.assertTrue(len(dataset[split]) > 0)
