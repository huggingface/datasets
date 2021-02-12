import importlib
import os
import shutil
import tempfile
import time
from hashlib import sha256
from unittest import TestCase

import pyarrow as pa
import pytest
import requests

import datasets
from datasets import load_dataset

from .utils import offline


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
            # prepare module from file path
            dummy_code = "MY_DUMMY_VARIABLE = 'general kenobi'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name1__", dummy_code)
            module_path = os.path.join(module_dir, "__dummy_module_name1__.py")
            importable_module_path, module_hash = datasets.load.prepare_module(
                module_path, dynamic_modules_path=self.dynamic_modules_path
            )
            dummy_module = importlib.import_module(importable_module_path)
            self.assertEqual(dummy_module.MY_DUMMY_VARIABLE, "general kenobi")
            self.assertEqual(module_hash, sha256(dummy_code.encode("utf-8")).hexdigest())
            # missing module
            with offline():
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
        with offline():
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
        with offline():
            with self.assertRaises(ConnectionError) as context:
                datasets.load_dataset("_dummy")
            self.assertIn(
                "https://raw.githubusercontent.com/huggingface/datasets/master/datasets/_dummy/_dummy.py",
                str(context.exception),
            )

    def test_load_dataset_users(self):
        with self.assertRaises(FileNotFoundError) as context:
            datasets.load_dataset("dummy_user/_dummy")
        self.assertIn(
            "https://s3.amazonaws.com/datasets.huggingface.co/datasets/datasets/dummy_user/_dummy/_dummy.py",
            str(context.exception),
        )
        with offline():
            with self.assertRaises(ConnectionError) as context:
                datasets.load_dataset("dummy_user/_dummy")
            self.assertIn(
                "https://s3.amazonaws.com/datasets.huggingface.co/datasets/datasets/dummy_user/_dummy/_dummy.py",
                str(context.exception),
            )


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_load_dataset_local(dataset_loading_script_dir, data_dir, keep_in_memory, caplog):
    previous_allocated_memory = pa.total_allocated_bytes()
    dataset = load_dataset(dataset_loading_script_dir, data_dir=data_dir, keep_in_memory=keep_in_memory)
    increased_allocated_memory = (pa.total_allocated_bytes() - previous_allocated_memory) > 0
    assert len(dataset) == 2
    assert increased_allocated_memory == keep_in_memory
    with offline():
        caplog.clear()
        # Load dataset from cache
        dataset = datasets.load_dataset(DATASET_LOADING_SCRIPT_NAME, data_dir=data_dir)
        assert len(dataset) == 2
        assert "Using the latest cached version of the module" in caplog.text
    with pytest.raises(FileNotFoundError) as exc_info:
        datasets.load_dataset("_dummy")
    assert "at " + os.path.join("_dummy", "_dummy.py") in str(exc_info.value)
