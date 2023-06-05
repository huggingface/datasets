import pytest
from datasets.parallel import parallel_backend
from datasets.utils.py_utils import map_nested


def test_parallel_backend_input():
    with parallel_backend("spark", steps=["downloading"]) as backend:
        assert backend.backend_name == "spark"

    with pytest.raises(ValueError):
        with parallel_backend("ray", steps=["downloading"]):
            pass


def test_parallel_backend_map_nested():
    def add_one(i):  # picklable for multiprocessing
        return i + 1

    s1 = {}
    s2 = []
    s3 = 1
    s4 = [1, 2]
    s5 = {"a": 1, "b": 2}
    s6 = {"a": [1, 2], "b": [3, 4]}
    s7 = {"a": {"1": 1}, "b": 2}
    s8 = {"a": 1, "b": 2, "c": 3, "d": 4}
    expected_map_nested_s1 = {}
    expected_map_nested_s2 = []
    expected_map_nested_s3 = 2
    expected_map_nested_s4 = [2, 3]
    expected_map_nested_s5 = {"a": 2, "b": 3}
    expected_map_nested_s6 = {"a": [2, 3], "b": [4, 5]}
    expected_map_nested_s7 = {"a": {"1": 2}, "b": 3}
    expected_map_nested_s8 = {"a": 2, "b": 3, "c": 4, "d": 5}

    with parallel_backend("spark", steps=["downloading"]) as backend:
        assert map_nested(add_one, s1, parallel_backend=backend) == expected_map_nested_s1
        assert map_nested(add_one, s2, parallel_backend=backend) == expected_map_nested_s2
        assert map_nested(add_one, s3, parallel_backend=backend) == expected_map_nested_s3
        assert map_nested(add_one, s4, parallel_backend=backend) == expected_map_nested_s4
        assert map_nested(add_one, s5, parallel_backend=backend) == expected_map_nested_s5
        assert map_nested(add_one, s6, parallel_backend=backend) == expected_map_nested_s6
        assert map_nested(add_one, s7, parallel_backend=backend) == expected_map_nested_s7
        assert map_nested(add_one, s8, parallel_backend=backend) == expected_map_nested_s8
