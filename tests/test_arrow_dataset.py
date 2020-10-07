import os
import pickle
import tempfile
from functools import partial
from unittest import TestCase

import numpy as np
import pandas as pd
import pyarrow as pa
from absl.testing import parameterized

import datasets.arrow_dataset
from datasets import concatenate_datasets, load_from_disk, temp_seed
from datasets.arrow_dataset import Dataset, transmit_format
from datasets.dataset_dict import DatasetDict
from datasets.features import ClassLabel, Features, Sequence, Value
from datasets.info import DatasetInfo

from .utils import require_tf, require_torch


class Unpicklable:
    def __getstate__(self):
        raise pickle.PicklingError()


def picklable_map_function(x):
    return {"id": int(x["filename"].split("_")[-1])}


def picklable_map_function_with_indices(x, i):
    return {"id": i}


def picklable_filter_function(x):
    return int(x["filename"].split("_")[-1]) < 10


IN_MEMORY_PARAMETERS = [
    {"testcase_name": name, "in_memory": im} for im, name in [(True, "in_memory"), (False, "on_disk")]
]


@parameterized.named_parameters(IN_MEMORY_PARAMETERS)
class BaseDatasetTest(TestCase):
    def setUp(self):
        # google colab doesn't allow to pickle loggers
        # so we want to make sure each tests passes without pickling the logger
        def reduce_ex(self):
            raise pickle.PicklingError()

        datasets.arrow_dataset.logger.__reduce_ex__ = reduce_ex

    def _create_dummy_dataset(self, in_memory: bool, tmp_dir: str, multiple_columns=False) -> Dataset:
        if multiple_columns:
            data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
            dset = Dataset.from_dict(data)
        else:
            dset = Dataset.from_dict({"filename": ["my_name-train" + "_" + str(x) for x in np.arange(30).tolist()]})
        if not in_memory:
            dset = self._to(in_memory, tmp_dir, dset)
        return dset

    def _to(self, in_memory, tmp_dir, *datasets):
        if in_memory:
            datasets = [dataset.map(keep_in_memory=True) for dataset in datasets]
        else:
            start = 0
            while os.path.isfile(os.path.join(tmp_dir, f"dataset{start}.arrow")):
                start += 1
            datasets = [
                dataset.map(cache_file_name=os.path.join(tmp_dir, f"dataset{start + i}.arrow"))
                for i, dataset in enumerate(datasets)
            ]
        return datasets if len(datasets) > 1 else datasets[0]

    def test_dummy_dataset(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:

            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertEqual(dset[0]["filename"], "my_name-train_0")
            self.assertEqual(dset["filename"][0], "my_name-train_0")
            del dset

            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))
            self.assertEqual(dset[0]["col_1"], 3)
            self.assertEqual(dset["col_1"][0], 3)
            del dset

    def test_dataset_getitem(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:

            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            self.assertEqual(dset[0]["filename"], "my_name-train_0")
            self.assertEqual(dset["filename"][0], "my_name-train_0")

            self.assertEqual(dset[-1]["filename"], "my_name-train_29")
            self.assertEqual(dset["filename"][-1], "my_name-train_29")

            self.assertListEqual(dset[:2]["filename"], ["my_name-train_0", "my_name-train_1"])
            self.assertListEqual(dset["filename"][:2], ["my_name-train_0", "my_name-train_1"])

            self.assertEqual(dset[:-1]["filename"][-1], "my_name-train_28")
            self.assertEqual(dset["filename"][:-1][-1], "my_name-train_28")

            self.assertListEqual(dset[[0, -1]]["filename"], ["my_name-train_0", "my_name-train_29"])
            self.assertListEqual(dset[np.array([0, -1])]["filename"], ["my_name-train_0", "my_name-train_29"])

            del dset

    def test_dummy_dataset_pickle(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "dset.pt")

            dset = self._create_dummy_dataset(in_memory, tmp_dir).select(range(10))

            with open(tmp_file, "wb") as f:
                pickle.dump(dset, f)

            with open(tmp_file, "rb") as f:
                dset = pickle.load(f)

            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertEqual(dset[0]["filename"], "my_name-train_0")
            self.assertEqual(dset["filename"][0], "my_name-train_0")
            del dset

            dset = self._create_dummy_dataset(in_memory, tmp_dir).select(
                range(10), indices_cache_file_name=os.path.join(tmp_dir, "ind.arrow")
            )
            if not in_memory:
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
            del dset

    def test_dummy_dataset_serialize(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:

            dset = self._create_dummy_dataset(in_memory, tmp_dir).select(range(10))
            dataset_path = os.path.join(tmp_dir, "my_dataset")
            dset.save_to_disk(dataset_path)
            dset = dset.load_from_disk(dataset_path)

            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertEqual(dset[0]["filename"], "my_name-train_0")
            self.assertEqual(dset["filename"][0], "my_name-train_0")
            del dset

            dset = self._create_dummy_dataset(in_memory, tmp_dir).select(
                range(10), indices_cache_file_name=os.path.join(tmp_dir, "ind.arrow")
            )
            if not in_memory:
                dset._data = Unpicklable()
            dset._indices = Unpicklable()

            dset.save_to_disk(dataset_path)
            dset = dset.load_from_disk(dataset_path)

            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertEqual(dset[0]["filename"], "my_name-train_0")
            self.assertEqual(dset["filename"][0], "my_name-train_0")
            del dset

    def test_dummy_dataset_load_from_disk(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:

            dset = self._create_dummy_dataset(in_memory, tmp_dir).select(range(10))
            dataset_path = os.path.join(tmp_dir, "my_dataset")
            dset.save_to_disk(dataset_path)
            dset = load_from_disk(dataset_path)

            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertEqual(dset[0]["filename"], "my_name-train_0")
            self.assertEqual(dset["filename"][0], "my_name-train_0")
            del dset

    def test_set_format_numpy_multiple_columns(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            fingerprint = dset._fingerprint
            dset.set_format(type="numpy", columns=["col_1"])
            self.assertEqual(len(dset[0]), 1)
            self.assertIsInstance(dset[0]["col_1"], np.ndarray)
            self.assertListEqual(list(dset[0]["col_1"].shape), [])
            self.assertEqual(dset[0]["col_1"].item(), 3)
            self.assertIsInstance(dset["col_1"], np.ndarray)
            self.assertListEqual(list(dset["col_1"].shape), [4])
            np.testing.assert_array_equal(dset["col_1"], np.array([3, 2, 1, 0]))
            self.assertNotEqual(dset._fingerprint, fingerprint)

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
            del dset

    @require_torch
    def test_set_format_torch(self, in_memory):
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
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
            del dset

    @require_tf
    def test_set_format_tf(self, in_memory):
        import tensorflow as tf

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
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
            del dset

    def test_set_format_pandas(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            dset.set_format(type="pandas", columns=["col_1"])
            self.assertEqual(len(dset[0].columns), 1)
            self.assertIsInstance(dset[0], pd.DataFrame)
            self.assertListEqual(list(dset[0].shape), [1, 1])
            self.assertEqual(dset[0]["col_1"].item(), 3)

            dset.set_format(type="pandas", columns=["col_1", "col_2"])
            self.assertEqual(len(dset[0].columns), 2)
            self.assertEqual(dset[0]["col_2"].item(), "a")
            del dset

    def test_cast_(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            features = dset.features
            features["col_1"] = Value("float64")
            features = Features({k: features[k] for k in list(features)[::-1]})
            fingerprint = dset._fingerprint
            dset.cast_(features)
            self.assertEqual(dset.num_columns, 2)
            self.assertEqual(dset.features["col_1"], Value("float64"))
            self.assertIsInstance(dset[0]["col_1"], float)
            self.assertNotEqual(dset._fingerprint, fingerprint)
            del dset

    def test_remove_columns_(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            fingerprint = dset._fingerprint
            dset.remove_columns_(column_names="col_1")
            self.assertEqual(dset.num_columns, 1)
            self.assertListEqual(list(dset.column_names), ["col_2"])
            del dset

            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            dset.remove_columns_(column_names=["col_1", "col_2"])
            self.assertEqual(dset.num_columns, 0)
            self.assertNotEqual(dset._fingerprint, fingerprint)
            del dset

    def test_rename_column_(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            fingerprint = dset._fingerprint
            dset.rename_column_(original_column_name="col_1", new_column_name="new_name")
            self.assertEqual(dset.num_columns, 2)
            self.assertListEqual(list(dset.column_names), ["new_name", "col_2"])
            self.assertNotEqual(dset._fingerprint, fingerprint)
            del dset

    def test_concatenate(self, in_memory):
        data1, data2, data3 = {"id": [0, 1, 2]}, {"id": [3, 4, 5]}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1),
                Dataset.from_dict(data2, info=info2),
                Dataset.from_dict(data3),
            )
            dset1, dset2, dset3 = self._to(in_memory, tmp_dir, dset1, dset2, dset3)

            dset_concat = concatenate_datasets([dset1, dset2, dset3])
            self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
            self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
            self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
            self.assertEqual(len(dset_concat._data_files), 0 if in_memory else 3)
            self.assertEqual(len(dset_concat._indices_data_files), 0)
            self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")
            del dset_concat, dset1, dset2, dset3

    def test_concatenate_formatted(self, in_memory):
        data1, data2, data3 = {"id": [0, 1, 2]}, {"id": [3, 4, 5]}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1),
                Dataset.from_dict(data2, info=info2),
                Dataset.from_dict(data3),
            )
            dset1, dset2, dset3 = self._to(in_memory, tmp_dir, dset1, dset2, dset3)

            dset1.set_format("numpy")
            dset_concat = concatenate_datasets([dset1, dset2, dset3])
            self.assertEqual(dset_concat.format["type"], None)
            dset2.set_format("numpy")
            dset3.set_format("numpy")
            dset_concat = concatenate_datasets([dset1, dset2, dset3])
            self.assertEqual(dset_concat.format["type"], "numpy")
            del dset_concat, dset1, dset2, dset3

    def test_concatenate_with_indices(self, in_memory):
        data1, data2, data3 = {"id": [0, 1, 2] * 2}, {"id": [3, 4, 5] * 2}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1),
                Dataset.from_dict(data2, info=info2),
                Dataset.from_dict(data3),
            )
            dset1, dset2, dset3 = self._to(in_memory, tmp_dir, dset1, dset2, dset3)
            dset1, dset2, dset3 = dset1.select([0, 1, 2]), dset2.select([0, 1, 2]), dset3

            dset_concat = concatenate_datasets([dset1, dset2, dset3])
            self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
            self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
            self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
            self.assertEqual(len(dset_concat._data_files), 0 if in_memory else 3)
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
                    _ = concatenate_datasets([dset1, dset2, dset3])
                del dset_concat, dset1, dset2, dset3

    def test_concatenate_with_indices_from_disk(self, in_memory):
        data1, data2, data3 = {"id": [0, 1, 2] * 2}, {"id": [3, 4, 5] * 2}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1),
                Dataset.from_dict(data2, info=info2),
                Dataset.from_dict(data3),
            )
            dset1, dset2, dset3 = self._to(in_memory, tmp_dir, dset1, dset2, dset3)
            dset1, dset2, dset3 = (
                dset1.select([0, 1, 2], indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow")),
                dset2.select([0, 1, 2], indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow")),
                dset3.select([0, 1], indices_cache_file_name=os.path.join(tmp_dir, "i3.arrow")),
            )

            dset_concat = concatenate_datasets([dset1, dset2, dset3])
            self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
            self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
            self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
            self.assertEqual(len(dset_concat._data_files), 0 if in_memory else 3)
            self.assertEqual(len(dset_concat._indices_data_files), 0)  # now in memory since an offset is applied
            self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")
            del dset_concat, dset1, dset2, dset3

    def test_concatenate_pickle_with_history(self, in_memory):
        data1, data2, data3 = {"id": [0, 1, 2] * 2}, {"id": [3, 4, 5] * 2}, {"id": [6, 7], "foo": ["bar", "bar"]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1),
                Dataset.from_dict(data2, info=info2),
                Dataset.from_dict(data3),
            )
            dset1, dset2, dset3 = self._to(in_memory, tmp_dir, dset1, dset2, dset3)
            dset1, dset2, dset3 = (
                dset1.select([0, 1, 2], indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow")),
                dset2.select([0, 1, 2], indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow")),
                dset3.select([0, 1], indices_cache_file_name=os.path.join(tmp_dir, "i3.arrow")),
            )

            dset3.remove_columns_("foo")
            if not in_memory:
                dset1._data, dset2._data, dset3._data = Unpicklable(), Unpicklable(), Unpicklable()
            dset1, dset2, dset3 = [pickle.loads(pickle.dumps(d)) for d in (dset1, dset2, dset3)]
            dset_concat = concatenate_datasets([dset1, dset2, dset3])
            if not in_memory:
                dset_concat._data = Unpicklable()
            dset_concat = pickle.loads(pickle.dumps(dset_concat))
            self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
            self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
            self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
            self.assertEqual(len(dset_concat._data_files), 0 if in_memory else 3)
            self.assertEqual(len(dset_concat._inplace_history), 0 if in_memory else 3)
            self.assertEqual(len(dset_concat._indices_data_files), 0)
            self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")
            del dset_concat, dset1, dset2, dset3

    def test_flatten(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict(
                {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10},
                features=Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")}),
            )
            dset = self._to(in_memory, tmp_dir, dset)
            fingerprint = dset._fingerprint
            dset.flatten_()
            self.assertListEqual(dset.column_names, ["a.b.c", "foo"])
            self.assertListEqual(list(dset.features.keys()), ["a.b.c", "foo"])
            self.assertDictEqual(dset.features, Features({"a.b.c": Sequence(Value("string")), "foo": Value("int64")}))
            self.assertNotEqual(dset._fingerprint, fingerprint)
            del dset

    def test_map(self, in_memory):
        # standard
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)

            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            fingerprint = dset._fingerprint
            dset_test = dset.map(lambda x: {"name": x["filename"][:-2], "id": int(x["filename"].split("_")[-1])})
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test.features,
                Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
            )
            self.assertListEqual(dset_test["id"], list(range(30)))
            self.assertNotEqual(dset_test._fingerprint, fingerprint)
            del dset, dset_test

        # with indices
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset_test_with_indices = dset.map(lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True)
            self.assertEqual(len(dset_test_with_indices), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test_with_indices.features,
                Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
            )
            self.assertListEqual(dset_test_with_indices["id"], list(range(30)))
            del dset, dset_test_with_indices

        # interrupted
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)

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
            self.assertListEqual(dset_test_with_indices["id"], list(range(30)))
            del dset, dset_test_with_indices

        # formatted
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            dset.set_format("numpy", columns=["col_1"])

            dset_test = dset.map(lambda x: {"col_1_plus_one": x["col_1"].item() + 1})
            self.assertEqual(len(dset_test), 4)
            self.assertEqual(dset_test.format["type"], "numpy")
            self.assertIsInstance(dset_test["col_1"], np.ndarray)
            self.assertIsInstance(dset_test["col_1_plus_one"], np.ndarray)
            self.assertListEqual(sorted(dset_test[0].keys()), ["col_1", "col_1_plus_one"])
            self.assertListEqual(sorted(dset_test.column_names), ["col_1", "col_1_plus_one", "col_2"])
            del dset, dset_test

    def test_map_multiprocessing(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:  # standard
            dset = self._create_dummy_dataset(in_memory, tmp_dir)

            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            fingerprint = dset._fingerprint
            dset_test = dset.map(picklable_map_function, num_proc=2)
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test.features,
                Features({"filename": Value("string"), "id": Value("int64")}),
            )
            self.assertEqual(len(dset_test._data_files), 0 if in_memory else 2)
            self.assertListEqual(dset_test["id"], list(range(30)))
            self.assertNotEqual(dset_test._fingerprint, fingerprint)
            del dset, dset_test

        with tempfile.TemporaryDirectory() as tmp_dir:  # with_indices
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            fingerprint = dset._fingerprint
            dset_test = dset.map(picklable_map_function_with_indices, num_proc=3, with_indices=True)
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test.features,
                Features({"filename": Value("string"), "id": Value("int64")}),
            )
            self.assertEqual(len(dset_test._data_files), 0 if in_memory else 3)
            self.assertListEqual(dset_test["id"], list(range(30)))
            self.assertNotEqual(dset_test._fingerprint, fingerprint)
            del dset, dset_test

        with tempfile.TemporaryDirectory() as tmp_dir:  # lambda (requires multiprocess from pathos)
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            fingerprint = dset._fingerprint
            dset_test = dset.map(lambda x: {"id": int(x["filename"].split("_")[-1])}, num_proc=2)
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test.features,
                Features({"filename": Value("string"), "id": Value("int64")}),
            )
            self.assertEqual(len(dset_test._data_files), 0 if in_memory else 2)
            self.assertListEqual(dset_test["id"], list(range(30)))
            self.assertNotEqual(dset_test._fingerprint, fingerprint)
            del dset, dset_test

    def test_new_features(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            features = Features({"filename": Value("string"), "label": ClassLabel(names=["positive", "negative"])})
            dset_test_with_indices = dset.map(lambda x, i: {"label": i % 2}, with_indices=True, features=features)
            self.assertEqual(len(dset_test_with_indices), 30)
            self.assertDictEqual(
                dset_test_with_indices.features,
                features,
            )
            del dset, dset_test_with_indices

    def test_map_batched(self, in_memory):
        def map_batched(example):
            return {"filename_new": [x + "_extension" for x in example["filename"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset_test_batched = dset.map(map_batched, batched=True)
            self.assertEqual(len(dset_test_batched), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test_batched.features, Features({"filename": Value("string"), "filename_new": Value("string")})
            )
            del dset, dset_test_batched

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            with dset.formatted_as("numpy", columns=["filename"]):
                dset_test_batched = dset.map(map_batched, batched=True)
                self.assertEqual(len(dset_test_batched), 30)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertDictEqual(
                    dset_test_batched.features,
                    Features({"filename": Value("string"), "filename_new": Value("string")}),
                )
            del dset, dset_test_batched

        def map_batched_with_indices(example, idx):
            return {"filename_new": [x + "_extension_" + str(idx) for x in example["filename"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset_test_with_indices_batched = dset.map(map_batched_with_indices, batched=True, with_indices=True)
            self.assertEqual(len(dset_test_with_indices_batched), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(
                dset_test_with_indices_batched.features,
                Features({"filename": Value("string"), "filename_new": Value("string")}),
            )
            del dset, dset_test_with_indices_batched

    def test_map_nested(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"field": ["a", "b"]})
            dset = self._to(in_memory, tmp_dir, dset)
            dset = dset.map(lambda example: {"otherfield": {"capital": example["field"].capitalize()}})
            dset = dset.map(lambda example: {"otherfield": {"append_x": example["field"] + "x"}})
            self.assertEqual(dset[0], {"field": "a", "otherfield": {"append_x": "ax"}})
            del dset

    @require_torch
    def test_map_torch(self, in_memory):
        import torch

        def func(example):
            return {"tensor": torch.Tensor([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset_test = dset.map(func)
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(
                dset_test.features, Features({"filename": Value("string"), "tensor": Sequence(Value("float64"))})
            )
            self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])
            del dset, dset_test

    @require_tf
    def test_map_tf(self, in_memory):
        import tensorflow as tf

        def func(example):
            return {"tensor": tf.constant([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset_test = dset.map(func)
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(
                dset_test.features, Features({"filename": Value("string"), "tensor": Sequence(Value("float64"))})
            )
            self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])
            del dset, dset_test

    def test_map_numpy(self, in_memory):
        def func(example):
            return {"tensor": np.array([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset_test = dset.map(func)
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(
                dset_test.features, Features({"filename": Value("string"), "tensor": Sequence(Value("float64"))})
            )
            self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])
            del dset, dset_test

    def test_map_remove_colums(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset = dset.map(lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True)
            self.assertTrue("id" in dset[0])
            self.assertDictEqual(
                dset.features, Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")})
            )

            dset = dset.map(lambda x: x, remove_columns=["id"])
            self.assertTrue("id" not in dset[0])
            self.assertDictEqual(dset.features, Features({"filename": Value("string"), "name": Value("string")}))
            del dset

    def test_filter(self, in_memory):
        # keep only first five examples

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            fingerprint = dset._fingerprint
            dset_filter_first_five = dset.filter(lambda x, i: i < 5, with_indices=True)
            self.assertEqual(len(dset_filter_first_five), 5)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_filter_first_five.features, Features({"filename": Value("string")}))
            self.assertNotEqual(dset_filter_first_five._fingerprint, fingerprint)
            del dset, dset_filter_first_five

        # filter filenames with even id at the end + formatted
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset.set_format("numpy")
            fingerprint = dset._fingerprint
            dset_filter_even_num = dset.filter(lambda x: (int(x["filename"].item()[-1]) % 2 == 0))
            self.assertEqual(len(dset_filter_even_num), 15)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_filter_even_num.features, Features({"filename": Value("string")}))
            self.assertNotEqual(dset_filter_even_num._fingerprint, fingerprint)
            self.assertEqual(dset_filter_even_num.format["type"], "numpy")
            del dset, dset_filter_even_num

    def test_filter_multiprocessing(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            fingerprint = dset._fingerprint
            dset_filter_first_ten = dset.filter(picklable_filter_function, num_proc=2)
            self.assertEqual(len(dset_filter_first_ten), 10)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_filter_first_ten.features, Features({"filename": Value("string")}))
            self.assertEqual(len(dset_filter_first_ten._data_files), 0 if in_memory else 2)
            self.assertNotEqual(dset_filter_first_ten._fingerprint, fingerprint)
            del dset, dset_filter_first_ten

    def test_keep_features_after_transform_specified(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)
            dset = self._to(in_memory, tmp_dir, dset)
            inverted_dset = dset.map(invert_labels, features=features)
            self.assertEqual(inverted_dset.features.type, features.type)
            self.assertDictEqual(inverted_dset.features, features)
            del dset, inverted_dset

    def test_keep_features_after_transform_unspecified(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)
            dset = self._to(in_memory, tmp_dir, dset)
            inverted_dset = dset.map(invert_labels)
            self.assertEqual(inverted_dset.features.type, features.type)
            self.assertDictEqual(inverted_dset.features, features)
            del dset, inverted_dset

    def test_keep_features_after_transform_to_file(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)
            dset = self._to(in_memory, tmp_dir, dset)
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset.map(invert_labels, cache_file_name=tmp_file)
            inverted_dset = Dataset.from_file(tmp_file)
            self.assertEqual(inverted_dset.features.type, features.type)
            self.assertDictEqual(inverted_dset.features, features)
            del dset, inverted_dset

    def test_keep_features_after_transform_to_memory(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)
            dset = self._to(in_memory, tmp_dir, dset)
            inverted_dset = dset.map(invert_labels, keep_in_memory=True)
            self.assertEqual(inverted_dset.features.type, features.type)
            self.assertDictEqual(inverted_dset.features, features)
            del dset, inverted_dset

    def test_keep_features_after_loading_from_cache(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)
            dset = self._to(in_memory, tmp_dir, dset)
            tmp_file1 = os.path.join(tmp_dir, "test1.arrow")
            tmp_file2 = os.path.join(tmp_dir, "test2.arrow")
            inverted_dset = dset.map(invert_labels, cache_file_name=tmp_file1)
            inverted_dset = dset.map(invert_labels, cache_file_name=tmp_file2)
            self.assertGreater(len(inverted_dset.cache_files), 0)
            self.assertEqual(inverted_dset.features.type, features.type)
            self.assertDictEqual(inverted_dset.features, features)
            del dset, inverted_dset

    def test_keep_features_with_new_features(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

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
            dset = Dataset.from_dict({"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features)
            dset = self._to(in_memory, tmp_dir, dset)
            inverted_dset = dset.map(invert_labels)
            self.assertEqual(inverted_dset.features.type, expected_features.type)
            self.assertDictEqual(inverted_dset.features, expected_features)
            del dset, inverted_dset

    def test_select(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            # select every two example
            indices = list(range(0, len(dset), 2))
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            fingerprint = dset._fingerprint
            dset_select_even = dset.select(indices, indices_cache_file_name=tmp_file)
            self.assertEqual(len(dset_select_even), 15)
            for row in dset_select_even:
                self.assertEqual(int(row["filename"][-1]) % 2, 0)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_select_even.features, Features({"filename": Value("string")}))
            self.assertNotEqual(dset_select_even._fingerprint, fingerprint)
            del dset, dset_select_even

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
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
            dset.set_format("numpy")
            dset_select_five = dset.select(
                range(5),
                indices_cache_file_name=tmp_file,
                writer_batch_size=2,
            )
            self.assertTrue(os.path.exists(tmp_file))
            self.assertEqual(len(dset_select_five), 5)
            self.assertEqual(dset_select_five.format["type"], "numpy")
            for i, row in enumerate(dset_select_five):
                self.assertEqual(int(row["filename"].item()[-1]), i)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_select_five.features, Features({"filename": Value("string")}))
            del dset, dset_select_five

    def test_select_then_map(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            d1 = dset.select([0])
            d2 = dset.select([1])
            d1 = d1.map(lambda x: {"id": int(x["filename"].split("_")[-1])})
            d2 = d2.map(lambda x: {"id": int(x["filename"].split("_")[-1])})
            self.assertEqual(d1[0]["id"], 0)
            self.assertEqual(d2[0]["id"], 1)
            del dset, d1, d2

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            d1 = dset.select([0], indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow"))
            d2 = dset.select([1], indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow"))
            d1 = d1.map(lambda x: {"id": int(x["filename"].split("_")[-1])})
            d2 = d2.map(lambda x: {"id": int(x["filename"].split("_")[-1])})
            self.assertEqual(d1[0]["id"], 0)
            self.assertEqual(d2[0]["id"], 1)
            del dset, d1, d2

    def test_pickle_after_many_transforms_on_disk(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            self.assertEqual(len(dset._data_files), 0 if in_memory else 1)
            dset.rename_column_("filename", "file")
            self.assertListEqual(dset.column_names, ["file"])
            dset = dset.select(range(5))
            self.assertEqual(len(dset), 5)
            dset = dset.map(lambda x: {"id": int(x["file"][-1])})
            self.assertListEqual(sorted(dset.column_names), ["file", "id"])
            dset.rename_column_("id", "number")
            self.assertListEqual(sorted(dset.column_names), ["file", "number"])
            dset = dset.select([1])
            self.assertEqual(dset[0]["file"], "my_name-train_1")
            self.assertEqual(dset[0]["number"], 1)

            self.assertEqual(dset._indices["indices"].to_pylist(), [1])
            self.assertEqual(
                dset._inplace_history,
                [] if in_memory else [{"transforms": [("rename_column_", ("id", "number"), {})]}],
            )
            if not in_memory:
                dset._data = Unpicklable()  # check that we don't pickle the entire table

            pickled = pickle.dumps(dset)
            loaded = pickle.loads(pickled)
            self.assertEqual(loaded[0]["file"], "my_name-train_1")
            self.assertEqual(loaded[0]["number"], 1)
            del dset, loaded

    def test_shuffle(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            fingerprint = dset._fingerprint
            dset_shuffled = dset.shuffle(seed=1234, indices_cache_file_name=tmp_file)
            self.assertEqual(len(dset_shuffled), 30)
            self.assertEqual(dset_shuffled[0]["filename"], "my_name-train_28")
            self.assertEqual(dset_shuffled[2]["filename"], "my_name-train_10")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_shuffled.features, Features({"filename": Value("string")}))
            self.assertNotEqual(dset_shuffled._fingerprint, fingerprint)

            # Reproducibility
            tmp_file = os.path.join(tmp_dir, "test_2.arrow")
            dset_shuffled_2 = dset.shuffle(seed=1234, indices_cache_file_name=tmp_file)
            self.assertListEqual(dset_shuffled["filename"], dset_shuffled_2["filename"])

            # Compatible with temp_seed
            with temp_seed(42):
                d1 = dset.shuffle()
            with temp_seed(42):
                d2 = dset.shuffle()
                d3 = dset.shuffle()
            self.assertListEqual(d1["filename"], d2["filename"])
            self.assertEqual(d1._fingerprint, d2._fingerprint)
            self.assertNotEqual(d3["filename"], d2["filename"])
            self.assertNotEqual(d3._fingerprint, d2._fingerprint)
            del dset, dset_shuffled, dset_shuffled_2, d1, d2, d3

    def test_sort(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
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
            fingerprint = dset._fingerprint
            dset_sorted = dset.sort("filename", indices_cache_file_name=tmp_file)
            for i, row in enumerate(dset_sorted):
                self.assertEqual(int(row["filename"][-1]), i)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sorted.features, Features({"filename": Value("string")}))
            self.assertNotEqual(dset_sorted._fingerprint, fingerprint)
            # Sort reversed
            tmp_file = os.path.join(tmp_dir, "test_4.arrow")
            fingerprint = dset._fingerprint
            dset_sorted = dset.sort("filename", indices_cache_file_name=tmp_file, reverse=True)
            for i, row in enumerate(dset_sorted):
                self.assertEqual(int(row["filename"][-1]), len(dset_sorted) - 1 - i)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sorted.features, Features({"filename": Value("string")}))
            self.assertNotEqual(dset_sorted._fingerprint, fingerprint)
            # formatted
            dset.set_format("numpy")
            dset_sorted_formatted = dset.sort("filename")
            self.assertEqual(dset_sorted_formatted.format["type"], "numpy")
            del dset, dset_sorted, dset_sorted_formatted

    @require_tf
    def test_export(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            # Export the data
            tfrecord_path = os.path.join(tmp_dir, "test.tfrecord")
            formatted_dset = dset.map(
                lambda ex, i: {
                    "id": i,
                    "question": f"Question {i}",
                    "answers": {"text": [f"Answer {i}-0", f"Answer {i}-1"], "answer_start": [0, 1]},
                },
                with_indices=True,
                remove_columns=["filename"],
            )
            formatted_dset.flatten_()
            formatted_dset.set_format("numpy")
            formatted_dset.export(filename=tfrecord_path, format="tfrecord")

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
                self.assertEqual(ex.keys(), formatted_dset[i].keys())
            # Test for equal number of elements
            self.assertEqual(i, len(formatted_dset) - 1)
            del dset, formatted_dset

    def test_train_test_split(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            fingerprint = dset._fingerprint
            dset_dict = dset.train_test_split(test_size=10, shuffle=False)
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
            self.assertNotEqual(dset_train._fingerprint, fingerprint)
            self.assertNotEqual(dset_test._fingerprint, fingerprint)
            self.assertNotEqual(dset_train._fingerprint, dset_test._fingerprint)

            dset_dict = dset.train_test_split(test_size=0.5, shuffle=False)
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

            dset_dict = dset.train_test_split(train_size=10, shuffle=False)
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

            dset.set_format("numpy")
            dset_dict = dset.train_test_split(train_size=10, seed=42)
            self.assertListEqual(list(dset_dict.keys()), ["train", "test"])
            dset_train = dset_dict["train"]
            dset_test = dset_dict["test"]

            self.assertEqual(len(dset_train), 10)
            self.assertEqual(len(dset_test), 20)
            self.assertEqual(dset_train.format["type"], "numpy")
            self.assertEqual(dset_test.format["type"], "numpy")
            self.assertNotEqual(dset_train[0]["filename"].item(), "my_name-train_0")
            self.assertNotEqual(dset_train[-1]["filename"].item(), "my_name-train_9")
            self.assertNotEqual(dset_test[0]["filename"].item(), "my_name-train_10")
            self.assertNotEqual(dset_test[-1]["filename"].item(), "my_name-train_29")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_train.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_test.features, Features({"filename": Value("string")}))
            del dset, dset_test, dset_train, dset_dict

    def test_shard(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.select(range(10), indices_cache_file_name=tmp_file)
            self.assertEqual(len(dset), 10)
            # Shard
            tmp_file_1 = os.path.join(tmp_dir, "test_1.arrow")
            fingerprint = dset._fingerprint
            dset_sharded = dset.shard(num_shards=8, index=1, indices_cache_file_name=tmp_file_1)
            self.assertEqual(2, len(dset_sharded))
            self.assertEqual(["my_name-train_1", "my_name-train_9"], dset_sharded["filename"])
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sharded.features, Features({"filename": Value("string")}))
            self.assertNotEqual(dset_sharded._fingerprint, fingerprint)
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
                [
                    len(dset.shard(3, index=i, contiguous=True, indices_cache_file_name=tmp_file_2 + str(i)))
                    for i in range(3)
                ],
            )
            # formatted
            dset.set_format("numpy")
            dset_sharded_formatted = dset.shard(num_shards=3, index=0)
            self.assertEqual(dset_sharded_formatted.format["type"], "numpy")
            del dset, dset_sharded, dset_sharded_contiguous, dset_sharded_formatted

    def test_flatten_indices(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            self.assertEqual(dset._indices, None)

            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.select(range(10), indices_cache_file_name=tmp_file)
            self.assertEqual(len(dset), 10)

            self.assertNotEqual(dset._indices, None)

            # Test unique fail
            with self.assertRaises(ValueError):
                dset.unique(dset.column_names[0])

            tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
            fingerprint = dset._fingerprint
            dset.set_format("numpy")
            dset = dset.flatten_indices(cache_file_name=tmp_file_2)

            self.assertEqual(len(dset), 10)
            self.assertEqual(dset._indices, None)
            self.assertNotEqual(dset._fingerprint, fingerprint)
            self.assertEqual(dset.format["type"], "numpy")
            # Test unique works
            dset.unique(dset.column_names[0])
            del dset

    @require_tf
    @require_torch
    def test_format_vectors(self, in_memory):
        import numpy as np
        import tensorflow as tf
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset = dset.map(lambda ex, i: {"vec": np.ones(3) * i}, with_indices=True)
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
            del dset

    @require_tf
    @require_torch
    def test_format_ragged_vectors(self, in_memory):
        import numpy as np
        import tensorflow as tf
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset = dset.map(lambda ex, i: {"vec": np.ones(3 + i) * i}, with_indices=True)
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
            del dset

    @require_tf
    @require_torch
    def test_format_nested(self, in_memory):
        import numpy as np
        import tensorflow as tf
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            dset = dset.map(lambda ex: {"nested": [{"foo": np.ones(3)}] * len(ex["filename"])}, batched=True)
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
            del dset

    def test_format_pandas(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            import pandas as pd

            dset.set_format("pandas")
            self.assertIsInstance(dset[0], pd.DataFrame)
            self.assertIsInstance(dset[:2], pd.DataFrame)
            self.assertIsInstance(dset["col_1"], pd.Series)
            del dset

    def test_transmit_format_single(self, in_memory):
        @transmit_format
        def my_single_transform(self, return_factory, *args, **kwargs):
            return return_factory()

        with tempfile.TemporaryDirectory() as tmp_dir:
            return_factory = partial(
                self._create_dummy_dataset, in_memory=in_memory, tmp_dir=tmp_dir, multiple_columns=True
            )
            dset = return_factory()
            dset.set_format("numpy", columns=["col_1"])
            prev_format = dset.format
            transformed_dset = my_single_transform(dset, return_factory)
            self.assertDictEqual(transformed_dset.format, prev_format)

            del dset, transformed_dset

    def test_transmit_format_dict(self, in_memory):
        @transmit_format
        def my_split_transform(self, return_factory, *args, **kwargs):
            return DatasetDict({"train": return_factory()})

        with tempfile.TemporaryDirectory() as tmp_dir:
            return_factory = partial(
                self._create_dummy_dataset, in_memory=in_memory, tmp_dir=tmp_dir, multiple_columns=True
            )
            dset = return_factory()
            dset.set_format("numpy", columns=["col_1"])
            prev_format = dset.format
            transformed_dset = my_split_transform(dset, return_factory)["train"]
            self.assertDictEqual(transformed_dset.format, prev_format)

            del dset, transformed_dset


class MiscellaneousDatasetTest(TestCase):
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

    def test_concatenate_mixed_memory_and_disk(self):
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
                _ = concatenate_datasets([dset1, dset2, dset3])
            del dset1, dset2, dset3
