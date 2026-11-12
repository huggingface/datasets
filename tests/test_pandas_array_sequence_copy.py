import numpy as np
import pandas as pd
import pytest

from datasets import Array2D, Array3D, Dataset, Features
from datasets.features.features import PandasArrayExtensionArray, PandasArrayExtensionDtype


@pytest.mark.parametrize("shape,array_type", [((2, 3), Array2D), ((2, 2, 3), Array3D)])
@pytest.mark.parametrize("dtype", ["int32", "float64"])
@pytest.mark.parametrize("copy", [False, True])
def test_pandas_constructs_arrayxd_from_separate_ndarray_rows(shape, array_type, dtype, copy):
    values = np.arange(3 * np.prod(shape), dtype=dtype).reshape(3, *shape)
    rows = [row.copy() for row in values]
    extension_dtype = PandasArrayExtensionDtype(np.dtype(dtype))

    array = pd.array(rows, dtype=extension_dtype, copy=copy)

    assert isinstance(array, PandasArrayExtensionArray)
    assert array._data.shape == values.shape
    assert array._data.dtype == values.dtype
    np.testing.assert_array_equal(array._data, values)
    frame = pd.DataFrame({"embedding": array})
    dataset = Dataset.from_pandas(frame, features=Features({"embedding": array_type(shape, dtype)}))
    assert dataset.to_dict() == {"embedding": values.tolist()}
    for row, original in zip(rows, values):
        np.testing.assert_array_equal(row, original)


@pytest.mark.parametrize("copy", [False, True])
@pytest.mark.parametrize("change_dtype", [False, True])
def test_pandas_array_copy_contract_with_contiguous_input(copy, change_dtype):
    source = np.arange(18, dtype=np.int32).reshape(3, 2, 3)
    expected = source.copy()
    dtype = np.dtype("float64" if change_dtype else "int32")

    array = pd.array(source, dtype=PandasArrayExtensionDtype(dtype), copy=copy)

    np.testing.assert_array_equal(array._data, expected)
    assert array._data.dtype == dtype
    assert np.shares_memory(array._data, source) == (not copy and not change_dtype)
    array._data[0, 0, 0] = 99
    assert source[0, 0, 0] == (99 if not copy and not change_dtype else expected[0, 0, 0])


@pytest.mark.parametrize("copy", [False, True])
def test_pandas_array_from_strided_input_can_share_storage(copy):
    source = np.arange(36, dtype=np.float32).reshape(3, 2, 6)[:, :, ::2]

    array = pd.array(source, dtype=PandasArrayExtensionDtype(np.dtype("float32")), copy=copy)

    np.testing.assert_array_equal(array._data, source)
    assert np.shares_memory(array._data, source) == (not copy)


@pytest.mark.parametrize("rows", [[], [np.ones((2, 2))], [np.ones((1, 2)), np.ones((3, 2))]])
def test_nondense_sequence_construction_keeps_existing_behavior(rows):
    array = pd.array(rows, dtype=PandasArrayExtensionDtype(np.dtype("float64")))
    assert len(array) == len(rows)
    assert array._data.dtype == object
    for actual, expected in zip(array, rows):
        np.testing.assert_array_equal(actual, expected)
