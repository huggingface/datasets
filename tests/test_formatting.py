from unittest import TestCase

import numpy as np
import pandas as pd
import pyarrow as pa

from datasets.formatting.formatting import NumpyArrowExtractor, PandasArrowExtractor, PythonArrowExtractor


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
