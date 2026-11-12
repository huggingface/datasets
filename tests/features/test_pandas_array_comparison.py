import numpy as np
import pytest

from datasets import Array2D, Array3D, Array4D, Array5D, Dataset, Features, Value
from datasets.features.features import PandasArrayExtensionArray


@pytest.mark.parametrize(
    "feature_class,shape",
    [(Array2D, (1, 2)), (Array3D, (1, 1, 2)), (Array4D, (1, 1, 1, 2)), (Array5D, (1, 1, 1, 1, 2))],
)
@pytest.mark.parametrize("dtype", ["int64", "float32", "bool"])
def test_arrayxd_pandas_comparison_returns_one_boolean_per_row(feature_class, shape, dtype):
    values = (np.arange(3 * np.prod(shape)).reshape(3, *shape) % 2).astype(dtype)
    other = values.copy()
    other[1].flat[0] = 1 - other[1].flat[0]
    features = Features({"tensor": feature_class(shape=shape, dtype=dtype)})
    left = Dataset.from_dict({"tensor": values}, features=features).to_pandas()["tensor"]
    right = Dataset.from_dict({"tensor": other}, features=features).to_pandas()["tensor"]

    np.testing.assert_array_equal(left.eq(right), [True, False, True])
    np.testing.assert_array_equal(left.ne(right), [False, True, False])
    assert left.array._data.shape == (3, *shape)
    np.testing.assert_array_equal(left.array._data, values)
    np.testing.assert_array_equal(right.array._data, other)


def test_dynamic_array_comparison_keeps_row_shapes_and_empty_arrays():
    features = Features({"tensor": Array2D(shape=(None, 2), dtype="int64")})
    left = Dataset.from_dict({"tensor": [[[1, 2]], [[3, 4], [5, 6]], []]}, features=features).to_pandas()
    right = Dataset.from_dict({"tensor": [[[1, 2]], [[3, 4]], []]}, features=features).to_pandas()

    np.testing.assert_array_equal(left["tensor"].eq(right["tensor"]), [True, False, True])
    np.testing.assert_array_equal(left["tensor"].ne(right["tensor"]), [False, True, False])


def test_null_and_nan_rows_do_not_hide_other_equal_rows():
    features = Features({"tensor": Array2D(shape=(1, 2), dtype="float32")})
    data = {"tensor": [[[1.0, 2.0]], None, [[float("nan"), 1.0]]]}
    left = Dataset.from_dict(data, features=features).to_pandas()["tensor"]
    right = Dataset.from_dict(data, features=features).to_pandas()["tensor"]

    np.testing.assert_array_equal(left.eq(right), [True, False, False])


@pytest.mark.parametrize("equal_rows", [[True, True, True], [False, False, False], [True, False, True]])
def test_series_comparison_preserves_each_independent_row_decision(equal_rows):
    left = PandasArrayExtensionArray(np.arange(6).reshape(3, 1, 2))
    values = left._data.copy()
    for index, equal in enumerate(equal_rows):
        if not equal:
            values[index] += 1
    right = PandasArrayExtensionArray(values)

    result = left == right

    assert isinstance(result, np.ndarray)
    assert result.shape == (3,)
    assert result.dtype == np.dtype(bool)
    np.testing.assert_array_equal(result, equal_rows)


@pytest.mark.parametrize("shape", [(0, 1, 2), (2, 0, 2)])
def test_empty_arrays_preserve_the_number_of_dataframe_rows(shape):
    left = PandasArrayExtensionArray(np.empty(shape))
    right = PandasArrayExtensionArray(np.empty(shape))

    result = left == right

    assert isinstance(result, np.ndarray)
    assert result.shape == (shape[0],)
    np.testing.assert_array_equal(result, np.ones(shape[0], dtype=bool))


@pytest.mark.parametrize("length", [0, 1])
def test_different_column_lengths_are_not_broadcast(length):
    left = PandasArrayExtensionArray(np.zeros((3, 1, 2)))
    right = PandasArrayExtensionArray(np.zeros((length, 1, 2)))

    with pytest.raises(ValueError, match="[Ll]ength"):
        left == right


def test_comparison_to_an_unsupported_type_keeps_the_existing_error():
    array = PandasArrayExtensionArray(np.zeros((3, 1, 2)))

    with pytest.raises(NotImplementedError, match="Invalid type to compare"):
        array == 0


def test_array_comparison_can_select_matching_dataset_rows():
    features = Features({"tensor": Array2D(shape=(1, 2), dtype="float32"), "row_id": Value("int64")})
    dataset = Dataset.from_dict(
        {"tensor": [[[1, 2]], [[3, 4]], [[5, 6]]], "row_id": [100, 101, 102]}, features=features
    )
    frame = dataset.to_pandas()
    reference = Dataset.from_dict(
        {"tensor": [[[1, 2]], [[9, 9]], [[5, 6]]]}, features=Features({"tensor": features["tensor"]})
    ).to_pandas()

    matching = frame["row_id"].loc[frame["tensor"].eq(reference["tensor"])]
    assert matching.tolist() == [100, 102]
    restored = dataset.select(matching.index.tolist())

    assert restored["row_id"][:] == [100, 102]
    assert restored["tensor"][:] == [[[1, 2]], [[5, 6]]]
