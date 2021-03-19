import os
import tempfile
from unittest import TestCase

import pyarrow as pa
import pytest
from packaging import version

from datasets.arrow_writer import ArrowWriter, OptimizedTypedSequence, TypedSequence
from datasets.features import Array2DExtensionType


class TypedSequenceTest(TestCase):
    def test_no_type(self):
        arr = pa.array(TypedSequence([1, 2, 3]))
        self.assertEqual(arr.type, pa.int64())

    def test_array_type_forbidden(self):
        with self.assertRaises(AssertionError):
            _ = pa.array(TypedSequence([1, 2, 3]), type=pa.int64())

    def test_try_type_and_type_forbidden(self):
        with self.assertRaises(AssertionError):
            _ = pa.array(TypedSequence([1, 2, 3], try_type=pa.bool_(), type=pa.int64()))

    def test_compatible_type(self):
        arr = pa.array(TypedSequence([1, 2, 3], type=pa.int32()))
        self.assertEqual(arr.type, pa.int32())

    def test_incompatible_type(self):
        with self.assertRaises((TypeError, pa.lib.ArrowInvalid)):
            _ = pa.array(TypedSequence(["foo", "bar"], type=pa.int64()))

    def test_try_compatible_type(self):
        arr = pa.array(TypedSequence([1, 2, 3], try_type=pa.int32()))
        self.assertEqual(arr.type, pa.int32())

    def test_try_incompatible_type(self):
        arr = pa.array(TypedSequence(["foo", "bar"], try_type=pa.int64()))
        self.assertEqual(arr.type, pa.string())

    def test_compatible_extension_type(self):
        arr = pa.array(TypedSequence([[[1, 2, 3]]], type=Array2DExtensionType((1, 3), "int64")))
        self.assertEqual(arr.type, Array2DExtensionType((1, 3), "int64"))

    def test_incompatible_extension_type(self):
        with self.assertRaises((TypeError, pa.lib.ArrowInvalid)):
            _ = pa.array(TypedSequence(["foo", "bar"], type=Array2DExtensionType((1, 3), "int64")))

    def test_try_compatible_extension_type(self):
        arr = pa.array(TypedSequence([[[1, 2, 3]]], try_type=Array2DExtensionType((1, 3), "int64")))
        self.assertEqual(arr.type, Array2DExtensionType((1, 3), "int64"))

    def test_try_incompatible_extension_type(self):
        arr = pa.array(TypedSequence(["foo", "bar"], try_type=Array2DExtensionType((1, 3), "int64")))
        self.assertEqual(arr.type, pa.string())

    def test_catch_overflow(self):
        if version.parse(pa.__version__) < version.parse("2.0.0"):
            with self.assertRaises(OverflowError):
                _ = pa.array(TypedSequence([["x" * 1024]] * ((2 << 20) + 1)))  # ListArray with a bit more than 2GB


class ArrowWriterTest(TestCase):
    def _check_output(self, output):
        mmap = pa.BufferReader(output) if isinstance(output, pa.Buffer) else pa.memory_map(output)
        f = pa.ipc.open_stream(mmap)
        pa_table: pa.Table = f.read_all()
        self.assertDictEqual(pa_table.to_pydict(), {"col_1": ["foo", "bar"], "col_2": [1, 2]})
        del pa_table

    def test_write_no_schema(self):
        output = pa.BufferOutputStream()
        with ArrowWriter(stream=output) as writer:
            writer.write({"col_1": "foo", "col_2": 1})
            writer.write({"col_1": "bar", "col_2": 2})
            num_examples, num_bytes = writer.finalize()
        self.assertEqual(num_examples, 2)
        self.assertGreater(num_bytes, 0)
        fields = {"col_1": pa.string(), "col_2": pa.int64()}
        self.assertEqual(writer._schema, pa.schema(fields, metadata=writer._schema.metadata))
        self._check_output(output.getvalue())

    def test_write_schema(self):
        fields = {"col_1": pa.string(), "col_2": pa.int64()}
        output = pa.BufferOutputStream()
        with ArrowWriter(stream=output, schema=pa.schema(fields)) as writer:
            writer.write({"col_1": "foo", "col_2": 1})
            writer.write({"col_1": "bar", "col_2": 2})
            num_examples, num_bytes = writer.finalize()
        self.assertEqual(num_examples, 2)
        self.assertGreater(num_bytes, 0)
        self.assertEqual(writer._schema, pa.schema(fields, metadata=writer._schema.metadata))
        self._check_output(output.getvalue())

    def test_write_batch_no_schema(self):
        output = pa.BufferOutputStream()
        with ArrowWriter(stream=output) as writer:
            writer.write_batch({"col_1": ["foo", "bar"], "col_2": [1, 2]})
            num_examples, num_bytes = writer.finalize()
        self.assertEqual(num_examples, 2)
        self.assertGreater(num_bytes, 0)
        fields = {"col_1": pa.string(), "col_2": pa.int64()}
        self.assertEqual(writer._schema, pa.schema(fields, metadata=writer._schema.metadata))
        self._check_output(output.getvalue())

    def test_write_batch_schema(self):
        fields = {"col_1": pa.string(), "col_2": pa.int64()}
        output = pa.BufferOutputStream()
        with ArrowWriter(stream=output, schema=pa.schema(fields)) as writer:
            writer.write_batch({"col_1": ["foo", "bar"], "col_2": [1, 2]})
            num_examples, num_bytes = writer.finalize()
        self.assertEqual(num_examples, 2)
        self.assertGreater(num_bytes, 0)
        self.assertEqual(writer._schema, pa.schema(fields, metadata=writer._schema.metadata))
        self._check_output(output.getvalue())

    def test_write_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            fields = {"col_1": pa.string(), "col_2": pa.int64()}
            output = os.path.join(tmp_dir, "test.arrow")
            with ArrowWriter(path=output, schema=pa.schema(fields)) as writer:
                writer.write_batch({"col_1": ["foo", "bar"], "col_2": [1, 2]})
                num_examples, num_bytes = writer.finalize()
            self.assertEqual(num_examples, 2)
            self.assertGreater(num_bytes, 0)
            self.assertEqual(writer._schema, pa.schema(fields, metadata=writer._schema.metadata))
            self._check_output(output)


def get_base_dtype(arr_type):
    if pa.types.is_list(arr_type):
        return get_base_dtype(arr_type.value_type)
    else:
        return arr_type


@pytest.mark.parametrize("optimized_int_type, expected_dtype", [(None, pa.int64()), (pa.int32(), pa.int32())])
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
    arr = pa.array(OptimizedTypedSequence(sequence, col=col))
    assert get_base_dtype(arr.type) == expected_dtype


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
