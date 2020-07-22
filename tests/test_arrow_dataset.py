import os
import tempfile
from unittest import TestCase

import numpy as np
import pandas as pd
import pyarrow as pa

from nlp.arrow_dataset import Dataset
from nlp.features import Features, Sequence, Value


class BaseDatasetTest(TestCase):
    def _create_dummy_dataset(self):
        dset = Dataset(pa.Table.from_pydict({
            "filename": ["my_name-train" + "_" + str(x) for x in np.arange(30).tolist()]
        }))
        return dset

    def test_dummy_dataset(self):
        dset = self._create_dummy_dataset()
        self.assertDictEqual(dset.features, Features({"filename": Value("string")}))

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

        features = Features({"col_1": Value("string"), "col_2": Value("string")})
        self.assertRaises(pa.ArrowTypeError, Dataset.from_dict, data, features=features)

    def test_flatten(self):
        dset = Dataset.from_dict(
            {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10},
            features=Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")}),
        )
        dset.flatten()
        self.assertListEqual(dset.column_names, ["a.b.c", "foo"])
        self.assertListEqual(list(dset.features.keys()), ["a.b.c", "foo"])
        self.assertDictEqual(dset.features, Features({"a.b.c": [Value("string")], "foo": Value("int64")}))

    def test_map(self):
        dset = self._create_dummy_dataset()
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            dset_test = dset.map(
                lambda x: {"name": x["filename"][:-2], "id": int(x["filename"][-1])}, cache_file_name=tmp_file
            )
            self.assertEqual(len(dset_test), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_test.features, Features({
                "filename": Value("string"), "name": Value("string"), "id": Value("int64")
            }))

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_test_with_indices = dset.map(
                lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True, cache_file_name=tmp_file
            )
            self.assertEqual(len(dset_test_with_indices), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_test_with_indices.features, Features({
                "filename": Value("string"), "name": Value("string"), "id": Value("int64")
            }))

    def test_map_batched(self):
        dset = self._create_dummy_dataset()

        def map_batched(example):
            return {"filename_new": [x + "_extension" for x in example["filename"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_test_batched = dset.map(map_batched, batched=True, cache_file_name=tmp_file)
            self.assertEqual(len(dset_test_batched), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_test_batched.features, Features({
                "filename": Value("string"), "filename_new": Value("string")
            }))

        def map_batched_with_indices(example, idx):
            return {"filename_new": [x + "_extension_" + str(idx) for x in example["filename"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_test_with_indices_batched = dset.map(
                map_batched_with_indices, batched=True, with_indices=True, cache_file_name=tmp_file
            )
            self.assertEqual(len(dset_test_with_indices_batched), 30)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_test_with_indices_batched.features, Features({
                "filename": Value("string"), "filename_new": Value("string")
            }))

    def test_remove_colums(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.map(
                lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True, cache_file_name=tmp_file
            )
            self.assertTrue("id" in dset[0])
            self.assertDictEqual(dset.features, Features({
                "filename": Value("string"), "name": Value("string"), "id": Value("int64")
            }))

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.map(lambda x: x, remove_columns=["id"], cache_file_name=tmp_file)
            self.assertTrue("id" not in dset[0])
            self.assertDictEqual(dset.features, Features({
                "filename": Value("string"), "name": Value("string")
            }))

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

    def test_select(self):
        dset = self._create_dummy_dataset()
        # select every two example
        indices = list(range(0, len(dset), 2))

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_select_even = dset.select(indices, cache_file_name=tmp_file)
            self.assertEqual(len(dset_select_even), 15)
            for row in dset_select_even:
                self.assertEqual(int(row["filename"][-1]) % 2, 0)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_select_even.features, Features({"filename": Value("string")}))

    def test_shuffle(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset_shuffled = dset.shuffle(seed=1234, cache_file_name=tmp_file)
            self.assertEqual(len(dset_shuffled), 30)
            self.assertEqual(dset_shuffled[0]["filename"], "my_name-train_28")
            self.assertEqual(dset_shuffled[2]["filename"], "my_name-train_10")
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_shuffled.features, Features({"filename": Value("string")}))

            # Reproducibility
            tmp_file = os.path.join(tmp_dir, "test_2.arrow")
            dset_shuffled_2 = dset.shuffle(seed=1234, cache_file_name=tmp_file)
            self.assertListEqual(dset_shuffled["filename"], dset_shuffled_2["filename"])

    def test_sort(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Keep only 10 examples
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            dset = dset.select(range(10), cache_file_name=tmp_file)
            tmp_file = os.path.join(tmp_dir, "test_2.arrow")
            dset = dset.shuffle(seed=1234, cache_file_name=tmp_file)
            self.assertEqual(len(dset), 10)
            self.assertEqual(dset[0]["filename"], "my_name-train_8")
            self.assertEqual(dset[1]["filename"], "my_name-train_9")
            # Sort
            tmp_file = os.path.join(tmp_dir, "test_3.arrow")
            dset_sorted = dset.sort("filename", cache_file_name=tmp_file)
            for i, row in enumerate(dset_sorted):
                self.assertEqual(int(row["filename"][-1]), i)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sorted.features, Features({"filename": Value("string")}))
            # Sort reversed
            tmp_file = os.path.join(tmp_dir, "test_4.arrow")
            dset_sorted = dset.sort("filename", cache_file_name=tmp_file, reverse=True)
            for i, row in enumerate(dset_sorted):
                self.assertEqual(int(row["filename"][-1]), len(dset_sorted) - 1 - i)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sorted.features, Features({"filename": Value("string")}))

    def test_train_test_split(self):
        dset = self._create_dummy_dataset()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
            dset_dict = dset.train_test_split(
                test_size=10, shuffle=False, train_cache_file_name=tmp_file, test_cache_file_name=tmp_file_2
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
                test_size=0.5, shuffle=False, train_cache_file_name=tmp_file, test_cache_file_name=tmp_file_2
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
                train_size=10, shuffle=False, train_cache_file_name=tmp_file, test_cache_file_name=tmp_file_2
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
                train_size=10, train_cache_file_name=tmp_file, test_cache_file_name=tmp_file_2, seed=42
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
            dset = dset.select(range(10), cache_file_name=tmp_file)
            self.assertEqual(len(dset), 10)
            # Shard
            dset_sharded = dset.shard(num_shards=8, index=1)
            self.assertEqual(2, len(dset_sharded))
            self.assertEqual(["my_name-train_1", "my_name-train_9"], dset_sharded["filename"])
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sharded.features, Features({"filename": Value("string")}))
            # Shard contiguous
            dset_sharded_contiguous = dset.shard(num_shards=3, index=0, contiguous=True)
            self.assertEqual([f"my_name-train_{i}" for i in (0, 1, 2, 3)], dset_sharded_contiguous["filename"])
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertDictEqual(dset_sharded.features, Features({"filename": Value("string")}))
            # Test lengths of sharded contiguous
            self.assertEqual([4, 3, 3], [len(dset.shard(3, index=i, contiguous=True)) for i in range(3)])

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
            self.assertDictEqual(dset.features, Features({"filename": Value("string"), "vec": [Value("float64")]}))

            # don't test if torch and tensorflow are stacked accross examples
            # we need to use the features definition to know at what depth we have to to the conversion

            dset.set_format("tensorflow")
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            for col in columns:
                self.assertIsInstance(dset[0][col], (tf.Tensor, tf.RaggedTensor))
                self.assertIsInstance(dset[:2][col][0], (tf.Tensor, tf.RaggedTensor))  # not stacked

            dset.set_format("numpy")
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            for col in columns:
                self.assertIsInstance(dset[0][col], np.ndarray)
                self.assertIsInstance(dset[:2][col], np.ndarray)  # stacked
            self.assertEqual(dset[:2]["vec"].shape, (2, 3))  # stacked

            dset.set_format("torch", columns=["vec"])
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            # torch.Tensor is only for numerical columns
            self.assertIsInstance(dset[0]["vec"], torch.Tensor)
            self.assertIsInstance(dset[:2]["vec"][0], torch.Tensor)  # not stacked

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
            self.assertDictEqual(dset.features, Features({"filename": Value("string"), "nested": {"foo": [Value("float64")]}}))

            dset.set_format("tensorflow")
            self.assertIsNotNone(dset[0])
            self.assertIsInstance(dset[0]["nested"]["foo"], (tf.Tensor, tf.RaggedTensor))
            self.assertIsNotNone(dset[:2])
            self.assertIsInstance(dset[:2]["nested"][0]["foo"], (tf.Tensor, tf.RaggedTensor))

            dset.set_format("numpy")
            self.assertIsNotNone(dset[0])
            self.assertIsInstance(dset[0]["nested"]["foo"], np.ndarray)
            self.assertIsNotNone(dset[:2])
            self.assertIsInstance(dset[:2]["nested"][0]["foo"], np.ndarray)

            dset.set_format("torch", columns="nested")
            self.assertIsNotNone(dset[0])
            self.assertIsInstance(dset[0]["nested"]["foo"], torch.Tensor)
            self.assertIsNotNone(dset[:2])
            self.assertIsInstance(dset[:2]["nested"][0]["foo"], torch.Tensor)
