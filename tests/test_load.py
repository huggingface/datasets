import importlib
import os
import tempfile
from hashlib import sha256
from unittest import TestCase

import datasets

from .utils import offline


class LoadTest(TestCase):
    def _dummy_module_dir(self, modules_dir, dummy_module_name, dummy_code):
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
            importable_module_path, module_hash = datasets.load.prepare_module(module_dir)
            dummy_module = importlib.import_module(importable_module_path)
            self.assertEqual(dummy_module.MY_DUMMY_VARIABLE, "hello there")
            self.assertEqual(module_hash, sha256(dummy_code.encode("utf-8")).hexdigest())
            # prepare module from file path
            dummy_code = "MY_DUMMY_VARIABLE = 'general kenobi'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name1__", dummy_code)
            module_path = os.path.join(module_dir, "__dummy_module_name1__.py")
            importable_module_path, module_hash = datasets.load.prepare_module(module_path)
            dummy_module = importlib.import_module(importable_module_path)
            self.assertEqual(dummy_module.MY_DUMMY_VARIABLE, "general kenobi")
            self.assertEqual(module_hash, sha256(dummy_code.encode("utf-8")).hexdigest())

    def test_offline_prepare_module(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_code = "MY_DUMMY_VARIABLE = 'hello there'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name2__", dummy_code)
            importable_module_path1, _ = datasets.load.prepare_module(module_dir)
            dummy_code = "MY_DUMMY_VARIABLE = 'general kenobi'"
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_module_name2__", dummy_code)
            importable_module_path2, _ = datasets.load.prepare_module(module_dir)
        with offline():
            # allow provide the module name without an explicit path to remote or local actual file
            importable_module_path3, _ = datasets.load.prepare_module("__dummy_module_name2__")
            # it loads the most recent version of the module
            self.assertEqual(importable_module_path2, importable_module_path3)
            self.assertNotEqual(importable_module_path1, importable_module_path3)
            assert "offline, reusing latest version of the module" in caplog.text  # TODO(QL): add + test logging

    def test_load_dataset(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_code = """
import os

from datasets import DatasetInfo, Features, GeneratorBasedBuilder, Split, SplitGenerator, Value


class __DummyDataset1__(GeneratorBasedBuilder):

    def _info(self) -> DatasetInfo:
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        return [
            SplitGenerator(Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_manager.manual_dir, "train.txt")}),
            SplitGenerator(Split.TEST, gen_kwargs={"filepath": os.path.join(dl_manager.manual_dir, "train.txt")}),
        ]

    def _generate_examples(self, filepath, **kwargs):
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                yield i, {"text": line.strip()}
            """
            with open(os.path.join(tmp_dir, "train.txt"), "w") as f:
                f.write("foo\n" * 10)
            with open(os.path.join(tmp_dir, "test.txt"), "w") as f:
                f.write("bar\n" * 10)
            module_dir = self._dummy_module_dir(tmp_dir, "__dummy_dataset1__", dummy_code)
            self.assertTrue(len(datasets.load_dataset(module_dir, data_dir=tmp_dir)), 2)
            with offline():
                self.assertTrue(len(datasets.load_dataset("__dummy_dataset1__", data_dir=tmp_dir)), 2)
