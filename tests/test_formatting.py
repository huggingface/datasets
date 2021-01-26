from unittest import TestCase

import numpy as np
import pandas as pd
import pyarrow as pa

from datasets.formatting import NumpyFormatter, PandasFormatter, PythonFormatter
from datasets.formatting.formatting import NumpyArrowExtractor, PandasArrowExtractor, PythonArrowExtractor

from .utils import require_tf, require_torch


_COL_A = [0, 1, 2]
_COL_B = ["foo", "bar", "foobar"]
_COL_C = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


class ArrowExtractorTest(TestCase):
    def _create_dummy_table(self):
        return pa.Table.from_pydict({"a": _COL_A, "b": _COL_B, "c": _COL_C})

    def test_python_extractor(self):
        pa_table = self._create_dummy_table()
        extractor = PythonArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertEqual(row, {"a": _COL_A[0], "b": _COL_B[0], "c": _COL_C[0]})
        col = extractor.extract_column(pa_table)
        self.assertEqual(col, _COL_A)
        batch = extractor.extract_batch(pa_table)
        self.assertEqual(batch, {"a": _COL_A, "b": _COL_B, "c": _COL_C})

    def test_numpy_extractor(self):
        pa_table = self._create_dummy_table()
        extractor = NumpyArrowExtractor()
        row = extractor.extract_row(pa_table)
        np.testing.assert_equal(row, {"a": _COL_A[0], "b": _COL_B[0], "c": np.array(_COL_C[0])})
        col = extractor.extract_column(pa_table)
        np.testing.assert_equal(col, np.array(_COL_A))
        batch = extractor.extract_batch(pa_table)
        np.testing.assert_equal(batch, {"a": np.array(_COL_A), "b": np.array(_COL_B), "c": np.array(_COL_C)})

    def test_numpy_extractor_np_array_kwargs(self):
        pa_table = self._create_dummy_table().drop(["b"])
        extractor = NumpyArrowExtractor(dtype=np.float16)
        row = extractor.extract_row(pa_table)
        self.assertEqual(row["c"].dtype, np.dtype(np.float16))
        col = extractor.extract_column(pa_table)
        self.assertEqual(col.dtype, np.float16)
        batch = extractor.extract_batch(pa_table)
        self.assertEqual(batch["a"].dtype, np.dtype(np.float16))
        self.assertEqual(batch["c"].dtype, np.dtype(np.float16))

    def test_pandas_extractor(self):
        pa_table = self._create_dummy_table()
        extractor = PandasArrowExtractor()
        row = extractor.extract_row(pa_table)
        pd.testing.assert_series_equal(row["a"], pd.Series(_COL_A, name="a")[:1])
        pd.testing.assert_series_equal(row["b"], pd.Series(_COL_B, name="b")[:1])
        pd.testing.assert_series_equal(row["c"], pd.Series(_COL_C, name="c")[:1])
        col = extractor.extract_column(pa_table)
        pd.testing.assert_series_equal(col, pd.Series(_COL_A, name="a"))
        batch = extractor.extract_batch(pa_table)
        pd.testing.assert_series_equal(batch["a"], pd.Series(_COL_A, name="a"))
        pd.testing.assert_series_equal(batch["b"], pd.Series(_COL_B, name="b"))
        pd.testing.assert_series_equal(batch["c"], pd.Series(_COL_C, name="c"))


class FormatterTest(TestCase):
    def _create_dummy_table(self):
        return pa.Table.from_pydict({"a": _COL_A, "b": _COL_B, "c": _COL_C})

    def test_python_formatter(self):
        pa_table = self._create_dummy_table()
        formatter = PythonFormatter()
        row = formatter.format_row(pa_table)
        self.assertEqual(row, {"a": _COL_A[0], "b": _COL_B[0], "c": _COL_C[0]})
        col = formatter.format_column(pa_table)
        self.assertEqual(col, _COL_A)
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch, {"a": _COL_A, "b": _COL_B, "c": _COL_C})

    def test_numpy_formatter(self):
        pa_table = self._create_dummy_table()
        formatter = NumpyFormatter()
        row = formatter.format_row(pa_table)
        np.testing.assert_equal(row, {"a": _COL_A[0], "b": _COL_B[0], "c": np.array(_COL_C[0])})
        col = formatter.format_column(pa_table)
        np.testing.assert_equal(col, np.array(_COL_A))
        batch = formatter.format_batch(pa_table)
        np.testing.assert_equal(batch, {"a": np.array(_COL_A), "b": np.array(_COL_B), "c": np.array(_COL_C)})

    def test_numpy_formatter_np_array_kwargs(self):
        pa_table = self._create_dummy_table().drop(["b"])
        formatter = NumpyFormatter(dtype=np.float16)
        row = formatter.format_row(pa_table)
        self.assertEqual(row["c"].dtype, np.dtype(np.float16))
        col = formatter.format_column(pa_table)
        self.assertEqual(col.dtype, np.float16)
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["a"].dtype, np.dtype(np.float16))
        self.assertEqual(batch["c"].dtype, np.dtype(np.float16))

    def test_pandas_formatter(self):
        pa_table = self._create_dummy_table()
        formatter = PandasFormatter()
        row = formatter.format_row(pa_table)
        pd.testing.assert_series_equal(row["a"], pd.Series(_COL_A, name="a")[:1])
        pd.testing.assert_series_equal(row["b"], pd.Series(_COL_B, name="b")[:1])
        pd.testing.assert_series_equal(row["c"], pd.Series(_COL_C, name="c")[:1])
        col = formatter.format_column(pa_table)
        pd.testing.assert_series_equal(col, pd.Series(_COL_A, name="a"))
        batch = formatter.format_batch(pa_table)
        pd.testing.assert_series_equal(batch["a"], pd.Series(_COL_A, name="a"))
        pd.testing.assert_series_equal(batch["b"], pd.Series(_COL_B, name="b"))
        pd.testing.assert_series_equal(batch["c"], pd.Series(_COL_C, name="c"))

    @require_torch
    def test_torch_formatter(self):
        import torch

        from datasets.formatting import TorchFormatter

        pa_table = self._create_dummy_table().drop(["b"])
        formatter = TorchFormatter()
        row = formatter.format_row(pa_table)
        torch.testing.assert_allclose(row["a"], torch.tensor(_COL_A, dtype=torch.int64)[0])
        torch.testing.assert_allclose(row["c"], torch.tensor(_COL_C, dtype=torch.float64)[0])
        col = formatter.format_column(pa_table)
        torch.testing.assert_allclose(col, torch.tensor(_COL_A, dtype=torch.int64))
        batch = formatter.format_batch(pa_table)
        torch.testing.assert_allclose(batch["a"], torch.tensor(_COL_A, dtype=torch.int64))
        torch.testing.assert_allclose(batch["c"], torch.tensor(_COL_C, dtype=torch.float64))

    @require_torch
    def test_torch_formatter_np_array_kwargs(self):
        import torch

        from datasets.formatting import TorchFormatter

        pa_table = self._create_dummy_table().drop(["b"])
        formatter = TorchFormatter(dtype=torch.float16)
        row = formatter.format_row(pa_table)
        self.assertEqual(row["c"].dtype, torch.float16)
        col = formatter.format_column(pa_table)
        self.assertEqual(col.dtype, torch.float16)
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["a"].dtype, torch.float16)
        self.assertEqual(batch["c"].dtype, torch.float16)

    @require_tf
    def test_tf_formatter(self):
        import tensorflow as tf

        from datasets.formatting import TFFormatter

        pa_table = self._create_dummy_table()
        formatter = TFFormatter()
        row = formatter.format_row(pa_table)
        tf.debugging.assert_equal(row["a"], tf.ragged.constant(_COL_A, dtype=tf.int64)[0])
        tf.debugging.assert_equal(row["b"], tf.ragged.constant(_COL_B, dtype=tf.string)[0])
        tf.debugging.assert_equal(row["c"], tf.ragged.constant(_COL_C, dtype=tf.float64)[0])
        col = formatter.format_column(pa_table)
        tf.debugging.assert_equal(col, tf.ragged.constant(_COL_A, dtype=tf.int64))
        batch = formatter.format_batch(pa_table)
        tf.debugging.assert_equal(batch["a"], tf.ragged.constant(_COL_A, dtype=tf.int64))
        tf.debugging.assert_equal(batch["b"], tf.ragged.constant(_COL_B, dtype=tf.string))
        self.assertIsInstance(batch["c"], tf.RaggedTensor)
        self.assertEqual(batch["c"].dtype, tf.float64)
        tf.debugging.assert_equal(
            batch["c"].bounding_shape(), tf.ragged.constant(_COL_C, dtype=tf.float64).bounding_shape()
        )
        tf.debugging.assert_equal(batch["c"].flat_values, tf.ragged.constant(_COL_C, dtype=tf.float64).flat_values)

    @require_tf
    def test_tf_formatter_np_array_kwargs(self):
        import tensorflow as tf

        from datasets.formatting import TFFormatter

        pa_table = self._create_dummy_table().drop(["b"])
        formatter = TFFormatter(dtype=tf.float16)
        row = formatter.format_row(pa_table)
        self.assertEqual(row["c"].dtype, tf.float16)
        col = formatter.format_column(pa_table)
        self.assertEqual(col.dtype, tf.float16)
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["a"].dtype, tf.float16)
        self.assertEqual(batch["c"].dtype, tf.float16)
