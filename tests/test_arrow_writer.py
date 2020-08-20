from unittest import TestCase

import pyarrow as pa

from nlp.arrow_writer import ArrowWriter, TypedSequence
from nlp.features import Array2DExtensionType


class TypedSequenceTest(TestCase):
    def test_no_type(self):
        arr = pa.array(TypedSequence([1, 2, 3]))
        self.assertEqual(arr.type, pa.int64())

    def test_array_type_forbidden(self):
        with self.assertRaises(AssertionError):
            arr = pa.array(TypedSequence([1, 2, 3]), type=pa.int64())

    def test_try_type_and_type_forbidden(self):
        with self.assertRaises(AssertionError):
            arr = pa.array(TypedSequence([1, 2, 3], try_type=pa.bool_(), type=pa.int64()))

    def test_compatible_type(self):
        arr = pa.array(TypedSequence([1, 2, 3], type=pa.int32()))
        self.assertEqual(arr.type, pa.int32())

    def test_incompatible_type(self):
        with self.assertRaises((TypeError, pa.lib.ArrowInvalid)):
            arr = pa.array(TypedSequence(["foo", "bar"], type=pa.int64()))

    def test_try_compatible_type(self):
        arr = pa.array(TypedSequence([1, 2, 3], try_type=pa.int32()))
        self.assertEqual(arr.type, pa.int32())

    def test_try_incompatible_type(self):
        arr = pa.array(TypedSequence(["foo", "bar"], try_type=pa.int64()))
        self.assertEqual(arr.type, pa.string())

    def test_compatible_extension_type(self):
        arr = pa.array(TypedSequence([[[1, 2, 3]]], type=Array2DExtensionType("int64")))
        self.assertEqual(arr.type, Array2DExtensionType("int64"))

    def test_incompatible_extension_type(self):
        with self.assertRaises((TypeError, pa.lib.ArrowInvalid)):
            arr = pa.array(TypedSequence(["foo", "bar"], type=Array2DExtensionType("int64")))

    def test_try_compatible_extension_type(self):
        arr = pa.array(TypedSequence([[[1, 2, 3]]], try_type=Array2DExtensionType("int64")))
        self.assertEqual(arr.type, Array2DExtensionType("int64"))

    def test_try_incompatible_extension_type(self):
        arr = pa.array(TypedSequence(["foo", "bar"], try_type=Array2DExtensionType("int64")))
        self.assertEqual(arr.type, pa.string())
