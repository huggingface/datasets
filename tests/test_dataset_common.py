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
import os
import tempfile
from multiprocessing import Pool
from unittest import TestCase

import requests
from absl.testing import parameterized

from datasets import (
    BuilderConfig,
    DatasetBuilder,
    DownloadConfig,
    GenerateMode,
    MockDownloadManager,
    cached_path,
    hf_api,
    hf_bucket_url,
    import_main_class,
    load_dataset,
    logging,
    prepare_module,
)

from .utils import aws, local, slow


logger = logging.get_logger(__name__)


class DatasetTester(object):
    def __init__(self, parent):
        self.parent = parent if parent is not None else TestCase()

    def load_builder_class(self, dataset_name, is_local=False):
        # Download/copy dataset script
        if is_local is True:
            module_path, _ = prepare_module("./datasets/" + dataset_name)
        else:
            module_path, _ = prepare_module(dataset_name, download_config=DownloadConfig(force_download=True))
        # Get dataset builder class
        builder_cls = import_main_class(module_path)
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
                name = config.name if config is not None else None
                dataset_builder = dataset_builder_cls(name=name, cache_dir=processed_temp_dir)

                # TODO: skip Beam datasets and datasets that lack dummy data for now
                if not dataset_builder.test_dummy_data:
                    logger.info("Skip tests for this dataset for now")
                    return

                if config is not None:
                    version = config.version
                else:
                    version = dataset_builder.VERSION

                # create mock data loader manager that has a special download_and_extract() method to download dummy data instead of real data
                mock_dl_manager = MockDownloadManager(
                    dataset_name=dataset_name,
                    config=config,
                    version=version,
                    cache_dir=raw_temp_dir,
                    is_local=is_local,
                )

                if dataset_builder.__class__.__name__ == "Csv":
                    # need slight adoption for csv dataset
                    mock_dl_manager.download_dummy_data()
                    path_to_dummy_data = mock_dl_manager.dummy_file
                    dataset_builder.config.data_files = {
                        "train": os.path.join(path_to_dummy_data, "train.csv"),
                        "test": os.path.join(path_to_dummy_data, "test.csv"),
                        "dev": os.path.join(path_to_dummy_data, "dev.csv"),
                    }
                elif dataset_builder.__class__.__name__ == "Json":
                    # need slight adoption for json dataset
                    mock_dl_manager.download_dummy_data()
                    path_to_dummy_data = mock_dl_manager.dummy_file
                    dataset_builder.config.data_files = {
                        "train": os.path.join(path_to_dummy_data, "train.json"),
                        "test": os.path.join(path_to_dummy_data, "test.json"),
                        "dev": os.path.join(path_to_dummy_data, "dev.json"),
                    }
                elif dataset_builder.__class__.__name__ == "Pandas":
                    # need slight adoption for json dataset
                    mock_dl_manager.download_dummy_data()
                    path_to_dummy_data = mock_dl_manager.dummy_file
                    dataset_builder.config.data_files = {
                        "train": os.path.join(path_to_dummy_data, "train.pkl"),
                        "test": os.path.join(path_to_dummy_data, "test.pkl"),
                        "dev": os.path.join(path_to_dummy_data, "dev.pkl"),
                    }
                elif dataset_builder.__class__.__name__ == "Text":
                    mock_dl_manager.download_dummy_data()
                    path_to_dummy_data = mock_dl_manager.dummy_file
                    dataset_builder.config.data_files = {
                        "train": os.path.join(path_to_dummy_data, "train.txt"),
                        "test": os.path.join(path_to_dummy_data, "test.txt"),
                        "dev": os.path.join(path_to_dummy_data, "dev.txt"),
                    }

                # mock size needed for dummy data instead of actual dataset
                if dataset_builder.info is not None:
                    # approximate upper bound of order of magnitude of dummy data files
                    one_mega_byte = 2 << 19
                    dataset_builder.info.size_in_bytes = 2 * one_mega_byte
                    dataset_builder.info.download_size = one_mega_byte
                    dataset_builder.info.dataset_size = one_mega_byte

                # generate examples from dummy data
                dataset_builder.download_and_prepare(
                    dl_manager=mock_dl_manager,
                    download_mode=GenerateMode.FORCE_REDOWNLOAD,
                    ignore_verifications=True,
                    try_from_hf_gcs=False,
                )

                # get dataset
                dataset = dataset_builder.as_dataset()

                # check that dataset is not empty
                for split in dataset_builder.info.splits.keys():
                    # check that loaded datset is not empty
                    self.parent.assertTrue(len(dataset[split]) > 0)
                del dataset


def get_local_dataset_names():
    datasets = [dataset_dir.split(os.sep)[-2] for dataset_dir in glob.glob("./datasets/*/")]
    return [{"testcase_name": x, "dataset_name": x} for x in datasets]


@parameterized.named_parameters(get_local_dataset_names())
@local
class LocalDatasetTest(parameterized.TestCase):
    dataset_name = None

    def setUp(self):
        self.dataset_tester = DatasetTester(self)

    def test_load_dataset(self, dataset_name):
        configs = self.dataset_tester.load_all_configs(dataset_name, is_local=True)[:1]
        self.dataset_tester.check_load_dataset(dataset_name, configs, is_local=True)

    def test_builder_class(self, dataset_name):
        builder_cls = self.dataset_tester.load_builder_class(dataset_name, is_local=True)
        name = builder_cls.BUILDER_CONFIGS[0].name if builder_cls.BUILDER_CONFIGS else None
        with tempfile.TemporaryDirectory() as tmp_cache_dir:
            builder = builder_cls(name=name, cache_dir=tmp_cache_dir)
            self.assertTrue(isinstance(builder, DatasetBuilder))

    def test_builder_configs(self, dataset_name):
        builder_configs = self.dataset_tester.load_all_configs(dataset_name, is_local=True)
        self.assertTrue(len(builder_configs) > 0)

        if builder_configs[0] is not None:
            all(self.assertTrue(isinstance(config, BuilderConfig)) for config in builder_configs)

    @slow
    def test_load_dataset_all_configs(self, dataset_name):
        configs = self.dataset_tester.load_all_configs(dataset_name, is_local=True)
        self.dataset_tester.check_load_dataset(dataset_name, configs, is_local=True)

    @slow
    def test_load_real_dataset(self, dataset_name):
        path = "./datasets/" + dataset_name
        module_path, hash = prepare_module(path, download_config=DownloadConfig(local_files_only=True), dataset=True)
        builder_cls = import_main_class(module_path, dataset=True)
        name = builder_cls.BUILDER_CONFIGS[0].name if builder_cls.BUILDER_CONFIGS else None
        with tempfile.TemporaryDirectory() as temp_cache_dir:
            dataset = load_dataset(
                path, name=name, cache_dir=temp_cache_dir, download_mode=GenerateMode.FORCE_REDOWNLOAD
            )
            for split in dataset.keys():
                self.assertTrue(len(dataset[split]) > 0)
            del dataset

    @slow
    def test_load_real_dataset_all_configs(self, dataset_name):
        path = "./datasets/" + dataset_name
        module_path, hash = prepare_module(path, download_config=DownloadConfig(local_files_only=True), dataset=True)
        builder_cls = import_main_class(module_path, dataset=True)
        config_names = (
            [config.name for config in builder_cls.BUILDER_CONFIGS] if len(builder_cls.BUILDER_CONFIGS) > 0 else [None]
        )
        for name in config_names:
            with tempfile.TemporaryDirectory() as temp_cache_dir:
                dataset = load_dataset(
                    path, name=name, cache_dir=temp_cache_dir, download_mode=GenerateMode.FORCE_REDOWNLOAD
                )
                for split in dataset.keys():
                    self.assertTrue(len(dataset[split]) > 0)
                del dataset


def distributed_load_dataset(args):
    data_name, tmp_dir, datafiles = args
    dataset = load_dataset(data_name, cache_dir=tmp_dir, data_files=datafiles)
    return dataset


class DistributedDatasetTest(TestCase):
    def test_load_dataset_distributed(self):
        num_workers = 5
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_name = "./datasets/csv"
            data_base_path = os.path.join(data_name, "dummy/0.0.0/dummy_data.zip")
            local_path = cached_path(
                data_base_path, cache_dir=tmp_dir, extract_compressed_file=True, force_extract=True
            )
            datafiles = {
                "train": os.path.join(local_path, "dummy_data/train.csv"),
                "dev": os.path.join(local_path, "dummy_data/dev.csv"),
                "test": os.path.join(local_path, "dummy_data/test.csv"),
            }
            args = data_name, tmp_dir, datafiles
            with Pool(processes=num_workers) as pool:  # start num_workers processes
                result = pool.apply_async(distributed_load_dataset, (args,))
                dataset = result.get(timeout=20)
                for k in dataset:
                    del dataset[k]._data
                datasets = pool.map(distributed_load_dataset, [args] * num_workers)
                for dataset in datasets:
                    for k in dataset:
                        del dataset[k]._data


def get_aws_dataset_names():
    api = hf_api.HfApi()
    # fetch all dataset names
    datasets = api.dataset_list(with_community_datasets=False, id_only=True)
    return [{"testcase_name": x, "dataset_name": x} for x in datasets]


@parameterized.named_parameters(get_aws_dataset_names())
@aws
class AWSDatasetTest(parameterized.TestCase):
    dataset_name = None

    def setUp(self):
        self.dataset_tester = DatasetTester(self)

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

    def test_builder_class(self, dataset_name):
        builder_cls = self.dataset_tester.load_builder_class(dataset_name)
        name = builder_cls.BUILDER_CONFIGS[0].name if builder_cls.BUILDER_CONFIGS else None
        with tempfile.TemporaryDirectory() as tmp_cache_dir:
            builder = builder_cls(name=name, cache_dir=tmp_cache_dir)
            self.assertTrue(isinstance(builder, DatasetBuilder))

    def test_builder_configs(self, dataset_name):
        builder_configs = self.dataset_tester.load_all_configs(dataset_name)
        self.assertTrue(len(builder_configs) > 0)

        if builder_configs[0] is not None:
            all(self.assertTrue(isinstance(config, BuilderConfig)) for config in builder_configs)

    def test_load_dataset(self, dataset_name):
        configs = self.dataset_tester.load_all_configs(dataset_name)[:1]
        self.dataset_tester.check_load_dataset(dataset_name, configs)

    @slow
    def test_load_real_dataset(self, dataset_name):
        path = dataset_name
        module_path, hash = prepare_module(path, download_config=DownloadConfig(force_download=True), dataset=True)
        builder_cls = import_main_class(module_path, dataset=True)
        name = builder_cls.BUILDER_CONFIGS[0].name if builder_cls.BUILDER_CONFIGS else None
        with tempfile.TemporaryDirectory() as temp_cache_dir:
            dataset = load_dataset(
                path, name=name, cache_dir=temp_cache_dir, download_mode=GenerateMode.FORCE_REDOWNLOAD
            )
            for split in dataset.keys():
                self.assertTrue(len(dataset[split]) > 0)
            del dataset

    @slow
    def test_load_real_dataset_all_configs(self, dataset_name):
        path = dataset_name
        module_path, hash = prepare_module(path, download_config=DownloadConfig(force_download=True), dataset=True)
        builder_cls = import_main_class(module_path, dataset=True)
        config_names = (
            [config.name for config in builder_cls.BUILDER_CONFIGS] if len(builder_cls.BUILDER_CONFIGS) > 0 else [None]
        )
        for name in config_names:
            with tempfile.TemporaryDirectory() as temp_cache_dir:
                dataset = load_dataset(
                    path, name=name, cache_dir=temp_cache_dir, download_mode=GenerateMode.FORCE_REDOWNLOAD
                )
                for split in dataset.keys():
                    self.assertTrue(len(dataset[split]) > 0)
                del dataset


class TextTest(TestCase):
    def test_caching(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            open(os.path.join(tmp_dir, "text.txt"), "w", encoding="utf-8").write("\n".join("foo" for _ in range(10)))
            ds = load_dataset(
                "./datasets/text", data_files=os.path.join(tmp_dir, "text.txt"), cache_dir=tmp_dir, split="train"
            )
            data_file = ds._data_files[0]
            fingerprint = ds._fingerprint
            del ds
            ds = load_dataset(
                "./datasets/text", data_files=os.path.join(tmp_dir, "text.txt"), cache_dir=tmp_dir, split="train"
            )
            self.assertEqual(ds._data_files[0], data_file)
            self.assertEqual(ds._fingerprint, fingerprint)
            del ds

            open(os.path.join(tmp_dir, "text.txt"), "w", encoding="utf-8").write("\n".join("bar" for _ in range(10)))
            ds = load_dataset(
                "./datasets/text", data_files=os.path.join(tmp_dir, "text.txt"), cache_dir=tmp_dir, split="train"
            )
            self.assertNotEqual(ds._data_files[0], data_file)
            self.assertNotEqual(ds._fingerprint, fingerprint)
            del ds
