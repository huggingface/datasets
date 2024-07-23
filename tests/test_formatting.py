import datetime
from pathlib import Path
from unittest import TestCase

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest

from datasets import Audio, Features, Image, IterableDataset
from datasets.formatting import NumpyFormatter, PandasFormatter, PythonFormatter, query_table
from datasets.formatting.formatting import (
    LazyBatch,
    LazyRow,
    NumpyArrowExtractor,
    PandasArrowExtractor,
    PythonArrowExtractor,
)
from datasets.table import InMemoryTable

from .utils import (
    require_jax,
    require_librosa,
    require_numpy1_on_windows,
    require_pil,
    require_polars,
    require_sndfile,
    require_tf,
    require_torch,
)


class AnyArray:
    def __init__(self, data) -> None:
        self.data = data

    def __array__(self) -> np.ndarray:
        return np.asarray(self.data)


def _gen_any_arrays():
    for _ in range(10):
        yield {"array": AnyArray(list(range(10)))}


@pytest.fixture
def any_arrays_dataset():
    return IterableDataset.from_generator(_gen_any_arrays)


_COL_A = [0, 1, 2]
_COL_B = ["foo", "bar", "foobar"]
_COL_C = [[[1.0, 0.0, 0.0]] * 2, [[0.0, 1.0, 0.0]] * 2, [[0.0, 0.0, 1.0]] * 2]
_COL_D = [datetime.datetime(2023, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)] * 3

_INDICES = [1, 0]

IMAGE_PATH_1 = Path(__file__).parent / "features" / "data" / "test_image_rgb.jpg"
IMAGE_PATH_2 = Path(__file__).parent / "features" / "data" / "test_image_rgba.png"
AUDIO_PATH_1 = Path(__file__).parent / "features" / "data" / "test_audio_44100.wav"


class ArrowExtractorTest(TestCase):
    def _create_dummy_table(self):
        return pa.Table.from_pydict({"a": _COL_A, "b": _COL_B, "c": _COL_C, "d": _COL_D})

    def test_python_extractor(self):
        pa_table = self._create_dummy_table()
        extractor = PythonArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertEqual(row, {"a": _COL_A[0], "b": _COL_B[0], "c": _COL_C[0], "d": _COL_D[0]})
        col = extractor.extract_column(pa_table)
        self.assertEqual(col, _COL_A)
        batch = extractor.extract_batch(pa_table)
        self.assertEqual(batch, {"a": _COL_A, "b": _COL_B, "c": _COL_C, "d": _COL_D})

    def test_numpy_extractor(self):
        pa_table = self._create_dummy_table().drop(["c", "d"])
        extractor = NumpyArrowExtractor()
        row = extractor.extract_row(pa_table)
        np.testing.assert_equal(row, {"a": _COL_A[0], "b": _COL_B[0]})
        col = extractor.extract_column(pa_table)
        np.testing.assert_equal(col, np.array(_COL_A))
        batch = extractor.extract_batch(pa_table)
        np.testing.assert_equal(batch, {"a": np.array(_COL_A), "b": np.array(_COL_B)})

    def test_numpy_extractor_nested(self):
        pa_table = self._create_dummy_table().drop(["a", "b", "d"])
        extractor = NumpyArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertEqual(row["c"][0].dtype, np.float64)
        self.assertEqual(row["c"].dtype, object)
        col = extractor.extract_column(pa_table)
        self.assertEqual(col[0][0].dtype, np.float64)
        self.assertEqual(col[0].dtype, object)
        self.assertEqual(col.dtype, object)
        batch = extractor.extract_batch(pa_table)
        self.assertEqual(batch["c"][0][0].dtype, np.float64)
        self.assertEqual(batch["c"][0].dtype, object)
        self.assertEqual(batch["c"].dtype, object)

    def test_numpy_extractor_temporal(self):
        pa_table = self._create_dummy_table().drop(["a", "b", "c"])
        extractor = NumpyArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertTrue(np.issubdtype(row["d"].dtype, np.datetime64))
        col = extractor.extract_column(pa_table)
        self.assertTrue(np.issubdtype(col[0].dtype, np.datetime64))
        self.assertTrue(np.issubdtype(col.dtype, np.datetime64))
        batch = extractor.extract_batch(pa_table)
        self.assertTrue(np.issubdtype(batch["d"][0].dtype, np.datetime64))
        self.assertTrue(np.issubdtype(batch["d"].dtype, np.datetime64))

    def test_pandas_extractor(self):
        pa_table = self._create_dummy_table()
        extractor = PandasArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertIsInstance(row, pd.DataFrame)
        pd.testing.assert_series_equal(row["a"], pd.Series(_COL_A, name="a")[:1])
        pd.testing.assert_series_equal(row["b"], pd.Series(_COL_B, name="b")[:1])
        col = extractor.extract_column(pa_table)
        pd.testing.assert_series_equal(col, pd.Series(_COL_A, name="a"))
        batch = extractor.extract_batch(pa_table)
        self.assertIsInstance(batch, pd.DataFrame)
        pd.testing.assert_series_equal(batch["a"], pd.Series(_COL_A, name="a"))
        pd.testing.assert_series_equal(batch["b"], pd.Series(_COL_B, name="b"))

    def test_pandas_extractor_nested(self):
        pa_table = self._create_dummy_table().drop(["a", "b", "d"])
        extractor = PandasArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertEqual(row["c"][0][0].dtype, np.float64)
        self.assertEqual(row["c"].dtype, object)
        col = extractor.extract_column(pa_table)
        self.assertEqual(col[0][0].dtype, np.float64)
        self.assertEqual(col[0].dtype, object)
        self.assertEqual(col.dtype, object)
        batch = extractor.extract_batch(pa_table)
        self.assertEqual(batch["c"][0][0].dtype, np.float64)
        self.assertEqual(batch["c"][0].dtype, object)
        self.assertEqual(batch["c"].dtype, object)

    def test_pandas_extractor_temporal(self):
        pa_table = self._create_dummy_table().drop(["a", "b", "c"])
        extractor = PandasArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(row["d"].dtype))
        col = extractor.extract_column(pa_table)
        self.assertTrue(isinstance(col[0], datetime.datetime))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(col.dtype))
        batch = extractor.extract_batch(pa_table)
        self.assertTrue(isinstance(batch["d"][0], datetime.datetime))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(batch["d"].dtype))

    @require_polars
    def test_polars_extractor(self):
        import polars as pl

        from datasets.formatting.polars_formatter import PolarsArrowExtractor

        pa_table = self._create_dummy_table()
        extractor = PolarsArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertIsInstance(row, pl.DataFrame)
        assert pl.Series.eq(row["a"], pl.Series("a", _COL_A)[:1]).all()
        assert pl.Series.eq(row["b"], pl.Series("b", _COL_B)[:1]).all()
        col = extractor.extract_column(pa_table)
        assert pl.Series.eq(col, pl.Series("a", _COL_A)).all()
        batch = extractor.extract_batch(pa_table)
        self.assertIsInstance(batch, pl.DataFrame)
        assert pl.Series.eq(batch["a"], pl.Series("a", _COL_A)).all()
        assert pl.Series.eq(batch["b"], pl.Series("b", _COL_B)).all()

    @require_polars
    def test_polars_nested(self):
        import polars as pl

        from datasets.formatting.polars_formatter import PolarsArrowExtractor

        pa_table = self._create_dummy_table().drop(["a", "b", "d"])
        extractor = PolarsArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertEqual(row["c"][0][0].dtype, pl.Float64)
        self.assertEqual(row["c"].dtype, pl.List(pl.List(pl.Float64)))
        col = extractor.extract_column(pa_table)
        self.assertEqual(col[0][0].dtype, pl.Float64)
        self.assertEqual(col[0].dtype, pl.List(pl.Float64))
        self.assertEqual(col.dtype, pl.List(pl.List(pl.Float64)))
        batch = extractor.extract_batch(pa_table)
        self.assertEqual(batch["c"][0][0].dtype, pl.Float64)
        self.assertEqual(batch["c"][0].dtype, pl.List(pl.Float64))
        self.assertEqual(batch["c"].dtype, pl.List(pl.List(pl.Float64)))

    @require_polars
    def test_polars_temporal(self):
        from datasets.formatting.polars_formatter import PolarsArrowExtractor

        pa_table = self._create_dummy_table().drop(["a", "b", "c"])
        extractor = PolarsArrowExtractor()
        row = extractor.extract_row(pa_table)
        self.assertTrue(row["d"].dtype.is_temporal())
        col = extractor.extract_column(pa_table)
        self.assertTrue(isinstance(col[0], datetime.datetime))
        self.assertTrue(col.dtype.is_temporal())
        batch = extractor.extract_batch(pa_table)
        self.assertTrue(isinstance(batch["d"][0], datetime.datetime))
        self.assertTrue(batch["d"].dtype.is_temporal())


class LazyDictTest(TestCase):
    def _create_dummy_table(self):
        return pa.Table.from_pydict({"a": _COL_A, "b": _COL_B, "c": _COL_C})

    def _create_dummy_formatter(self):
        return PythonFormatter(lazy=True)

    def test_lazy_dict_copy(self):
        pa_table = self._create_dummy_table()
        formatter = self._create_dummy_formatter()
        lazy_batch = formatter.format_batch(pa_table)
        lazy_batch_copy = lazy_batch.copy()
        self.assertEqual(type(lazy_batch), type(lazy_batch_copy))
        self.assertEqual(lazy_batch.items(), lazy_batch_copy.items())
        lazy_batch["d"] = [1, 2, 3]
        self.assertNotEqual(lazy_batch.items(), lazy_batch_copy.items())


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

    def test_python_formatter_lazy(self):
        pa_table = self._create_dummy_table()
        formatter = PythonFormatter(lazy=True)
        row = formatter.format_row(pa_table)
        self.assertIsInstance(row, LazyRow)
        self.assertEqual(row["a"], _COL_A[0])
        self.assertEqual(row["b"], _COL_B[0])
        self.assertEqual(row["c"], _COL_C[0])
        batch = formatter.format_batch(pa_table)
        self.assertIsInstance(batch, LazyBatch)
        self.assertEqual(batch["a"], _COL_A)
        self.assertEqual(batch["b"], _COL_B)
        self.assertEqual(batch["c"], _COL_C)

    def test_numpy_formatter(self):
        pa_table = self._create_dummy_table()
        formatter = NumpyFormatter()
        row = formatter.format_row(pa_table)
        np.testing.assert_equal(row, {"a": _COL_A[0], "b": _COL_B[0], "c": np.array(_COL_C[0])})
        col = formatter.format_column(pa_table)
        np.testing.assert_equal(col, np.array(_COL_A))
        batch = formatter.format_batch(pa_table)
        np.testing.assert_equal(batch, {"a": np.array(_COL_A), "b": np.array(_COL_B), "c": np.array(_COL_C)})
        assert batch["c"].shape == np.array(_COL_C).shape

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

    @require_pil
    def test_numpy_formatter_image(self):
        # same dimensions
        pa_table = pa.table({"image": [{"bytes": None, "path": str(IMAGE_PATH_1)}] * 2})
        formatter = NumpyFormatter(features=Features({"image": Image()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["image"].dtype, np.uint8)
        self.assertEqual(row["image"].shape, (480, 640, 3))
        col = formatter.format_column(pa_table)
        self.assertEqual(col.dtype, np.uint8)
        self.assertEqual(col.shape, (2, 480, 640, 3))
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["image"].dtype, np.uint8)
        self.assertEqual(batch["image"].shape, (2, 480, 640, 3))

        # different dimensions
        pa_table = pa.table(
            {"image": [{"bytes": None, "path": str(IMAGE_PATH_1)}, {"bytes": None, "path": str(IMAGE_PATH_2)}]}
        )
        formatter = NumpyFormatter(features=Features({"image": Image()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["image"].dtype, np.uint8)
        self.assertEqual(row["image"].shape, (480, 640, 3))
        col = formatter.format_column(pa_table)
        self.assertIsInstance(col, np.ndarray)
        self.assertEqual(col.dtype, object)
        self.assertEqual(col[0].dtype, np.uint8)
        self.assertEqual(col[0].shape, (480, 640, 3))
        batch = formatter.format_batch(pa_table)
        self.assertIsInstance(batch["image"], np.ndarray)
        self.assertEqual(batch["image"].dtype, object)
        self.assertEqual(batch["image"][0].dtype, np.uint8)
        self.assertEqual(batch["image"][0].shape, (480, 640, 3))

    @require_librosa
    @require_sndfile
    def test_numpy_formatter_audio(self):
        pa_table = pa.table({"audio": [{"bytes": None, "path": str(AUDIO_PATH_1)}]})
        formatter = NumpyFormatter(features=Features({"audio": Audio()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["audio"]["array"].dtype, np.dtype(np.float32))
        col = formatter.format_column(pa_table)
        self.assertEqual(col[0]["array"].dtype, np.float32)
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["audio"][0]["array"].dtype, np.dtype(np.float32))

    def test_pandas_formatter(self):
        pa_table = self._create_dummy_table()
        formatter = PandasFormatter()
        row = formatter.format_row(pa_table)
        self.assertIsInstance(row, pd.DataFrame)
        pd.testing.assert_series_equal(row["a"], pd.Series(_COL_A, name="a")[:1])
        pd.testing.assert_series_equal(row["b"], pd.Series(_COL_B, name="b")[:1])
        col = formatter.format_column(pa_table)
        pd.testing.assert_series_equal(col, pd.Series(_COL_A, name="a"))
        batch = formatter.format_batch(pa_table)
        self.assertIsInstance(batch, pd.DataFrame)
        pd.testing.assert_series_equal(batch["a"], pd.Series(_COL_A, name="a"))
        pd.testing.assert_series_equal(batch["b"], pd.Series(_COL_B, name="b"))

    @require_polars
    def test_polars_formatter(self):
        import polars as pl

        from datasets.formatting import PolarsFormatter

        pa_table = self._create_dummy_table()
        formatter = PolarsFormatter()
        row = formatter.format_row(pa_table)
        self.assertIsInstance(row, pl.DataFrame)
        assert pl.Series.eq(row["a"], pl.Series("a", _COL_A)[:1]).all()
        assert pl.Series.eq(row["b"], pl.Series("b", _COL_B)[:1]).all()
        col = formatter.format_column(pa_table)
        assert pl.Series.eq(col, pl.Series("a", _COL_A)).all()
        batch = formatter.format_batch(pa_table)
        self.assertIsInstance(batch, pl.DataFrame)
        assert pl.Series.eq(batch["a"], pl.Series("a", _COL_A)).all()
        assert pl.Series.eq(batch["b"], pl.Series("b", _COL_B)).all()

    @require_numpy1_on_windows
    @require_torch
    def test_torch_formatter(self):
        import torch

        from datasets.formatting import TorchFormatter

        pa_table = self._create_dummy_table()
        formatter = TorchFormatter()
        row = formatter.format_row(pa_table)
        torch.testing.assert_close(row["a"], torch.tensor(_COL_A, dtype=torch.int64)[0])
        assert row["b"] == _COL_B[0]
        torch.testing.assert_close(row["c"], torch.tensor(_COL_C, dtype=torch.float32)[0])
        col = formatter.format_column(pa_table)
        torch.testing.assert_close(col, torch.tensor(_COL_A, dtype=torch.int64))
        batch = formatter.format_batch(pa_table)
        torch.testing.assert_close(batch["a"], torch.tensor(_COL_A, dtype=torch.int64))
        assert batch["b"] == _COL_B
        torch.testing.assert_close(batch["c"], torch.tensor(_COL_C, dtype=torch.float32))
        assert batch["c"].shape == np.array(_COL_C).shape

    @require_numpy1_on_windows
    @require_torch
    def test_torch_formatter_torch_tensor_kwargs(self):
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

    @require_numpy1_on_windows
    @require_torch
    @require_pil
    def test_torch_formatter_image(self):
        import torch

        from datasets.formatting import TorchFormatter

        # same dimensions
        pa_table = pa.table({"image": [{"bytes": None, "path": str(IMAGE_PATH_1)}] * 2})
        formatter = TorchFormatter(features=Features({"image": Image()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["image"].dtype, torch.uint8)
        # torch uses CHW format contrary to numpy which uses HWC
        self.assertEqual(row["image"].shape, (3, 480, 640))
        col = formatter.format_column(pa_table)
        self.assertEqual(col.dtype, torch.uint8)
        self.assertEqual(col.shape, (2, 3, 480, 640))
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["image"].dtype, torch.uint8)
        self.assertEqual(batch["image"].shape, (2, 3, 480, 640))

        # different dimensions
        pa_table = pa.table(
            {"image": [{"bytes": None, "path": str(IMAGE_PATH_1)}, {"bytes": None, "path": str(IMAGE_PATH_2)}]}
        )
        formatter = TorchFormatter(features=Features({"image": Image()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["image"].dtype, torch.uint8)
        self.assertEqual(row["image"].shape, (3, 480, 640))
        col = formatter.format_column(pa_table)
        self.assertIsInstance(col, list)
        self.assertEqual(col[0].dtype, torch.uint8)
        self.assertEqual(col[0].shape, (3, 480, 640))
        batch = formatter.format_batch(pa_table)
        self.assertIsInstance(batch["image"], list)
        self.assertEqual(batch["image"][0].dtype, torch.uint8)
        self.assertEqual(batch["image"][0].shape, (3, 480, 640))

    @require_torch
    @require_librosa
    @require_sndfile
    def test_torch_formatter_audio(self):
        import torch

        from datasets.formatting import TorchFormatter

        pa_table = pa.table({"audio": [{"bytes": None, "path": str(AUDIO_PATH_1)}]})
        formatter = TorchFormatter(features=Features({"audio": Audio()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["audio"]["array"].dtype, torch.float32)
        col = formatter.format_column(pa_table)
        self.assertEqual(col[0]["array"].dtype, torch.float32)
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["audio"][0]["array"].dtype, torch.float32)

    @require_tf
    def test_tf_formatter(self):
        import tensorflow as tf

        from datasets.formatting import TFFormatter

        pa_table = self._create_dummy_table()
        formatter = TFFormatter()
        row = formatter.format_row(pa_table)
        tf.debugging.assert_equal(row["a"], tf.convert_to_tensor(_COL_A, dtype=tf.int64)[0])
        tf.debugging.assert_equal(row["b"], tf.convert_to_tensor(_COL_B, dtype=tf.string)[0])
        tf.debugging.assert_equal(row["c"], tf.convert_to_tensor(_COL_C, dtype=tf.float32)[0])
        col = formatter.format_column(pa_table)
        tf.debugging.assert_equal(col, tf.ragged.constant(_COL_A, dtype=tf.int64))
        batch = formatter.format_batch(pa_table)
        tf.debugging.assert_equal(batch["a"], tf.convert_to_tensor(_COL_A, dtype=tf.int64))
        tf.debugging.assert_equal(batch["b"], tf.convert_to_tensor(_COL_B, dtype=tf.string))
        self.assertIsInstance(batch["c"], tf.Tensor)
        self.assertEqual(batch["c"].dtype, tf.float32)
        tf.debugging.assert_equal(
            batch["c"].shape.as_list(), tf.convert_to_tensor(_COL_C, dtype=tf.float32).shape.as_list()
        )
        tf.debugging.assert_equal(tf.convert_to_tensor(batch["c"]), tf.convert_to_tensor(_COL_C, dtype=tf.float32))

    @require_tf
    def test_tf_formatter_tf_tensor_kwargs(self):
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

    @require_tf
    @require_pil
    def test_tf_formatter_image(self):
        import tensorflow as tf

        from datasets.formatting import TFFormatter

        # same dimensions
        pa_table = pa.table({"image": [{"bytes": None, "path": str(IMAGE_PATH_1)}] * 2})
        formatter = TFFormatter(features=Features({"image": Image()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["image"].dtype, tf.uint8)
        self.assertEqual(row["image"].shape, (480, 640, 3))
        col = formatter.format_column(pa_table)
        self.assertEqual(col.dtype, tf.uint8)
        self.assertEqual(col.shape, (2, 480, 640, 3))
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["image"][0].dtype, tf.uint8)
        self.assertEqual(batch["image"].shape, (2, 480, 640, 3))

        # different dimensions
        pa_table = pa.table(
            {"image": [{"bytes": None, "path": str(IMAGE_PATH_1)}, {"bytes": None, "path": str(IMAGE_PATH_2)}]}
        )
        formatter = TFFormatter(features=Features({"image": Image()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["image"].dtype, tf.uint8)
        self.assertEqual(row["image"].shape, (480, 640, 3))
        col = formatter.format_column(pa_table)
        self.assertIsInstance(col, list)
        self.assertEqual(col[0].dtype, tf.uint8)
        self.assertEqual(col[0].shape, (480, 640, 3))
        batch = formatter.format_batch(pa_table)
        self.assertIsInstance(batch["image"], list)
        self.assertEqual(batch["image"][0].dtype, tf.uint8)
        self.assertEqual(batch["image"][0].shape, (480, 640, 3))

    @require_tf
    @require_sndfile
    def test_tf_formatter_audio(self):
        import tensorflow as tf

        from datasets.formatting import TFFormatter

        pa_table = pa.table({"audio": [{"bytes": None, "path": str(AUDIO_PATH_1)}]})
        formatter = TFFormatter(features=Features({"audio": Audio()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["audio"]["array"].dtype, tf.float32)
        col = formatter.format_column(pa_table)
        self.assertEqual(col[0]["array"].dtype, tf.float32)
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["audio"][0]["array"].dtype, tf.float32)

    @require_jax
    def test_jax_formatter(self):
        import jax
        import jax.numpy as jnp

        from datasets.formatting import JaxFormatter

        pa_table = self._create_dummy_table()
        formatter = JaxFormatter()
        row = formatter.format_row(pa_table)
        jnp.allclose(row["a"], jnp.array(_COL_A, dtype=jnp.int64 if jax.config.jax_enable_x64 else jnp.int32)[0])
        assert row["b"] == _COL_B[0]
        jnp.allclose(row["c"], jnp.array(_COL_C, dtype=jnp.float32)[0])
        col = formatter.format_column(pa_table)
        jnp.allclose(col, jnp.array(_COL_A, dtype=jnp.int64 if jax.config.jax_enable_x64 else jnp.int32))
        batch = formatter.format_batch(pa_table)
        jnp.allclose(batch["a"], jnp.array(_COL_A, dtype=jnp.int64 if jax.config.jax_enable_x64 else jnp.int32))
        assert batch["b"] == _COL_B
        jnp.allclose(batch["c"], jnp.array(_COL_C, dtype=jnp.float32))
        assert batch["c"].shape == np.array(_COL_C).shape

    @require_jax
    def test_jax_formatter_jnp_array_kwargs(self):
        import jax.numpy as jnp

        from datasets.formatting import JaxFormatter

        pa_table = self._create_dummy_table().drop(["b"])
        formatter = JaxFormatter(dtype=jnp.float16)
        row = formatter.format_row(pa_table)
        self.assertEqual(row["c"].dtype, jnp.float16)
        col = formatter.format_column(pa_table)
        self.assertEqual(col.dtype, jnp.float16)
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["a"].dtype, jnp.float16)
        self.assertEqual(batch["c"].dtype, jnp.float16)

    @require_jax
    @require_pil
    def test_jax_formatter_image(self):
        import jax.numpy as jnp

        from datasets.formatting import JaxFormatter

        # same dimensions
        pa_table = pa.table({"image": [{"bytes": None, "path": str(IMAGE_PATH_1)}] * 2})
        formatter = JaxFormatter(features=Features({"image": Image()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["image"].dtype, jnp.uint8)
        self.assertEqual(row["image"].shape, (480, 640, 3))
        col = formatter.format_column(pa_table)
        self.assertEqual(col.dtype, jnp.uint8)
        self.assertEqual(col.shape, (2, 480, 640, 3))
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["image"].dtype, jnp.uint8)
        self.assertEqual(batch["image"].shape, (2, 480, 640, 3))

        # different dimensions
        pa_table = pa.table(
            {"image": [{"bytes": None, "path": str(IMAGE_PATH_1)}, {"bytes": None, "path": str(IMAGE_PATH_2)}]}
        )
        formatter = JaxFormatter(features=Features({"image": Image()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["image"].dtype, jnp.uint8)
        self.assertEqual(row["image"].shape, (480, 640, 3))
        col = formatter.format_column(pa_table)
        self.assertIsInstance(col, list)
        self.assertEqual(col[0].dtype, jnp.uint8)
        self.assertEqual(col[0].shape, (480, 640, 3))
        batch = formatter.format_batch(pa_table)
        self.assertIsInstance(batch["image"], list)
        self.assertEqual(batch["image"][0].dtype, jnp.uint8)
        self.assertEqual(batch["image"][0].shape, (480, 640, 3))

    @require_jax
    @require_librosa
    @require_sndfile
    def test_jax_formatter_audio(self):
        import jax.numpy as jnp

        from datasets.formatting import JaxFormatter

        pa_table = pa.table({"audio": [{"bytes": None, "path": str(AUDIO_PATH_1)}]})
        formatter = JaxFormatter(features=Features({"audio": Audio()}))
        row = formatter.format_row(pa_table)
        self.assertEqual(row["audio"]["array"].dtype, jnp.float32)
        col = formatter.format_column(pa_table)
        self.assertEqual(col[0]["array"].dtype, jnp.float32)
        batch = formatter.format_batch(pa_table)
        self.assertEqual(batch["audio"][0]["array"].dtype, jnp.float32)

    @require_jax
    def test_jax_formatter_device(self):
        import jax

        from datasets.formatting import JaxFormatter

        pa_table = self._create_dummy_table()
        device = jax.devices()[0]
        formatter = JaxFormatter(device=str(device))
        row = formatter.format_row(pa_table)
        assert row["a"].devices().pop() == device
        assert row["c"].devices().pop() == device
        col = formatter.format_column(pa_table)
        assert col.devices().pop() == device
        batch = formatter.format_batch(pa_table)
        assert batch["a"].devices().pop() == device
        assert batch["c"].devices().pop() == device


class QueryTest(TestCase):
    def _create_dummy_table(self):
        return pa.Table.from_pydict({"a": _COL_A, "b": _COL_B, "c": _COL_C})

    def _create_dummy_arrow_indices(self):
        return pa.Table.from_arrays([pa.array(_INDICES, type=pa.uint64())], names=["indices"])

    def assertTableEqual(self, first: pa.Table, second: pa.Table):
        self.assertEqual(first.schema, second.schema)
        for first_array, second_array in zip(first, second):
            self.assertEqual(first_array, second_array)
        self.assertEqual(first, second)

    def test_query_table_int(self):
        pa_table = self._create_dummy_table()
        table = InMemoryTable(pa_table)
        n = pa_table.num_rows
        # classical usage
        subtable = query_table(table, 0)
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[:1], "b": _COL_B[:1], "c": _COL_C[:1]}))
        subtable = query_table(table, 1)
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[1:2], "b": _COL_B[1:2], "c": _COL_C[1:2]}))
        subtable = query_table(table, -1)
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[-1:], "b": _COL_B[-1:], "c": _COL_C[-1:]}))
        # raise an IndexError
        with self.assertRaises(IndexError):
            query_table(table, n)
        with self.assertRaises(IndexError):
            query_table(table, -(n + 1))
        # with indices
        indices = InMemoryTable(self._create_dummy_arrow_indices())
        subtable = query_table(table, 0, indices=indices)
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": [_COL_A[_INDICES[0]]], "b": [_COL_B[_INDICES[0]]], "c": [_COL_C[_INDICES[0]]]}),
        )
        with self.assertRaises(IndexError):
            assert len(indices) < n
            query_table(table, len(indices), indices=indices)

    def test_query_table_slice(self):
        pa_table = self._create_dummy_table()
        table = InMemoryTable(pa_table)
        n = pa_table.num_rows
        # classical usage
        subtable = query_table(table, slice(0, 1))
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[:1], "b": _COL_B[:1], "c": _COL_C[:1]}))
        subtable = query_table(table, slice(1, 2))
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[1:2], "b": _COL_B[1:2], "c": _COL_C[1:2]}))
        subtable = query_table(table, slice(-2, -1))
        self.assertTableEqual(
            subtable, pa.Table.from_pydict({"a": _COL_A[-2:-1], "b": _COL_B[-2:-1], "c": _COL_C[-2:-1]})
        )
        # usage with None
        subtable = query_table(table, slice(-1, None))
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[-1:], "b": _COL_B[-1:], "c": _COL_C[-1:]}))
        subtable = query_table(table, slice(None, n + 1))
        self.assertTableEqual(
            subtable, pa.Table.from_pydict({"a": _COL_A[: n + 1], "b": _COL_B[: n + 1], "c": _COL_C[: n + 1]})
        )
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A, "b": _COL_B, "c": _COL_C}))
        subtable = query_table(table, slice(-(n + 1), None))
        self.assertTableEqual(
            subtable, pa.Table.from_pydict({"a": _COL_A[-(n + 1) :], "b": _COL_B[-(n + 1) :], "c": _COL_C[-(n + 1) :]})
        )
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A, "b": _COL_B, "c": _COL_C}))
        # usage with step
        subtable = query_table(table, slice(None, None, 2))
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[::2], "b": _COL_B[::2], "c": _COL_C[::2]}))
        # empty ouput but no errors
        subtable = query_table(table, slice(-1, 0))  # usage with both negative and positive idx
        assert len(_COL_A[-1:0]) == 0
        self.assertTableEqual(subtable, pa_table.slice(0, 0))
        subtable = query_table(table, slice(2, 1))
        assert len(_COL_A[2:1]) == 0
        self.assertTableEqual(subtable, pa_table.slice(0, 0))
        subtable = query_table(table, slice(n, n))
        assert len(_COL_A[n:n]) == 0
        self.assertTableEqual(subtable, pa_table.slice(0, 0))
        subtable = query_table(table, slice(n, n + 1))
        assert len(_COL_A[n : n + 1]) == 0
        self.assertTableEqual(subtable, pa_table.slice(0, 0))
        # it's not possible to get an error with a slice

        # with indices
        indices = InMemoryTable(self._create_dummy_arrow_indices())
        subtable = query_table(table, slice(0, 1), indices=indices)
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": [_COL_A[_INDICES[0]]], "b": [_COL_B[_INDICES[0]]], "c": [_COL_C[_INDICES[0]]]}),
        )
        subtable = query_table(table, slice(n - 1, n), indices=indices)
        assert len(indices.column(0).to_pylist()[n - 1 : n]) == 0
        self.assertTableEqual(subtable, pa_table.slice(0, 0))

    def test_query_table_range(self):
        pa_table = self._create_dummy_table()
        table = InMemoryTable(pa_table)
        n = pa_table.num_rows
        np_A, np_B, np_C = np.array(_COL_A, dtype=np.int64), np.array(_COL_B), np.array(_COL_C)
        # classical usage
        subtable = query_table(table, range(0, 1))
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": np_A[range(0, 1)], "b": np_B[range(0, 1)], "c": np_C[range(0, 1)].tolist()}),
        )
        subtable = query_table(table, range(1, 2))
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": np_A[range(1, 2)], "b": np_B[range(1, 2)], "c": np_C[range(1, 2)].tolist()}),
        )
        subtable = query_table(table, range(-2, -1))
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict(
                {"a": np_A[range(-2, -1)], "b": np_B[range(-2, -1)], "c": np_C[range(-2, -1)].tolist()}
            ),
        )
        # usage with both negative and positive idx
        subtable = query_table(table, range(-1, 0))
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": np_A[range(-1, 0)], "b": np_B[range(-1, 0)], "c": np_C[range(-1, 0)].tolist()}),
        )
        subtable = query_table(table, range(-1, n))
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": np_A[range(-1, n)], "b": np_B[range(-1, n)], "c": np_C[range(-1, n)].tolist()}),
        )
        # usage with step
        subtable = query_table(table, range(0, n, 2))
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict(
                {"a": np_A[range(0, n, 2)], "b": np_B[range(0, n, 2)], "c": np_C[range(0, n, 2)].tolist()}
            ),
        )
        subtable = query_table(table, range(0, n + 1, 2 * n))
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict(
                {
                    "a": np_A[range(0, n + 1, 2 * n)],
                    "b": np_B[range(0, n + 1, 2 * n)],
                    "c": np_C[range(0, n + 1, 2 * n)].tolist(),
                }
            ),
        )
        # empty ouput but no errors
        subtable = query_table(table, range(2, 1))
        assert len(np_A[range(2, 1)]) == 0
        self.assertTableEqual(subtable, pa.Table.from_batches([], schema=pa_table.schema))
        subtable = query_table(table, range(n, n))
        assert len(np_A[range(n, n)]) == 0
        self.assertTableEqual(subtable, pa.Table.from_batches([], schema=pa_table.schema))
        # raise an IndexError
        with self.assertRaises(IndexError):
            with self.assertRaises(IndexError):
                np_A[range(0, n + 1)]
            query_table(table, range(0, n + 1))
        with self.assertRaises(IndexError):
            with self.assertRaises(IndexError):
                np_A[range(-(n + 1), -1)]
            query_table(table, range(-(n + 1), -1))
        with self.assertRaises(IndexError):
            with self.assertRaises(IndexError):
                np_A[range(n, n + 1)]
            query_table(table, range(n, n + 1))
        # with indices
        indices = InMemoryTable(self._create_dummy_arrow_indices())
        subtable = query_table(table, range(0, 1), indices=indices)
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": [_COL_A[_INDICES[0]]], "b": [_COL_B[_INDICES[0]]], "c": [_COL_C[_INDICES[0]]]}),
        )
        with self.assertRaises(IndexError):
            assert len(indices) < n
            query_table(table, range(len(indices), len(indices) + 1), indices=indices)

    def test_query_table_str(self):
        pa_table = self._create_dummy_table()
        table = InMemoryTable(pa_table)
        subtable = query_table(table, "a")
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A}))
        with self.assertRaises(KeyError):
            query_table(table, "z")
        indices = InMemoryTable(self._create_dummy_arrow_indices())
        subtable = query_table(table, "a", indices=indices)
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": [_COL_A[i] for i in _INDICES]}))

    def test_query_table_iterable(self):
        pa_table = self._create_dummy_table()
        table = InMemoryTable(pa_table)
        n = pa_table.num_rows
        np_A, np_B, np_C = np.array(_COL_A, dtype=np.int64), np.array(_COL_B), np.array(_COL_C)
        # classical usage
        subtable = query_table(table, [0])
        self.assertTableEqual(
            subtable, pa.Table.from_pydict({"a": np_A[[0]], "b": np_B[[0]], "c": np_C[[0]].tolist()})
        )
        subtable = query_table(table, [1])
        self.assertTableEqual(
            subtable, pa.Table.from_pydict({"a": np_A[[1]], "b": np_B[[1]], "c": np_C[[1]].tolist()})
        )
        subtable = query_table(table, [-1])
        self.assertTableEqual(
            subtable, pa.Table.from_pydict({"a": np_A[[-1]], "b": np_B[[-1]], "c": np_C[[-1]].tolist()})
        )
        subtable = query_table(table, [0, -1, 1])
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": np_A[[0, -1, 1]], "b": np_B[[0, -1, 1]], "c": np_C[[0, -1, 1]].tolist()}),
        )
        # numpy iterable
        subtable = query_table(table, np.array([0, -1, 1]))
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": np_A[[0, -1, 1]], "b": np_B[[0, -1, 1]], "c": np_C[[0, -1, 1]].tolist()}),
        )
        # empty ouput but no errors
        subtable = query_table(table, [])
        assert len(np_A[[]]) == 0
        self.assertTableEqual(subtable, pa.Table.from_batches([], schema=pa_table.schema))
        # raise an IndexError
        with self.assertRaises(IndexError):
            with self.assertRaises(IndexError):
                np_A[[n]]
            query_table(table, [n])
        with self.assertRaises(IndexError):
            with self.assertRaises(IndexError):
                np_A[[-(n + 1)]]
            query_table(table, [-(n + 1)])
        # with indices
        indices = InMemoryTable(self._create_dummy_arrow_indices())
        subtable = query_table(table, [0], indices=indices)
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": [_COL_A[_INDICES[0]]], "b": [_COL_B[_INDICES[0]]], "c": [_COL_C[_INDICES[0]]]}),
        )
        with self.assertRaises(IndexError):
            assert len(indices) < n
            query_table(table, [len(indices)], indices=indices)

    def test_query_table_indexable_type(self):
        pa_table = self._create_dummy_table()
        table = InMemoryTable(pa_table)
        n = pa_table.num_rows
        # classical usage
        subtable = query_table(table, np.int64(0))
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[:1], "b": _COL_B[:1], "c": _COL_C[:1]}))
        subtable = query_table(table, np.int64(1))
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[1:2], "b": _COL_B[1:2], "c": _COL_C[1:2]}))
        subtable = query_table(table, np.int64(-1))
        self.assertTableEqual(subtable, pa.Table.from_pydict({"a": _COL_A[-1:], "b": _COL_B[-1:], "c": _COL_C[-1:]}))
        # raise an IndexError
        with self.assertRaises(IndexError):
            query_table(table, np.int64(n))
        with self.assertRaises(IndexError):
            query_table(table, np.int64(-(n + 1)))
        # with indices
        indices = InMemoryTable(self._create_dummy_arrow_indices())
        subtable = query_table(table, np.int64(0), indices=indices)
        self.assertTableEqual(
            subtable,
            pa.Table.from_pydict({"a": [_COL_A[_INDICES[0]]], "b": [_COL_B[_INDICES[0]]], "c": [_COL_C[_INDICES[0]]]}),
        )
        with self.assertRaises(IndexError):
            assert len(indices) < n
            query_table(table, np.int64(len(indices)), indices=indices)

    def test_query_table_invalid_key_type(self):
        pa_table = self._create_dummy_table()
        table = InMemoryTable(pa_table)
        with self.assertRaises(TypeError):
            query_table(table, 0.0)
        with self.assertRaises(TypeError):
            query_table(table, [0, "a"])
        with self.assertRaises(TypeError):
            query_table(table, int)
        with self.assertRaises(TypeError):

            def iter_to_inf(start=0):
                while True:
                    yield start
                    start += 1

            query_table(table, iter_to_inf())


@pytest.fixture(scope="session")
def arrow_table():
    return pa.Table.from_pydict({"col_int": [0, 1, 2], "col_float": [0.0, 1.0, 2.0]})


@require_tf
@pytest.mark.parametrize(
    "cast_schema",
    [
        None,
        [("col_int", pa.int64()), ("col_float", pa.float64())],
        [("col_int", pa.int32()), ("col_float", pa.float64())],
        [("col_int", pa.int64()), ("col_float", pa.float32())],
    ],
)
def test_tf_formatter_sets_default_dtypes(cast_schema, arrow_table):
    import tensorflow as tf

    from datasets.formatting import TFFormatter

    if cast_schema:
        arrow_table = arrow_table.cast(pa.schema(cast_schema))
    arrow_table_dict = arrow_table.to_pydict()
    list_int = arrow_table_dict["col_int"]
    list_float = arrow_table_dict["col_float"]
    formatter = TFFormatter()

    row = formatter.format_row(arrow_table)
    tf.debugging.assert_equal(row["col_int"], tf.ragged.constant(list_int, dtype=tf.int64)[0])
    tf.debugging.assert_equal(row["col_float"], tf.ragged.constant(list_float, dtype=tf.float32)[0])

    col = formatter.format_column(arrow_table)
    tf.debugging.assert_equal(col, tf.ragged.constant(list_int, dtype=tf.int64))

    batch = formatter.format_batch(arrow_table)
    tf.debugging.assert_equal(batch["col_int"], tf.ragged.constant(list_int, dtype=tf.int64))
    tf.debugging.assert_equal(batch["col_float"], tf.ragged.constant(list_float, dtype=tf.float32))


@require_numpy1_on_windows
@require_torch
@pytest.mark.parametrize(
    "cast_schema",
    [
        None,
        [("col_int", pa.int64()), ("col_float", pa.float64())],
        [("col_int", pa.int32()), ("col_float", pa.float64())],
        [("col_int", pa.int64()), ("col_float", pa.float32())],
    ],
)
def test_torch_formatter_sets_default_dtypes(cast_schema, arrow_table):
    import torch

    from datasets.formatting import TorchFormatter

    if cast_schema:
        arrow_table = arrow_table.cast(pa.schema(cast_schema))
    arrow_table_dict = arrow_table.to_pydict()
    list_int = arrow_table_dict["col_int"]
    list_float = arrow_table_dict["col_float"]
    formatter = TorchFormatter()

    row = formatter.format_row(arrow_table)
    torch.testing.assert_close(row["col_int"], torch.tensor(list_int, dtype=torch.int64)[0])
    torch.testing.assert_close(row["col_float"], torch.tensor(list_float, dtype=torch.float32)[0])

    col = formatter.format_column(arrow_table)
    torch.testing.assert_close(col, torch.tensor(list_int, dtype=torch.int64))

    batch = formatter.format_batch(arrow_table)
    torch.testing.assert_close(batch["col_int"], torch.tensor(list_int, dtype=torch.int64))
    torch.testing.assert_close(batch["col_float"], torch.tensor(list_float, dtype=torch.float32))


def test_iterable_dataset_of_arrays_format_to_arrow(any_arrays_dataset: IterableDataset):
    formatted = any_arrays_dataset.with_format("arrow")
    assert all(isinstance(example, pa.Table) for example in formatted)


def test_iterable_dataset_of_arrays_format_to_numpy(any_arrays_dataset: IterableDataset):
    formatted = any_arrays_dataset.with_format("np")
    assert all(isinstance(example["array"], np.ndarray) for example in formatted)


@require_torch
def test_iterable_dataset_of_arrays_format_to_torch(any_arrays_dataset: IterableDataset):
    import torch

    formatted = any_arrays_dataset.with_format("torch")
    assert all(isinstance(example["array"], torch.Tensor) for example in formatted)


@require_tf
def test_iterable_dataset_of_arrays_format_to_tf(any_arrays_dataset: IterableDataset):
    import tensorflow as tf

    formatted = any_arrays_dataset.with_format("tf")
    assert all(isinstance(example["array"], tf.Tensor) for example in formatted)


@require_jax
def test_iterable_dataset_of_arrays_format_to_jax(any_arrays_dataset: IterableDataset):
    import jax.numpy as jnp

    formatted = any_arrays_dataset.with_format("jax")
    assert all(isinstance(example["array"], jnp.ndarray) for example in formatted)
