import importlib
import os
import shutil
import tempfile
import time
from hashlib import sha256
from unittest import TestCase
from unittest.mock import patch

import pytest
import requests

import datasets
from datasets import load_dataset, load_from_disk

from .utils import OfflineSimulationMode, assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases, offline


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

SAMPLE_DATASET_IDENTIFIER = "lhoestq/test"
SAMPLE_NOT_EXISTING_DATASET_IDENTIFIER = "lhoestq/_dummy"


@pytest.fixture
def data_dir(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    with open(data_dir / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(data_dir / "test.txt", "w") as f:
        f.write("bar\n" * 10)
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


class LoadTest(TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def setUp(self):
        self.hf_modules_cache = tempfile.mkdtemp()
        self.dynamic_modules_path = datasets.load.init_dynamic_modules("test_datasets_modules", self.hf_modules_cache)

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

    def test_prepare_module(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # prepare module from directory path
            dummy_code = "MY_DUMMY_VARIABLE = 'hello there'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name1__", dummy_code)
            importable_module_path, module_hash = datasets.load.prepare_module(
                module_dir, dynamic_modules_path=self.dynamic_modules_path
            )
            dummy_module = importlib.import_module(importable_module_path)
            self.assertEqual(dummy_module.MY_DUMMY_VARIABLE, "hello there")
            self.assertEqual(module_hash, sha256(dummy_code.encode("utf-8")).hexdigest())
            # prepare module from file path + check resolved_file_path
            dummy_code = "MY_DUMMY_VARIABLE = 'general kenobi'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name1__", dummy_code)
            module_path = os.path.join(module_dir, "__dummy_module_name1__.py")
            importable_module_path, module_hash, resolved_file_path = datasets.load.prepare_module(
                module_path, dynamic_modules_path=self.dynamic_modules_path, return_resolved_file_path=True
            )
            self.assertEqual(resolved_file_path, module_path)
            dummy_module = importlib.import_module(importable_module_path)
            self.assertEqual(dummy_module.MY_DUMMY_VARIABLE, "general kenobi")
            self.assertEqual(module_hash, sha256(dummy_code.encode("utf-8")).hexdigest())
            # missing module
            for offline_simulation_mode in list(OfflineSimulationMode):
                with offline(offline_simulation_mode):
                    with self.assertRaises((FileNotFoundError, ConnectionError, requests.exceptions.ConnectionError)):
                        datasets.load.prepare_module(
                            "__missing_dummy_module_name__", dynamic_modules_path=self.dynamic_modules_path
                        )

    def test_offline_prepare_module(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_code = "MY_DUMMY_VARIABLE = 'hello there'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name2__", dummy_code)
            importable_module_path1, _ = datasets.load.prepare_module(
                module_dir, dynamic_modules_path=self.dynamic_modules_path
            )
            time.sleep(0.1)  # make sure there's a difference in the OS update time of the python file
            dummy_code = "MY_DUMMY_VARIABLE = 'general kenobi'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name2__", dummy_code)
            importable_module_path2, _ = datasets.load.prepare_module(
                module_dir, dynamic_modules_path=self.dynamic_modules_path
            )
        for offline_simulation_mode in list(OfflineSimulationMode):
            with offline(offline_simulation_mode):
                self._caplog.clear()
                # allow provide the module name without an explicit path to remote or local actual file
                importable_module_path3, _ = datasets.load.prepare_module(
                    "__dummy_module_name2__", dynamic_modules_path=self.dynamic_modules_path
                )
                # it loads the most recent version of the module
                self.assertEqual(importable_module_path2, importable_module_path3)
                self.assertNotEqual(importable_module_path1, importable_module_path3)
                self.assertIn("Using the latest cached version of the module", self._caplog.text)

    def test_load_dataset_canonical(self):
        with self.assertRaises(FileNotFoundError) as context:
            datasets.load_dataset("_dummy")
        self.assertIn(
            "https://raw.githubusercontent.com/huggingface/datasets/master/datasets/_dummy/_dummy.py",
            str(context.exception),
        )
        with self.assertRaises(FileNotFoundError) as context:
            datasets.load_dataset("_dummy", script_version="0.0.0")
        self.assertIn(
            "https://raw.githubusercontent.com/huggingface/datasets/0.0.0/datasets/_dummy/_dummy.py",
            str(context.exception),
        )
        for offline_simulation_mode in list(OfflineSimulationMode):
            with offline(offline_simulation_mode):
                with self.assertRaises(ConnectionError) as context:
                    datasets.load_dataset("_dummy")
                self.assertIn(
                    "https://raw.githubusercontent.com/huggingface/datasets/master/datasets/_dummy/_dummy.py",
                    str(context.exception),
                )

    def test_load_dataset_users(self):
        with self.assertRaises(FileNotFoundError) as context:
            datasets.load_dataset("lhoestq/_dummy")
        self.assertIn(
            "https://huggingface.co/datasets/lhoestq/_dummy/resolve/main/_dummy.py",
            str(context.exception),
        )
        for offline_simulation_mode in list(OfflineSimulationMode):
            with offline(offline_simulation_mode):
                with self.assertRaises(ConnectionError) as context:
                    datasets.load_dataset("lhoestq/_dummy")
                self.assertIn(
                    "https://huggingface.co/datasets/lhoestq/_dummy/resolve/main/_dummy.py",
                    str(context.exception),
                )


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_load_dataset_local(dataset_loading_script_dir, data_dir, keep_in_memory, caplog):
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = load_dataset(dataset_loading_script_dir, data_dir=data_dir, keep_in_memory=keep_in_memory)
    assert len(dataset) == 2
    for offline_simulation_mode in list(OfflineSimulationMode):
        with offline(offline_simulation_mode):
            caplog.clear()
            # Load dataset from cache
            dataset = datasets.load_dataset(DATASET_LOADING_SCRIPT_NAME, data_dir=data_dir)
            assert len(dataset) == 2
            assert "Using the latest cached version of the module" in caplog.text
    with pytest.raises(FileNotFoundError) as exc_info:
        datasets.load_dataset("_dummy")
    assert "at " + os.path.join("_dummy", "_dummy.py") in str(exc_info.value)


def test_loading_from_the_datasets_hub():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dataset = load_dataset(SAMPLE_DATASET_IDENTIFIER, cache_dir=tmp_dir)
        assert len(dataset["train"]), 2
        assert len(dataset["validation"]), 3
        del dataset


def test_loading_from_the_datasets_hub_with_use_auth_token():
    from datasets.utils.file_utils import http_head

    def assert_auth(url, *args, headers, **kwargs):
        assert headers["authorization"] == "Bearer foo"
        return http_head(url, *args, headers=headers, **kwargs)

    with patch("datasets.utils.file_utils.http_head") as mock_head:
        mock_head.side_effect = assert_auth
        with tempfile.TemporaryDirectory() as tmp_dir:
            with offline():
                with pytest.raises(ConnectionError):
                    load_dataset(SAMPLE_NOT_EXISTING_DATASET_IDENTIFIER, cache_dir=tmp_dir, use_auth_token="foo")
        mock_head.assert_called()


@pytest.mark.parametrize("max_in_memory_dataset_size", ["default", None, 0, 50, 500])
def test_load_dataset_local_with_default_in_memory(
    max_in_memory_dataset_size, dataset_loading_script_dir, data_dir, monkeypatch
):
    current_dataset_size = 148
    if max_in_memory_dataset_size == "default":
        # default = 250 * 2 ** 20
        max_in_memory_dataset_size = datasets.config.MAX_IN_MEMORY_DATASET_SIZE_IN_BYTES
    else:
        monkeypatch.setattr(datasets.config, "MAX_IN_MEMORY_DATASET_SIZE_IN_BYTES", max_in_memory_dataset_size)
    if max_in_memory_dataset_size is None:
        max_in_memory_dataset_size = 0
        expected_in_memory = False
    else:
        expected_in_memory = current_dataset_size < max_in_memory_dataset_size

    with assert_arrow_memory_increases() if expected_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = load_dataset(dataset_loading_script_dir, data_dir=data_dir)
    assert (dataset["train"].dataset_size < max_in_memory_dataset_size) is expected_in_memory


@pytest.mark.parametrize("max_in_memory_dataset_size", ["default", None, 0, 100, 1000])
def test_load_from_disk_with_default_in_memory(
    max_in_memory_dataset_size, dataset_loading_script_dir, data_dir, tmp_path, monkeypatch
):
    current_dataset_size = 512  # arrow file size = 512, in-memory dataset size = 148
    if max_in_memory_dataset_size == "default":
        # default = 250 * 2 ** 20
        max_in_memory_dataset_size = datasets.config.MAX_IN_MEMORY_DATASET_SIZE_IN_BYTES
    else:
        monkeypatch.setattr(datasets.config, "MAX_IN_MEMORY_DATASET_SIZE_IN_BYTES", max_in_memory_dataset_size)
    if max_in_memory_dataset_size is None:
        expected_in_memory = False
    else:
        expected_in_memory = current_dataset_size < max_in_memory_dataset_size

    dset = load_dataset(dataset_loading_script_dir, data_dir=data_dir, keep_in_memory=True)
    dataset_path = os.path.join(tmp_path, "saved_dataset")
    dset.save_to_disk(dataset_path)

    with assert_arrow_memory_increases() if expected_in_memory else assert_arrow_memory_doesnt_increase():
        _ = load_from_disk(dataset_path)
