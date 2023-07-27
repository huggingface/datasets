import importlib
import os
import pickle
import shutil
import tempfile
import time
from hashlib import sha256
from multiprocessing import Pool
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import dill
import pyarrow as pa
import pytest
import requests

import datasets
from datasets import config, load_dataset, load_from_disk
from datasets.arrow_dataset import Dataset
from datasets.arrow_writer import ArrowWriter
from datasets.builder import DatasetBuilder
from datasets.config import METADATA_CONFIGS_FIELD
from datasets.data_files import DataFilesDict
from datasets.dataset_dict import DatasetDict, IterableDatasetDict
from datasets.download.download_config import DownloadConfig
from datasets.features import Features, Value
from datasets.iterable_dataset import IterableDataset
from datasets.load import (
    CachedDatasetModuleFactory,
    CachedMetricModuleFactory,
    GithubMetricModuleFactory,
    HubDatasetModuleFactoryWithoutScript,
    HubDatasetModuleFactoryWithScript,
    LocalDatasetModuleFactoryWithoutScript,
    LocalDatasetModuleFactoryWithScript,
    LocalMetricModuleFactory,
    PackagedDatasetModuleFactory,
    infer_module_for_data_files_list,
    infer_module_for_data_files_list_in_archives,
)
from datasets.packaged_modules.audiofolder.audiofolder import AudioFolder, AudioFolderConfig
from datasets.packaged_modules.imagefolder.imagefolder import ImageFolder, ImageFolderConfig
from datasets.utils.logging import INFO, get_logger

from .utils import (
    OfflineSimulationMode,
    assert_arrow_memory_doesnt_increase,
    assert_arrow_memory_increases,
    offline,
    require_pil,
    require_sndfile,
    set_current_working_directory_to_temp_dir,
)


DATASET_LOADING_SCRIPT_NAME = "__dummy_dataset1__"

DATASET_LOADING_SCRIPT_CODE = """
import os

import datasets
from datasets import DatasetInfo, Features, Split, SplitGenerator, Value


class __DummyDataset1__(datasets.GeneratorBasedBuilder):

    def _info(self) -> DatasetInfo:
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        return [
            SplitGenerator(Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_manager.manual_dir, "train.txt")}),
            SplitGenerator(Split.TEST, gen_kwargs={"filepath": os.path.join(dl_manager.manual_dir, "test.txt")}),
        ]

    def _generate_examples(self, filepath, **kwargs):
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                yield i, {"text": line.strip()}
"""

SAMPLE_DATASET_IDENTIFIER = "lhoestq/test"  # has dataset script
SAMPLE_DATASET_IDENTIFIER2 = "lhoestq/test2"  # only has data files
SAMPLE_DATASET_IDENTIFIER3 = "mariosasko/test_multi_dir_dataset"  # has multiple data directories
SAMPLE_DATASET_IDENTIFIER4 = "mariosasko/test_imagefolder_with_metadata"  # imagefolder with a metadata file outside of the train/test directories
SAMPLE_NOT_EXISTING_DATASET_IDENTIFIER = "lhoestq/_dummy"
SAMPLE_DATASET_NAME_THAT_DOESNT_EXIST = "_dummy"
SAMPLE_DATASET_NO_CONFIGS_IN_METADATA = "datasets-maintainers/audiofolder_no_configs_in_metadata"
SAMPLE_DATASET_SINGLE_CONFIG_IN_METADATA = "datasets-maintainers/audiofolder_single_config_in_metadata"
SAMPLE_DATASET_TWO_CONFIG_IN_METADATA = "datasets-maintainers/audiofolder_two_configs_in_metadata"
SAMPLE_DATASET_TWO_CONFIG_IN_METADATA_WITH_DEFAULT = (
    "datasets-maintainers/audiofolder_two_configs_in_metadata_with_default"
)


METRIC_LOADING_SCRIPT_NAME = "__dummy_metric1__"

METRIC_LOADING_SCRIPT_CODE = """
import datasets
from datasets import MetricInfo, Features, Value


class __DummyMetric1__(datasets.Metric):

    def _info(self):
        return MetricInfo(features=Features({"predictions": Value("int"), "references": Value("int")}))

    def _compute(self, predictions, references):
        return {"__dummy_metric1__": sum(int(p == r) for p, r in zip(predictions, references))}
"""


@pytest.fixture
def data_dir(tmp_path):
    data_dir = tmp_path / "data_dir"
    data_dir.mkdir()
    with open(data_dir / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(data_dir / "test.txt", "w") as f:
        f.write("bar\n" * 10)
    return str(data_dir)


@pytest.fixture
def data_dir_with_arrow(tmp_path):
    data_dir = tmp_path / "data_dir"
    data_dir.mkdir()
    output_train = os.path.join(data_dir, "train.arrow")
    with ArrowWriter(path=output_train) as writer:
        writer.write_table(pa.Table.from_pydict({"col_1": ["foo"] * 10}))
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 10
    assert num_bytes > 0
    output_test = os.path.join(data_dir, "test.arrow")
    with ArrowWriter(path=output_test) as writer:
        writer.write_table(pa.Table.from_pydict({"col_1": ["bar"] * 10}))
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 10
    assert num_bytes > 0
    return str(data_dir)


@pytest.fixture
def data_dir_with_metadata(tmp_path):
    data_dir = tmp_path / "data_dir_with_metadata"
    data_dir.mkdir()
    with open(data_dir / "train.jpg", "wb") as f:
        f.write(b"train_image_bytes")
    with open(data_dir / "test.jpg", "wb") as f:
        f.write(b"test_image_bytes")
    with open(data_dir / "metadata.jsonl", "w") as f:
        f.write(
            """\
        {"file_name": "train.jpg", "caption": "Cool tran image"}
        {"file_name": "test.jpg", "caption": "Cool test image"}
        """
        )
    return str(data_dir)


@pytest.fixture
def data_dir_with_single_config_in_metadata(tmp_path):
    data_dir = tmp_path / "data_dir_with_one_default_config_in_metadata"

    cats_data_dir = data_dir / "cats"
    cats_data_dir.mkdir(parents=True)
    dogs_data_dir = data_dir / "dogs"
    dogs_data_dir.mkdir(parents=True)

    with open(cats_data_dir / "cat.jpg", "wb") as f:
        f.write(b"this_is_a_cat_image_bytes")
    with open(dogs_data_dir / "dog.jpg", "wb") as f:
        f.write(b"this_is_a_dog_image_bytes")
    with open(data_dir / "README.md", "w") as f:
        f.write(
            f"""\
---
{METADATA_CONFIGS_FIELD}:
  - config_name: custom
    drop_labels: true
---
        """
        )
    return str(data_dir)


@pytest.fixture
def data_dir_with_two_config_in_metadata(tmp_path):
    data_dir = tmp_path / "data_dir_with_two_configs_in_metadata"
    cats_data_dir = data_dir / "cats"
    cats_data_dir.mkdir(parents=True)
    dogs_data_dir = data_dir / "dogs"
    dogs_data_dir.mkdir(parents=True)

    with open(cats_data_dir / "cat.jpg", "wb") as f:
        f.write(b"this_is_a_cat_image_bytes")
    with open(dogs_data_dir / "dog.jpg", "wb") as f:
        f.write(b"this_is_a_dog_image_bytes")

    with open(data_dir / "README.md", "w") as f:
        f.write(
            f"""\
---
{METADATA_CONFIGS_FIELD}:
  - config_name: "v1"
    drop_labels: true
    default: true
  - config_name: "v2"
    drop_labels: false
---
        """
        )
    return str(data_dir)


@pytest.fixture
def data_dir_with_data_dir_configs_in_metadata(tmp_path):
    data_dir = tmp_path / "data_dir_with_two_configs_in_metadata"
    cats_data_dir = data_dir / "cats"
    cats_data_dir.mkdir(parents=True)
    dogs_data_dir = data_dir / "dogs"
    dogs_data_dir.mkdir(parents=True)

    with open(cats_data_dir / "cat.jpg", "wb") as f:
        f.write(b"this_is_a_cat_image_bytes")
    with open(dogs_data_dir / "dog.jpg", "wb") as f:
        f.write(b"this_is_a_dog_image_bytes")


@pytest.fixture
def sub_data_dirs(tmp_path):
    data_dir2 = tmp_path / "data_dir2"
    relative_subdir1 = "subdir1"
    sub_data_dir1 = data_dir2 / relative_subdir1
    sub_data_dir1.mkdir(parents=True)
    with open(sub_data_dir1 / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(sub_data_dir1 / "test.txt", "w") as f:
        f.write("bar\n" * 10)

    relative_subdir2 = "subdir2"
    sub_data_dir2 = tmp_path / data_dir2 / relative_subdir2
    sub_data_dir2.mkdir(parents=True)
    with open(sub_data_dir2 / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(sub_data_dir2 / "test.txt", "w") as f:
        f.write("bar\n" * 10)

    return str(data_dir2), relative_subdir1


@pytest.fixture
def complex_data_dir(tmp_path):
    data_dir = tmp_path / "complex_data_dir"
    data_dir.mkdir()
    (data_dir / "data").mkdir()
    with open(data_dir / "data" / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(data_dir / "data" / "test.txt", "w") as f:
        f.write("bar\n" * 10)
    with open(data_dir / "README.md", "w") as f:
        f.write("This is a readme")
    with open(data_dir / ".dummy", "w") as f:
        f.write("this is a dummy file that is not a data file")
    return str(data_dir)


@pytest.fixture
def dataset_loading_script_dir(tmp_path):
    script_name = DATASET_LOADING_SCRIPT_NAME
    script_dir = tmp_path / script_name
    script_dir.mkdir()
    script_path = script_dir / f"{script_name}.py"
    with open(script_path, "w") as f:
        f.write(DATASET_LOADING_SCRIPT_CODE)
    return str(script_dir)


@pytest.fixture
def dataset_loading_script_dir_readonly(tmp_path):
    script_name = DATASET_LOADING_SCRIPT_NAME
    script_dir = tmp_path / "readonly" / script_name
    script_dir.mkdir(parents=True)
    script_path = script_dir / f"{script_name}.py"
    with open(script_path, "w") as f:
        f.write(DATASET_LOADING_SCRIPT_CODE)
    dataset_loading_script_dir = str(script_dir)
    # Make this directory readonly
    os.chmod(dataset_loading_script_dir, 0o555)
    os.chmod(os.path.join(dataset_loading_script_dir, f"{script_name}.py"), 0o555)
    return dataset_loading_script_dir


@pytest.fixture
def metric_loading_script_dir(tmp_path):
    script_name = METRIC_LOADING_SCRIPT_NAME
    script_dir = tmp_path / script_name
    script_dir.mkdir()
    script_path = script_dir / f"{script_name}.py"
    with open(script_path, "w") as f:
        f.write(METRIC_LOADING_SCRIPT_CODE)
    return str(script_dir)


@pytest.mark.parametrize(
    "data_files, expected_module, expected_builder_kwargs",
    [
        (["train.csv"], "csv", {}),
        (["train.tsv"], "csv", {"sep": "\t"}),
        (["train.json"], "json", {}),
        (["train.jsonl"], "json", {}),
        (["train.parquet"], "parquet", {}),
        (["train.arrow"], "arrow", {}),
        (["train.txt"], "text", {}),
        (["uppercase.TXT"], "text", {}),
        (["unsupported.ext"], None, {}),
        ([""], None, {}),
    ],
)
def test_infer_module_for_data_files(data_files, expected_module, expected_builder_kwargs):
    module, builder_kwargs = infer_module_for_data_files_list(data_files)
    assert module == expected_module
    assert builder_kwargs == expected_builder_kwargs


@pytest.mark.parametrize(
    "data_file, expected_module",
    [
        ("zip_csv_path", "csv"),
        ("zip_csv_with_dir_path", "csv"),
        ("zip_uppercase_csv_path", "csv"),
        ("zip_unsupported_ext_path", None),
    ],
)
def test_infer_module_for_data_files_in_archives(
    data_file, expected_module, zip_csv_path, zip_csv_with_dir_path, zip_uppercase_csv_path, zip_unsupported_ext_path
):
    data_file_paths = {
        "zip_csv_path": zip_csv_path,
        "zip_csv_with_dir_path": zip_csv_with_dir_path,
        "zip_uppercase_csv_path": zip_uppercase_csv_path,
        "zip_unsupported_ext_path": zip_unsupported_ext_path,
    }
    data_files = [str(data_file_paths[data_file])]
    inferred_module, _ = infer_module_for_data_files_list_in_archives(data_files)
    assert inferred_module == expected_module


class ModuleFactoryTest(TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(
        self,
        jsonl_path,
        data_dir,
        data_dir_with_metadata,
        data_dir_with_single_config_in_metadata,
        data_dir_with_two_config_in_metadata,
        sub_data_dirs,
        dataset_loading_script_dir,
        metric_loading_script_dir,
    ):
        self._jsonl_path = jsonl_path
        self._data_dir = data_dir
        self._data_dir_with_metadata = data_dir_with_metadata
        self._data_dir_with_single_config_in_metadata = data_dir_with_single_config_in_metadata
        self._data_dir_with_two_config_in_metadata = data_dir_with_two_config_in_metadata
        self._data_dir2 = sub_data_dirs[0]
        self._sub_data_dir = sub_data_dirs[1]
        self._dataset_loading_script_dir = dataset_loading_script_dir
        self._metric_loading_script_dir = metric_loading_script_dir

    def setUp(self):
        self.hf_modules_cache = tempfile.mkdtemp()
        self.cache_dir = tempfile.mkdtemp()
        self.download_config = DownloadConfig(cache_dir=self.cache_dir)
        self.dynamic_modules_path = datasets.load.init_dynamic_modules(
            name="test_datasets_modules_" + os.path.basename(self.hf_modules_cache),
            hf_modules_cache=self.hf_modules_cache,
        )

    def test_HubDatasetModuleFactoryWithScript_with_github_dataset(self):
        # "wmt_t2t" has additional imports (internal)
        factory = HubDatasetModuleFactoryWithScript(
            "wmt_t2t", download_config=self.download_config, dynamic_modules_path=self.dynamic_modules_path
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert module_factory_result.builder_kwargs["base_path"].startswith(config.HF_ENDPOINT)

    def test_GithubMetricModuleFactory_with_internal_import(self):
        # "squad_v2" requires additional imports (internal)
        factory = GithubMetricModuleFactory(
            "squad_v2", download_config=self.download_config, dynamic_modules_path=self.dynamic_modules_path
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None

    @pytest.mark.filterwarnings("ignore:GithubMetricModuleFactory is deprecated:FutureWarning")
    def test_GithubMetricModuleFactory_with_external_import(self):
        # "bleu" requires additional imports (external from github)
        factory = GithubMetricModuleFactory(
            "bleu", download_config=self.download_config, dynamic_modules_path=self.dynamic_modules_path
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None

    def test_LocalMetricModuleFactory(self):
        path = os.path.join(self._metric_loading_script_dir, f"{METRIC_LOADING_SCRIPT_NAME}.py")
        factory = LocalMetricModuleFactory(
            path, download_config=self.download_config, dynamic_modules_path=self.dynamic_modules_path
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None

    def test_LocalDatasetModuleFactoryWithScript(self):
        path = os.path.join(self._dataset_loading_script_dir, f"{DATASET_LOADING_SCRIPT_NAME}.py")
        factory = LocalDatasetModuleFactoryWithScript(
            path, download_config=self.download_config, dynamic_modules_path=self.dynamic_modules_path
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert os.path.isdir(module_factory_result.builder_kwargs["base_path"])

    def test_LocalDatasetModuleFactoryWithoutScript(self):
        factory = LocalDatasetModuleFactoryWithoutScript(self._data_dir)
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert os.path.isdir(module_factory_result.builder_kwargs["base_path"])

    def test_LocalDatasetModuleFactoryWithoutScript_with_data_dir(self):
        factory = LocalDatasetModuleFactoryWithoutScript(self._data_dir2, data_dir=self._sub_data_dir)
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert (
            module_factory_result.builder_kwargs["data_files"] is not None
            and len(module_factory_result.builder_kwargs["data_files"]["train"]) == 1
            and len(module_factory_result.builder_kwargs["data_files"]["test"]) == 1
        )
        assert all(
            self._sub_data_dir in Path(data_file).parts
            for data_file in module_factory_result.builder_kwargs["data_files"]["train"]
            + module_factory_result.builder_kwargs["data_files"]["test"]
        )

    def test_LocalDatasetModuleFactoryWithoutScript_with_metadata(self):
        factory = LocalDatasetModuleFactoryWithoutScript(self._data_dir_with_metadata)
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert (
            module_factory_result.builder_kwargs["data_files"] is not None
            and len(module_factory_result.builder_kwargs["data_files"]["train"]) > 0
            and len(module_factory_result.builder_kwargs["data_files"]["test"]) > 0
        )
        assert any(
            Path(data_file).name == "metadata.jsonl"
            for data_file in module_factory_result.builder_kwargs["data_files"]["train"]
        )
        assert any(
            Path(data_file).name == "metadata.jsonl"
            for data_file in module_factory_result.builder_kwargs["data_files"]["test"]
        )

    def test_LocalDatasetModuleFactoryWithoutScript_with_single_config_in_metadata(self):
        factory = LocalDatasetModuleFactoryWithoutScript(
            self._data_dir_with_single_config_in_metadata,
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None

        module_metadata_configs = module_factory_result.builder_configs_parameters.metadata_configs
        assert module_metadata_configs is not None
        assert len(module_metadata_configs) == 1
        assert next(iter(module_metadata_configs)) == "custom"
        assert "drop_labels" in next(iter(module_metadata_configs.values()))
        assert next(iter(module_metadata_configs.values()))["drop_labels"] is True

        module_builder_configs = module_factory_result.builder_configs_parameters.builder_configs
        assert module_builder_configs is not None
        assert len(module_builder_configs) == 1
        assert isinstance(module_builder_configs[0], ImageFolderConfig)
        assert module_builder_configs[0].name == "custom"
        assert module_builder_configs[0].data_files is not None
        assert isinstance(module_builder_configs[0].data_files, DataFilesDict)
        assert len(module_builder_configs[0].data_files) == 1  # one train split
        assert len(module_builder_configs[0].data_files["train"]) == 2  # two files
        assert module_builder_configs[0].drop_labels is True  # parameter is passed from metadata

        # config named "default" is automatically considered to be a default config
        assert module_factory_result.builder_configs_parameters.default_config_name is None

        # we don't pass config params to builder in builder_kwargs, they are stored in builder_configs directly
        assert "drop_labels" not in module_factory_result.builder_kwargs

    def test_LocalDatasetModuleFactoryWithoutScript_with_two_configs_in_metadata(self):
        factory = LocalDatasetModuleFactoryWithoutScript(
            self._data_dir_with_two_config_in_metadata,
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None

        module_metadata_configs = module_factory_result.builder_configs_parameters.metadata_configs
        assert module_metadata_configs is not None
        assert len(module_metadata_configs) == 2
        assert list(module_metadata_configs) == ["v1", "v2"]
        assert "drop_labels" in module_metadata_configs["v1"]
        assert module_metadata_configs["v1"]["drop_labels"] is True
        assert "drop_labels" in module_metadata_configs["v2"]
        assert module_metadata_configs["v2"]["drop_labels"] is False

        module_builder_configs = module_factory_result.builder_configs_parameters.builder_configs
        assert module_builder_configs is not None
        assert len(module_builder_configs) == 2
        module_builder_config_v1, module_builder_config_v2 = module_builder_configs
        assert module_builder_config_v1.name == "v1"
        assert module_builder_config_v2.name == "v2"
        assert isinstance(module_builder_config_v1, ImageFolderConfig)
        assert isinstance(module_builder_config_v2, ImageFolderConfig)
        assert isinstance(module_builder_config_v1.data_files, DataFilesDict)
        assert isinstance(module_builder_config_v2.data_files, DataFilesDict)
        assert sorted(module_builder_config_v1.data_files) == ["train"]
        assert len(module_builder_config_v1.data_files["train"]) == 2
        assert sorted(module_builder_config_v2.data_files) == ["train"]
        assert len(module_builder_config_v2.data_files["train"]) == 2
        assert module_builder_config_v1.drop_labels is True  # parameter is passed from metadata
        assert module_builder_config_v2.drop_labels is False  # parameter is passed from metadata

        assert (
            module_factory_result.builder_configs_parameters.default_config_name == "v1"
        )  # it's marked as a default one in yaml

        # we don't pass config params to builder in builder_kwargs, they are stored in builder_configs directly
        assert "drop_labels" not in module_factory_result.builder_kwargs

    def test_PackagedDatasetModuleFactory(self):
        factory = PackagedDatasetModuleFactory(
            "json", data_files=self._jsonl_path, download_config=self.download_config
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None

    def test_PackagedDatasetModuleFactory_with_data_dir(self):
        factory = PackagedDatasetModuleFactory("json", data_dir=self._data_dir, download_config=self.download_config)
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert (
            module_factory_result.builder_kwargs["data_files"] is not None
            and len(module_factory_result.builder_kwargs["data_files"]["train"]) > 0
            and len(module_factory_result.builder_kwargs["data_files"]["test"]) > 0
        )
        assert Path(module_factory_result.builder_kwargs["data_files"]["train"][0]).parent.samefile(self._data_dir)
        assert Path(module_factory_result.builder_kwargs["data_files"]["test"][0]).parent.samefile(self._data_dir)

    def test_PackagedDatasetModuleFactory_with_data_dir_and_metadata(self):
        factory = PackagedDatasetModuleFactory(
            "imagefolder", data_dir=self._data_dir_with_metadata, download_config=self.download_config
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert (
            module_factory_result.builder_kwargs["data_files"] is not None
            and len(module_factory_result.builder_kwargs["data_files"]["train"]) > 0
            and len(module_factory_result.builder_kwargs["data_files"]["test"]) > 0
        )
        assert Path(module_factory_result.builder_kwargs["data_files"]["train"][0]).parent.samefile(
            self._data_dir_with_metadata
        )
        assert Path(module_factory_result.builder_kwargs["data_files"]["test"][0]).parent.samefile(
            self._data_dir_with_metadata
        )
        assert any(
            Path(data_file).name == "metadata.jsonl"
            for data_file in module_factory_result.builder_kwargs["data_files"]["train"]
        )
        assert any(
            Path(data_file).name == "metadata.jsonl"
            for data_file in module_factory_result.builder_kwargs["data_files"]["test"]
        )

    @pytest.mark.integration
    def test_HubDatasetModuleFactoryWithoutScript(self):
        factory = HubDatasetModuleFactoryWithoutScript(
            SAMPLE_DATASET_IDENTIFIER2, download_config=self.download_config
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert module_factory_result.builder_kwargs["base_path"].startswith(config.HF_ENDPOINT)

    @pytest.mark.integration
    def test_HubDatasetModuleFactoryWithoutScript_with_data_dir(self):
        data_dir = "data2"
        factory = HubDatasetModuleFactoryWithoutScript(
            SAMPLE_DATASET_IDENTIFIER3, data_dir=data_dir, download_config=self.download_config
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert module_factory_result.builder_kwargs["base_path"].startswith(config.HF_ENDPOINT)
        assert (
            module_factory_result.builder_kwargs["data_files"] is not None
            and len(module_factory_result.builder_kwargs["data_files"]["train"]) == 1
            and len(module_factory_result.builder_kwargs["data_files"]["test"]) == 1
        )
        assert all(
            data_dir in Path(data_file).parts
            for data_file in module_factory_result.builder_kwargs["data_files"]["train"]
            + module_factory_result.builder_kwargs["data_files"]["test"]
        )

    @pytest.mark.integration
    def test_HubDatasetModuleFactoryWithoutScript_with_metadata(self):
        factory = HubDatasetModuleFactoryWithoutScript(
            SAMPLE_DATASET_IDENTIFIER4, download_config=self.download_config
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert module_factory_result.builder_kwargs["base_path"].startswith(config.HF_ENDPOINT)
        assert (
            module_factory_result.builder_kwargs["data_files"] is not None
            and len(module_factory_result.builder_kwargs["data_files"]["train"]) > 0
            and len(module_factory_result.builder_kwargs["data_files"]["test"]) > 0
        )
        assert any(
            Path(data_file).name == "metadata.jsonl"
            for data_file in module_factory_result.builder_kwargs["data_files"]["train"]
        )
        assert any(
            Path(data_file).name == "metadata.jsonl"
            for data_file in module_factory_result.builder_kwargs["data_files"]["test"]
        )

    @pytest.mark.integration
    def test_HubDatasetModuleFactoryWithoutScript_with_one_default_config_in_metadata(self):
        factory = HubDatasetModuleFactoryWithoutScript(
            SAMPLE_DATASET_SINGLE_CONFIG_IN_METADATA,
            download_config=self.download_config,
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert module_factory_result.builder_kwargs["base_path"].startswith(config.HF_ENDPOINT)

        module_metadata_configs = module_factory_result.builder_configs_parameters.metadata_configs
        assert module_metadata_configs is not None
        assert len(module_metadata_configs) == 1
        assert next(iter(module_metadata_configs)) == "custom"
        assert "drop_labels" in next(iter(module_metadata_configs.values()))
        assert next(iter(module_metadata_configs.values()))["drop_labels"] is True

        module_builder_configs = module_factory_result.builder_configs_parameters.builder_configs
        assert module_builder_configs is not None
        assert len(module_builder_configs) == 1
        assert isinstance(module_builder_configs[0], AudioFolderConfig)
        assert module_builder_configs[0].name == "custom"
        assert module_builder_configs[0].data_files is not None
        assert isinstance(module_builder_configs[0].data_files, DataFilesDict)
        assert sorted(module_builder_configs[0].data_files) == ["test", "train"]
        assert len(module_builder_configs[0].data_files["train"]) == 3
        assert len(module_builder_configs[0].data_files["test"]) == 3
        assert module_builder_configs[0].drop_labels is True  # parameter is passed from metadata

        # config named "default" is automatically considered to be a default config
        assert module_factory_result.builder_configs_parameters.default_config_name is None

        # we don't pass config params to builder in builder_kwargs, they are stored in builder_configs directly
        assert "drop_labels" not in module_factory_result.builder_kwargs

    @pytest.mark.integration
    def test_HubDatasetModuleFactoryWithoutScript_with_two_configs_in_metadata(self):
        datasets_names = [SAMPLE_DATASET_TWO_CONFIG_IN_METADATA, SAMPLE_DATASET_TWO_CONFIG_IN_METADATA_WITH_DEFAULT]
        for dataset_name in datasets_names:
            factory = HubDatasetModuleFactoryWithoutScript(dataset_name, download_config=self.download_config)
            module_factory_result = factory.get_module()
            assert importlib.import_module(module_factory_result.module_path) is not None

            module_metadata_configs = module_factory_result.builder_configs_parameters.metadata_configs
            assert module_metadata_configs is not None
            assert len(module_metadata_configs) == 2
            assert list(module_metadata_configs) == ["v1", "v2"]
            assert "drop_labels" in module_metadata_configs["v1"]
            assert module_metadata_configs["v1"]["drop_labels"] is True
            assert "drop_labels" in module_metadata_configs["v2"]
            assert module_metadata_configs["v2"]["drop_labels"] is False

            module_builder_configs = module_factory_result.builder_configs_parameters.builder_configs
            assert module_builder_configs is not None
            assert len(module_builder_configs) == 2
            module_builder_config_v1, module_builder_config_v2 = module_builder_configs
            assert module_builder_config_v1.name == "v1"
            assert module_builder_config_v2.name == "v2"
            assert isinstance(module_builder_config_v1, AudioFolderConfig)
            assert isinstance(module_builder_config_v2, AudioFolderConfig)
            assert isinstance(module_builder_config_v1.data_files, DataFilesDict)
            assert isinstance(module_builder_config_v2.data_files, DataFilesDict)
            assert sorted(module_builder_config_v1.data_files) == ["test", "train"]
            assert len(module_builder_config_v1.data_files["train"]) == 3
            assert len(module_builder_config_v1.data_files["test"]) == 3
            assert sorted(module_builder_config_v2.data_files) == ["test", "train"]
            assert len(module_builder_config_v2.data_files["train"]) == 2
            assert len(module_builder_config_v2.data_files["test"]) == 1
            assert module_builder_config_v1.drop_labels is True  # parameter is passed from metadata
            assert module_builder_config_v2.drop_labels is False  # parameter is passed from metadata
            # we don't pass config params to builder in builder_kwargs, they are stored in builder_configs directly
            assert "drop_labels" not in module_factory_result.builder_kwargs

            if dataset_name == SAMPLE_DATASET_TWO_CONFIG_IN_METADATA_WITH_DEFAULT:
                assert module_factory_result.builder_configs_parameters.default_config_name == "v1"
            else:
                assert module_factory_result.builder_configs_parameters.default_config_name is None

    @pytest.mark.integration
    def test_HubDatasetModuleFactoryWithScript(self):
        factory = HubDatasetModuleFactoryWithScript(
            SAMPLE_DATASET_IDENTIFIER,
            download_config=self.download_config,
            dynamic_modules_path=self.dynamic_modules_path,
        )
        module_factory_result = factory.get_module()
        assert importlib.import_module(module_factory_result.module_path) is not None
        assert module_factory_result.builder_kwargs["base_path"].startswith(config.HF_ENDPOINT)

    def test_CachedDatasetModuleFactory(self):
        path = os.path.join(self._dataset_loading_script_dir, f"{DATASET_LOADING_SCRIPT_NAME}.py")
        factory = LocalDatasetModuleFactoryWithScript(
            path, download_config=self.download_config, dynamic_modules_path=self.dynamic_modules_path
        )
        module_factory_result = factory.get_module()
        for offline_mode in OfflineSimulationMode:
            with offline(offline_mode):
                factory = CachedDatasetModuleFactory(
                    DATASET_LOADING_SCRIPT_NAME,
                    dynamic_modules_path=self.dynamic_modules_path,
                )
                module_factory_result = factory.get_module()
                assert importlib.import_module(module_factory_result.module_path) is not None

    @pytest.mark.filterwarnings("ignore:LocalMetricModuleFactory is deprecated:FutureWarning")
    @pytest.mark.filterwarnings("ignore:CachedMetricModuleFactory is deprecated:FutureWarning")
    def test_CachedMetricModuleFactory(self):
        path = os.path.join(self._metric_loading_script_dir, f"{METRIC_LOADING_SCRIPT_NAME}.py")
        factory = LocalMetricModuleFactory(
            path, download_config=self.download_config, dynamic_modules_path=self.dynamic_modules_path
        )
        module_factory_result = factory.get_module()
        for offline_mode in OfflineSimulationMode:
            with offline(offline_mode):
                factory = CachedMetricModuleFactory(
                    METRIC_LOADING_SCRIPT_NAME,
                    dynamic_modules_path=self.dynamic_modules_path,
                )
                module_factory_result = factory.get_module()
                assert importlib.import_module(module_factory_result.module_path) is not None


@pytest.mark.parametrize(
    "factory_class",
    [
        CachedDatasetModuleFactory,
        CachedMetricModuleFactory,
        GithubMetricModuleFactory,
        HubDatasetModuleFactoryWithoutScript,
        HubDatasetModuleFactoryWithScript,
        LocalDatasetModuleFactoryWithoutScript,
        LocalDatasetModuleFactoryWithScript,
        LocalMetricModuleFactory,
        PackagedDatasetModuleFactory,
    ],
)
def test_module_factories(factory_class):
    name = "dummy_name"
    factory = factory_class(name)
    assert factory.name == name


@pytest.mark.integration
class LoadTest(TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def setUp(self):
        self.hf_modules_cache = tempfile.mkdtemp()
        self.dynamic_modules_path = datasets.load.init_dynamic_modules(
            name="test_datasets_modules2", hf_modules_cache=self.hf_modules_cache
        )

    def tearDown(self):
        shutil.rmtree(self.hf_modules_cache)

    def _dummy_module_dir(self, modules_dir, dummy_module_name, dummy_code):
        assert dummy_module_name.startswith("__")
        module_dir = os.path.join(modules_dir, dummy_module_name)
        os.makedirs(module_dir, exist_ok=True)
        module_path = os.path.join(module_dir, dummy_module_name + ".py")
        with open(module_path, "w") as f:
            f.write(dummy_code)
        return module_dir

    def test_dataset_module_factory(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # prepare module from directory path
            dummy_code = "MY_DUMMY_VARIABLE = 'hello there'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name1__", dummy_code)
            dataset_module = datasets.load.dataset_module_factory(
                module_dir, dynamic_modules_path=self.dynamic_modules_path
            )
            dummy_module = importlib.import_module(dataset_module.module_path)
            self.assertEqual(dummy_module.MY_DUMMY_VARIABLE, "hello there")
            self.assertEqual(dataset_module.hash, sha256(dummy_code.encode("utf-8")).hexdigest())
            # prepare module from file path + check resolved_file_path
            dummy_code = "MY_DUMMY_VARIABLE = 'general kenobi'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name1__", dummy_code)
            module_path = os.path.join(module_dir, "__dummy_module_name1__.py")
            dataset_module = datasets.load.dataset_module_factory(
                module_path, dynamic_modules_path=self.dynamic_modules_path
            )
            dummy_module = importlib.import_module(dataset_module.module_path)
            self.assertEqual(dummy_module.MY_DUMMY_VARIABLE, "general kenobi")
            self.assertEqual(dataset_module.hash, sha256(dummy_code.encode("utf-8")).hexdigest())
            # missing module
            for offline_simulation_mode in list(OfflineSimulationMode):
                with offline(offline_simulation_mode):
                    with self.assertRaises((FileNotFoundError, ConnectionError, requests.exceptions.ConnectionError)):
                        datasets.load.dataset_module_factory(
                            "__missing_dummy_module_name__", dynamic_modules_path=self.dynamic_modules_path
                        )

    def test_offline_dataset_module_factory(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_code = "MY_DUMMY_VARIABLE = 'hello there'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name2__", dummy_code)
            dataset_module_1 = datasets.load.dataset_module_factory(
                module_dir, dynamic_modules_path=self.dynamic_modules_path
            )
            time.sleep(0.1)  # make sure there's a difference in the OS update time of the python file
            dummy_code = "MY_DUMMY_VARIABLE = 'general kenobi'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name2__", dummy_code)
            dataset_module_2 = datasets.load.dataset_module_factory(
                module_dir, dynamic_modules_path=self.dynamic_modules_path
            )
        for offline_simulation_mode in list(OfflineSimulationMode):
            with offline(offline_simulation_mode):
                self._caplog.clear()
                # allow provide the module name without an explicit path to remote or local actual file
                dataset_module_3 = datasets.load.dataset_module_factory(
                    "__dummy_module_name2__", dynamic_modules_path=self.dynamic_modules_path
                )
                # it loads the most recent version of the module
                self.assertEqual(dataset_module_2.module_path, dataset_module_3.module_path)
                self.assertNotEqual(dataset_module_1.module_path, dataset_module_3.module_path)
                self.assertIn("Using the latest cached version of the module", self._caplog.text)

    def test_load_dataset_from_hub(self):
        with self.assertRaises(FileNotFoundError) as context:
            datasets.load_dataset("_dummy")
        self.assertIn(
            "Dataset '_dummy' doesn't exist on the Hub",
            str(context.exception),
        )
        with self.assertRaises(FileNotFoundError) as context:
            datasets.load_dataset("_dummy", revision="0.0.0")
        self.assertIn(
            "Dataset '_dummy' doesn't exist on the Hub",
            str(context.exception),
        )
        self.assertIn(
            "at revision '0.0.0'",
            str(context.exception),
        )
        for offline_simulation_mode in list(OfflineSimulationMode):
            with offline(offline_simulation_mode):
                with self.assertRaises(ConnectionError) as context:
                    datasets.load_dataset("_dummy")
                if offline_simulation_mode != OfflineSimulationMode.HF_DATASETS_OFFLINE_SET_TO_1:
                    self.assertIn(
                        "Couldn't reach '_dummy' on the Hub",
                        str(context.exception),
                    )

    def test_load_dataset_users(self):
        with self.assertRaises(FileNotFoundError) as context:
            datasets.load_dataset("lhoestq/_dummy")
        self.assertIn(
            "lhoestq/_dummy",
            str(context.exception),
        )
        for offline_simulation_mode in list(OfflineSimulationMode):
            with offline(offline_simulation_mode):
                with self.assertRaises(ConnectionError) as context:
                    datasets.load_dataset("lhoestq/_dummy")
                self.assertIn("lhoestq/_dummy", str(context.exception), msg=offline_simulation_mode)


@pytest.mark.integration
def test_load_dataset_builder_with_metadata():
    builder = datasets.load_dataset_builder(SAMPLE_DATASET_IDENTIFIER4)
    assert isinstance(builder, ImageFolder)
    assert builder.config.name == "default"
    assert builder.config.data_files is not None
    assert builder.config.drop_metadata is None
    builder = datasets.load_dataset_builder(SAMPLE_DATASET_IDENTIFIER4, "non-existing-config")
    assert isinstance(builder, ImageFolder)
    assert builder.config.name == "non-existing-config"


@pytest.mark.integration
def test_load_dataset_builder_config_kwargs_passed_as_arguments():
    builder_default = datasets.load_dataset_builder(SAMPLE_DATASET_IDENTIFIER4)
    builder_custom = datasets.load_dataset_builder(SAMPLE_DATASET_IDENTIFIER4, drop_metadata=True)
    assert builder_custom.config.drop_metadata != builder_default.config.drop_metadata
    assert builder_custom.config.drop_metadata is True


@pytest.mark.integration
def test_load_dataset_builder_with_two_configs_in_metadata():
    builder = datasets.load_dataset_builder(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA, "v1")
    assert isinstance(builder, AudioFolder)
    assert builder.config.name == "v1"
    assert builder.config.data_files is not None
    with pytest.raises(ValueError):
        datasets.load_dataset_builder(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA)
    with pytest.raises(ValueError):
        datasets.load_dataset_builder(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA, "non-existing-config")


@pytest.mark.parametrize("serializer", [pickle, dill])
def test_load_dataset_builder_with_metadata_configs_pickable(serializer):
    builder = datasets.load_dataset_builder(SAMPLE_DATASET_SINGLE_CONFIG_IN_METADATA)
    builder_unpickled = serializer.loads(serializer.dumps(builder))
    assert builder.BUILDER_CONFIGS == builder_unpickled.BUILDER_CONFIGS
    assert list(builder_unpickled.builder_configs) == ["custom"]
    assert isinstance(builder_unpickled.builder_configs["custom"], AudioFolderConfig)

    builder2 = datasets.load_dataset_builder(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA, "v1")
    builder2_unpickled = serializer.loads(serializer.dumps(builder2))
    assert builder2.BUILDER_CONFIGS == builder2_unpickled.BUILDER_CONFIGS != builder_unpickled.BUILDER_CONFIGS
    assert list(builder2_unpickled.builder_configs) == ["v1", "v2"]
    assert isinstance(builder2_unpickled.builder_configs["v1"], AudioFolderConfig)
    assert isinstance(builder2_unpickled.builder_configs["v2"], AudioFolderConfig)


def test_load_dataset_builder_for_absolute_script_dir(dataset_loading_script_dir, data_dir):
    builder = datasets.load_dataset_builder(dataset_loading_script_dir, data_dir=data_dir)
    assert isinstance(builder, DatasetBuilder)
    assert builder.name == DATASET_LOADING_SCRIPT_NAME
    assert builder.dataset_name == DATASET_LOADING_SCRIPT_NAME
    assert builder.info.features == Features({"text": Value("string")})


def test_load_dataset_builder_for_relative_script_dir(dataset_loading_script_dir, data_dir):
    with set_current_working_directory_to_temp_dir():
        relative_script_dir = DATASET_LOADING_SCRIPT_NAME
        shutil.copytree(dataset_loading_script_dir, relative_script_dir)
        builder = datasets.load_dataset_builder(relative_script_dir, data_dir=data_dir)
        assert isinstance(builder, DatasetBuilder)
        assert builder.name == DATASET_LOADING_SCRIPT_NAME
        assert builder.dataset_name == DATASET_LOADING_SCRIPT_NAME
        assert builder.info.features == Features({"text": Value("string")})


def test_load_dataset_builder_for_script_path(dataset_loading_script_dir, data_dir):
    builder = datasets.load_dataset_builder(
        os.path.join(dataset_loading_script_dir, DATASET_LOADING_SCRIPT_NAME + ".py"), data_dir=data_dir
    )
    assert isinstance(builder, DatasetBuilder)
    assert builder.name == DATASET_LOADING_SCRIPT_NAME
    assert builder.dataset_name == DATASET_LOADING_SCRIPT_NAME
    assert builder.info.features == Features({"text": Value("string")})


def test_load_dataset_builder_for_absolute_data_dir(complex_data_dir):
    builder = datasets.load_dataset_builder(complex_data_dir)
    assert isinstance(builder, DatasetBuilder)
    assert builder.name == "text"
    assert builder.dataset_name == Path(complex_data_dir).name
    assert builder.config.name == "default"
    assert isinstance(builder.config.data_files, DataFilesDict)
    assert len(builder.config.data_files["train"]) > 0
    assert len(builder.config.data_files["test"]) > 0


def test_load_dataset_builder_for_relative_data_dir(complex_data_dir):
    with set_current_working_directory_to_temp_dir():
        relative_data_dir = "relative_data_dir"
        shutil.copytree(complex_data_dir, relative_data_dir)
        builder = datasets.load_dataset_builder(relative_data_dir)
        assert isinstance(builder, DatasetBuilder)
        assert builder.name == "text"
        assert builder.dataset_name == relative_data_dir
        assert builder.config.name == "default"
        assert isinstance(builder.config.data_files, DataFilesDict)
        assert len(builder.config.data_files["train"]) > 0
        assert len(builder.config.data_files["test"]) > 0


@pytest.mark.integration
def test_load_dataset_builder_for_community_dataset_with_script():
    builder = datasets.load_dataset_builder(SAMPLE_DATASET_IDENTIFIER)
    assert isinstance(builder, DatasetBuilder)
    assert builder.name == SAMPLE_DATASET_IDENTIFIER.split("/")[-1]
    assert builder.dataset_name == SAMPLE_DATASET_IDENTIFIER.split("/")[-1]
    assert builder.config.name == "default"
    assert builder.info.features == Features({"text": Value("string")})
    namespace = SAMPLE_DATASET_IDENTIFIER[: SAMPLE_DATASET_IDENTIFIER.index("/")]
    assert builder._relative_data_dir().startswith(namespace)
    assert SAMPLE_DATASET_IDENTIFIER.replace("/", "--") in builder.__module__


@pytest.mark.integration
def test_load_dataset_builder_for_community_dataset_without_script():
    builder = datasets.load_dataset_builder(SAMPLE_DATASET_IDENTIFIER2)
    assert isinstance(builder, DatasetBuilder)
    assert builder.name == "text"
    assert builder.dataset_name == SAMPLE_DATASET_IDENTIFIER2.split("/")[-1]
    assert builder.config.name == "default"
    assert isinstance(builder.config.data_files, DataFilesDict)
    assert len(builder.config.data_files["train"]) > 0
    assert len(builder.config.data_files["test"]) > 0


def test_load_dataset_builder_fail():
    with pytest.raises(FileNotFoundError):
        datasets.load_dataset_builder("blabla")


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_load_dataset_local(dataset_loading_script_dir, data_dir, keep_in_memory, caplog):
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = load_dataset(dataset_loading_script_dir, data_dir=data_dir, keep_in_memory=keep_in_memory)
    assert isinstance(dataset, DatasetDict)
    assert all(isinstance(d, Dataset) for d in dataset.values())
    assert len(dataset) == 2
    assert isinstance(next(iter(dataset["train"])), dict)
    for offline_simulation_mode in list(OfflineSimulationMode):
        with offline(offline_simulation_mode):
            caplog.clear()
            # Load dataset from cache
            dataset = datasets.load_dataset(DATASET_LOADING_SCRIPT_NAME, data_dir=data_dir)
            assert len(dataset) == 2
            assert "Using the latest cached version of the module" in caplog.text
    with pytest.raises(FileNotFoundError) as exc_info:
        datasets.load_dataset(SAMPLE_DATASET_NAME_THAT_DOESNT_EXIST)
    assert f"Dataset '{SAMPLE_DATASET_NAME_THAT_DOESNT_EXIST}' doesn't exist on the Hub" in str(exc_info.value)
    assert os.path.abspath(SAMPLE_DATASET_NAME_THAT_DOESNT_EXIST) in str(exc_info.value)


def test_load_dataset_streaming(dataset_loading_script_dir, data_dir):
    dataset = load_dataset(dataset_loading_script_dir, streaming=True, data_dir=data_dir)
    assert isinstance(dataset, IterableDatasetDict)
    assert all(isinstance(d, IterableDataset) for d in dataset.values())
    assert len(dataset) == 2
    assert isinstance(next(iter(dataset["train"])), dict)


def test_load_dataset_streaming_gz_json(jsonl_gz_path):
    data_files = jsonl_gz_path
    ds = load_dataset("json", split="train", data_files=data_files, streaming=True)
    assert isinstance(ds, IterableDataset)
    ds_item = next(iter(ds))
    assert ds_item == {"col_1": "0", "col_2": 0, "col_3": 0.0}


@pytest.mark.integration
@pytest.mark.parametrize(
    "path", ["sample.jsonl", "sample.jsonl.gz", "sample.tar", "sample.jsonl.xz", "sample.zip", "sample.jsonl.zst"]
)
def test_load_dataset_streaming_compressed_files(path):
    repo_id = "albertvillanova/datasets-tests-compression"
    data_files = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{path}"
    if data_files[-3:] in ("zip", "tar"):  # we need to glob "*" inside archives
        data_files = data_files[-3:] + "://*::" + data_files
        return  # TODO(QL, albert): support re-add support for ZIP and TAR archives streaming
    ds = load_dataset("json", split="train", data_files=data_files, streaming=True)
    assert isinstance(ds, IterableDataset)
    ds_item = next(iter(ds))
    assert ds_item == {
        "tokens": ["Ministeri", "de", "Justícia", "d'Espanya"],
        "ner_tags": [1, 2, 2, 2],
        "langs": ["ca", "ca", "ca", "ca"],
        "spans": ["PER: Ministeri de Justícia d'Espanya"],
    }


@pytest.mark.parametrize("path_extension", ["csv", "csv.bz2"])
@pytest.mark.parametrize("streaming", [False, True])
def test_load_dataset_streaming_csv(path_extension, streaming, csv_path, bz2_csv_path):
    paths = {"csv": csv_path, "csv.bz2": bz2_csv_path}
    data_files = str(paths[path_extension])
    features = Features({"col_1": Value("string"), "col_2": Value("int32"), "col_3": Value("float32")})
    ds = load_dataset("csv", split="train", data_files=data_files, features=features, streaming=streaming)
    assert isinstance(ds, IterableDataset if streaming else Dataset)
    ds_item = next(iter(ds))
    assert ds_item == {"col_1": "0", "col_2": 0, "col_3": 0.0}


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("data_file", ["zip_csv_path", "zip_csv_with_dir_path", "csv_path"])
def test_load_dataset_zip_csv(data_file, streaming, zip_csv_path, zip_csv_with_dir_path, csv_path):
    data_file_paths = {
        "zip_csv_path": zip_csv_path,
        "zip_csv_with_dir_path": zip_csv_with_dir_path,
        "csv_path": csv_path,
    }
    data_files = str(data_file_paths[data_file])
    expected_size = 8 if data_file.startswith("zip") else 4
    features = Features({"col_1": Value("string"), "col_2": Value("int32"), "col_3": Value("float32")})
    ds = load_dataset("csv", split="train", data_files=data_files, features=features, streaming=streaming)
    if streaming:
        ds_item_counter = 0
        for ds_item in ds:
            if ds_item_counter == 0:
                assert ds_item == {"col_1": "0", "col_2": 0, "col_3": 0.0}
            ds_item_counter += 1
        assert ds_item_counter == expected_size
    else:
        assert ds.shape[0] == expected_size
        ds_item = next(iter(ds))
        assert ds_item == {"col_1": "0", "col_2": 0, "col_3": 0.0}


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("data_file", ["zip_jsonl_path", "zip_jsonl_with_dir_path", "jsonl_path"])
def test_load_dataset_zip_jsonl(data_file, streaming, zip_jsonl_path, zip_jsonl_with_dir_path, jsonl_path):
    data_file_paths = {
        "zip_jsonl_path": zip_jsonl_path,
        "zip_jsonl_with_dir_path": zip_jsonl_with_dir_path,
        "jsonl_path": jsonl_path,
    }
    data_files = str(data_file_paths[data_file])
    expected_size = 8 if data_file.startswith("zip") else 4
    features = Features({"col_1": Value("string"), "col_2": Value("int32"), "col_3": Value("float32")})
    ds = load_dataset("json", split="train", data_files=data_files, features=features, streaming=streaming)
    if streaming:
        ds_item_counter = 0
        for ds_item in ds:
            if ds_item_counter == 0:
                assert ds_item == {"col_1": "0", "col_2": 0, "col_3": 0.0}
            ds_item_counter += 1
        assert ds_item_counter == expected_size
    else:
        assert ds.shape[0] == expected_size
        ds_item = next(iter(ds))
        assert ds_item == {"col_1": "0", "col_2": 0, "col_3": 0.0}


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("data_file", ["zip_text_path", "zip_text_with_dir_path", "text_path"])
def test_load_dataset_zip_text(data_file, streaming, zip_text_path, zip_text_with_dir_path, text_path):
    data_file_paths = {
        "zip_text_path": zip_text_path,
        "zip_text_with_dir_path": zip_text_with_dir_path,
        "text_path": text_path,
    }
    data_files = str(data_file_paths[data_file])
    expected_size = 8 if data_file.startswith("zip") else 4
    ds = load_dataset("text", split="train", data_files=data_files, streaming=streaming)
    if streaming:
        ds_item_counter = 0
        for ds_item in ds:
            if ds_item_counter == 0:
                assert ds_item == {"text": "0"}
            ds_item_counter += 1
        assert ds_item_counter == expected_size
    else:
        assert ds.shape[0] == expected_size
        ds_item = next(iter(ds))
        assert ds_item == {"text": "0"}


@pytest.mark.parametrize("streaming", [False, True])
def test_load_dataset_arrow(streaming, data_dir_with_arrow):
    ds = load_dataset("arrow", split="train", data_dir=data_dir_with_arrow, streaming=streaming)
    expected_size = 10
    if streaming:
        ds_item_counter = 0
        for ds_item in ds:
            if ds_item_counter == 0:
                assert ds_item == {"col_1": "foo"}
            ds_item_counter += 1
        assert ds_item_counter == 10
    else:
        assert ds.num_rows == 10
        assert ds.shape[0] == expected_size
        ds_item = next(iter(ds))
        assert ds_item == {"col_1": "foo"}


def test_load_dataset_text_with_unicode_new_lines(text_path_with_unicode_new_lines):
    data_files = str(text_path_with_unicode_new_lines)
    ds = load_dataset("text", split="train", data_files=data_files)
    assert ds.num_rows == 3


def test_load_dataset_with_unsupported_extensions(text_dir_with_unsupported_extension):
    data_files = str(text_dir_with_unsupported_extension)
    ds = load_dataset("text", split="train", data_files=data_files)
    assert ds.num_rows == 4


@pytest.mark.integration
def test_loading_from_the_datasets_hub():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dataset = load_dataset(SAMPLE_DATASET_IDENTIFIER, cache_dir=tmp_dir)
        assert len(dataset["train"]) == 2
        assert len(dataset["validation"]) == 3
        del dataset


@pytest.mark.integration
def test_loading_from_the_datasets_hub_with_token():
    true_request = requests.Session().request

    def assert_auth(method, url, *args, headers, **kwargs):
        assert headers["authorization"] == "Bearer foo"
        return true_request(method, url, *args, headers=headers, **kwargs)

    with patch("requests.Session.request") as mock_request:
        mock_request.side_effect = assert_auth
        with tempfile.TemporaryDirectory() as tmp_dir:
            with offline():
                with pytest.raises((ConnectionError, requests.exceptions.ConnectionError)):
                    load_dataset(SAMPLE_NOT_EXISTING_DATASET_IDENTIFIER, cache_dir=tmp_dir, token="foo")
        mock_request.assert_called()


@pytest.mark.integration
def test_load_streaming_private_dataset(hf_token, hf_private_dataset_repo_txt_data):
    ds = load_dataset(hf_private_dataset_repo_txt_data, streaming=True)
    assert next(iter(ds)) is not None


@pytest.mark.integration
def test_load_streaming_private_dataset_with_zipped_data(hf_token, hf_private_dataset_repo_zipped_txt_data):
    ds = load_dataset(hf_private_dataset_repo_zipped_txt_data, streaming=True)
    assert next(iter(ds)) is not None


@pytest.mark.integration
def test_load_dataset_config_kwargs_passed_as_arguments():
    ds_default = load_dataset(SAMPLE_DATASET_IDENTIFIER4)
    ds_custom = load_dataset(SAMPLE_DATASET_IDENTIFIER4, drop_metadata=True)
    assert list(ds_default["train"].features) == ["image", "caption"]
    assert list(ds_custom["train"].features) == ["image"]


@require_sndfile
@pytest.mark.integration
def test_load_hub_dataset_without_script_with_single_config_in_metadata():
    # load the same dataset but with no configurations (=with default parameters)
    ds = load_dataset(SAMPLE_DATASET_NO_CONFIGS_IN_METADATA)
    assert list(ds["train"].features) == ["audio", "label"]  # assert label feature is here as expected by default
    assert len(ds["train"]) == 5 and len(ds["test"]) == 4

    ds2 = load_dataset(SAMPLE_DATASET_SINGLE_CONFIG_IN_METADATA)  # single config -> no need to specify it
    assert list(ds2["train"].features) == ["audio"]  # assert param `drop_labels=True` from metadata is passed
    assert len(ds2["train"]) == 3 and len(ds2["test"]) == 3

    ds3 = load_dataset(SAMPLE_DATASET_SINGLE_CONFIG_IN_METADATA, "custom")
    assert list(ds3["train"].features) == ["audio"]  # assert param `drop_labels=True` from metadata is passed
    assert len(ds3["train"]) == 3 and len(ds3["test"]) == 3

    with pytest.raises(ValueError):
        # no config named "default"
        _ = load_dataset(SAMPLE_DATASET_SINGLE_CONFIG_IN_METADATA, "default")


@require_sndfile
@pytest.mark.integration
def test_load_hub_dataset_without_script_with_two_config_in_metadata():
    ds = load_dataset(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA, "v1")
    assert list(ds["train"].features) == ["audio"]  # assert param `drop_labels=True` from metadata is passed
    assert len(ds["train"]) == 3 and len(ds["test"]) == 3

    ds2 = load_dataset(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA, "v2")
    assert list(ds2["train"].features) == [
        "audio",
        "label",
    ]  # assert param `drop_labels=False` from metadata is passed
    assert len(ds2["train"]) == 2 and len(ds2["test"]) == 1

    with pytest.raises(ValueError):
        # config is required but not specified
        _ = load_dataset(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA)

    with pytest.raises(ValueError):
        # no config named "default"
        _ = load_dataset(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA, "default")

    ds_with_default = load_dataset(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA_WITH_DEFAULT)
    # it's a dataset with the same data but "v1" config is marked as a default one
    assert list(ds_with_default["train"].features) == list(ds["train"].features)
    assert len(ds_with_default["train"]) == len(ds["train"]) and len(ds_with_default["test"]) == len(ds["test"])


@require_sndfile
@pytest.mark.integration
def test_load_hub_dataset_without_script_with_metadata_config_in_parallel():
    # assert it doesn't fail (pickling of dynamically created class works)
    ds = load_dataset(SAMPLE_DATASET_SINGLE_CONFIG_IN_METADATA, num_proc=2)
    assert "label" not in ds["train"].features  # assert param `drop_labels=True` from metadata is passed
    assert len(ds["train"]) == 3 and len(ds["test"]) == 3

    ds = load_dataset(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA, "v1", num_proc=2)
    assert "label" not in ds["train"].features  # assert param `drop_labels=True` from metadata is passed
    assert len(ds["train"]) == 3 and len(ds["test"]) == 3

    ds = load_dataset(SAMPLE_DATASET_TWO_CONFIG_IN_METADATA, "v2", num_proc=2)
    assert "label" in ds["train"].features
    assert len(ds["train"]) == 2 and len(ds["test"]) == 1


@require_pil
@pytest.mark.integration
@pytest.mark.parametrize("implicit_token", [True])
@pytest.mark.parametrize("streaming", [True])
def test_load_dataset_private_zipped_images(
    hf_private_dataset_repo_zipped_img_data, hf_token, streaming, implicit_token
):
    token = None if implicit_token else hf_token
    ds = load_dataset(hf_private_dataset_repo_zipped_img_data, split="train", streaming=streaming, token=token)
    assert isinstance(ds, IterableDataset if streaming else Dataset)
    ds_items = list(ds)
    assert len(ds_items) == 2


def test_load_dataset_then_move_then_reload(dataset_loading_script_dir, data_dir, tmp_path, caplog):
    cache_dir1 = tmp_path / "cache1"
    cache_dir2 = tmp_path / "cache2"
    dataset = load_dataset(dataset_loading_script_dir, data_dir=data_dir, split="train", cache_dir=cache_dir1)
    fingerprint1 = dataset._fingerprint
    del dataset
    os.rename(cache_dir1, cache_dir2)
    caplog.clear()
    with caplog.at_level(INFO, logger=get_logger().name):
        dataset = load_dataset(dataset_loading_script_dir, data_dir=data_dir, split="train", cache_dir=cache_dir2)
    assert "Found cached dataset" in caplog.text
    assert dataset._fingerprint == fingerprint1, "for the caching mechanism to work, fingerprint should stay the same"
    dataset = load_dataset(dataset_loading_script_dir, data_dir=data_dir, split="test", cache_dir=cache_dir2)
    assert dataset._fingerprint != fingerprint1


def test_load_dataset_readonly(dataset_loading_script_dir, dataset_loading_script_dir_readonly, data_dir, tmp_path):
    cache_dir1 = tmp_path / "cache1"
    cache_dir2 = tmp_path / "cache2"
    dataset = load_dataset(dataset_loading_script_dir, data_dir=data_dir, split="train", cache_dir=cache_dir1)
    fingerprint1 = dataset._fingerprint
    del dataset
    # Load readonly dataset and check that the fingerprint is the same.
    dataset = load_dataset(dataset_loading_script_dir_readonly, data_dir=data_dir, split="train", cache_dir=cache_dir2)
    assert dataset._fingerprint == fingerprint1, "Cannot load a dataset in a readonly folder."


@pytest.mark.parametrize("max_in_memory_dataset_size", ["default", 0, 50, 500])
def test_load_dataset_local_with_default_in_memory(
    max_in_memory_dataset_size, dataset_loading_script_dir, data_dir, monkeypatch
):
    current_dataset_size = 148
    if max_in_memory_dataset_size == "default":
        max_in_memory_dataset_size = 0  # default
    else:
        monkeypatch.setattr(datasets.config, "IN_MEMORY_MAX_SIZE", max_in_memory_dataset_size)
    if max_in_memory_dataset_size:
        expected_in_memory = current_dataset_size < max_in_memory_dataset_size
    else:
        expected_in_memory = False

    with assert_arrow_memory_increases() if expected_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = load_dataset(dataset_loading_script_dir, data_dir=data_dir)
    assert (dataset["train"].dataset_size < max_in_memory_dataset_size) is expected_in_memory


@pytest.mark.parametrize("max_in_memory_dataset_size", ["default", 0, 100, 1000])
def test_load_from_disk_with_default_in_memory(
    max_in_memory_dataset_size, dataset_loading_script_dir, data_dir, tmp_path, monkeypatch
):
    current_dataset_size = 512  # arrow file size = 512, in-memory dataset size = 148
    if max_in_memory_dataset_size == "default":
        max_in_memory_dataset_size = 0  # default
    else:
        monkeypatch.setattr(datasets.config, "IN_MEMORY_MAX_SIZE", max_in_memory_dataset_size)
    if max_in_memory_dataset_size:
        expected_in_memory = current_dataset_size < max_in_memory_dataset_size
    else:
        expected_in_memory = False

    dset = load_dataset(dataset_loading_script_dir, data_dir=data_dir, keep_in_memory=True)
    dataset_path = os.path.join(tmp_path, "saved_dataset")
    dset.save_to_disk(dataset_path)

    with assert_arrow_memory_increases() if expected_in_memory else assert_arrow_memory_doesnt_increase():
        _ = load_from_disk(dataset_path)


@pytest.mark.integration
def test_remote_data_files():
    repo_id = "albertvillanova/tests-raw-jsonl"
    filename = "wikiann-bn-validation.jsonl"
    data_files = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{filename}"
    ds = load_dataset("json", split="train", data_files=data_files, streaming=True)
    assert isinstance(ds, IterableDataset)
    ds_item = next(iter(ds))
    assert ds_item.keys() == {"langs", "ner_tags", "spans", "tokens"}


@pytest.mark.parametrize("deleted", [False, True])
def test_load_dataset_deletes_extracted_files(deleted, jsonl_gz_path, tmp_path):
    data_files = jsonl_gz_path
    cache_dir = tmp_path / "cache"
    if deleted:
        download_config = DownloadConfig(delete_extracted=True, cache_dir=cache_dir / "downloads")
        ds = load_dataset(
            "json", split="train", data_files=data_files, cache_dir=cache_dir, download_config=download_config
        )
    else:  # default
        ds = load_dataset("json", split="train", data_files=data_files, cache_dir=cache_dir)
    assert ds[0] == {"col_1": "0", "col_2": 0, "col_3": 0.0}
    assert (
        [path for path in (cache_dir / "downloads" / "extracted").iterdir() if path.suffix != ".lock"] == []
    ) is deleted


def distributed_load_dataset(args):
    data_name, tmp_dir, datafiles = args
    dataset = load_dataset(data_name, cache_dir=tmp_dir, data_files=datafiles)
    return dataset


def test_load_dataset_distributed(tmp_path, csv_path):
    num_workers = 5
    args = "csv", str(tmp_path), csv_path
    with Pool(processes=num_workers) as pool:  # start num_workers processes
        datasets = pool.map(distributed_load_dataset, [args] * num_workers)
        assert len(datasets) == num_workers
        assert all(len(dataset) == len(datasets[0]) > 0 for dataset in datasets)
        assert len(datasets[0].cache_files) > 0
        assert all(dataset.cache_files == datasets[0].cache_files for dataset in datasets)


def test_load_dataset_with_storage_options(mockfs):
    with mockfs.open("data.txt", "w") as f:
        f.write("Hello there\n")
        f.write("General Kenobi !")
    data_files = {"train": ["mock://data.txt"]}
    ds = load_dataset("text", data_files=data_files, storage_options=mockfs.storage_options)
    assert list(ds["train"]) == [{"text": "Hello there"}, {"text": "General Kenobi !"}]


@require_pil
def test_load_dataset_with_storage_options_with_decoding(mockfs, image_file):
    import PIL.Image

    filename = os.path.basename(image_file)
    with mockfs.open(filename, "wb") as fout:
        with open(image_file, "rb") as fin:
            fout.write(fin.read())
    data_files = {"train": ["mock://" + filename]}
    ds = load_dataset("imagefolder", data_files=data_files, storage_options=mockfs.storage_options)
    assert len(ds["train"]) == 1
    assert isinstance(ds["train"][0]["image"], PIL.Image.Image)
