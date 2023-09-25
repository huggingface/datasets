import copy
import os
import tempfile
from unittest import TestCase
from unittest.mock import patch

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from datasets.arrow_writer import ArrowWriter, OptimizedTypedSequence, ParquetWriter, TypedSequence
from datasets.features import Array2D, ClassLabel, Features, Image, Value
from datasets.features.features import Array2DExtensionType, cast_to_python_objects
from datasets.keyhash import DuplicatedKeysError, InvalidKeyError

from .utils import require_pil


class TypedSequenceTest(TestCase):
    def test_no_type(self):
        arr = pa.array(TypedSequence([1, 2, 3]))
        self.assertEqual(arr.type, pa.int64())

    def test_array_type_forbidden(self):
        with self.assertRaises(ValueError):
            _ = pa.array(TypedSequence([1, 2, 3]), type=pa.int64())

    def test_try_type_and_type_forbidden(self):
        with self.assertRaises(ValueError):
            _ = pa.array(TypedSequence([1, 2, 3], try_type=Value("bool"), type=Value("int64")))

    def test_compatible_type(self):
        arr = pa.array(TypedSequence([1, 2, 3], type=Value("int32")))
        self.assertEqual(arr.type, pa.int32())

    def test_incompatible_type(self):
        with self.assertRaises((TypeError, pa.lib.ArrowInvalid)):
            _ = pa.array(TypedSequence(["foo", "bar"], type=Value("int64")))

    def test_try_compatible_type(self):
        arr = pa.array(TypedSequence([1, 2, 3], try_type=Value("int32")))
        self.assertEqual(arr.type, pa.int32())

    def test_try_incompatible_type(self):
        arr = pa.array(TypedSequence(["foo", "bar"], try_type=Value("int64")))
        self.assertEqual(arr.type, pa.string())

    def test_compatible_extension_type(self):
        arr = pa.array(TypedSequence([[[1, 2, 3]]], type=Array2D((1, 3), "int64")))
        self.assertEqual(arr.type, Array2DExtensionType((1, 3), "int64"))

    def test_incompatible_extension_type(self):
        with self.assertRaises((TypeError, pa.lib.ArrowInvalid)):
            _ = pa.array(TypedSequence(["foo", "bar"], type=Array2D((1, 3), "int64")))

    def test_try_compatible_extension_type(self):
        arr = pa.array(TypedSequence([[[1, 2, 3]]], try_type=Array2D((1, 3), "int64")))
        self.assertEqual(arr.type, Array2DExtensionType((1, 3), "int64"))

    def test_try_incompatible_extension_type(self):
        arr = pa.array(TypedSequence(["foo", "bar"], try_type=Array2D((1, 3), "int64")))
        self.assertEqual(arr.type, pa.string())

    @require_pil
    def test_exhaustive_cast(self):
        import PIL.Image

        pil_image = PIL.Image.fromarray(np.arange(10, dtype=np.uint8).reshape(2, 5))
        with patch(
            "datasets.arrow_writer.cast_to_python_objects", side_effect=cast_to_python_objects
        ) as mock_cast_to_python_objects:
            _ = pa.array(TypedSequence([{"path": None, "bytes": b"image_bytes"}, pil_image], type=Image()))
            args, kwargs = mock_cast_to_python_objects.call_args_list[-1]
            self.assertIn("optimize_list_casting", kwargs)
            self.assertFalse(kwargs["optimize_list_casting"])


def _check_output(output, expected_num_chunks: int):
    stream = pa.BufferReader(output) if isinstance(output, pa.Buffer) else pa.memory_map(output)
    f = pa.ipc.open_stream(stream)
    pa_table: pa.Table = f.read_all()
    assert len(pa_table.to_batches()) == expected_num_chunks
    assert pa_table.to_pydict() == {"col_1": ["foo", "bar"], "col_2": [1, 2]}
    del pa_table


@pytest.mark.parametrize("writer_batch_size", [None, 1, 10])
@pytest.mark.parametrize(
    "fields", [None, {"col_1": pa.string(), "col_2": pa.int64()}, {"col_1": pa.string(), "col_2": pa.int32()}]
)
def test_write(fields, writer_batch_size):
    output = pa.BufferOutputStream()
    schema = pa.schema(fields) if fields else None
    with ArrowWriter(stream=output, schema=schema, writer_batch_size=writer_batch_size) as writer:
        writer.write({"col_1": "foo", "col_2": 1})
        writer.write({"col_1": "bar", "col_2": 2})
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 2
    assert num_bytes > 0
    if not fields:
        fields = {"col_1": pa.string(), "col_2": pa.int64()}
    assert writer._schema == pa.schema(fields, metadata=writer._schema.metadata)
    _check_output(output.getvalue(), expected_num_chunks=num_examples if writer_batch_size == 1 else 1)


def test_write_with_features():
    output = pa.BufferOutputStream()
    features = Features({"labels": ClassLabel(names=["neg", "pos"])})
    with ArrowWriter(stream=output, features=features) as writer:
        writer.write({"labels": 0})
        writer.write({"labels": 1})
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 2
    assert num_bytes > 0
    assert writer._schema == features.arrow_schema
    assert writer._schema.metadata == features.arrow_schema.metadata
    stream = pa.BufferReader(output.getvalue())
    f = pa.ipc.open_stream(stream)
    pa_table: pa.Table = f.read_all()
    schema = pa_table.schema
    assert pa_table.num_rows == 2
    assert schema == features.arrow_schema
    assert schema.metadata == features.arrow_schema.metadata
    assert features == Features.from_arrow_schema(schema)


@pytest.mark.parametrize("writer_batch_size", [None, 1, 10])
def test_key_datatype(writer_batch_size):
    output = pa.BufferOutputStream()
    with ArrowWriter(
        stream=output,
        writer_batch_size=writer_batch_size,
        hash_salt="split_name",
        check_duplicates=True,
    ) as writer:
        with pytest.raises(InvalidKeyError):
            writer.write({"col_1": "foo", "col_2": 1}, key=[1, 2])
            num_examples, num_bytes = writer.finalize()


@pytest.mark.parametrize("writer_batch_size", [None, 2, 10])
def test_duplicate_keys(writer_batch_size):
    output = pa.BufferOutputStream()
    with ArrowWriter(
        stream=output,
        writer_batch_size=writer_batch_size,
        hash_salt="split_name",
        check_duplicates=True,
    ) as writer:
        with pytest.raises(DuplicatedKeysError):
            writer.write({"col_1": "foo", "col_2": 1}, key=10)
            writer.write({"col_1": "bar", "col_2": 2}, key=10)
            num_examples, num_bytes = writer.finalize()


@pytest.mark.parametrize("writer_batch_size", [None, 2, 10])
def test_write_with_keys(writer_batch_size):
    output = pa.BufferOutputStream()
    with ArrowWriter(
        stream=output,
        writer_batch_size=writer_batch_size,
        hash_salt="split_name",
        check_duplicates=True,
    ) as writer:
        writer.write({"col_1": "foo", "col_2": 1}, key=1)
        writer.write({"col_1": "bar", "col_2": 2}, key=2)
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 2
    assert num_bytes > 0
    _check_output(output.getvalue(), expected_num_chunks=num_examples if writer_batch_size == 1 else 1)


@pytest.mark.parametrize("writer_batch_size", [None, 1, 10])
@pytest.mark.parametrize(
    "fields", [None, {"col_1": pa.string(), "col_2": pa.int64()}, {"col_1": pa.string(), "col_2": pa.int32()}]
)
def test_write_batch(fields, writer_batch_size):
    output = pa.BufferOutputStream()
    schema = pa.schema(fields) if fields else None
    with ArrowWriter(stream=output, schema=schema, writer_batch_size=writer_batch_size) as writer:
        writer.write_batch({"col_1": ["foo", "bar"], "col_2": [1, 2]})
        writer.write_batch({"col_1": [], "col_2": []})
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 2
    assert num_bytes > 0
    if not fields:
        fields = {"col_1": pa.string(), "col_2": pa.int64()}
    assert writer._schema == pa.schema(fields, metadata=writer._schema.metadata)
    _check_output(output.getvalue(), expected_num_chunks=num_examples if writer_batch_size == 1 else 1)


@pytest.mark.parametrize("writer_batch_size", [None, 1, 10])
@pytest.mark.parametrize(
    "fields", [None, {"col_1": pa.string(), "col_2": pa.int64()}, {"col_1": pa.string(), "col_2": pa.int32()}]
)
def test_write_table(fields, writer_batch_size):
    output = pa.BufferOutputStream()
    schema = pa.schema(fields) if fields else None
    with ArrowWriter(stream=output, schema=schema, writer_batch_size=writer_batch_size) as writer:
        writer.write_table(pa.Table.from_pydict({"col_1": ["foo", "bar"], "col_2": [1, 2]}))
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 2
    assert num_bytes > 0
    if not fields:
        fields = {"col_1": pa.string(), "col_2": pa.int64()}
    assert writer._schema == pa.schema(fields, metadata=writer._schema.metadata)
    _check_output(output.getvalue(), expected_num_chunks=num_examples if writer_batch_size == 1 else 1)


@pytest.mark.parametrize("writer_batch_size", [None, 1, 10])
@pytest.mark.parametrize(
    "fields", [None, {"col_1": pa.string(), "col_2": pa.int64()}, {"col_1": pa.string(), "col_2": pa.int32()}]
)
def test_write_row(fields, writer_batch_size):
    output = pa.BufferOutputStream()
    schema = pa.schema(fields) if fields else None
    with ArrowWriter(stream=output, schema=schema, writer_batch_size=writer_batch_size) as writer:
        writer.write_row(pa.Table.from_pydict({"col_1": ["foo"], "col_2": [1]}))
        writer.write_row(pa.Table.from_pydict({"col_1": ["bar"], "col_2": [2]}))
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 2
    assert num_bytes > 0
    if not fields:
        fields = {"col_1": pa.string(), "col_2": pa.int64()}
    assert writer._schema == pa.schema(fields, metadata=writer._schema.metadata)
    _check_output(output.getvalue(), expected_num_chunks=num_examples if writer_batch_size == 1 else 1)


def test_write_file():
    with tempfile.TemporaryDirectory() as tmp_dir:
        fields = {"col_1": pa.string(), "col_2": pa.int64()}
        output = os.path.join(tmp_dir, "test.arrow")
        with ArrowWriter(path=output, schema=pa.schema(fields)) as writer:
            writer.write_batch({"col_1": ["foo", "bar"], "col_2": [1, 2]})
            num_examples, num_bytes = writer.finalize()
        assert num_examples == 2
        assert num_bytes > 0
        assert writer._schema == pa.schema(fields, metadata=writer._schema.metadata)
        _check_output(output, 1)


def get_base_dtype(arr_type):
    if pa.types.is_list(arr_type):
        return get_base_dtype(arr_type.value_type)
    else:
        return arr_type


def change_first_primitive_element_in_list(lst, value):
    if isinstance(lst[0], list):
        change_first_primitive_element_in_list(lst[0], value)
    else:
        lst[0] = value


@pytest.mark.parametrize("optimized_int_type, expected_dtype", [(None, pa.int64()), (Value("int32"), pa.int32())])
@pytest.mark.parametrize("sequence", [[1, 2, 3], [[1, 2, 3]], [[[1, 2, 3]]]])
def test_optimized_int_type_for_typed_sequence(sequence, optimized_int_type, expected_dtype):
    arr = pa.array(TypedSequence(sequence, optimized_int_type=optimized_int_type))
    assert get_base_dtype(arr.type) == expected_dtype


@pytest.mark.parametrize(
    "col, expected_dtype",
    [
        ("attention_mask", pa.int8()),
        ("special_tokens_mask", pa.int8()),
        ("token_type_ids", pa.int8()),
        ("input_ids", pa.int32()),
        ("other", pa.int64()),
    ],
)
@pytest.mark.parametrize("sequence", [[1, 2, 3], [[1, 2, 3]], [[[1, 2, 3]]]])
def test_optimized_typed_sequence(sequence, col, expected_dtype):
    # in range
    arr = pa.array(OptimizedTypedSequence(sequence, col=col))
    assert get_base_dtype(arr.type) == expected_dtype

    # not in range
    if col != "other":
        # avoids errors due to in-place modifications
        sequence = copy.deepcopy(sequence)
        value = np.iinfo(expected_dtype.to_pandas_dtype()).max + 1
        change_first_primitive_element_in_list(sequence, value)
        arr = pa.array(OptimizedTypedSequence(sequence, col=col))
        assert get_base_dtype(arr.type) == pa.int64()


@pytest.mark.parametrize("raise_exception", [False, True])
def test_arrow_writer_closes_stream(raise_exception, tmp_path):
    path = str(tmp_path / "dataset-train.arrow")
    try:
        with ArrowWriter(path=path) as writer:
            if raise_exception:
                raise pa.lib.ArrowInvalid()
            else:
                writer.stream.close()
    except pa.lib.ArrowInvalid:
        pass
    finally:
        assert writer.stream.closed


def test_arrow_writer_with_filesystem(mockfs):
    path = "mock://dataset-train.arrow"
    with ArrowWriter(path=path, storage_options=mockfs.storage_options) as writer:
        assert isinstance(writer._fs, type(mockfs))
        assert writer._fs.storage_options == mockfs.storage_options
        writer.write({"col_1": "foo", "col_2": 1})
        writer.write({"col_1": "bar", "col_2": 2})
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 2
    assert num_bytes > 0
    assert mockfs.exists(path)


def test_parquet_writer_write():
    output = pa.BufferOutputStream()
    with ParquetWriter(stream=output) as writer:
        writer.write({"col_1": "foo", "col_2": 1})
        writer.write({"col_1": "bar", "col_2": 2})
        num_examples, num_bytes = writer.finalize()
    assert num_examples == 2
    assert num_bytes > 0
    stream = pa.BufferReader(output.getvalue())
    pa_table: pa.Table = pq.read_table(stream)
    assert pa_table.to_pydict() == {"col_1": ["foo", "bar"], "col_2": [1, 2]}


@require_pil
@pytest.mark.parametrize("embed_local_files", [False, True])
def test_writer_embed_local_files(tmp_path, embed_local_files):
    import PIL.Image

    image_path = str(tmp_path / "test_image_rgb.jpg")
    PIL.Image.fromarray(np.zeros((5, 5), dtype=np.uint8)).save(image_path, format="png")
    output = pa.BufferOutputStream()
    with ParquetWriter(
        stream=output, features=Features({"image": Image()}), embed_local_files=embed_local_files
    ) as writer:
        writer.write({"image": image_path})
        writer.finalize()
    stream = pa.BufferReader(output.getvalue())
    pa_table: pa.Table = pq.read_table(stream)
    out = pa_table.to_pydict()
    if embed_local_files:
        assert isinstance(out["image"][0]["path"], str)
        with open(image_path, "rb") as f:
            assert out["image"][0]["bytes"] == f.read()
    else:
        assert out["image"][0]["path"] == image_path
        assert out["image"][0]["bytes"] is None


def test_always_nullable():
    non_nullable_schema = pa.schema([pa.field("col_1", pa.string(), nullable=False)])
    output = pa.BufferOutputStream()
    with ArrowWriter(stream=output) as writer:
        writer._build_writer(inferred_schema=non_nullable_schema)
        assert writer._schema == pa.schema([pa.field("col_1", pa.string())])
