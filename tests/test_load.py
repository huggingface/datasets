import importlib
import os
import tempfile
from hashlib import sha256
from unittest import TestCase

import datasets


class LoadTest(TestCase):
    def test_prepare_module(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dummy_module_name = "__dummy_module_name__"
            module_dir = os.path.join(tmpdir, dummy_module_name)
            os.makedirs(module_dir, exist_ok=True)
            module_path = os.path.join(module_dir, dummy_module_name + ".py")
            # prepare module from directory path
            dummy_code = "MY_DUMMY_VARIABLE = 'hello there'"
            with open(module_path, "w") as f:
                f.write(dummy_code)
            importable_module_path, module_hash = datasets.load.prepare_module(module_dir)
            dummy_module = importlib.import_module(importable_module_path)
            self.assertEqual(dummy_module.MY_DUMMY_VARIABLE, "hello there")
            self.assertEqual(module_hash, sha256(dummy_code.encode("utf-8")).hexdigest())
            # prepare module from file path
            dummy_code = "MY_DUMMY_VARIABLE = 'general kenobi'"
            with open(module_path, "w") as f:
                f.write(dummy_code)
            importable_module_path, module_hash = datasets.load.prepare_module(module_path)
            dummy_module = importlib.import_module(importable_module_path)
            self.assertEqual(dummy_module.MY_DUMMY_VARIABLE, "general kenobi")
            self.assertEqual(module_hash, sha256(dummy_code.encode("utf-8")).hexdigest())
