import importlib.util

import pytest

from datasets.parallel import ParallelBackendConfig, parallel_backend
from datasets.utils.py_utils import map_nested


pytest.importorskip("joblib")


@pytest.mark.parametrize("outer", ["threading", "sequential"])
@pytest.mark.parametrize("inner", ["threading", "sequential"])
@pytest.mark.parametrize("raises", [False, True])
def test_nested_backend_restores_the_outer_mapping_backend(outer, inner, raises):
    offset = 10

    def transform(value):
        return value + offset

    examples = {"train": [1, 2], "test": [3, 4]}
    expected = {"train": [11, 12], "test": [13, 14]}
    original = ParallelBackendConfig.backend_name
    with parallel_backend(outer):
        assert map_nested(transform, examples, num_proc=2) == expected
        try:
            with parallel_backend(inner):
                assert map_nested(transform, examples, num_proc=2) == expected
                if raises:
                    raise RuntimeError("inner operation failed")
        except RuntimeError as error:
            assert raises and str(error) == "inner operation failed"

        # This closure cannot be pickled by the default multiprocessing backend.
        # The selected outer joblib backend must remain usable after the inner one exits.
        assert map_nested(transform, examples, num_proc=2) == expected
        assert ParallelBackendConfig.backend_name == outer
    assert ParallelBackendConfig.backend_name == original


@pytest.mark.parametrize("backend", ["threading", "sequential"])
@pytest.mark.parametrize("raises", [False, True])
def test_top_level_backend_restores_the_original_default(backend, raises):
    original = ParallelBackendConfig.backend_name
    try:
        with parallel_backend(backend):
            assert map_nested(lambda value: value * 2, [1, 2, 3], num_proc=2) == [
                2,
                4,
                6,
            ]
            if raises:
                raise RuntimeError("mapping failed")
    except RuntimeError as error:
        assert raises and str(error) == "mapping failed"
    assert ParallelBackendConfig.backend_name == original


def test_invalid_inner_joblib_backend_does_not_discard_the_outer_backend():
    with parallel_backend("threading"):
        with pytest.raises(ValueError, match="Invalid backend"):
            with parallel_backend("not-a-real-joblib-backend"):
                map_nested(lambda value: value + 1, [1, 2], num_proc=2)

        assert map_nested(lambda value: value + 1, [1, 2], num_proc=2) == [2, 3]
        assert ParallelBackendConfig.backend_name == "threading"


@pytest.mark.skipif(
    importlib.util.find_spec("joblibspark") is not None,
    reason="Requires the optional Spark package to be absent",
)
def test_failed_optional_backend_import_restores_the_outer_backend():
    with parallel_backend("threading"):
        with pytest.raises(ModuleNotFoundError, match="joblibspark"):
            with parallel_backend("spark"):
                pytest.fail("The backend cannot initialize without its optional package")

        assert map_nested(lambda value: value + 1, [1, 2], num_proc=2) == [2, 3]
        assert ParallelBackendConfig.backend_name == "threading"
