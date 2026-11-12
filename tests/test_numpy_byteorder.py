import numpy as np
import pyarrow as pa
import pytest

from datasets import Array2D, Array3D, Array4D, Array5D, Dataset, Features, Value, load_from_disk
from datasets.features.features import numpy_to_pyarrow_listarray


@pytest.mark.parametrize("dtype", ["int16", "uint32", "int64", "uint64", "float32", "float64"])
@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("declare_type", [False, True])
def test_numpy_byte_order_in_scalar_columns(dtype, native, declare_type):
    order = "=" if native else "S"
    storage_dtype = np.dtype(dtype).newbyteorder(order)
    values = [1, 256, 65_000] if dtype != "int16" else [-32_000, 1, 25_600]
    if dtype == "uint64" and not declare_type:
        values = [0, 2**63 + 1, 2**64 - 1]
    elif dtype.startswith("float"):
        values = [-2.5, 0.125, 1024.5]
    data = np.array(values, dtype=storage_dtype)
    before = data.tobytes()

    features = Features({"x": Value(dtype)}) if declare_type else None
    dataset = Dataset.from_dict({"x": data}, features=features)

    assert dataset["x"] == values
    assert dataset.features["x"] == Value(dtype)
    assert data.tobytes() == before
    assert data.dtype == storage_dtype


@pytest.mark.parametrize("feature_type,ndim", [(Array2D, 2), (Array3D, 3), (Array4D, 4), (Array5D, 5)])
@pytest.mark.parametrize("native", [False, True])
def test_numpy_byte_order_in_array_features(feature_type, ndim, native):
    shape = (2,) * ndim
    dtype = np.dtype("float32").newbyteorder("=" if native else "S")
    data = (np.arange(3 * 2**ndim).reshape(3, *shape) / 4).astype(dtype)
    features = Features({"x": feature_type(shape=shape, dtype="float32")})
    expected = data.tolist()
    before = data.tobytes()

    dataset = Dataset.from_dict({"x": data}, features=features)

    assert dataset.to_dict() == {"x": expected}
    assert dataset.features == features
    assert data.tobytes() == before
    assert data.dtype == dtype


@pytest.mark.parametrize("layout", ["reversed", "strided", "fortran", "readonly"])
def test_non_native_numpy_layouts_keep_values_and_ownership(layout):
    data = np.arange(48).reshape(2, 4, 6).astype(np.dtype("float64").newbyteorder("S"))
    if layout == "reversed":
        data = data[..., ::-1]
    elif layout == "strided":
        data = data[..., ::2]
    elif layout == "fortran":
        data = np.asfortranarray(data)
    else:
        data.setflags(write=False)
    before = data.tobytes()
    expected = data.tolist()
    writable = data.flags.writeable

    result = numpy_to_pyarrow_listarray(data, type=pa.float64())

    assert result.to_pylist() == expected
    assert data.tobytes() == before
    assert not data.dtype.isnative
    assert data.flags.writeable == writable
    if writable:
        data[...] = -1
        assert result.to_pylist() == expected


def test_non_native_ragged_numpy_rows():
    dtype = np.dtype("int32").newbyteorder("S")
    data = [np.array([[1, 2]], dtype=dtype), None, np.array([[3, 4], [5, 6]], dtype=dtype)]
    features = Features({"x": Array2D(shape=(None, 2), dtype="int32")})

    dataset = Dataset.from_dict({"x": data}, features=features)

    assert dataset.data.column("x").chunk(0).storage.to_pylist() == [[[1, 2]], None, [[3, 4], [5, 6]]]
    assert all(row is None or row.dtype == dtype for row in data)


@pytest.mark.parametrize("empty_shape", [(0,), (0, 2), (2, 0, 3)])
def test_non_native_empty_arrays_keep_nested_shape(empty_shape):
    data = np.empty(empty_shape, dtype=np.dtype("float32").newbyteorder("S"))
    result = numpy_to_pyarrow_listarray(data)
    assert result.to_pylist() == data.tolist()
    value_type = result.type
    while pa.types.is_list(value_type):
        value_type = value_type.value_type
    assert value_type == pa.float32()


def test_non_native_npy_training_features_survive_disk_roundtrip(tmp_path):
    dtype = np.dtype("float32").newbyteorder("S")
    values = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=dtype)
    path = tmp_path / "features.npy"
    np.save(path, values)
    original_file = path.read_bytes()
    mapped = np.load(path, mmap_mode="r", allow_pickle=False)

    dataset = Dataset.from_dict({"features": mapped})
    dataset.save_to_disk(tmp_path / "dataset")
    restored = load_from_disk(tmp_path / "dataset").with_format("numpy")

    actual = restored[:]["features"]
    np.testing.assert_array_equal(actual, [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    np.testing.assert_array_equal(actual @ np.array([0.5, -1.0]), [-1.5, -2.5, -3.5])
    assert path.read_bytes() == original_file
    assert mapped.dtype == dtype
    assert not mapped.flags.writeable


def test_numpy_python_list_conversion_is_unchanged():
    assert numpy_to_pyarrow_listarray([[1, 2], [3, 4]]).to_pylist() == [[1, 2], [3, 4]]
