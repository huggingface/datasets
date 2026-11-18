import numpy as np
import pytest

from datasets import Array2D, Array3D, Array4D, Array5D, Dataset, Features
from datasets.features.features import PandasArrayExtensionArray


@pytest.mark.parametrize(
    "feature",
    [
        Array2D((2, 3), "int64"),
        Array3D((2, 2, 3), "float32"),
        Array4D((1, 2, 2, 3), "int32"),
        Array5D((1, 1, 2, 2, 3), "float64"),
    ],
)
@pytest.mark.parametrize("index", [1, np.int8(1), np.int64(1), np.uint64(1)])
def test_arrayxd_pandas_scalar_index_returns_one_array(feature, index):
    values = np.arange(3 * np.prod(feature.shape), dtype=feature.dtype).reshape(3, *feature.shape)
    dataset = Dataset.from_dict({"embedding": values}, features=Features({"embedding": feature}))
    series = dataset.to_pandas()["embedding"]

    for row in (series.array[index], series.iloc[index], series.iat[index]):
        assert isinstance(row, np.ndarray)
        assert row.shape == feature.shape
        assert row.dtype == np.dtype(feature.dtype)
        np.testing.assert_array_equal(row, values[1])
    np.testing.assert_array_equal(series.array._data, values)


@pytest.mark.parametrize("index", [np.int32(0), np.uint64(1), np.int64(-1), -1])
def test_dynamic_array_scalar_indices_preserve_row_shapes(index):
    values = [
        np.empty((0, 2), dtype=np.float32),
        np.array([[1, 2]], dtype=np.float32),
        np.ones((3, 2), dtype=np.float32),
    ]
    dataset = Dataset.from_dict({"embedding": values}, features=Features({"embedding": Array2D((None, 2), "float32")}))
    series = dataset.to_pandas()["embedding"]

    actual = series.iloc[index]

    assert isinstance(actual, np.ndarray)
    np.testing.assert_array_equal(actual, values[int(index)])
    assert actual.shape == values[int(index)].shape


def test_numpy_selected_pandas_embedding_is_a_torch_input():
    torch = pytest.importorskip("torch")
    values = np.arange(24, dtype=np.float32).reshape(3, 2, 4)
    dataset = Dataset.from_dict({"embedding": values}, features=Features({"embedding": Array2D((2, 4), "float32")}))
    frame = dataset.to_pandas()
    index = np.argmax([0.1, 0.9, 0.2])

    tensor = torch.from_numpy(frame["embedding"].iloc[index].copy())
    output = tensor @ torch.tensor([1.0, -1.0, 2.0, 0.5])

    torch.testing.assert_close(output, torch.tensor([24.5, 34.5]))


@pytest.mark.parametrize("index", [slice(0, 2), np.array([0, 2]), np.array([True, False, True])])
def test_nonscalar_selection_still_returns_an_extension_array(index):
    values = np.arange(18).reshape(3, 2, 3)
    extension_array = (
        Dataset.from_dict({"embedding": values}, features=Features({"embedding": Array2D((2, 3), "int64")}))
        .to_pandas()["embedding"]
        .array
    )

    selected = extension_array[index]

    assert isinstance(selected, PandasArrayExtensionArray)
    np.testing.assert_array_equal(selected._data, values[index])


@pytest.mark.parametrize("index", [np.int64(3), np.int64(-4)])
def test_numpy_scalar_out_of_bounds_still_raises(index):
    extension_array = PandasArrayExtensionArray(np.arange(18).reshape(3, 2, 3))
    with pytest.raises(IndexError):
        extension_array[index]
