import pytest

import numpy as np
import pandas as pd
import pyarrow as pa
from datasets.features.base_extension import BasePyarrowExtensionType, ExtensionArray
from datasets.table import InMemoryTable


class CustomBinaryType(BasePyarrowExtensionType):
    pa_storage_type = pa.binary()


class CustomBinaryTypeCastableFromInt(BasePyarrowExtensionType):
    pa_storage_type = pa.binary()

    def cast_storage(self, array: pa.Array) -> pa.Array:
        if pa.types.is_integer(array.type):
            return pa.array([f"{i}".encode() for i in array.to_pylist()], pa.binary())
        else:
            return array.cast(pa.storage_type)


class CustomComplexType(BasePyarrowExtensionType):
    pa_storage_type = pa.struct({"a": pa.list_(pa.struct({"b": pa.list_(pa.int64())}))})


def test_extension_type_wrap_array():
    arr = CustomBinaryType().wrap_array(pa.array([b"foo"]))
    assert isinstance(arr, ExtensionArray)
    assert isinstance(arr.storage, pa.BinaryArray)
    assert len(arr) == 1


def test_extension_type_from_storage():
    arr = pa.ExtensionArray.from_storage(CustomBinaryType(), pa.array([b"foo"]))
    assert isinstance(arr, ExtensionArray)
    assert isinstance(arr.storage, pa.BinaryArray)
    assert len(arr) == 1


def test_extension_array_getitem():
    arr = CustomBinaryType().wrap_array(pa.array([b"foo"]))
    assert arr[0] == arr.storage[0]


def test_extension_array_to_python():
    arr = CustomBinaryType().wrap_array(pa.array([b"foo"]))
    assert arr.to_pylist() == [b"foo"]


def test_extension_array_to_numpy():
    arr = CustomBinaryType().wrap_array(pa.array([b"foo"]))
    assert arr.to_numpy(zero_copy_only=False) == np.array([b"foo"])


def test_extension_array_to_pandas():
    arr = CustomBinaryType().wrap_array(pa.array([b"foo"]))
    assert isinstance(arr.to_pandas(), pd.Series)
    assert arr.to_pandas().to_numpy() == np.array([b"foo"])


def test_extension_array_concatenate():
    arr1 = CustomBinaryType().wrap_array(pa.array([b"foo"]))
    arr2 = CustomBinaryType().wrap_array(pa.array([b"bar"]))
    concatenated_array = pa.concat_arrays([arr1, arr2])
    assert concatenated_array.to_pylist() == [b"foo", b"bar"]


def test_extension_type_wrap_array_from_castable_type():
    arr = CustomBinaryTypeCastableFromInt().wrap_array(pa.array([0]))
    assert isinstance(arr, ExtensionArray)
    assert isinstance(arr.storage, pa.BinaryArray)
    assert len(arr) == 1


def test_extension_type_from_storage_from_castable_type():
    with pytest.raises(TypeError):
        pa.ExtensionArray.from_storage(CustomBinaryTypeCastableFromInt(), pa.array([0]))


def test_custom_complex_type():
    data = [
        {"a": [{"b": [0]}]}
    ]
    arr = CustomComplexType().wrap_array(pa.array(data))
    assert isinstance(arr, ExtensionArray)
    assert isinstance(arr.storage, pa.StructArray)
    assert arr.to_pylist() == data
