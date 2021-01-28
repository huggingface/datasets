import importlib
from pathlib import Path

import pytest

from datasets.load import prepare_module
from datasets.utils.file_utils import init_dynamic_modules_cache


@pytest.fixture
def dynamic_modules_path(tmp_path):
    dynamic_modules_path = init_dynamic_modules_cache(hf_modules_cache=tmp_path)
    return dynamic_modules_path


@pytest.mark.parametrize("subpath", [
    Path("datasets/dummy_dataset"),
    Path("datasets/dummy_dataset/dummy_dataset.py"),
])
def test_prepare_module(subpath, shared_datadir, dynamic_modules_path):
    path = str(shared_datadir / subpath)
    module_name, hash = prepare_module(path, dynamic_modules_path=dynamic_modules_path)
    module = importlib.import_module(module_name)
    assert module.DESCRIPTION == "This is a dummy dataset for tests."
