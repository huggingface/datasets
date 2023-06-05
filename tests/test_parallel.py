import pytest
from unittest.mock import patch

from datasets.parallel import parallel_backend, ParallelBackendConfig
from datasets.utils.py_utils import map_nested


def add_one(i):  # picklable for multiprocessing
    return i + 1


def test_parallel_backend_input():
    with parallel_backend("spark", steps=["downloading"]):
        assert ParallelBackendConfig.backend_name == "spark"

    with pytest.raises(NotImplementedError):
        with parallel_backend("spark", steps=["downloading", "prepare"]):
            pass

    lst = [1, 2, 3]
    with pytest.raises(ValueError):
        with parallel_backend("unsupported backend", steps=["downloading"]):
            map_nested(add_one, lst, num_proc=2)


def test_parallel_backend_map_nested():
    s1 = [1, 2]
    s2 = {"a": 1, "b": 2}
    s3 = {"a": [1, 2], "b": [3, 4]}
    s4 = {"a": {"1": 1}, "b": 2}
    s5 = {"a": 1, "b": 2, "c": 3, "d": 4}
    expected_map_nested_s1 = [2, 3]
    expected_map_nested_s2 = {"a": 2, "b": 3}
    expected_map_nested_s3 = {"a": [2, 3], "b": [4, 5]}
    expected_map_nested_s4 = {"a": {"1": 2}, "b": 3}
    expected_map_nested_s5 = {"a": 2, "b": 3, "c": 4, "d": 5}

    with parallel_backend("spark", steps=["downloading"]):
        assert map_nested(add_one, s1) == expected_map_nested_s1
        assert map_nested(add_one, s2) == expected_map_nested_s2
        assert map_nested(add_one, s3) == expected_map_nested_s3
        assert map_nested(add_one, s4) == expected_map_nested_s4
        assert map_nested(add_one, s5) == expected_map_nested_s5
