import json
import os
import pickle
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest

from datasets import Dataset, Features, List, Tensor, Value, config, load_from_disk

from ..utils import require_jax, require_polars, require_tf, require_torch


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (2, None), (None, None), ()])
def test_tensor_features_round_trip(shape):
    feature = Tensor(shape, "int32")
    features = Features({"x": feature})
    assert Features.from_dict(json.loads(json.dumps(features.to_dict()))) == features
    assert Features.from_arrow_schema(features.arrow_schema.remove_metadata()) == features
    assert pickle.loads(pickle.dumps(feature)) == feature
    assert features.flatten() == features
    assert Features({"nested": {"x": feature}}).flatten() == Features({"nested.x": feature})


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
def test_tensor_arrow_storage(shape):
    feature = Tensor(shape)
    arrow_type = feature()
    if shape == (2, 3):
        assert arrow_type == pa.fixed_shape_tensor(pa.float32(), (2, 3))
    else:
        assert arrow_type.extension_name == "arrow.variable_shape_tensor"
        assert arrow_type.storage_type == pa.struct(
            [("data", pa.list_(pa.float32())), ("shape", pa.list_(pa.int32(), len(shape)))]
        )
        metadata = json.loads(arrow_type.__arrow_ext_serialize__())
        assert metadata == ({"uniform_shape": [None, 3]} if shape == (None, 3) else {})
        assert (
            pa.ipc.read_schema(pa.BufferReader(pa.schema([("x", arrow_type)]).serialize())).field("x").type
            == arrow_type
        )


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
@pytest.mark.parametrize("dtype", ["bool", "int8", "uint8", "int64", "uint64", "float16", "float32", "float64"])
def test_tensor_encode_decode(shape, dtype):
    feature = Tensor(shape, dtype)
    expected = np.asarray([[0, 1, 0], [1, 0, 1]], dtype=dtype)
    for value in [expected, expected.tolist(), tuple(map(tuple, expected.tolist()))]:
        decoded = feature.decode_example(feature.encode_example(value))
        assert isinstance(decoded, np.ndarray)
        assert decoded.dtype == expected.dtype
        np.testing.assert_array_equal(decoded, expected)


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
@pytest.mark.parametrize("representation", ["nested_lists", "row_arrays", "ndarray", "mixed_rows"])
@pytest.mark.parametrize(
    "dtype,values",
    [
        ("int32", [[1, 2, 3], [4, 5, 6]]),
        ("int64", [[0, 2**53 + 1, 2**63 - 1], [-(2**63), 1, 2]]),
        ("uint64", [[0, 2**63 + 1, 2**64 - 1], [1, 2, 3]]),
        ("bool", [[True, False, True], [False, True, False]]),
        ("float32", [[1, 2, 3], [4, 5, 6]]),
    ],
)
def test_tensor_encode_input_representations(shape, representation, dtype, values):
    expected = np.asarray(values, dtype=dtype)
    value = values
    if representation == "row_arrays":
        value = [np.asarray(row, dtype="uint64" if dtype == "uint64" else None) for row in values]
    elif representation == "ndarray":
        value = expected
    elif representation == "mixed_rows":
        value = [values[0], expected[1]]
    feature = Tensor(shape, dtype)
    encoded = feature.encode_example(value)
    decoded = feature.decode_example(encoded)
    assert decoded.dtype == expected.dtype
    assert decoded.tolist() == values
    dataset = Dataset.from_dict({"x": [value]}, features=Features({"x": feature}))
    assert dataset[0]["x"].dtype == expected.dtype
    assert dataset[0]["x"].tolist() == values


@pytest.mark.parametrize("dtype", ["string", "object", "complex64", "datetime64[ns]", "not_a_dtype"])
def test_tensor_invalid_dtype(dtype):
    with pytest.raises(ValueError, match="dtype"):
        Tensor((None,), dtype=dtype)


@pytest.mark.parametrize("shape", [(-1, 3), (1.5, 3), (True, 3), "bad", 2])
def test_tensor_invalid_shape(shape):
    with pytest.raises(ValueError, match="shape"):
        Tensor(shape)


@pytest.mark.parametrize(
    "shape,value",
    [
        ((2, 3), [[1, 2], [3, 4]]),
        ((None, 3), [1, 2, 3]),
        ((None, 3), [[[1, 2, 3]]]),
        ((None, 3), [[1, 2]]),
    ],
)
def test_tensor_rejects_wrong_shape(shape, value):
    with pytest.raises(ValueError, match="shape"):
        Tensor(shape).encode_example(value)


@pytest.mark.parametrize(
    "dtype,value",
    [
        ("int32", ["hello"]),
        ("int8", [128]),
        ("uint8", [-1]),
        ("int32", [1.5]),
        ("float32", [1 + 2j]),
        ("float32", [[1], [2, 3]]),
    ],
)
def test_tensor_rejects_invalid_values(dtype, value):
    with pytest.raises(ValueError, match="Tensor|dtype"):
        Tensor((None,), dtype=dtype).encode_example(value)


@pytest.mark.parametrize(
    "shape,values",
    [
        ((2, 3), [np.arange(6).reshape(2, 3), None, np.ones((2, 3))]),
        ((None, 3), [None, np.ones((2, 3)), np.ones((4, 3))]),
        ((2, None), [np.ones((2, 3)), np.ones((2, 4)), None]),
        ((None, None, 3), [np.ones((1, 2, 3)), np.ones((2, 1, 3)), None]),
        ((None, None, None), [np.empty((0, 3, 2)), np.empty((2, 0, 4)), None]),
        ((), [np.array(7), None]),
        ((0, 3), [np.empty((0, 3)), None]),
    ],
)
def test_tensor_dataset_and_batch(shape, values):
    feature = Tensor(shape, "float32")
    features = Features({"x": feature})
    encoded = features.encode_batch({"x": values})
    decoded = features.decode_batch(encoded)["x"]
    dataset = Dataset.from_dict({"x": values}, features=features)
    assert dataset.features == features
    assert dataset.flatten().features == features
    for actual_values in [decoded, dataset[:]["x"], dataset["x"][:]]:
        for actual, expected in zip(actual_values, values):
            if expected is None:
                assert actual is None
            else:
                assert actual.shape == expected.shape
                assert actual.dtype == np.float32
                np.testing.assert_array_equal(actual, expected)


def test_tensor_fixed_rank_validates_every_row():
    with pytest.raises(ValueError, match="shape"):
        Dataset.from_dict({"x": [np.ones((2, 3)), np.ones((2, 3, 1))]}, features=Features({"x": Tensor((None, 3))}))


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
def test_tensor_nulls_and_empty_dataset(shape):
    features = Features({"x": Tensor(shape)})
    assert Tensor(shape).encode_example(None) is None
    assert Tensor(shape).decode_example(None) is None
    for values in [[], [None, None]]:
        dataset = Dataset.from_dict({"x": values}, features=features)
        assert dataset[:]["x"] == values
        assert dataset.with_format("numpy")[:]["x"].tolist() == values


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
def test_tensor_disk_and_parquet_round_trip(shape, tmp_path):
    feature = Tensor(shape, "int64")
    values = [np.full((2, 3), 2**53 + 1, dtype=np.int64), None, np.ones((2, 3), dtype=np.int64)]
    if shape != (2, 3):
        values.append(np.ones((4, 3), dtype=np.int64))
    dataset = Dataset.from_dict({"x": values}, features=Features({"x": feature}))
    dataset.save_to_disk(str(tmp_path / "saved"))
    dataset.to_parquet(str(tmp_path / "tensor.parquet"))
    restored_datasets = [
        load_from_disk(str(tmp_path / "saved")),
        Dataset.from_parquet(str(tmp_path / "tensor.parquet"), cache_dir=str(tmp_path / "cache")),
    ]
    for restored in restored_datasets:
        assert restored.features == dataset.features
        for actual, expected in zip(restored["x"], values):
            if expected is None:
                assert actual is None
            else:
                assert actual.dtype == np.int64
                np.testing.assert_array_equal(actual, expected)


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
@pytest.mark.parametrize("nesting", ["struct", "list", "large_list", "fixed_size_list"])
@pytest.mark.parametrize("operation", ["array", "table", "disk", "hub_preparation"])
def test_tensor_embed_with_image_sibling(shape, nesting, operation, image_file, tmp_path):
    from PIL import Image as PILImage

    from datasets import Image, LargeList
    from datasets.table import embed_array_storage, embed_table_storage

    image_bytes = Path(image_file).read_bytes()
    image_path = tmp_path / "image.jpg"
    image_path.write_bytes(image_bytes)
    expected = np.arange(6, dtype=np.float32).reshape(2, 3)
    feature = {"img": Image(), "t": Tensor(shape)}
    value = {"img": str(image_path), "t": expected}
    empty = {"img": None, "t": None}
    if nesting == "struct":
        rows = [None, value, empty]
    else:
        feature = (
            LargeList(feature)
            if nesting == "large_list"
            else List(feature, length=3 if nesting == "fixed_size_list" else -1)
        )
        rows = [None, [value, None, empty]]
    features = Features({"x": feature})
    dataset = Dataset.from_dict({"x": rows}, features=features)
    table = dataset.data.table
    if operation == "array":
        embedded = embed_array_storage(table["x"].chunk(0), feature, local_files=True, remote_files=False)
        assert embedded.type == table["x"].type
        restored = Dataset(pa.Table.from_arrays([embedded], schema=features.arrow_schema))
    elif operation == "table":
        embedded = embed_table_storage(table, local_files=True, remote_files=False)
        assert embedded.schema == features.arrow_schema
        restored = Dataset(embedded)
    elif operation == "disk":
        dataset.save_to_disk(str(tmp_path / "saved"))
        restored = load_from_disk(str(tmp_path / "saved"))
    else:
        # Exercise the local embedding and Parquet preparation used by push_to_hub.
        embedded = dataset.with_format("arrow").map(
            embed_table_storage,
            batched=True,
            keep_in_memory=True,
            fn_kwargs={"local_files": True, "remote_files": False},
        )
        path = str(tmp_path / "shard.parquet")
        embedded.to_parquet(path)
        restored = Dataset.from_parquet(path, cache_dir=str(tmp_path / "cache"))
    image_path.unlink()
    assert restored.features == features
    assert restored.data.schema == features.arrow_schema
    assert restored[0]["x"] is None
    actual = restored[1]["x"]
    storage = restored.data.table["x"].to_pylist()[1]
    if nesting != "struct":
        assert actual[1] is None
        assert actual[2] == empty
        actual = actual[0]
        storage = storage[0]
    else:
        assert restored[2]["x"] == empty
    assert storage["img"]["bytes"] == image_bytes
    assert isinstance(actual["img"], PILImage.Image)
    with PILImage.open(image_file) as expected_image:
        np.testing.assert_array_equal(np.asarray(actual["img"]), np.asarray(expected_image))
    assert actual["t"].dtype == expected.dtype
    np.testing.assert_array_equal(actual["t"], expected)


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
def test_tensor_embed_storage_is_noop(shape):
    from datasets.table import embed_array_storage

    feature = Tensor(shape)
    dataset = Dataset.from_dict({"x": [None, np.ones((2, 3))]}, features=Features({"x": feature}))
    array = dataset.data.table["x"].chunk(0)
    assert feature.embed_storage(array) is array
    assert embed_array_storage(array, feature) is array


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
@pytest.mark.parametrize("ragged", [False, True])
def test_tensor_numpy_and_pandas(shape, ragged):
    if shape == (2, 3) and ragged:
        pytest.skip("A fixed shape cannot be ragged")
    values = [np.arange(6).reshape(2, 3), np.ones((4 if ragged else 2, 3))]
    dataset = Dataset.from_dict({"x": values}, features=Features({"x": Tensor(shape)}))
    formatted = dataset.with_format("numpy")
    np.testing.assert_array_equal(formatted[0]["x"], values[0])
    batch = formatted[:]["x"]
    assert batch.shape == ((2,) if ragged else (2, 2, 3))
    if ragged:
        assert batch.dtype == object
    for frame in [dataset.to_pandas(), dataset.with_format("pandas")[:]]:
        assert isinstance(frame, pd.DataFrame)
        for actual, expected in zip(frame["x"], values):
            assert isinstance(actual, np.ndarray)
            np.testing.assert_array_equal(actual, expected)


@require_torch
def test_tensor_torch_format():
    import torch

    _check_native_format("torch", torch.Tensor)


@require_tf
def test_tensor_tf_format():
    import tensorflow as tf

    _check_native_format("tensorflow", tf.Tensor)


@require_jax
def test_tensor_jax_format():
    import jax

    _check_native_format("jax", jax.Array)


def _check_native_format(format_name, tensor_type):
    for shape in [(2, 3), (None, 3), (None, None)]:
        values = [np.ones((2, 3)), np.ones((2, 3))]
        dataset = Dataset.from_dict({"x": values}, features=Features({"x": Tensor(shape)})).with_format(format_name)
        assert isinstance(dataset[0]["x"], tensor_type)
        assert tuple(dataset[:]["x"].shape) == (2, 2, 3)
        np.testing.assert_array_equal(np.asarray(dataset[0]["x"]), values[0])
        if shape != (2, 3):
            values[1] = np.ones((4, 3))
            dataset = Dataset.from_dict({"x": values}, features=Features({"x": Tensor(shape)})).with_format(
                format_name
            )
            for actual, expected in zip(dataset[:]["x"], values):
                np.testing.assert_array_equal(np.asarray(actual), expected)


@require_polars
def test_tensor_polars_format():
    import polars as pl

    for shape in [(2, 3), (None, 3), (None, None)]:
        values = [np.ones((2, 3)), None]
        dataset = Dataset.from_dict({"x": values}, features=Features({"x": Tensor(shape)}))
        for frame in [dataset.with_format("polars")[:], dataset.with_format("polars")[0]]:
            assert isinstance(frame, pl.DataFrame)
            np.testing.assert_array_equal(frame["x"][0], values[0])


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
def test_tensor_nested_lists(shape):
    features = Features({"x": List(Tensor(shape))})
    values = [[np.ones((2, 3)), None, np.zeros((2, 3))]]
    dataset = Dataset.from_dict({"x": values}, features=features)
    assert dataset[0]["x"][1] is None
    np.testing.assert_array_equal(dataset[0]["x"][0], values[0][0])


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None,), (None, None)])
def test_tensor_map_and_cast(shape):
    value = np.arange(3 if shape == (None,) else 6, dtype=np.int32)
    if shape != (None,):
        value = value.reshape(2, 3)
    dataset = Dataset.from_dict({"x": [value, None]}, features=Features({"x": Tensor(shape, "int32")}))
    mapped = dataset.map(lambda row: {"x": row["x"] + 1} if row["x"] is not None else row)
    assert mapped.features == dataset.features
    np.testing.assert_array_equal(mapped[0]["x"], value + 1)
    casted = dataset.cast(Features({"x": Tensor(shape, "float64")}))
    assert casted[0]["x"].dtype == np.float64
    np.testing.assert_array_equal(casted[0]["x"], value)


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
def test_tensor_pandas_nulls_and_precision(shape):
    value = np.full((2, 3), 2**53 + 1, dtype=np.int64)
    dataset = Dataset.from_dict({"x": [None, value]}, features=Features({"x": Tensor(shape, "int64")}))
    for frame in [dataset.to_pandas(), dataset.with_format("pandas")[:]]:
        assert frame["x"].iloc[0] is None
        assert frame["x"].iloc[1].dtype == np.int64
        np.testing.assert_array_equal(frame["x"].iloc[1], value)
    for actual in dataset.with_format("numpy")[:]["x"]:
        if actual is not None:
            np.testing.assert_array_equal(actual, value)


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
def test_tensor_parquet_writer_and_nested_round_trip(shape, tmp_path):
    from datasets.arrow_writer import ParquetWriter

    feature = Tensor(shape, "int32")
    features = Features({"nested": {"x": List(feature)}})
    values = {"nested": [{"x": [np.ones((2, 3), dtype=np.int32), None]}, None]}
    dataset = Dataset.from_dict(values, features=features)
    path = str(tmp_path / "nested.parquet")
    with ParquetWriter(features=features, path=path) as writer:
        writer.write_table(dataset.data.table)
    restored = Dataset.from_parquet(path, cache_dir=str(tmp_path / "cache"))
    assert restored.features == features
    assert restored[1]["nested"] is None
    assert restored[0]["nested"]["x"][1] is None
    np.testing.assert_array_equal(restored[0]["nested"]["x"][0], values["nested"][0]["x"][0])


@pytest.mark.parametrize("shape", [(), (0, 3), (None, 3), (None, None)])
def test_tensor_empty_and_scalar_persistence(shape, tmp_path):
    value = np.array(7, dtype=np.int32) if shape == () else np.empty((0, 3), dtype=np.int32)
    dataset = Dataset.from_dict({"x": [None, value]}, features=Features({"x": Tensor(shape, "int32")}))
    path = str(tmp_path / "edge.parquet")
    dataset.to_parquet(path)
    restored = Dataset.from_parquet(path, cache_dir=str(tmp_path / "cache"))
    assert restored.features == dataset.features
    assert restored[0]["x"] is None
    assert restored[1]["x"].shape == value.shape
    assert restored[1]["x"].dtype == value.dtype


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
def test_tensor_deeply_nested(shape):
    value = np.ones((2, 3), dtype=np.float32)
    features = Features({"x": List(List(Tensor(shape)))})
    dataset = Dataset.from_dict({"x": [[[value, None]]]}, features=features)
    assert dataset[0]["x"][0][1] is None
    np.testing.assert_array_equal(dataset[0]["x"][0][0], value)


def test_tensor_cast_preserves_source_shape():
    value = np.arange(6, dtype=np.int32).reshape(2, 3)
    dataset = Dataset.from_dict({"x": [value, None]}, features=Features({"x": Tensor((2, 3), "int32")}))
    for shape in [(None, 3), (None, None), (2, 3)]:
        casted = dataset.cast_column("x", Tensor(shape, "float64"))
        assert casted[0]["x"].shape == (2, 3)
        np.testing.assert_array_equal(casted[0]["x"], value)
        assert casted[1]["x"] is None


@pytest.mark.parametrize(
    "value",
    [
        {"data": [1.5], "shape": [1]},
        {"data": [1], "shape": [-1]},
        {"data": [1], "shape": None},
        {"data": [1], "shape": [True]},
    ],
)
def test_tensor_validates_encoded_storage(value):
    with pytest.raises(ValueError):
        Tensor((None,), dtype="int32").encode_example(value)


@pytest.mark.parametrize(
    "metadata", [b"{}", b'{"uniform_shape":[null,3]}', b'{"permutation":[1,0],"dim_names":["x","y"]}']
)
def test_tensor_registration_preserves_canonical_schema_reading(metadata):
    from datasets.features.tensor import normalize_tensor_type

    storage = pa.struct([("data", pa.list_(pa.float32())), ("shape", pa.list_(pa.int32(), 2))])
    schema = pa.schema(
        [
            pa.field(
                "x",
                storage,
                metadata={
                    b"ARROW:extension:name": b"arrow.variable_shape_tensor",
                    b"ARROW:extension:metadata": metadata,
                },
            )
        ]
    )
    restored = pa.ipc.read_schema(pa.BufferReader(schema.serialize()))
    assert restored.field("x").type.storage_type == storage
    assert json.loads(normalize_tensor_type(restored.field("x").type).__arrow_ext_serialize__()) == json.loads(
        metadata
    )


@pytest.mark.parametrize(
    "value",
    [
        {"data": [1.0], "shape": [1]},
        {"data": [1.0], "shape": [-1]},
        {"data": [1.0], "shape": None},
        {"data": None, "shape": [1, 3]},
        {"data": [1.0], "shape": [1, 3]},
    ],
)
def test_tensor_cast_validates_storage(value):
    from datasets.table import cast_array_to_feature

    raw = pa.array([value], type=pa.struct([("data", pa.list_(pa.float32())), ("shape", pa.list_(pa.int32()))]))
    with pytest.raises(ValueError):
        cast_array_to_feature(raw, Tensor((None, 3)))


@pytest.mark.parametrize("shape", [()])
def test_tensor_pandas_scalar_precision(shape):
    value = np.array(2**53 + 1, dtype=np.int64)
    for values in [[None, value], [value, value]]:
        dataset = Dataset.from_dict({"x": values}, features=Features({"x": Tensor(shape, "int64")}))
        for frame in [dataset.to_pandas(), dataset.with_format("pandas")[:]]:
            for actual, expected in zip(frame["x"], values):
                if expected is None:
                    assert actual is None
                else:
                    assert isinstance(actual, np.ndarray)
                    assert actual.shape == ()
                    assert actual.dtype == np.int64
                    assert actual.item() == 2**53 + 1


def test_tensor_parquet_uint64(tmp_path):
    value = np.array([0, 2**63 + 1], dtype=np.uint64)
    features = Features({"x": Tensor((2,), "uint64"), "nested": List(Tensor((2,), "uint64"))})
    dataset = Dataset.from_dict({"x": [value, None], "nested": [[value, None], None]}, features=features)
    path = str(tmp_path / "uint64.parquet")
    dataset.to_parquet(path)
    restored = Dataset.from_parquet(path, cache_dir=str(tmp_path / "cache"))
    assert restored[0]["x"].dtype == np.uint64
    np.testing.assert_array_equal(restored[0]["x"], value)
    np.testing.assert_array_equal(restored[0]["nested"][0], value)


def test_tensor_nested_map_with_dynamic_shapes():
    values = [np.ones((2, 3), dtype=np.float32), np.ones((4, 2), dtype=np.float32)]
    dataset = Dataset.from_dict({"x": [values]}, features=Features({"x": List(Tensor((None, None)))}))
    mapped = dataset.map(lambda row: {"x": row["x"]})
    assert mapped.features == dataset.features
    for actual, expected in zip(mapped[0]["x"], values):
        np.testing.assert_array_equal(actual, expected)


def test_tensor_requires_ndim():
    with pytest.raises(ValueError, match="shape.*None.*ndim"):
        Tensor(shape=None)


@pytest.mark.parametrize("ndim", [0, 1, 2, 3])
def test_tensor_explicit_ndim(ndim):
    feature = Tensor(ndim=ndim)
    assert feature.shape == (None,) * ndim
    assert feature.ndim == ndim
    features = Features({"x": feature})
    assert Features.from_dict(json.loads(json.dumps(features.to_dict()))) == features
    assert Features.from_arrow_schema(features.arrow_schema.remove_metadata()) == features
    value = np.ones((2,) * ndim, dtype=np.float32)
    np.testing.assert_array_equal(feature.decode_example(feature.encode_example(value)), value)
    with pytest.raises(ValueError, match="shape"):
        feature.encode_example(np.ones((2,) * (ndim + 1)))


@pytest.mark.parametrize("ndim", [-1, 1.5, True, "2", 2**31])
def test_tensor_invalid_ndim(ndim):
    with pytest.raises(ValueError, match="ndim"):
        Tensor(ndim=ndim)


def test_tensor_ndim_matches_shape():
    assert Tensor((None, None, 3)).ndim == 3
    assert Tensor((None, 3), ndim=2) == Tensor((None, 3))
    with pytest.raises(ValueError, match="ndim"):
        Tensor((None, None, 3), ndim=2)


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
@pytest.mark.parametrize("file_format", ["ipc", "parquet"])
@pytest.mark.parametrize("with_null", [False, True])
def test_tensor_plain_arrow_interop(shape, file_format, with_null, tmp_path):
    values = [np.arange(6, dtype=np.int32).reshape(2, 3)]
    if shape != (2, 3):
        values.append(np.arange(12, dtype=np.int32).reshape(4, 3))
    if with_null:
        values.insert(1, None)
    dataset = Dataset.from_dict({"x": values}, features=Features({"x": Tensor(shape, "int32")}))
    path = tmp_path / ("tensor." + file_format)
    if file_format == "ipc":
        with pa.ipc.new_file(str(path), dataset.data.schema) as writer:
            writer.write_table(dataset.data.table)
    else:
        dataset.to_parquet(str(path), batch_size=1)
    extension_name = "arrow.fixed_shape_tensor" if shape == (2, 3) else "arrow.variable_shape_tensor"
    # -S excludes site customizations; PYTHONPATH exposes PyArrow's directory,
    # which may also contain Datasets. The child must never import Datasets.
    reader = """
import base64
import json
import sys
import pyarrow as pa
import pyarrow.parquet as pq
assert "datasets" not in sys.modules
path, file_format, extension_name, expected_json = sys.argv[1:]
table = pa.ipc.open_file(path).read_all() if file_format == "ipc" else pq.read_table(path)
tensor_type = table.column("x").type
fallback = b"huggingface:tensor_schema" in (table.schema.metadata or {})
if fallback:
    assert not isinstance(tensor_type, pa.BaseExtensionType), tensor_type
    schema = pa.ipc.read_schema(pa.BufferReader(base64.b64decode(table.schema.metadata[b"huggingface:tensor_schema"])))
    tensor_type = schema.field("x").type
assert isinstance(tensor_type, pa.BaseExtensionType), tensor_type
assert not isinstance(tensor_type, pa.ExtensionType), tensor_type
assert tensor_type.extension_name == extension_name, tensor_type
values = table.column("x").to_pylist()
expected = json.loads(expected_json)
if extension_name == "arrow.variable_shape_tensor":
    assert pa.types.is_fixed_size_list(tensor_type.storage_type.field("shape").type)
    assert tensor_type.storage_type.field("shape").type.list_size == 2
    assert values == expected
else:
    assert isinstance(tensor_type, pa.FixedShapeTensorType)
    assert list(tensor_type.shape) == [2, 3]
    assert values == [value["data"] if value is not None else None for value in expected]
assert "datasets" not in sys.modules
print(f"{file_format}: {tensor_type}; rows={table.num_rows}; storage_fallback={fallback}; datasets_imported=False")
"""
    expected = [
        {"data": value.reshape(-1).tolist(), "shape": list(value.shape)} if value is not None else None
        for value in values
    ]
    result = subprocess.run(
        [sys.executable, "-S", "-c", reader, str(path), file_format, extension_name, json.dumps(expected)],
        env={**os.environ, "PYTHONPATH": str(Path(pa.__file__).parent.parent)},
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    print(result.stdout, end="")


@pytest.mark.parametrize("shape", [(2,), (None,)])
def test_tensor_uint64_mixed_magnitudes(shape):
    feature = Tensor(shape, "uint64")
    expected = np.array([0, 2**63 + 1], dtype=np.uint64)
    for value in [expected, expected.tolist(), {"data": expected.tolist(), "shape": [2]}]:
        np.testing.assert_array_equal(feature.decode_example(feature.encode_example(value)), expected)
    dataset = Dataset.from_dict({"x": [expected, None]}, features=Features({"x": feature}))
    np.testing.assert_array_equal(dataset[0]["x"], expected)


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
def test_tensor_parquet_fixed_length_outer_list(shape, tmp_path):
    value = [np.ones((2, 3), dtype=np.float32)] * 2
    features = Features({"x": List(Tensor(shape), length=2)})
    dataset = Dataset.from_dict({"x": [value, None]}, features=features)
    path = str(tmp_path / "outer_list.parquet")
    dataset.to_parquet(path, batch_size=1)
    import pyarrow.parquet as pq

    storage = pq.read_table(path)
    assert storage["x"].to_pylist()[1] is None
    restored = Dataset.from_parquet(path, cache_dir=str(tmp_path / "cache"))
    assert restored.features == features
    assert restored[1]["x"] is None
    assert len(restored[0]["x"]) == 2
    for actual, expected in zip(restored[0]["x"], value):
        np.testing.assert_array_equal(actual, expected)


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
def test_tensor_cast_nullable_list_to_fixed_length(shape):
    features = Features({"x": List(Tensor(shape))})
    value = np.ones((2, 3), dtype=np.float32)
    dataset = Dataset.from_dict({"x": [[value, value], None]}, features=features)
    target = Features({"x": List(Tensor(shape), length=2)})
    casted = dataset.cast(target)
    assert casted.features == target
    assert casted[1]["x"] is None
    for actual in casted[0]["x"]:
        np.testing.assert_array_equal(actual, value)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"uniform_shape": (None, 4)},
        {"permutation": [1, 0]},
        {"dim_names": ["row", "column"]},
        {"value_type": pa.int32()},
        {"uniform_shape": (None, 3, None), "ndim": 3},
    ],
)
def test_tensor_variable_equality_parameters(kwargs):
    from datasets.features.tensor import VariableShapeTensorType

    original = Tensor((None, 3))()
    different = VariableShapeTensorType(**{"value_type": pa.float32(), "uniform_shape": (None, 3), **kwargs})
    assert original != different
    assert not original.equals(different)
    assert pa.schema([("x", original)]) != pa.schema([("x", different)])


def test_tensor_cast_rejects_incompatible_uniform_shape():
    dataset = Dataset.from_dict({"x": [np.ones((2, 3))]}, features=Features({"x": Tensor((None, 3))}))
    with pytest.raises(ValueError, match="shape"):
        dataset.cast_column("x", Tensor((None, 4)))


@pytest.mark.parametrize("fixed", [False, True])
@pytest.mark.parametrize("metadata", [{"permutation": [1, 0]}, {"dim_names": ["row", "column"]}])
def test_tensor_cast_rejects_unsupported_metadata(fixed, metadata):
    from datasets.features.tensor import VariableShapeTensorType
    from datasets.table import cast_array_to_feature

    feature = Tensor((2, 3) if fixed else (None, 3))
    arrow_type = (
        pa.fixed_shape_tensor(pa.float32(), (2, 3), **metadata)
        if fixed
        else VariableShapeTensorType(pa.float32(), (None, 3), **metadata)
    )
    values = [[0, 1, 2, 3, 4, 5]] if fixed else [{"data": [0, 1, 2, 3, 4, 5], "shape": [2, 3]}]
    array = pa.ExtensionArray.from_storage(arrow_type, pa.array(values, type=arrow_type.storage_type))
    with pytest.raises(ValueError, match="permut|dimension names"):
        cast_array_to_feature(array, feature)


@pytest.mark.parametrize("dtype,large", [("int64", 2**53 + 1), ("uint64", 2**63 + 1)])
@pytest.mark.parametrize("shape", [(2,), (None,)])
@pytest.mark.parametrize("batched", [False, True])
def test_tensor_map_python_integer_precision(dtype, large, shape, batched):
    features = Features({"x": Tensor(shape, dtype)})
    dataset = Dataset.from_dict({"x": [[0, large]]}, features=features)
    assert dataset[0]["x"].tolist() == [0, large]
    mapped = dataset.map(lambda _: {"x": [[0, large]] if batched else [0, large]}, batched=batched, features=features)
    assert mapped[0]["x"].tolist() == [0, large]


@pytest.mark.parametrize("dtype,large", [("int64", 2**53 + 1), ("uint64", 2**63 + 1)])
@pytest.mark.parametrize("shape", [(1,), (None,)])
@pytest.mark.parametrize("nested", [False, True])
@pytest.mark.parametrize("format_name", ["numpy", "torch", "pandas", "to_pandas"])
def test_tensor_nullable_integer_formats(dtype, large, shape, nested, format_name):
    if format_name == "torch":
        pytest.importorskip("torch")
    feature = Tensor(shape, dtype)
    value = np.array([large], dtype=dtype)
    features = Features({"x": List(feature) if nested else feature})
    dataset = Dataset.from_dict({"x": [[value, None]] if nested else [value, None]}, features=features)
    for current in [dataset, dataset.map(lambda row: row, features=features)]:
        if format_name == "to_pandas":
            rows = [current.to_pandas()["x"].iloc[0]]
        elif format_name == "pandas":
            formatted = current.with_format(format_name)
            rows = [formatted[0]["x"].iloc[0], formatted[:]["x"].iloc[0], formatted["x"][:].iloc[0]]
        else:
            formatted = current.with_format(format_name)
            rows = [formatted[0]["x"], formatted[:]["x"][0], formatted["x"][:][0]]
        for row in rows:
            if nested:
                assert row[1] is None
                row = row[0]
            assert row.tolist() == [large]


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
@pytest.mark.parametrize("depth", [1, 2])
def test_tensor_null_struct_parent(shape, depth):
    feature = Tensor(shape)
    value = np.ones((2, 3), dtype=np.float32)
    for _ in range(depth):
        feature = {"t": feature}
        value = {"t": value}
    features = Features({"x": feature})
    for rows in [[None], [None, value]]:
        dataset = Dataset.from_dict({"x": rows}, features=features)
        assert dataset[0]["x"] is None
        assert dataset.map(lambda row: row, features=features)[0]["x"] is None


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
@pytest.mark.parametrize("batched", [False, True])
def test_tensor_map_infers_replacement_type(shape, batched):
    from datasets import Value

    dataset = Dataset.from_dict({"x": [np.ones((2, 3))]}, features=Features({"x": Tensor(shape)}))

    def replace(_):
        return {"x": ["hello"] if batched else "hello"}

    mapped = dataset.map(replace, batched=batched)
    assert mapped.features == Features({"x": Value("string")})
    assert mapped[0]["x"] == "hello"
    with pytest.raises((ValueError, TypeError), match="Tensor"):
        dataset.map(replace, batched=batched, features=dataset.features)


@pytest.mark.parametrize("batched", [False, True])
def test_tensor_map_rejects_flat_value_for_higher_rank(batched):
    features = Features({"x": Tensor((2, 3), "int32")})
    dataset = Dataset.from_dict({"x": [np.arange(6).reshape(2, 3)]}, features=features)
    with pytest.raises(ValueError, match="shape"):
        dataset.map(
            lambda _: {"x": [[0, 1, 2, 3, 4, 5]] if batched else [0, 1, 2, 3, 4, 5]},
            features=features,
            batched=batched,
        )
    storage = {"data": [0, 1, 2, 3, 4, 5], "shape": [2, 3]}
    mapped = dataset.map(lambda _: {"x": [storage] if batched else storage}, features=features, batched=batched)
    assert mapped[0]["x"].tolist() == [[0, 1, 2], [3, 4, 5]]


@pytest.mark.parametrize("fixed", [False, True])
@pytest.mark.parametrize("layout", [{}, {"permutation": [0, 1]}, {"permutation": [1, 0]}, {"dim_names": ["r", "c"]}])
def test_tensor_schema_created_before_datasets_import(fixed, layout, tmp_path):
    reader = """
import json
import sys
import pyarrow as pa
assert "datasets" not in sys.modules
fixed = sys.argv[1] == "True"
layout = json.loads(sys.argv[2])
metadata = {"shape": [2, 3]} if fixed else {"uniform_shape": [None, 3]}
metadata.update(layout)
storage = pa.list_(pa.int64(), 6) if fixed else pa.struct(
    [("data", pa.list_(pa.int64())), ("shape", pa.list_(pa.int32(), 2))]
)
schema = pa.schema([pa.field("x", storage, metadata={
    b"ARROW:extension:name": b"arrow.fixed_shape_tensor" if fixed else b"arrow.variable_shape_tensor",
    b"ARROW:extension:metadata": json.dumps(metadata).encode(),
})])
schema = pa.ipc.read_schema(pa.BufferReader(schema.serialize()))
assert isinstance(schema.field("x").type, pa.BaseExtensionType)
assert not isinstance(schema.field("x").type, pa.ExtensionType)
from datasets import Dataset, Features, Tensor
if layout.get("dim_names") or layout.get("permutation") == [1, 0]:
    try:
        Features.from_arrow_schema(schema)
    except ValueError as error:
        assert "dimension" in str(error), str(error)
    else:
        raise AssertionError("Unsupported tensor layout was silently discarded")
    sys.exit(0)
features = Features.from_arrow_schema(schema)
assert features == Features({"x": Tensor((2, 3) if fixed else (None, 3), "int64")})
values = [[9007199254740993] * 6] if fixed else [{"data": [9007199254740993] * 6, "shape": [2, 3]}]
array = pa.ExtensionArray.from_storage(schema.field("x").type, pa.array(values, type=storage))
dataset = Dataset(pa.Table.from_arrays([array], schema=schema))
assert dataset[0]["x"].tolist() == [[9007199254740993] * 3] * 2
"""
    result = subprocess.run(
        [sys.executable, "-c", reader, str(fixed), json.dumps(layout)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr


TENSOR_FORMATS = [
    "numpy",
    pytest.param("torch", marks=pytest.mark.skipif(not config.TORCH_AVAILABLE, reason="Requires torch")),
    pytest.param("tensorflow", marks=pytest.mark.skipif(not config.TF_AVAILABLE, reason="Requires tensorflow")),
    pytest.param("jax", marks=pytest.mark.skipif(not config.JAX_AVAILABLE, reason="Requires jax")),
    "pandas",
    pytest.param("polars", marks=pytest.mark.skipif(not config.POLARS_AVAILABLE, reason="Requires polars")),
]


def _nest_tensor(feature, value, nesting):
    if nesting == "list":
        return List(feature), [value, None]
    if nesting == "struct":
        return {"t": feature}, {"t": value}
    if nesting == "list_struct":
        return List({"t": List(feature)}), [{"t": [value, None]}, None]
    return feature, value


@pytest.mark.parametrize("format_name", TENSOR_FORMATS)
@pytest.mark.parametrize(
    "dtype,values", [("bool", [True, False]), ("uint64", [0, 2**63 + 1]), ("float64", [0.5, 1.5])]
)
@pytest.mark.parametrize("shape", [(2,), (None,)])
@pytest.mark.parametrize("nesting", ["top", "list", "struct", "list_struct"])
def test_tensor_format_preserves_dtype_and_nulls(format_name, dtype, values, shape, nesting):
    expected = np.asarray(values, dtype=dtype)
    feature, value = _nest_tensor(Tensor(shape, dtype), expected, nesting)
    dataset = Dataset.from_dict(
        {"x": [value, None], "other": [1, 2]}, features=Features({"x": feature, "other": Value("int64")})
    )
    formatted = dataset.with_format(format_name)

    def get_rows():
        if format_name == "pandas":
            return [formatted[0]["x"].iloc[0], formatted[:]["x"].iloc[0], formatted["x"][:].iloc[0]], [
                formatted[1]["x"].iloc[0],
                formatted[:]["x"].iloc[1],
                formatted["x"][:].iloc[1],
            ]
        if format_name == "polars":
            return [formatted[0]["x"][0], formatted[:]["x"][0], formatted["x"][:][0]], [
                formatted[1]["x"][0],
                formatted[:]["x"][1],
                formatted["x"][:][1],
            ]
        return [formatted[0]["x"], formatted[:]["x"][0], formatted["x"][:][0]], [
            formatted[1]["x"],
            formatted[:]["x"][1],
            formatted["x"][:][1],
        ]

    if format_name == "jax" and dtype in ("uint64", "float64"):
        import jax

        with jax.experimental.enable_x64(True):
            rows, nulls = get_rows()
    else:
        rows, nulls = get_rows()
    assert all(row is None for row in nulls)
    for row in rows:
        if nesting == "list_struct":
            assert row[1] is None
            row = row[0]["t"]
        if nesting in ("list", "list_struct"):
            assert row[1] is None
            row = row[0]
        elif nesting == "struct":
            row = row["t"]
        if format_name in ("numpy", "pandas", "polars"):
            assert isinstance(row, np.ndarray)
        actual = np.asarray(row)
        assert actual.dtype == expected.dtype
        np.testing.assert_array_equal(actual, expected)


@require_polars
@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
@pytest.mark.parametrize("nesting", ["list", "struct", "list_struct"])
def test_tensor_polars_nested_arrays(shape, nesting):
    expected = np.arange(6, dtype=np.float32).reshape(2, 3)
    feature, value = _nest_tensor(Tensor(shape), expected, nesting)
    formatted = Dataset.from_dict({"x": [value, None]}, features=Features({"x": feature})).with_format("polars")
    for column in [formatted[:]["x"], formatted["x"][:]]:
        assert column[1] is None
        row = column[0]
        if nesting == "list_struct":
            assert row[1] is None
            row = row[0]["t"]
        if nesting in ("list", "list_struct"):
            assert row[1] is None
            row = row[0]
        else:
            row = row["t"]
        assert isinstance(row, np.ndarray)
        np.testing.assert_array_equal(row, expected)


@pytest.mark.parametrize("value", [[0, 1, 2], [0.5], [float("nan")], [-1], [float("inf")]])
@pytest.mark.parametrize("representation", ["list", "array", "storage"])
def test_tensor_bool_rejects_lossy_values(value, representation):
    if representation == "array":
        value = np.asarray(value)
    elif representation == "storage":
        value = {"data": value, "shape": [len(value)]}
    with pytest.raises(ValueError, match="bool"):
        Tensor((None,), "bool").encode_example(value)


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
@pytest.mark.parametrize("nesting", ["list", "struct", "list_struct"])
@pytest.mark.parametrize("batched", [False, True])
def test_tensor_nested_map_infers_scalar_replacement(shape, nesting, batched):
    feature, value = _nest_tensor(Tensor(shape), np.ones((2, 3)), nesting)
    dataset = Dataset.from_dict({"x": [value]}, features=Features({"x": feature}))

    def replace(_):
        return {"x": [0] if batched else 0}

    mapped = dataset.map(replace, batched=batched)
    assert mapped.features == Features({"x": Value("int64")})
    assert mapped[0]["x"] == 0
    with pytest.raises((ValueError, TypeError, AttributeError)):
        dataset.map(replace, batched=batched, features=dataset.features)


@require_jax
@pytest.mark.parametrize("enabled", [False, True])
def test_tensor_jax_uint64_requires_x64(enabled):
    import jax

    with jax.experimental.enable_x64(enabled):
        dataset = Dataset.from_dict(
            {"x": [[0, 2**63 + 1]]}, features=Features({"x": Tensor((2,), "uint64")})
        ).with_format("jax")
        if enabled:
            actual = np.asarray(dataset[0]["x"])
            assert actual.dtype == np.uint64
            assert actual.tolist() == [0, 2**63 + 1]
        else:
            with pytest.raises(ValueError, match="uint64.*jax_enable_x64"):
                dataset[0]


def test_tensor_pandas_decodes_sibling_features():
    from PIL import Image as PILImage

    from datasets import Image

    expected = np.zeros((2, 2, 3), dtype=np.uint8)
    features = Features({"x": {"t": Tensor((2,), "bool"), "image": Image()}})
    dataset = Dataset.from_dict(
        {"x": [{"t": [True, False], "image": PILImage.fromarray(expected)}, None]}, features=features
    ).with_format("pandas")
    for column in [dataset[0]["x"], dataset[:]["x"], dataset["x"][:]]:
        value = column.iloc[0]
        assert isinstance(value["image"], PILImage.Image)
        np.testing.assert_array_equal(np.asarray(value["image"]), expected)
        assert value["t"].dtype == np.bool_
        assert value["t"].tolist() == [True, False]
    assert dataset[1]["x"].iloc[0] is None
    assert dataset[:]["x"].iloc[1] is None


@pytest.mark.parametrize("batched", [False, True])
def test_tensor_map_preserves_fractional_sibling(batched):
    features = Features({"x": {"t": Tensor((2,)), "n": Value("int64")}})
    dataset = Dataset.from_dict({"x": [{"t": [1.0, 2.0], "n": 1}]}, features=features)
    value = {"t": [1.0, 2.0], "n": 1.5}
    mapped = dataset.map(lambda _: {"x": [value] if batched else value}, batched=batched)
    assert mapped[0]["x"]["n"] == 1.5
    assert mapped.features["x"]["n"] == Value("float64")


@pytest.mark.parametrize("batched", [False, True])
def test_tensor_map_preserves_added_sibling(batched):
    features = Features({"x": {"t": Tensor((2,))}})
    dataset = Dataset.from_dict({"x": [{"t": [1.0, 2.0]}]}, features=features)
    value = {"t": [1.0, 2.0], "added": 42}
    mapped = dataset.map(lambda _: {"x": [value] if batched else value}, batched=batched)
    assert "added" in mapped[0]["x"]
    assert mapped[0]["x"]["added"] == 42
    assert mapped.features["x"]["added"] == Value("int64")


@pytest.mark.parametrize("batched", [False, True])
@pytest.mark.parametrize("shape", [(2,), (None,)])
def test_tensor_map_preserves_json_sibling(batched, shape):
    from datasets import Json

    features = Features({"x": {"t": Tensor(shape, "int64"), "j": Json()}})
    dataset = Dataset.from_dict({"x": [{"t": [1, 2], "j": {"a": 1}}]}, features=features)
    mapped = dataset.map(lambda row: {"x": row["x"]}, batched=batched)
    assert mapped.features == features
    assert mapped[0]["x"]["j"] == {"a": 1}
    np.testing.assert_array_equal(mapped[0]["x"]["t"], [1, 2])


@pytest.mark.parametrize("shape", [(2,), (None,)])
@pytest.mark.parametrize("json_value", [{"a": 1}, [1, "two"], "text", None])
def test_tensor_pandas_decodes_json_sibling_once(shape, json_value):
    from datasets import Json

    features = Features({"x": {"t": Tensor(shape, "int64"), "j": Json()}})
    dataset = Dataset.from_dict({"x": [{"t": [1, 2], "j": json_value}, None]}, features=features)
    formatted = dataset.with_format("pandas")
    for column in [formatted[0]["x"], formatted[:]["x"], formatted["x"][:]]:
        value = column.iloc[0]
        assert value["j"] == json_value
        np.testing.assert_array_equal(value["t"], [1, 2])
        assert value["t"].dtype == np.int64
    assert formatted[1]["x"].iloc[0] is None


@pytest.mark.parametrize("shape", [(2,), (None,)])
def test_tensor_large_list_construction_and_map(shape):
    from datasets import LargeList

    features = Features({"x": LargeList(Tensor(shape, "int64"))})
    dataset = Dataset.from_dict({"x": [[[1, 2]], None, [None]]}, features=features)
    for current in [dataset, dataset.map(lambda row: row, features=features)]:
        assert current.features == features
        np.testing.assert_array_equal(current[0]["x"][0], [1, 2])
        assert current[1]["x"] is None
        assert current[2]["x"] == [None]


@require_torch
@pytest.mark.parametrize("batched", [False, True])
@pytest.mark.parametrize("shape", [(2,), (None,)])
@pytest.mark.parametrize("nested", [False, True])
def test_tensor_map_detaches_torch_gradients(batched, shape, nested):
    import torch

    feature = {"t": Tensor(shape)} if nested else Tensor(shape)
    value = {"t": [1.0, 2.0]} if nested else [1.0, 2.0]
    dataset = Dataset.from_dict({"x": [value]}, features=Features({"x": feature}))

    def replace(_):
        value = torch.tensor([1.0, 2.0], requires_grad=True)
        if nested:
            value = {"t": value}
        return {"x": [value] if batched else value}

    mapped = dataset.map(replace, features=dataset.features, batched=batched)
    actual = mapped[0]["x"]["t"] if nested else mapped[0]["x"]
    np.testing.assert_array_equal(actual, [1.0, 2.0])
    assert mapped.features == dataset.features


@pytest.mark.parametrize("fixed", [False, True])
@pytest.mark.parametrize("strict_equality", [False, True])
def test_tensor_external_canonical_registration(fixed, strict_equality, tmp_path):
    # A different implementation must retain its registration and interoperate
    # without Arrow attempting an extension-to-extension cast.
    script = """
import json
import sys

import numpy as np
import pyarrow as pa

assert "datasets" not in sys.modules
fixed = sys.argv[1] == "True"
name = "arrow.fixed_shape_tensor" if fixed else "arrow.variable_shape_tensor"

class ExternalTensorType(pa.ExtensionType):
    def __init__(self, storage_type, serialized):
        self.serialized = serialized
        super().__init__(storage_type, name)

    def __arrow_ext_serialize__(self):
        return self.serialized

    @classmethod
    def __arrow_ext_deserialize__(cls, storage_type, serialized):
        return cls(storage_type, serialized)

    def __eq__(self, other):
        return (
            isinstance(other, ExternalTensorType)
            and self.storage_type == other.storage_type
            and json.loads(self.serialized) == json.loads(other.serialized)
        )

if sys.argv[2] == "False":
    del ExternalTensorType.__eq__

storage_type = pa.list_(pa.int32(), 6) if fixed else pa.struct([
    ("data", pa.list_(pa.int32())), ("shape", pa.list_(pa.int32(), 2))
])
metadata = {"shape": [2, 3]} if fixed else {"uniform_shape": [None, 3]}
external = ExternalTensorType(storage_type, json.dumps(metadata).encode())
try:
    pa.unregister_extension_type(name)
except pa.ArrowKeyError:
    pass
pa.register_extension_type(external)

from datasets import Dataset, Features, List, Tensor
from datasets.features.tensor import normalize_tensor_type, tensor_to_parquet_table
from datasets.table import array_cast, cast_array_to_feature, embed_array_storage, table_cast

schema = pa.schema([("x", external)])
restored = pa.ipc.read_schema(pa.BufferReader(schema.serialize()))
assert isinstance(restored.field("x").type, ExternalTensorType), "Datasets replaced the existing registration"
feature = Tensor((2, 3) if fixed else (None, 3), "int32")
assert Features.from_arrow_schema(restored) == Features({"x": feature})
assert normalize_tensor_type(external) == feature()
values = [[0, 1, 2, 3, 4, 5], None] if fixed else [
    {"data": [0, 1, 2, 3, 4, 5], "shape": [2, 3]}, None
]
array = pa.ExtensionArray.from_storage(external, pa.array(values, type=storage_type))
for result in [cast_array_to_feature(array, feature), embed_array_storage(array, feature)]:
    assert result.type == feature()
    assert result.storage.to_pylist() == values
    assert result.storage.buffers() == array.storage.buffers()
local = cast_array_to_feature(array, feature)
assert array_cast(local, external).storage.to_pylist() == values
assert table_cast(pa.table({"x": local}), schema).column("x").to_pylist() == values
assert tensor_to_parquet_table(pa.table({"x": local}), schema).column("x").to_pylist() == values

dataset = Dataset(pa.Table.from_arrays([array], schema=restored))
for shape in [(2, 3), (None, 3), (None, None)]:
    casted = dataset.cast_column("x", Tensor(shape, "float64"))
    assert casted[0]["x"].tolist() == [[0, 1, 2], [3, 4, 5]]
    assert casted[0]["x"].dtype == np.float64
    assert casted[1]["x"] is None
try:
    dataset.cast_column("x", Tensor((None, 4), "int32"))
except ValueError:
    pass
else:
    raise AssertionError("Incompatible uniform_shape was accepted")

for fmt in [None, "numpy", "pandas"]:
    formatted = dataset.with_format(fmt)
    row = formatted[0]["x"]
    if fmt == "pandas":
        row = row.iloc[0]
    assert row.tolist() == [[0, 1, 2], [3, 4, 5]]
    assert len(formatted[:]["x"]) == 2

value = np.arange(6, dtype=np.int32).reshape(2, 3)
features = Features({"x": List(feature)})
nested = Dataset.from_dict({"x": [[value, value], None]}, features=features)
nested = nested.cast(Features({"x": List(feature, length=2)}))
assert nested[1]["x"] is None
assert nested[0]["x"][0].tolist() == value.tolist()
mapped = nested.map(lambda row: row, features=nested.features)
assert mapped[0]["x"][0].tolist() == value.tolist()
assert mapped[1]["x"] is None
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(fixed), str(strict_equality)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
@pytest.mark.parametrize("sliced", [False, True])
def test_tensor_nullable_list_with_hidden_children(shape, sliced):
    from datasets.table import array_cast, cast_array_to_feature

    feature = Tensor(shape, "int32")
    value = np.arange(6, dtype=np.int32).reshape(2, 3)
    tensors = Dataset.from_dict({"x": [value] * 6}, features=Features({"x": feature})).data.column("x").chunk(0)
    array = pa.ListArray.from_arrays([0, 2, 4, 6], tensors, mask=pa.array([False, True, False]))
    if sliced:
        array = array.slice(1)
    target = List(feature, length=2)
    for result in [array_cast(array, pa.list_(feature(), 2)), cast_array_to_feature(array, target)]:
        result.validate(full=True)
        assert result.is_null().to_pylist() == ([True, False] if sliced else [False, True, False])
        assert result.to_pylist() == array.to_pylist()


@pytest.mark.parametrize("variable_list", [False, True])
def test_tensor_cast_zero_length_list(variable_list):
    from datasets.table import array_cast, cast_array_to_feature, table_cast

    feature = Tensor((None, 3), "int32")
    child = pa.ExtensionArray.from_storage(feature(), pa.array([], type=feature().storage_type))
    target = pa.list_(feature(), 0)
    array = (
        pa.ListArray.from_arrays([0, 0, 0, 0], child, mask=pa.array([False, True, False]))
        if variable_list
        else pa.Array.from_buffers(target, 3, [pa.array([True, False, True]).buffers()[1]], children=[child])
    )
    for casted in [array_cast(array, target), cast_array_to_feature(array, List(feature, length=0))]:
        casted.validate(full=True)
        assert casted.to_pylist() == [[], None, []]
    table = table_cast(pa.table({"x": array}), pa.schema([("x", target)]))
    assert table.column("x").to_pylist() == [[], None, []]


@pytest.mark.parametrize("shape", [(2, 3), (None, 3)])
@pytest.mark.parametrize("native_target", [False, True])
def test_tensor_parquet_table_canonical_schema(shape, native_target):
    from datasets.features.tensor import tensor_to_parquet_table

    feature = Tensor(shape, "int32")
    schema = Features({"x": feature}).arrow_schema
    native = pa.ipc.read_schema(pa.BufferReader(schema.serialize()))
    source_schema, target_schema = (schema, native) if native_target else (native, schema)
    source_type = source_schema.field("x").type
    values = [[0, 1, 2, 3, 4, 5]] if shape == (2, 3) else [{"data": [0, 1, 2, 3, 4, 5], "shape": [2, 3]}]
    array = pa.ExtensionArray.from_storage(source_type, pa.array(values, type=source_type.storage_type))
    table = tensor_to_parquet_table(pa.Table.from_arrays([array], schema=source_schema), target_schema)
    assert table.column("x").to_pylist() == values
    assert Features.from_arrow_schema(table.schema) == Features({"x": feature})


@pytest.mark.parametrize("shape", [(2, 3), (None, 3), (None, None)])
@pytest.mark.parametrize("native_source", [False, True])
@pytest.mark.parametrize("sliced", [False, True])
@pytest.mark.parametrize("nesting", ["top", "list", "json_sibling", "required_fields"])
def test_tensor_parquet_null_storage(shape, native_source, sliced, nesting, tmp_path):
    import pyarrow.parquet as pq

    from datasets.features.tensor import tensor_to_parquet_table

    schema = Features({"x": Tensor(shape, "int64")}).arrow_schema
    if native_source:
        schema = pa.ipc.read_schema(pa.BufferReader(schema.serialize()))
    arrow_type = schema.field("x").type
    values = [list(range(6)), [2**53 + 1] * 6, None, list(range(6)), None]
    if shape != (2, 3):
        values = [{"data": value, "shape": [2, 3]} if value is not None else None for value in values]
    array = pa.ExtensionArray.from_storage(arrow_type, pa.array(values, type=arrow_type.storage_type))
    if sliced:
        array = array.slice(1)
        values = values[1:]
    if nesting == "list":
        array = pa.ListArray.from_arrays([0, len(array), len(array)], array, mask=pa.array([False, True]))
        values = [values, None]
    elif nesting == "json_sibling":
        json_array = pa.array(['{"a":1}'] * len(array), type=pa.json_())
        array = pa.StructArray.from_arrays([array, json_array], names=["t", "j"])
        values = [{"t": value, "j": '{"a":1}'} for value in values]
    elif nesting == "required_fields":
        # Required children may have valid values beneath a null struct parent.
        mask = array.is_null()
        filled = pa.ExtensionArray.from_storage(
            arrow_type,
            pa.array([value if value is not None else values[0] for value in values], type=arrow_type.storage_type),
        )
        array = pa.StructArray.from_arrays(
            [filled, pa.array([1] * len(array))],
            fields=[pa.field("t", array.type, nullable=False), pa.field("n", pa.int64(), nullable=False)],
            mask=mask,
        )
        values = [{"t": value, "n": 1} if value is not None else None for value in values]
    schema = pa.schema([schema.field("x").with_type(array.type)])
    table = tensor_to_parquet_table(pa.Table.from_arrays([array], schema=schema))
    path = tmp_path / "null_tensor.parquet"
    pq.write_table(table, path)
    reader = """
import json
import sys
import pyarrow.parquet as pq
assert "datasets" not in sys.modules
table = pq.read_table(sys.argv[1])
assert table.column("x").to_pylist() == json.loads(sys.argv[2])
assert "datasets" not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-S", "-c", reader, str(path), json.dumps(values)],
        env={**os.environ, "PYTHONPATH": str(Path(pa.__file__).parent.parent)},
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("list_kind", ["list", "large_list", "fixed_size_list"])
def test_tensor_array_cast_preserves_list_value_field(list_kind):
    from datasets.table import array_cast

    feature = Tensor((None, 3), "int32")
    child = pa.ExtensionArray.from_storage(
        feature(), pa.array([{"data": [1, 2, 3], "shape": [1, 3]}], type=feature().storage_type)
    )
    field = pa.field("custom", feature(), nullable=False, metadata={"unit": "test"})
    if list_kind == "fixed_size_list":
        target = pa.list_(field, 1)
        array = pa.Array.from_buffers(target, 1, [None], children=[child])
    else:
        target = pa.large_list(field) if list_kind == "large_list" else pa.list_(field)
        array_class = pa.LargeListArray if list_kind == "large_list" else pa.ListArray
        array = array_class.from_arrays([0, 1], child, type=target)
    casted = array_cast(array, target)
    assert casted.type.value_field.equals(field, check_metadata=True)
    assert casted.to_pylist() == [[{"data": [1, 2, 3], "shape": [1, 3]}]]


@pytest.mark.parametrize("large", [False, True])
def test_tensor_list_cast_slice_after_null(large):
    from datasets.table import array_cast, cast_array_to_feature

    feature = Tensor((None, 1), "int32")
    values = [{"data": [i], "shape": [1, 1]} for i in range(4)]
    children = pa.ExtensionArray.from_storage(feature(), pa.array(values, type=feature().storage_type))
    array_class = pa.LargeListArray if large else pa.ListArray
    array = array_class.from_arrays([0, 0, 2, 4], children, mask=pa.array([True, False, False])).slice(1)
    for casted in [
        array_cast(array, pa.list_(feature(), 2)),
        cast_array_to_feature(array, List(feature, length=2)),
    ]:
        casted.validate(full=True)
        assert casted.to_pylist() == [values[:2], values[2:]]
