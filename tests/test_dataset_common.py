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
import warnings
from functools import wraps
from multiprocessing import Pool
from unittest import TestCase

from absl.testing import parameterized

from datasets import (
    BuilderConfig,
    DatasetBuilder,
    DownloadConfig,
    Features,
    GenerateMode,
    MockDownloadManager,
    Value,
    cached_path,
    hf_api,
    import_main_class,
    load_dataset,
    logging,
    prepare_module,
)
from datasets.search import _has_faiss
from datasets.utils.file_utils import is_remote_url

from .utils import for_all_test_methods, local, remote, slow


logger = logging.get_logger(__name__)


REQUIRE_FAISS = {"wiki_dpr"}


def skip_if_dataset_requires_faiss(test_case):
    @wraps(test_case)
    def wrapper(self, dataset_name):
        if not _has_faiss and dataset_name in REQUIRE_FAISS:
            self.skipTest('"test requires Faiss"')
        else:
            test_case(self, dataset_name)

    return wrapper


def skip_if_not_compatible_with_windows(test_case):
    if os.name == "nt":  # windows

        @wraps(test_case)
        def wrapper(self, dataset_name):
            try:
                test_case(self, dataset_name)
            except FileNotFoundError as e:
                if "[WinError 206]" in str(e):  # if there's a path that exceeds windows' 256 characters limit
                    warnings.warn("test not compatible with windows ([WinError 206] error)")
                    self.skipTest('"test not compatible with windows ([WinError 206] error)"')
                else:
                    raise

        return wrapper
    else:
        return test_case


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

                def check_if_url_is_valid(url):
                    if is_remote_url(url) and "\\" in url:
                        raise ValueError(f"Bad remote url '{url}'' since it contains a backslash")

                # create mock data loader manager that has a special download_and_extract() method to download dummy data instead of real data
                mock_dl_manager = MockDownloadManager(
                    dataset_name=dataset_name,
                    config=config,
                    version=version,
                    cache_dir=raw_temp_dir,
                    is_local=is_local,
                    download_callbacks=[check_if_url_is_valid],
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
                dataset = dataset_builder.as_dataset(ignore_verifications=True)

                # check that dataset is not empty
                self.parent.assertListEqual(sorted(dataset_builder.info.splits.keys()), sorted(dataset))
                for split in dataset_builder.info.splits.keys():
                    # check that loaded datset is not empty
                    self.parent.assertTrue(len(dataset[split]) > 0)
                del dataset


def get_local_dataset_names():
    datasets = [dataset_dir.split(os.sep)[-2] for dataset_dir in glob.glob("./datasets/*/")]
    return [{"testcase_name": x, "dataset_name": x} for x in datasets]


@parameterized.named_parameters(get_local_dataset_names())
@for_all_test_methods(skip_if_dataset_requires_faiss, skip_if_not_compatible_with_windows)
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
                del result, dataset
                datasets = pool.map(distributed_load_dataset, [args] * num_workers)
                for _ in range(len(datasets)):
                    dataset = datasets.pop()
                    del dataset


def get_remote_dataset_names():
    api = hf_api.HfApi()
    # fetch all dataset names
    datasets = api.dataset_list(with_community_datasets=False, id_only=True)
    return [{"testcase_name": x, "dataset_name": x} for x in datasets]


@parameterized.named_parameters(get_remote_dataset_names())
@for_all_test_methods(skip_if_dataset_requires_faiss, skip_if_not_compatible_with_windows)
@remote
class RemoteDatasetTest(parameterized.TestCase):
    dataset_name = None

    def setUp(self):
        self.dataset_tester = DatasetTester(self)

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
        n_samples = 10
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Use \n for newline. Windows automatically adds the \r when writing the file
            # see https://docs.python.org/3/library/os.html#os.linesep
            open(os.path.join(tmp_dir, "text.txt"), "w", encoding="utf-8").write(
                "\n".join("foo" for _ in range(n_samples))
            )
            ds = load_dataset(
                "./datasets/text", data_files=os.path.join(tmp_dir, "text.txt"), cache_dir=tmp_dir, split="train"
            )
            data_file = ds._data_files[0]
            fingerprint = ds._fingerprint
            self.assertEqual(len(ds), n_samples)
            del ds
            ds = load_dataset(
                "./datasets/text", data_files=os.path.join(tmp_dir, "text.txt"), cache_dir=tmp_dir, split="train"
            )
            self.assertEqual(ds._data_files[0], data_file)
            self.assertEqual(ds._fingerprint, fingerprint)
            del ds

            open(os.path.join(tmp_dir, "text.txt"), "w", encoding="utf-8").write(
                "\n".join("bar" for _ in range(n_samples))
            )
            ds = load_dataset(
                "./datasets/text", data_files=os.path.join(tmp_dir, "text.txt"), cache_dir=tmp_dir, split="train"
            )
            self.assertNotEqual(ds._data_files[0], data_file)
            self.assertNotEqual(ds._fingerprint, fingerprint)
            self.assertEqual(len(ds), n_samples)
            del ds


class CsvTest(TestCase):
    def test_caching(self):
        n_rows = 10

        features = Features({"foo": Value("string"), "bar": Value("string")})

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Use \n for newline. Windows automatically adds the \r when writing the file
            # see https://docs.python.org/3/library/os.html#os.linesep
            open(os.path.join(tmp_dir, "table.csv"), "w", encoding="utf-8").write(
                "\n".join(",".join(["foo", "bar"]) for _ in range(n_rows + 1))
            )
            ds = load_dataset(
                "./datasets/csv", data_files=os.path.join(tmp_dir, "table.csv"), cache_dir=tmp_dir, split="train"
            )
            data_file = ds._data_files[0]
            fingerprint = ds._fingerprint
            self.assertEqual(len(ds), n_rows)
            del ds
            ds = load_dataset(
                "./datasets/csv", data_files=os.path.join(tmp_dir, "table.csv"), cache_dir=tmp_dir, split="train"
            )
            self.assertEqual(ds._data_files[0], data_file)
            self.assertEqual(ds._fingerprint, fingerprint)
            del ds
            ds = load_dataset(
                "./datasets/csv",
                data_files=os.path.join(tmp_dir, "table.csv"),
                cache_dir=tmp_dir,
                split="train",
                features=features,
            )
            self.assertNotEqual(ds._data_files[0], data_file)
            self.assertNotEqual(ds._fingerprint, fingerprint)
            del ds

            open(os.path.join(tmp_dir, "table.csv"), "w", encoding="utf-8").write(
                "\n".join(",".join(["Foo", "Bar"]) for _ in range(n_rows + 1))
            )
            ds = load_dataset(
                "./datasets/csv", data_files=os.path.join(tmp_dir, "table.csv"), cache_dir=tmp_dir, split="train"
            )
            self.assertNotEqual(ds._data_files[0], data_file)
            self.assertNotEqual(ds._fingerprint, fingerprint)
            self.assertEqual(len(ds), n_rows)
            del ds

    def test_sep(self):
        n_rows = 10
        n_cols = 3

        with tempfile.TemporaryDirectory() as tmp_dir:
            open(os.path.join(tmp_dir, "table_comma.csv"), "w", encoding="utf-8").write(
                "\n".join(",".join([str(i) for i in range(n_cols)]) for _ in range(n_rows + 1))
            )
            open(os.path.join(tmp_dir, "table_tab.csv"), "w", encoding="utf-8").write(
                "\n".join("\t".join([str(i) for i in range(n_cols)]) for _ in range(n_rows + 1))
            )
            ds = load_dataset(
                "./datasets/csv",
                data_files=os.path.join(tmp_dir, "table_comma.csv"),
                cache_dir=tmp_dir,
                split="train",
                sep=",",
            )
            self.assertEqual(len(ds), n_rows)
            self.assertEqual(len(ds.column_names), n_cols)
            del ds
            ds = load_dataset(
                "./datasets/csv",
                data_files=os.path.join(tmp_dir, "table_tab.csv"),
                cache_dir=tmp_dir,
                split="train",
                sep="\t",
            )
            self.assertEqual(len(ds), n_rows)
            self.assertEqual(len(ds.column_names), n_cols)
            del ds
            ds = load_dataset(
                "./datasets/csv",
                data_files=os.path.join(tmp_dir, "table_comma.csv"),
                cache_dir=tmp_dir,
                split="train",
                sep="\t",
            )
            self.assertEqual(len(ds), n_rows)
            self.assertEqual(len(ds.column_names), 1)
            del ds

    def test_features(self):
        n_rows = 10
        n_cols = 3

        def get_features(type):
            return Features({str(i): Value(type) for i in range(n_cols)})

        with tempfile.TemporaryDirectory() as tmp_dir:
            open(os.path.join(tmp_dir, "table.csv"), "w", encoding="utf-8").write(
                "\n".join(",".join([str(i) for i in range(n_cols)]) for _ in range(n_rows + 1))
            )
            for type in ["float64", "int8"]:
                features = get_features(type)
                ds = load_dataset(
                    "./datasets/csv",
                    data_files=os.path.join(tmp_dir, "table.csv"),
                    cache_dir=tmp_dir,
                    split="train",
                    features=features,
                )
                self.assertEqual(len(ds), n_rows)
                self.assertDictEqual(ds.features, features)
                del ds
