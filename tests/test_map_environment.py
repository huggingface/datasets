import json
import os
import subprocess
import sys
from unittest.mock import patch

import pytest

from datasets import Dataset


TOKENIZERS_PARALLELISM = "TOKENIZERS_PARALLELISM"
UNRELATED_VARIABLE = "DATASETS_MAP_ENVIRONMENT_TEST"


def _map_tokenizers_parallelism(example):
    return {"value": example["value"] + 1, "parallelism": os.environ.get(TOKENIZERS_PARALLELISM)}


def _set_optional_environment_variable(environ, key, value):
    if value is None:
        environ.pop(key, None)
    else:
        environ[key] = value


def _inherited_environment():
    # env=None probes the native process environment rather than passing os.environ.
    output = subprocess.check_output(
        [
            sys.executable,
            "-c",
            "import json, os; print(json.dumps([os.environ.get('TOKENIZERS_PARALLELISM'), "
            "os.environ.get('DATASETS_MAP_ENVIRONMENT_TEST')]))",
        ],
        text=True,
        timeout=15,
    )
    return json.loads(output)


@pytest.fixture(params=[None, "true", "false"], ids=["unset", "enabled", "disabled"])
def tokenizers_environment(request):
    original_environ = os.environ
    original_parallelism = original_environ.get(TOKENIZERS_PARALLELISM)
    original_unrelated = original_environ.get(UNRELATED_VARIABLE)
    _set_optional_environment_variable(original_environ, TOKENIZERS_PARALLELISM, request.param)
    try:
        yield original_environ, request.param
    finally:
        # Also restore the original object when exercising the old implementation.
        os.environ = original_environ
        _set_optional_environment_variable(original_environ, TOKENIZERS_PARALLELISM, original_parallelism)
        _set_optional_environment_variable(original_environ, UNRELATED_VARIABLE, original_unrelated)


def test_map_multiprocessing_restores_parent_environment(tokenizers_environment):
    original_environ, parallelism = tokenizers_environment
    with Dataset.from_dict({"value": [0, 1, 2, 3]}) as dataset:
        with dataset.map(_map_tokenizers_parallelism, num_proc=2) as mapped:
            assert mapped["value"][:] == [1, 2, 3, 4]
            assert mapped["parallelism"][:] == ["false"] * 4
    inherited_parallelism, _ = _inherited_environment()
    assert (os.environ is original_environ, os.environ.get(TOKENIZERS_PARALLELISM), inherited_parallelism) == (
        True,
        parallelism,
        parallelism,
    )


def test_map_multiprocessing_cached_preserves_parent_environment(tokenizers_environment, tmp_path):
    original_environ, parallelism = tokenizers_environment
    cache_file_name = str(tmp_path / "mapped.arrow")
    with Dataset.from_dict({"value": [0, 1, 2, 3]}) as dataset:
        with dataset.map(_map_tokenizers_parallelism, num_proc=2, cache_file_name=cache_file_name) as mapped:
            assert mapped["parallelism"][:] == ["false"] * 4
            cache_files = mapped.cache_files
        # Isolate the cached call even when the cold call uses the old implementation.
        os.environ = original_environ
        _set_optional_environment_variable(original_environ, TOKENIZERS_PARALLELISM, parallelism)
        with patch("datasets.arrow_dataset.mp.Pool", side_effect=AssertionError("cached map must not spawn")):
            with dataset.map(_map_tokenizers_parallelism, num_proc=2, cache_file_name=cache_file_name) as cached:
                assert cached["value"][:] == [1, 2, 3, 4]
                assert cached.cache_files == cache_files
    inherited_parallelism, _ = _inherited_environment()
    assert (os.environ is original_environ, os.environ.get(TOKENIZERS_PARALLELISM), inherited_parallelism) == (
        True,
        parallelism,
        parallelism,
    )


def test_map_multiprocessing_pool_failure_restores_parent_environment(tokenizers_environment):
    original_environ, parallelism = tokenizers_environment
    error = RuntimeError("pool construction failed")

    def fail_pool(*args, **kwargs):
        assert os.environ[TOKENIZERS_PARALLELISM] == "false"
        os.environ[UNRELATED_VARIABLE] = "changed during construction"
        raise error

    with Dataset.from_dict({"value": [0, 1, 2, 3]}) as dataset:
        with patch("datasets.arrow_dataset.mp.Pool", side_effect=fail_pool):
            with pytest.raises(RuntimeError) as caught:
                dataset.map(_map_tokenizers_parallelism, num_proc=2)
    assert caught.value is error
    inherited_parallelism, inherited_unrelated = _inherited_environment()
    assert (os.environ is original_environ, os.environ.get(TOKENIZERS_PARALLELISM), inherited_parallelism) == (
        True,
        parallelism,
        parallelism,
    )
    assert os.environ[UNRELATED_VARIABLE] == inherited_unrelated == "changed during construction"
