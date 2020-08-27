import os
import pickle
import tempfile
from unittest import TestCase

import numpy as np
import pandas as pd
import pyarrow as pa

from nlp import concatenate_datasets
from nlp.arrow_dataset import Dataset
from nlp.features import ClassLabel, Features, Sequence, Value
from nlp.info import DatasetInfo

from .utils import require_tf, require_torch


class BaseDatasetTest(TestCase):
    def _create_dummy_dataset(self, multiple_columns=False):
        if multiple_columns:
            data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
            dset = Dataset.from_dict(data)
        else:
            dset = Dataset.from_dict({"filename": ["my_name-train" + "_" + str(x) for x in np.arange(30).tolist()]})
        return dset

    def test_dummy_dataset(self):
        dset = self._create_dummy_dataset()
        self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
        self.assertEqual(dset[0]["filename"], "my_name-train_0")
        self.assertEqual(dset["filename"][0], "my_name-train_0")

        dset = self._create_dummy_dataset(multiple_columns=True)
        self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))
        self.assertEqual(dset[0]["col_1"], 3)
        self.assertEqual(dset["col_1"][0], 3)

    def test_dummy_dataset_pickle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "dset.pt")

            dset = self._create_dummy_dataset().select(range(10))

            with open(tmp_file, "wb") as f:
                pickle.dump(dset, f)

            with open(tmp_file, "rb") as f:
                dset = pickle.load(f)

        self.assertEqual(len(dset), 10)
        self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
        self.assertEqual(dset[0]["filename"], "my_name-train_0")
        self.assertEqual(dset["filename"][0], "my_name-train_0")

    def test_dummy_dataset_pickle_memory_mapped(self):
        class Unpicklable:
            def __getstate__(self):
                raise pickle.PicklingError()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "dset.pt")

            dset = (
                self._create_dummy_dataset().map(cache_file_name=os.path.join(tmp_dir, "test.arrow")).select(range(10))
            )
            dset._data = Unpicklable()

            with open(tmp_file, "wb") as f:
                pickle.dump(dset, f)

            with open(tmp_file, "rb") as f:
                dset = pickle.load(f)

            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertEqual(dset[0]["filename"], "my_name-train_0")
            self.assertEqual(dset["filename"][0], "my_name-train_0")

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "dset.pt")

            dset = (
                self._create_dummy_dataset()
                .map(cache_file_name=os.path.join(tmp_dir, "test.arrow"))
                .select(range(10), indices_cache_file_name=os.path.join(tmp_dir, "ind.arrow"))
            )
            dset._data = Unpicklable()
            dset._indices = Unpicklable()

            with open(tmp_file, "wb") as f:
                pickle.dump(dset, f)

            with open(tmp_file, "rb") as f:
                dset = pickle.load(f)

            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertEqual(dset[0]["filename"], "my_name-train_0")
            self.assertEqual(dset["filename"][0], "my_name-train_0")

    def test_from_pandas(self):
        data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
        df = pd.DataFrame.from_dict(data)
        dset = Dataset.from_pandas(df)
        self.assertListEqual(dset["col_1"], data["col_1"])
        self.assertListEqual(dset["col_2"], data["col_2"])
        self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
        self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("string")})
        dset = Dataset.from_pandas(df, features=features)
        self.assertListEqual(dset["col_1"], data["col_1"])
        self.assertListEqual(dset["col_2"], data["col_2"])
        self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
        self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("string")})
        dset = Dataset.from_pandas(df, features=features, info=DatasetInfo(features=features))
        self.assertListEqual(dset["col_1"], data["col_1"])
        self.assertListEqual(dset["col_2"], data["col_2"])
        self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
        self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("string"), "col_2": Value("string")})
        self.assertRaises(pa.ArrowTypeError, Dataset.from_pandas, df, features=features)

    def test_from_dict(self):
        data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
        dset = Dataset.from_dict(data)
        self.assertListEqual(dset["col_1"], data["col_1"])
        self.assertListEqual(dset["col_2"], data["col_2"])
        self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
        self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("string")})
        dset = Dataset.from_dict(data, features=features)
        self.assertListEqual(dset["col_1"], data["col_1"])
        self.assertListEqual(dset["col_2"], data["col_2"])
        self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
        self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("string")})
        dset = Dataset.from_dict(data, features=features, info=DatasetInfo(features=features))
        self.assertListEqual(dset["col_1"], data["col_1"])
        self.assertListEqual(dset["col_2"], data["col_2"])
        self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
        self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("string"), "col_2": Value("string")})
        self.assertRaises(pa.ArrowTypeError, Dataset.from_dict, data, features=features)

    def test_set_format_numpy_multiple_columns(self):
        dset = self._create_dummy_dataset(multiple_columns=True)
        dset.set_format(type="numpy", columns=["col_1"])
        self.assertEqual(len(dset[0]), 1)
        self.assertIsInstance(dset[0]["col_1"], np.ndarray)
        self.assertListEqual(list(dset[0]["col_1"].shape), [])
        self.assertEqual(dset[0]["col_1"].item(), 3)
        self.assertIsInstance(dset["col_1"], np.ndarray)
        self.assertListEqual(list(dset["col_1"].shape), [4])
        np.testing.assert_array_equal(dset["col_1"], np.array([3, 2, 1, 0]))

        dset.reset_format()
        with dset.formatted_as(type="numpy", columns=["col_1"]):
            self.assertEqual(len(dset[0]), 1)
            self.assertIsInstance(dset[0]["col_1"], np.ndarray)
            self.assertListEqual(list(dset[0]["col_1"].shape), [])
            self.assertEqual(dset[0]["col_1"].item(), 3)
            self.assertIsInstance(dset["col_1"], np.ndarray)
            self.assertListEqual(list(dset["col_1"].shape), [4])
            np.testing.assert_array_equal(dset["col_1"], np.array([3, 2, 1, 0]))

        self.assertEqual(dset.format["type"], None)
        self.assertEqual(dset.format["format_kwargs"], {})
        self.assertEqual(dset.format["columns"], dset.column_names)
        self.assertEqual(dset.format["output_all_columns"], False)

        dset.set_format(type="numpy", columns=["col_1"], output_all_columns=True)
        self.assertEqual(len(dset[0]), 2)
        self.assertIsInstance(dset[0]["col_2"], str)
        self.assertEqual(dset[0]["col_2"], "a")

        dset.set_format(type="numpy", columns=["col_1", "col_2"])
        self.assertEqual(len(dset[0]), 2)
        self.assertEqual(dset[0]["col_2"].item(), "a")

    @require_torch
    def test_set_format_torch(self):
        import torch

        dset = self._create_dummy_dataset(multiple_columns=True)
        dset.set_format(type="torch", columns=["col_1"])
        self.assertEqual(len(dset[0]), 1)
        self.assertIsInstance(dset[0]["col_1"], torch.Tensor)
        self.assertIsInstance(dset["col_1"], torch.Tensor)
        self.assertListEqual(list(dset[0]["col_1"].shape), [])
        self.assertEqual(dset[0]["col_1"].item(), 3)

        dset.set_format(type="torch", columns=["col_1"], output_all_columns=True)
        self.assertEqual(len(dset[0]), 2)
        self.assertIsInstance(dset[0]["col_2"], str)
        self.assertEqual(dset[0]["col_2"], "a")

        dset.set_format(type="torch", columns=["col_1", "col_2"])
        with self.assertRaises(TypeError):
            dset[0]

    @require_tf
    def test_set_format_tf(self):
        import tensorflow as tf

        dset = self._create_dummy_dataset(multiple_columns=True)
        dset.set_format(type="tensorflow", columns=["col_1"])
        self.assertEqual(len(dset[0]), 1)
        self.assertIsInstance(dset[0]["col_1"], tf.Tensor)
        self.assertListEqual(list(dset[0]["col_1"].shape), [])
        self.assertEqual(dset[0]["col_1"].numpy().item(), 3)

        dset.set_format(type="tensorflow", columns=["col_1"], output_all_columns=True)
        self.assertEqual(len(dset[0]), 2)
        self.assertIsInstance(dset[0]["col_2"], str)
        self.assertEqual(dset[0]["col_2"], "a")

        dset.set_format(type="tensorflow", columns=["col_1", "col_2"])
        self.assertEqual(len(dset[0]), 2)
        self.assertEqual(dset[0]["col_2"].numpy().decode("utf-8"), "a")

    def test_set_format_pandas(self):
        dset = self._create_dummy_dataset(multiple_columns=True)
        dset.set_format(type="pandas", columns=["col_1"])
        self.assertEqual(len(dset[0].columns), 1)
        self.assertIsInstance(dset[0], pd.DataFrame)
        self.assertListEqual(list(dset[0].shape), [1, 1])
        self.assertEqual(dset[0]["col_1"].item(), 3)

        dset.set_format(type="pandas", columns=["col_1", "col_2"])
        self.assertEqual(len(dset[0].columns), 2)
        self.assertEqual(dset[0]["col_2"].item(), "a")

    def test_cast_(self):
        dset = self._create_dummy_dataset(multiple_columns=True)
        features = dset.features
        features["col_1"] = Value("float64")
        dset.cast_(features)
        self.assertEqual(dset.num_columns, 2)
        self.assertEqual(dset.features["col_1"], Value("float64"))
        self.assertIsInstance(dset[0]["col_1"], float)

    def test_remove_columns_(self):
        dset = self._create_dummy_dataset(multiple_columns=True)
        dset.remove_columns_(column_names="col_1")
        self.assertEqual(dset.num_columns, 1)
        self.assertListEqual(list(dset.column_names), ["col_2"])

        dset = self._create_dummy_dataset(multiple_columns=True)
        dset.remove_columns_(column_names=["col_1", "col_2"])
        self.assertEqual(dset.num_columns, 0)

    def test_rename_column_(self):
        dset = self._create_dummy_dataset(multiple_columns=True)
        dset.rename_column_(original_column_name="col_1", new_column_name="new_name")
        self.assertEqual(dset.num_columns, 2)
        self.assertListEqual(list(dset.column_names), ["new_name", "col_2"])

    def test_concatenate_from_memory(self):
        data1, data2, data3 = {"id": [0, 1, 2]}, {"id": [3, 4, 5]}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        dset1, dset2, dset3 = (
            Dataset.from_dict(data1, info=info1),
            Dataset.from_dict(data2, info=info2),
            Dataset.from_dict(data3),
        )

        dset_concat = concatenate_datasets([dset1, dset2, dset3])
        self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
        self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
        self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(len(dset_concat._data_files), 0)
        self.assertEqual(len(dset_concat._indices_data_files), 0)
        self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")

    def test_concatenate_from_disk(self):
        data1, data2, data3 = {"id": [0, 1, 2]}, {"id": [3, 4, 5]}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1).map(cache_file_name=os.path.join(tmp_dir, "d1.arrow")),
                Dataset.from_dict(data2, info=info2).map(cache_file_name=os.path.join(tmp_dir, "d2.arrow")),
                Dataset.from_dict(data3),
            )
            with self.assertRaises(ValueError):
                dset_concat = concatenate_datasets([dset1, dset2, dset3])

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1).map(cache_file_name=os.path.join(tmp_dir, "d1.arrow")),
                Dataset.from_dict(data2, info=info2).map(cache_file_name=os.path.join(tmp_dir, "d2.arrow")),
                Dataset.from_dict(data3).map(cache_file_name=os.path.join(tmp_dir, "d3.arrow")),
            )
            dset_concat = concatenate_datasets([dset1, dset2, dset3])
            self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
            self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
            self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
            self.assertEqual(len(dset_concat._data_files), 3)
            self.assertEqual(len(dset_concat._indices_data_files), 0)
            self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")

    def test_concatenate_with_indices(self):
        data1, data2, data3 = {"id": [0, 1, 2] * 2}, {"id": [3, 4, 5] * 2}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        dset1, dset2, dset3 = (
            Dataset.from_dict(data1, info=info1).select([0, 1, 2]),
            Dataset.from_dict(data2, info=info2).select([0, 1, 2]),
            Dataset.from_dict(data3),
        )

        dset_concat = concatenate_datasets([dset1, dset2, dset3])
        self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
        self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
        self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(len(dset_concat._data_files), 0)
        self.assertEqual(len(dset_concat._indices_data_files), 0)
        self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1).select(
                    [0, 1, 2], indices_cache_file_name=os.path.join(tmp_dir, "i.arrow")
                ),
                Dataset.from_dict(data2, info=info2).select([0, 1, 2]),
                Dataset.from_dict(data3),
            )
            with self.assertRaises(ValueError):
                dset_concat = concatenate_datasets([dset1, dset2, dset3])

    def test_concatenate_with_indices_from_disk(self):
        data1, data2, data3 = {"id": [0, 1, 2] * 2}, {"id": [3, 4, 5] * 2}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1).select(
                    [0, 1, 2], indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow")
                ),
                Dataset.from_dict(data2, info=info2).select(
                    [0, 1, 2], indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow")
                ),
                Dataset.from_dict(data3).select([0, 1], indices_cache_file_name=os.path.join(tmp_dir, "i3.arrow")),
            )

            dset_concat = concatenate_datasets([dset1, dset2, dset3])
            self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
            self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
            self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
            self.assertEqual(len(dset_concat._data_files), 0)
            self.assertEqual(len(dset_concat._indices_data_files), 3)
            self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")

    def test_flatten(self):
        dset = Dataset.from_dict(
            {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10},
            features=Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")}),
        )
        dset.flatten_()
        self.assertListEqual(dset.column_names, ["a.b.c", "foo"])
        self.assertListEqual(list(dset.features.keys()), ["a.b.c", "foo"])
        self.assertDictEqual(dset.features, Features({"a.b.c": Sequence(Value("string")), "foo": Value("int64")}))

    def test_map_not_cached(self):
        dset = self._create_dummy_dataset()

        self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
        dset_test = dset.map(
            lambda x: {"name": x["filename"][:-2], "id": int(x["filename"][-1])}, cache_file_name=None
        )
        self.assertEqual(len(dset_test), 30)
        self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
        self.assertDictEqual(
            dset_test.features,
            Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
        )

        self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
        dset_test = dset.map(lambda x: None, cache_file_name=None)
        self.assertEqual(len(dset_test), 30)
        self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
        self.assertDictEqual(
            dset_test.features,
            Features({"filename": Value("string")}),
        )

    def test_map_cached(self):
        dset = self._create_dummy_dataset()
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            dset_test = dset.map(
                lambda x: {"name": x["filename"][:-2], "id": int(x["filename"][-1])}, cache_file_name=tmp_file
            )
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test.features,
                Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
            )

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_test_with_indices = dset.map(
                lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True, cache_file_name=tmp_file
            )
            self.assertEqual(len(dset_test_with_indices), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test_with_indices.features,
                Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
            )

        with tempfile.TemporaryDirectory() as tmp_dir:

            def func(x, i):
                if i == 4:
                    raise KeyboardInterrupt()
                return {"name": x["filename"][:-2], "id": i}

            tmp_file = os.path.join(tmp_dir, "test.arrow")
            self.assertRaises(
                KeyboardInterrupt,
                dset.map,
                function=func,
                with_indices=True,
                cache_file_name=tmp_file,
                writer_batch_size=2,
            )
            self.assertFalse(os.path.exists(tmp_file))
            dset_test_with_indices = dset.map(
                lambda x, i: {"name": x["filename"][:-2], "id": i},
                with_indices=True,
                cache_file_name=tmp_file,
                writer_batch_size=2,
            )
            self.assertTrue(os.path.exists(tmp_file))
            self.assertEqual(len(dset_test_with_indices), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test_with_indices.features,
                Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
            )

    def test_new_features(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            features = Features({"filename": Value("string"), "label": ClassLabel(names=["positive", "negative"])})
            dset_test_with_indices = dset.map(
                lambda x, i: {"label": i % 2}, with_indices=True, cache_file_name=tmp_file, features=features
            )
            self.assertEqual(len(dset_test_with_indices), 30)
            self.assertDictEqual(
                dset_test_with_indices.features,
                features,
            )

    def test_map_batched(self):
        dset = self._create_dummy_dataset()

        def map_batched(example):
            return {"filename_new": [x + "_extension" for x in example["filename"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_test_batched = dset.map(map_batched, batched=True, cache_file_name=tmp_file)
            self.assertEqual(len(dset_test_batched), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test_batched.features, Features({"filename": Value("string"), "filename_new": Value("string")})
            )

        with tempfile.TemporaryDirectory() as tmp_dir:
            with dset.formatted_as("numpy", columns=["filename"]):
                tmp_file = os.path.join(tmp_dir, "test.arrow")
                dset_test_batched = dset.map(map_batched, batched=True, cache_file_name=tmp_file)
                self.assertEqual(len(dset_test_batched), 30)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertDictEqual(
                    dset_test_batched.features,
                    Features({"filename": Value("string"), "filename_new": Value("string")}),
                )

        def map_batched_with_indices(example, idx):
            return {"filename_new": [x + "_extension_" + str(idx) for x in example["filename"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_test_with_indices_batched = dset.map(
                map_batched_with_indices, batched=True, with_indices=True, cache_file_name=tmp_file
            )
            self.assertEqual(len(dset_test_with_indices_batched), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test_with_indices_batched.features,
                Features({"filename": Value("string"), "filename_new": Value("string")}),
            )

    @require_torch
    def test_map_torch(self):
        import torch

        dset = self._create_dummy_dataset()

        def func(example):
            return {"tensor": torch.Tensor([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_test = dset.map(func, cache_file_name=tmp_file)
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(
                dset_test.features, Features({"filename": Value("string"), "tensor": Sequence(Value("float64"))})
            )
            self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])

    @require_tf
    def test_map_tf(self):
        import tensorflow as tf

        dset = self._create_dummy_dataset()

        def func(example):
            return {"tensor": tf.constant([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_test = dset.map(func, cache_file_name=tmp_file)
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(
                dset_test.features, Features({"filename": Value("string"), "tensor": Sequence(Value("float64"))})
            )
            self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])

    def test_map_numpy(self):
        dset = self._create_dummy_dataset()

        def func(example):
            return {"tensor": np.array([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_test = dset.map(func, cache_file_name=tmp_file)
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(
                dset_test.features, Features({"filename": Value("string"), "tensor": Sequence(Value("float64"))})
            )
            self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])

    def test_map_remove_colums(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.map(
                lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True, cache_file_name=tmp_file
            )
            self.assertTrue("id" in dset[0])
            self.assertDictEqual(
                dset.features, Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")})
            )

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.map(lambda x: x, remove_columns=["id"], cache_file_name=tmp_file)
            self.assertTrue("id" not in dset[0])
            self.assertDictEqual(dset.features, Features({"filename": Value("string"), "name": Value("string")}))

    def test_filter(self):
        dset = self._create_dummy_dataset()
        # keep only first five examples

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_filter_first_five = dset.filter(lambda x, i: i < 5, with_indices=True, cache_file_name=tmp_file)
            self.assertEqual(len(dset_filter_first_five), 5)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_filter_first_five.features, Features({"filename": Value("string")}))

        # filter filenames with even id at the end
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_filter_even_num = dset.filter(lambda x: (int(x["filename"][-1]) % 2 == 0), cache_file_name=tmp_file)
            self.assertEqual(len(dset_filter_even_num), 15)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_filter_even_num.features, Features({"filename": Value("string")}))

    def test_keep_features_after_transform_specified(self):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )
        dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            inverted_dset = dset.map(invert_labels, cache_file_name=tmp_file, features=features)
            self.assertEqual(inverted_dset.features.type, features.type)
            self.assertDictEqual(inverted_dset.features, features)

    def test_keep_features_after_transform_unspecified(self):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )
        dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            inverted_dset = dset.map(invert_labels, cache_file_name=tmp_file)
            self.assertEqual(inverted_dset.features.type, features.type)
            self.assertDictEqual(inverted_dset.features, features)

    def test_keep_features_after_transform_from_file(self):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )
        dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset.map(invert_labels, cache_file_name=tmp_file)
            inverted_dset = Dataset.from_file(tmp_file)
            self.assertEqual(inverted_dset.features.type, features.type)
            self.assertDictEqual(inverted_dset.features, features)

    def test_keep_features_after_transform_in_memory(self):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )
        dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        inverted_dset = dset.map(invert_labels, keep_in_memory=True)
        self.assertEqual(inverted_dset.features.type, features.type)
        self.assertDictEqual(inverted_dset.features, features)

    def test_keep_features_after_loading_from_cache(self):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )
        dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            inverted_dset = dset.map(invert_labels, cache_file_name=tmp_file)
            inverted_dset = dset.map(invert_labels, cache_file_name=tmp_file)
            self.assertGreater(len(inverted_dset.cache_files), 0)
            self.assertEqual(inverted_dset.features.type, features.type)
            self.assertDictEqual(inverted_dset.features, features)

    def test_keep_features_with_new_features(self):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )
        dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]], "labels2": x["labels"]}

        expected_features = Features(
            {
                "tokens": Sequence(Value("string")),
                "labels": Sequence(ClassLabel(names=["negative", "positive"])),
                "labels2": Sequence(Value("int64")),
            }
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            inverted_dset = dset.map(invert_labels, cache_file_name=tmp_file)
            self.assertEqual(inverted_dset.features.type, expected_features.type)
            self.assertDictEqual(inverted_dset.features, expected_features)

    def test_select(self):
        dset = self._create_dummy_dataset()
        # select every two example
        indices = list(range(0, len(dset), 2))

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_select_even = dset.select(indices, indices_cache_file_name=tmp_file)
            self.assertEqual(len(dset_select_even), 15)
            for row in dset_select_even:
                self.assertEqual(int(row["filename"][-1]) % 2, 0)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_select_even.features, Features({"filename": Value("string")}))

        with tempfile.TemporaryDirectory() as tmp_dir:
            bad_indices = list(range(5))
            bad_indices[3] = "foo"
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            self.assertRaises(
                Exception,
                dset.select,
                indices=bad_indices,
                indices_cache_file_name=tmp_file,
                writer_batch_size=2,
            )
            self.assertFalse(os.path.exists(tmp_file))
            dset_select_five = dset.select(
                range(5),
                indices_cache_file_name=tmp_file,
                writer_batch_size=2,
            )
            self.assertTrue(os.path.exists(tmp_file))
            self.assertEqual(len(dset_select_five), 5)
            for i, row in enumerate(dset_select_five):
                self.assertEqual(int(row["filename"][-1]), i)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_select_even.features, Features({"filename": Value("string")}))

    def test_select_then_map(self):
        dset = self._create_dummy_dataset()

        d1 = dset.select([0])
        d2 = dset.select([1])
        d1 = d1.map(lambda x: {"id": int(x["filename"][-1])})
        d2 = d2.map(lambda x: {"id": int(x["filename"][-1])})
        self.assertEqual(d1[0]["id"], 0)
        self.assertEqual(d2[0]["id"], 1)

        with tempfile.TemporaryDirectory() as tmp_dir:
            d1 = dset.select([0], indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow"))
            d2 = dset.select([1], indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow"))
            d1 = d1.map(lambda x: {"id": int(x["filename"][-1])})
            d2 = d2.map(lambda x: {"id": int(x["filename"][-1])})
            self.assertEqual(d1[0]["id"], 0)
            self.assertEqual(d2[0]["id"], 1)

        with tempfile.TemporaryDirectory() as tmp_dir:
            dataset = dset.map(cache_file_name=os.path.join(tmp_dir, "test.arrow"))
            d1 = dataset.select([0])
            d2 = dataset.select([1])
            d1 = d1.map(lambda x: {"id": int(x["filename"][-1])})
            d2 = d2.map(lambda x: {"id": int(x["filename"][-1])})
            self.assertEqual(d1[0]["id"], 0)
            self.assertEqual(d2[0]["id"], 1)

        with tempfile.TemporaryDirectory() as tmp_dir:
            dataset = dset.map(cache_file_name=os.path.join(tmp_dir, "test.arrow"))
            d1 = dataset.select([0], indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow"))
            d2 = dataset.select([1], indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow"))
            d1 = d1.map(lambda x: {"id": int(x["filename"][-1])})
            d2 = d2.map(lambda x: {"id": int(x["filename"][-1])})
            self.assertEqual(d1[0]["id"], 0)
            self.assertEqual(d2[0]["id"], 1)

    def test_shuffle(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_shuffled = dset.shuffle(seed=1234, indices_cache_file_name=tmp_file)
            self.assertEqual(len(dset_shuffled), 30)
            self.assertEqual(dset_shuffled[0]["filename"], "my_name-train_28")
            self.assertEqual(dset_shuffled[2]["filename"], "my_name-train_10")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_shuffled.features, Features({"filename": Value("string")}))

            # Reproducibility
            tmp_file = os.path.join(tmp_dir, "test_2.arrow")
            dset_shuffled_2 = dset.shuffle(seed=1234, indices_cache_file_name=tmp_file)
            self.assertListEqual(dset_shuffled["filename"], dset_shuffled_2["filename"])

    def test_sort(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Keep only 10 examples
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.select(range(10), indices_cache_file_name=tmp_file)
            tmp_file = os.path.join(tmp_dir, "test_2.arrow")
            dset = dset.shuffle(seed=1234, indices_cache_file_name=tmp_file)
            self.assertEqual(len(dset), 10)
            self.assertEqual(dset[0]["filename"], "my_name-train_8")
            self.assertEqual(dset[1]["filename"], "my_name-train_9")
            # Sort
            tmp_file = os.path.join(tmp_dir, "test_3.arrow")
            dset_sorted = dset.sort("filename", indices_cache_file_name=tmp_file)
            for i, row in enumerate(dset_sorted):
                self.assertEqual(int(row["filename"][-1]), i)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sorted.features, Features({"filename": Value("string")}))
            # Sort reversed
            tmp_file = os.path.join(tmp_dir, "test_4.arrow")
            dset_sorted = dset.sort("filename", indices_cache_file_name=tmp_file, reverse=True)
            for i, row in enumerate(dset_sorted):
                self.assertEqual(int(row["filename"][-1]), len(dset_sorted) - 1 - i)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sorted.features, Features({"filename": Value("string")}))

    def test_export(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            # Export the data
            tfrecord_path = os.path.join(tmp_dir, "test.tfrecord")
            dset = dset.map(
                lambda ex, i: {
                    "id": i,
                    "question": f"Question {i}",
                    "answers": {"text": [f"Answer {i}-0", f"Answer {i}-1"], "answer_start": [0, 1]},
                },
                with_indices=True,
                remove_columns=["filename"],
                cache_file_name=tmp_file,
            )
            dset.flatten_()
            dset.set_format("numpy")
            dset.export(filename=tfrecord_path, format="tfrecord")

            # Import the data
            import tensorflow as tf

            tf_dset = tf.data.TFRecordDataset([tfrecord_path])
            feature_description = {
                "id": tf.io.FixedLenFeature([], tf.int64),
                "question": tf.io.FixedLenFeature([], tf.string),
                "answers.text": tf.io.VarLenFeature(tf.string),
                "answers.answer_start": tf.io.VarLenFeature(tf.int64),
            }
            tf_parsed_dset = tf_dset.map(
                lambda example_proto: tf.io.parse_single_example(example_proto, feature_description)
            )
            # Test that keys match original dataset
            for i, ex in enumerate(tf_parsed_dset):
                self.assertEqual(ex.keys(), dset[i].keys())
            # Test for equal number of elements
            self.assertEqual(i, len(dset) - 1)

    def test_train_test_split(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
            dset_dict = dset.train_test_split(
                test_size=10,
                shuffle=False,
                train_indices_cache_file_name=tmp_file,
                test_indices_cache_file_name=tmp_file_2,
            )
            self.assertListEqual(list(dset_dict.keys()), ["train", "test"])
            dset_train = dset_dict["train"]
            dset_test = dset_dict["test"]

            self.assertEqual(len(dset_train), 20)
            self.assertEqual(len(dset_test), 10)
            self.assertEqual(dset_train[0]["filename"], "my_name-train_0")
            self.assertEqual(dset_train[-1]["filename"], "my_name-train_19")
            self.assertEqual(dset_test[0]["filename"], "my_name-train_20")
            self.assertEqual(dset_test[-1]["filename"], "my_name-train_29")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_train.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_test.features, Features({"filename": Value("string")}))

            tmp_file = os.path.join(tmp_dir, "test_3.arrow")
            tmp_file_2 = os.path.join(tmp_dir, "test_4.arrow")
            dset_dict = dset.train_test_split(
                test_size=0.5,
                shuffle=False,
                train_indices_cache_file_name=tmp_file,
                test_indices_cache_file_name=tmp_file_2,
            )
            self.assertListEqual(list(dset_dict.keys()), ["train", "test"])
            dset_train = dset_dict["train"]
            dset_test = dset_dict["test"]

            self.assertEqual(len(dset_train), 15)
            self.assertEqual(len(dset_test), 15)
            self.assertEqual(dset_train[0]["filename"], "my_name-train_0")
            self.assertEqual(dset_train[-1]["filename"], "my_name-train_14")
            self.assertEqual(dset_test[0]["filename"], "my_name-train_15")
            self.assertEqual(dset_test[-1]["filename"], "my_name-train_29")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_train.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_test.features, Features({"filename": Value("string")}))

            tmp_file = os.path.join(tmp_dir, "test_5.arrow")
            tmp_file_2 = os.path.join(tmp_dir, "test_6.arrow")
            dset_dict = dset.train_test_split(
                train_size=10,
                shuffle=False,
                train_indices_cache_file_name=tmp_file,
                test_indices_cache_file_name=tmp_file_2,
            )
            self.assertListEqual(list(dset_dict.keys()), ["train", "test"])
            dset_train = dset_dict["train"]
            dset_test = dset_dict["test"]

            self.assertEqual(len(dset_train), 10)
            self.assertEqual(len(dset_test), 20)
            self.assertEqual(dset_train[0]["filename"], "my_name-train_0")
            self.assertEqual(dset_train[-1]["filename"], "my_name-train_9")
            self.assertEqual(dset_test[0]["filename"], "my_name-train_10")
            self.assertEqual(dset_test[-1]["filename"], "my_name-train_29")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_train.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_test.features, Features({"filename": Value("string")}))

            tmp_file = os.path.join(tmp_dir, "test_7.arrow")
            tmp_file_2 = os.path.join(tmp_dir, "test_8.arrow")
            dset_dict = dset.train_test_split(
                train_size=10, train_indices_cache_file_name=tmp_file, test_indices_cache_file_name=tmp_file_2, seed=42
            )
            self.assertListEqual(list(dset_dict.keys()), ["train", "test"])
            dset_train = dset_dict["train"]
            dset_test = dset_dict["test"]

            self.assertEqual(len(dset_train), 10)
            self.assertEqual(len(dset_test), 20)
            self.assertNotEqual(dset_train[0]["filename"], "my_name-train_0")
            self.assertNotEqual(dset_train[-1]["filename"], "my_name-train_9")
            self.assertNotEqual(dset_test[0]["filename"], "my_name-train_10")
            self.assertNotEqual(dset_test[-1]["filename"], "my_name-train_29")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_train.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_test.features, Features({"filename": Value("string")}))

    def test_shard(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.select(range(10), indices_cache_file_name=tmp_file)
            self.assertEqual(len(dset), 10)
            # Shard
            tmp_file_1 = os.path.join(tmp_dir, "test_1.arrow")
            dset_sharded = dset.shard(num_shards=8, index=1, indices_cache_file_name=tmp_file_1)
            self.assertEqual(2, len(dset_sharded))
            self.assertEqual(["my_name-train_1", "my_name-train_9"], dset_sharded["filename"])
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sharded.features, Features({"filename": Value("string")}))
            # Shard contiguous
            tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
            dset_sharded_contiguous = dset.shard(
                num_shards=3, index=0, contiguous=True, indices_cache_file_name=tmp_file_2
            )
            self.assertEqual([f"my_name-train_{i}" for i in (0, 1, 2, 3)], dset_sharded_contiguous["filename"])
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sharded_contiguous.features, Features({"filename": Value("string")}))
            # Test lengths of sharded contiguous
            self.assertEqual(
                [4, 3, 3],
                [len(dset.shard(3, index=i, contiguous=True, indices_cache_file_name=tmp_file_2)) for i in range(3)],
            )

    def test_flatten_indices(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            self.assertEqual(dset._indices, None)

            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.select(range(10), indices_cache_file_name=tmp_file)
            self.assertEqual(len(dset), 10)

            self.assertNotEqual(dset._indices, None)

            # Test unique fail
            with self.assertRaises(ValueError):
                dset.unique(dset.column_names[0])

            tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
            dset = dset.flatten_indices(cache_file_name=tmp_file_2)

            self.assertEqual(len(dset), 10)
            self.assertEqual(dset._indices, None)
            # Test unique works
            dset.unique(dset.column_names[0])

    def test_format_vectors(self):
        dset = self._create_dummy_dataset()
        import numpy as np
        import tensorflow as tf
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.map(lambda ex, i: {"vec": np.ones(3) * i}, with_indices=True, cache_file_name=tmp_file)
            columns = dset.column_names

            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            for col in columns:
                self.assertIsInstance(dset[0][col], (str, list))
                self.assertIsInstance(dset[:2][col], list)
            self.assertDictEqual(
                dset.features, Features({"filename": Value("string"), "vec": Sequence(Value("float64"))})
            )

            dset.set_format("tensorflow")
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            for col in columns:
                self.assertIsInstance(dset[0][col], (tf.Tensor, tf.RaggedTensor))
                self.assertIsInstance(dset[:2][col], (tf.Tensor, tf.RaggedTensor))
                self.assertIsInstance(dset[col], (tf.Tensor, tf.RaggedTensor))
            self.assertEqual(tuple(dset[:2]["vec"].shape), (2, None))
            self.assertEqual(tuple(dset["vec"][:2].shape), (2, None))

            dset.set_format("numpy")
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            for col in columns:
                self.assertIsInstance(dset[0][col], np.ndarray)
                self.assertIsInstance(dset[:2][col], np.ndarray)
                self.assertIsInstance(dset[col], np.ndarray)
            self.assertEqual(dset[:2]["vec"].shape, (2, 3))
            self.assertEqual(dset["vec"][:2].shape, (2, 3))

            dset.set_format("torch", columns=["vec"])
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            # torch.Tensor is only for numerical columns
            self.assertIsInstance(dset[0]["vec"], torch.Tensor)
            self.assertIsInstance(dset[:2]["vec"], torch.Tensor)
            self.assertIsInstance(dset["vec"][:2], torch.Tensor)
            self.assertEqual(dset[:2]["vec"].shape, (2, 3))
            self.assertEqual(dset["vec"][:2].shape, (2, 3))

    def test_format_ragged_vectors(self):
        dset = self._create_dummy_dataset()
        import numpy as np
        import tensorflow as tf
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.map(lambda ex, i: {"vec": np.ones(3 + i) * i}, with_indices=True, cache_file_name=tmp_file)
            columns = dset.column_names

            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            for col in columns:
                self.assertIsInstance(dset[0][col], (str, list))
                self.assertIsInstance(dset[:2][col], list)
            self.assertDictEqual(
                dset.features, Features({"filename": Value("string"), "vec": Sequence(Value("float64"))})
            )

            dset.set_format("tensorflow")
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            for col in columns:
                self.assertIsInstance(dset[0][col], (tf.Tensor, tf.RaggedTensor))
                self.assertIsInstance(dset[:2][col], (tf.Tensor, tf.RaggedTensor))
                self.assertIsInstance(dset[col], (tf.Tensor, tf.RaggedTensor))
            # dim is None for ragged vectors in tensorflow
            self.assertListEqual(dset[:2]["vec"].shape.as_list(), [2, None])
            self.assertListEqual(dset["vec"][:2].shape.as_list(), [2, None])

            dset.set_format("numpy")
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            for col in columns:
                self.assertIsInstance(dset[0][col], np.ndarray)
                self.assertIsInstance(dset[:2][col], np.ndarray)
                self.assertIsInstance(dset[col], np.ndarray)
            # array is flat for raged vectors in numpy
            self.assertEqual(dset[:2]["vec"].shape, (2,))
            self.assertEqual(dset["vec"][:2].shape, (2,))

            dset.set_format("torch", columns=["vec"])
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            # torch.Tensor is only for numerical columns
            self.assertIsInstance(dset[0]["vec"], torch.Tensor)
            self.assertIsInstance(dset[:2]["vec"][0], torch.Tensor)
            self.assertIsInstance(dset["vec"][0], torch.Tensor)
            # pytorch doesn't support ragged tensors, so we should have lists
            self.assertIsInstance(dset[:2]["vec"], list)
            self.assertIsInstance(dset["vec"][:2], list)

    def test_format_nested(self):
        dset = self._create_dummy_dataset()
        import numpy as np
        import tensorflow as tf
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.map(
                lambda ex: {"nested": [{"foo": np.ones(3)}] * len(ex["filename"])},
                cache_file_name=tmp_file,
                batched=True,
            )
            self.assertDictEqual(
                dset.features, Features({"filename": Value("string"), "nested": {"foo": Sequence(Value("float64"))}})
            )

            dset.set_format("tensorflow")
            self.assertIsNotNone(dset[0])
            self.assertIsInstance(dset[0]["nested"]["foo"], (tf.Tensor, tf.RaggedTensor))
            self.assertIsNotNone(dset[:2])
            self.assertIsInstance(dset[:2]["nested"][0]["foo"], (tf.Tensor, tf.RaggedTensor))
            self.assertIsInstance(dset["nested"][0]["foo"], (tf.Tensor, tf.RaggedTensor))

            dset.set_format("numpy")
            self.assertIsNotNone(dset[0])
            self.assertIsInstance(dset[0]["nested"]["foo"], np.ndarray)
            self.assertIsNotNone(dset[:2])
            self.assertIsInstance(dset[:2]["nested"][0]["foo"], np.ndarray)
            self.assertIsInstance(dset["nested"][0]["foo"], np.ndarray)

            dset.set_format("torch", columns="nested")
            self.assertIsNotNone(dset[0])
            self.assertIsInstance(dset[0]["nested"]["foo"], torch.Tensor)
            self.assertIsNotNone(dset[:2])
            self.assertIsInstance(dset[:2]["nested"][0]["foo"], torch.Tensor)
            self.assertIsInstance(dset["nested"][0]["foo"], torch.Tensor)

    def test_format_pandas(self):
        dset = self._create_dummy_dataset(multiple_columns=True)
        import pandas as pd

        dset.set_format("pandas")
        self.assertIsInstance(dset[0], pd.DataFrame)
        self.assertIsInstance(dset[:2], pd.DataFrame)
        self.assertIsInstance(dset["col_1"], pd.Series)
