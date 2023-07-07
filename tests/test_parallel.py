import pytest

from datasets.parallel import ParallelBackendConfig, parallel_backend
from datasets.utils.py_utils import map_nested

from .utils import require_dill_gt_0_3_2, require_joblibspark, require_not_windows


def add_one(i):  # picklable for multiprocessing
    return i + 1


@require_dill_gt_0_3_2
@require_joblibspark
@require_not_windows
def test_parallel_backend_input():
    with parallel_backend("spark"):
        assert ParallelBackendConfig.backend_name == "spark"

    lst = [1, 2, 3]
    with pytest.raises(ValueError):
        with parallel_backend("unsupported backend"):
            map_nested(add_one, lst, num_proc=2)

    with pytest.raises(ValueError):
        with parallel_backend("unsupported backend"):
            map_nested(add_one, lst, num_proc=-1)


@require_dill_gt_0_3_2
@require_joblibspark
@require_not_windows
@pytest.mark.parametrize("num_proc", [2, -1])
def test_parallel_backend_map_nested(num_proc):
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

    with parallel_backend("spark"):
        assert map_nested(add_one, s1, num_proc=num_proc) == expected_map_nested_s1
        assert map_nested(add_one, s2, num_proc=num_proc) == expected_map_nested_s2
        assert map_nested(add_one, s3, num_proc=num_proc) == expected_map_nested_s3
        assert map_nested(add_one, s4, num_proc=num_proc) == expected_map_nested_s4
        assert map_nested(add_one, s5, num_proc=num_proc) == expected_map_nested_s5
