import copy
import os
import pickle
import tempfile
from functools import partial
from unittest import TestCase

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest
from absl.testing import parameterized

import datasets.arrow_dataset
from datasets import concatenate_datasets, temp_seed
from datasets.arrow_dataset import Dataset, transmit_format
from datasets.dataset_dict import DatasetDict
from datasets.features import Array2D, Array3D, ClassLabel, Features, Sequence, Value
from datasets.info import DatasetInfo
from datasets.utils.logging import WARNING

from .utils import assert_arrow_memory_doesnt_increase, require_tf, require_torch, require_transformers


class Unpicklable:
    def __getstate__(self):
        raise pickle.PicklingError()


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

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def _create_dummy_dataset(
        self, in_memory: bool, tmp_dir: str, multiple_columns=False, array_features=False
    ) -> Dataset:
        if multiple_columns:
            if array_features:
                data = {
                    "col_1": [[[True, False], [False, True]]] * 4,  # 2D
                    "col_2": [[[["a", "b"], ["c", "d"]], [["e", "f"], ["g", "h"]]]] * 4,  # 3D array
                    "col_3": [[3, 2, 1, 0]] * 4,  # Sequence
                }
                features = Features(
                    {
                        "col_1": Array2D(shape=(2, 2), dtype="bool"),
                        "col_2": Array3D(shape=(2, 2, 2), dtype="string"),
                        "col_3": Sequence(feature=Value("int64")),
                    }
                )
            else:
                data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"], "col_3": [False, True, False, True]}
                features = None
            dset = Dataset.from_dict(data, features=features)
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

    def test_dummy_dataset_deepcopy(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir).select(range(10)) as dset:
                with assert_arrow_memory_doesnt_increase():
                    dset2 = copy.deepcopy(dset)
                # don't copy the underlying arrow data using memory
                self.assertEqual(len(dset2), 10)
                self.assertDictEqual(dset2.features, Features({"filename": Value("string")}))
                self.assertEqual(dset2[0]["filename"], "my_name-train_0")
                self.assertEqual(dset2["filename"][0], "my_name-train_0")
                del dset2

    def test_dummy_dataset_pickle(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "dset.pt")

            with self._create_dummy_dataset(in_memory, tmp_dir).select(range(10)) as dset:
                with open(tmp_file, "wb") as f:
                    pickle.dump(dset, f)

            with open(tmp_file, "rb") as f:
                with pickle.load(f) as dset:
                    self.assertEqual(len(dset), 10)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertEqual(dset[0]["filename"], "my_name-train_0")
                    self.assertEqual(dset["filename"][0], "my_name-train_0")

            with self._create_dummy_dataset(in_memory, tmp_dir).select(
                range(10), indices_cache_file_name=os.path.join(tmp_dir, "ind.arrow")
            ) as dset:
                if not in_memory:
                    dset._data.table = Unpicklable()
                dset._indices.table = Unpicklable()
                with open(tmp_file, "wb") as f:
                    pickle.dump(dset, f)

            with open(tmp_file, "rb") as f:
                with pickle.load(f) as dset:
                    self.assertEqual(len(dset), 10)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertEqual(dset[0]["filename"], "my_name-train_0")
                    self.assertEqual(dset["filename"][0], "my_name-train_0")

    def test_concatenate_pickle(self, in_memory):
        data1, data2, data3 = {"id": [0, 1, 2] * 2}, {"id": [3, 4, 5] * 2}, {"id": [6, 7], "foo": ["bar", "bar"]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset1, dset2, dset3 = (
                Dataset.from_dict(data1, info=info1),
                Dataset.from_dict(data2, info=info2),
                Dataset.from_dict(data3),
            )
            # mix from in-memory and on-disk datasets
            dset1, dset2 = self._to(in_memory, tmp_dir, dset1, dset2)
            dset3 = self._to(not in_memory, tmp_dir, dset3)
            dset1, dset2, dset3 = (
                dset1.select(
                    [0, 1, 2],
                    keep_in_memory=in_memory,
                    indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow") if not in_memory else None,
                ),
                dset2.select(
                    [0, 1, 2],
                    keep_in_memory=in_memory,
                    indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow") if not in_memory else None,
                ),
                dset3.select(
                    [0, 1],
                    keep_in_memory=in_memory,
                    indices_cache_file_name=os.path.join(tmp_dir, "i3.arrow") if not in_memory else None,
                ),
            )

            dset3 = dset3.rename_column("foo", "new_foo")
            dset3.remove_columns_("new_foo")
            if in_memory:
                dset3._data.table = Unpicklable()
            else:
                dset1._data.table, dset2._data.table = Unpicklable(), Unpicklable()
            dset1, dset2, dset3 = [pickle.loads(pickle.dumps(d)) for d in (dset1, dset2, dset3)]
            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                if not in_memory:
                    dset_concat._data.table = Unpicklable()
                with pickle.loads(pickle.dumps(dset_concat)) as dset_concat:
                    self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
                    self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
                    self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
                    # in_memory = True: 1 cache file for dset3
                    # in_memory = False: 2 caches files for dset1 and dset2, and 1 cache file for i1.arrow
                    self.assertEqual(len(dset_concat.cache_files), 1 if in_memory else 2 + 1)
                    self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")
            del dset1, dset2, dset3

    def test_map_caching(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(WARNING):
                with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                    with dset.map(lambda x: {"foo": "bar"}) as dset_test1:
                        dset_test1_data_files = list(dset_test1.cache_files)
                    with dset.map(lambda x: {"foo": "bar"}) as dset_test2:
                        self.assertEqual(dset_test1_data_files, dset_test2.cache_files)
                        self.assertEqual(len(dset_test2.cache_files), 1 - int(in_memory))
                        self.assertTrue(("Loading cached processed dataset" in self._caplog.text) ^ in_memory)

        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(WARNING):
                with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                    with dset.map(lambda x: {"foo": "bar"}) as dset_test1:
                        dset_test1_data_files = list(dset_test1.cache_files)
                    with dset.map(lambda x: {"foo": "bar"}, load_from_cache_file=False) as dset_test2:
                        self.assertEqual(dset_test1_data_files, dset_test2.cache_files)
                        self.assertEqual(len(dset_test2.cache_files), 1 - int(in_memory))
                        self.assertNotIn("Loading cached processed dataset", self._caplog.text)

        if not in_memory:
            try:
                self._caplog.clear()
                with tempfile.TemporaryDirectory() as tmp_dir:
                    with self._caplog.at_level(WARNING):
                        with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                            datasets.set_caching_enabled(False)
                            with dset.map(lambda x: {"foo": "bar"}) as dset_test1:
                                with dset.map(lambda x: {"foo": "bar"}) as dset_test2:
                                    self.assertNotEqual(dset_test1.cache_files, dset_test2.cache_files)
                                    self.assertEqual(len(dset_test1.cache_files), 1)
                                    self.assertEqual(len(dset_test2.cache_files), 1)
                                    self.assertNotIn("Loading cached processed dataset", self._caplog.text)
                                    # make sure the arrow files are going to be removed
                                    self.assertIn("tmp", dset_test1.cache_files[0])
                                    self.assertIn("tmp", dset_test2.cache_files[0])
            finally:
                datasets.set_caching_enabled(True)

    @require_torch
    def test_map_torch(self, in_memory):
        import torch

        def func(example):
            return {"tensor": torch.tensor([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "tensor": Sequence(Value("float64"))}),
                    )
                    self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])

    @require_tf
    def test_map_tf(self, in_memory):
        import tensorflow as tf

        def func(example):
            return {"tensor": tf.constant([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "tensor": Sequence(Value("float64"))}),
                    )
                    self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])

    def test_map_numpy(self, in_memory):
        def func(example):
            return {"tensor": np.array([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "tensor": Sequence(Value("float64"))}),
                    )
                    self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])

    def test_map_remove_colums(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True) as dset:
                    self.assertTrue("id" in dset[0])
                    self.assertDictEqual(
                        dset.features,
                        Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
                    )

                    with dset.map(lambda x: x, remove_columns=["id"]) as dset:
                        self.assertTrue("id" not in dset[0])
                        self.assertDictEqual(
                            dset.features, Features({"filename": Value("string"), "name": Value("string")})
                        )

    def test_map_stateful_callable(self, in_memory):
        # be sure that the state of the map callable is unaffected
        # before processing the dataset examples

        class ExampleCounter:
            def __init__(self, batched=False):
                self.batched = batched
                # state
                self.cnt = 0

            def __call__(self, example):
                if self.batched:
                    self.cnt += len(example)
                else:
                    self.cnt += 1

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:

                ex_cnt = ExampleCounter()
                dset.map(ex_cnt)
                self.assertEqual(ex_cnt.cnt, len(dset))

                ex_cnt = ExampleCounter(batched=True)
                dset.map(ex_cnt)
                self.assertEqual(ex_cnt.cnt, len(dset))

    def test_filter(self, in_memory):
        # keep only first five examples

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.filter(lambda x, i: i < 5, with_indices=True) as dset_filter_first_five:
                    self.assertEqual(len(dset_filter_first_five), 5)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_filter_first_five.features, Features({"filename": Value("string")}))
                    self.assertNotEqual(dset_filter_first_five._fingerprint, fingerprint)

        # filter filenames with even id at the end + formatted
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                dset.set_format("numpy")
                fingerprint = dset._fingerprint
                with dset.filter(lambda x: (int(x["filename"][-1]) % 2 == 0)) as dset_filter_even_num:
                    self.assertEqual(len(dset_filter_even_num), 15)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_filter_even_num.features, Features({"filename": Value("string")}))
                    self.assertNotEqual(dset_filter_even_num._fingerprint, fingerprint)
                    self.assertEqual(dset_filter_even_num.format["type"], "numpy")

    def test_filter_multiprocessing(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.filter(picklable_filter_function, num_proc=2) as dset_filter_first_ten:
                    self.assertEqual(len(dset_filter_first_ten), 10)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_filter_first_ten.features, Features({"filename": Value("string")}))
                    # only one cache file since the there is only 10 examples from the 1 processed shard
                    self.assertEqual(len(dset_filter_first_ten.cache_files), 0 if in_memory else 1)
                    self.assertNotEqual(dset_filter_first_ten._fingerprint, fingerprint)

    def test_keep_features_after_transform_specified(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    with dset.map(invert_labels, features=features) as inverted_dset:
                        self.assertEqual(inverted_dset.features.type, features.type)
                        self.assertDictEqual(inverted_dset.features, features)

    def test_keep_features_after_transform_unspecified(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    with dset.map(invert_labels) as inverted_dset:
                        self.assertEqual(inverted_dset.features.type, features.type)
                        self.assertDictEqual(inverted_dset.features, features)

    def test_keep_features_after_transform_to_file(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    tmp_file = os.path.join(tmp_dir, "test.arrow")
                    dset.map(invert_labels, cache_file_name=tmp_file)
                    with Dataset.from_file(tmp_file) as inverted_dset:
                        self.assertEqual(inverted_dset.features.type, features.type)
                        self.assertDictEqual(inverted_dset.features, features)

    def test_keep_features_after_transform_to_memory(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    with dset.map(invert_labels, keep_in_memory=True) as inverted_dset:
                        self.assertEqual(inverted_dset.features.type, features.type)
                        self.assertDictEqual(inverted_dset.features, features)

    def test_keep_features_after_loading_from_cache(self, in_memory):
        features = Features(
            {"tokens": Sequence(Value("string")), "labels": Sequence(ClassLabel(names=["negative", "positive"]))}
        )

        def invert_labels(x):
            return {"labels": [(1 - label) for label in x["labels"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    tmp_file1 = os.path.join(tmp_dir, "test1.arrow")
                    tmp_file2 = os.path.join(tmp_dir, "test2.arrow")
                    # TODO: Why mapped twice?
                    inverted_dset = dset.map(invert_labels, cache_file_name=tmp_file1)
                    inverted_dset = dset.map(invert_labels, cache_file_name=tmp_file2)
                    self.assertGreater(len(inverted_dset.cache_files), 0)
                    self.assertEqual(inverted_dset.features.type, features.type)
                    self.assertDictEqual(inverted_dset.features, features)
                    del inverted_dset

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
            with Dataset.from_dict(
                {"tokens": [["foo"] * 5] * 10, "labels": [[1] * 5] * 10}, features=features
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    with dset.map(invert_labels) as inverted_dset:
                        self.assertEqual(inverted_dset.features.type, expected_features.type)
                        self.assertDictEqual(inverted_dset.features, expected_features)

    def test_select(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                # select every two example
                indices = list(range(0, len(dset), 2))
                tmp_file = os.path.join(tmp_dir, "test.arrow")
                fingerprint = dset._fingerprint
                with dset.select(indices, indices_cache_file_name=tmp_file) as dset_select_even:
                    self.assertEqual(len(dset_select_even), 15)
                    for row in dset_select_even:
                        self.assertEqual(int(row["filename"][-1]) % 2, 0)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_select_even.features, Features({"filename": Value("string")}))
                    self.assertNotEqual(dset_select_even._fingerprint, fingerprint)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
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
                with dset.select(
                    range(5),
                    indices_cache_file_name=tmp_file,
                    writer_batch_size=2,
                ) as dset_select_five:
                    self.assertTrue(os.path.exists(tmp_file))
                    self.assertEqual(len(dset_select_five), 5)
                    self.assertEqual(dset_select_five.format["type"], "numpy")
                    for i, row in enumerate(dset_select_five):
                        self.assertEqual(int(row["filename"][-1]), i)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_select_five.features, Features({"filename": Value("string")}))

    def test_select_then_map(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.select([0]) as d1:
                    with d1.map(lambda x: {"id": int(x["filename"].split("_")[-1])}) as d1:
                        self.assertEqual(d1[0]["id"], 0)
                with dset.select([1]) as d2:
                    with d2.map(lambda x: {"id": int(x["filename"].split("_")[-1])}) as d2:
                        self.assertEqual(d2[0]["id"], 1)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.select([0], indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow")) as d1:
                    with d1.map(lambda x: {"id": int(x["filename"].split("_")[-1])}) as d1:
                        self.assertEqual(d1[0]["id"], 0)
                with dset.select([1], indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow")) as d2:
                    with d2.map(lambda x: {"id": int(x["filename"].split("_")[-1])}) as d2:
                        self.assertEqual(d2[0]["id"], 1)

    def test_pickle_after_many_transforms_on_disk(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertEqual(len(dset.cache_files), 0 if in_memory else 1)
                dset.rename_column_("filename", "file")
                self.assertListEqual(dset.column_names, ["file"])
                with dset.select(range(5)) as dset:
                    self.assertEqual(len(dset), 5)
                    with dset.map(lambda x: {"id": int(x["file"][-1])}) as dset:
                        self.assertListEqual(sorted(dset.column_names), ["file", "id"])
                        dset.rename_column_("id", "number")
                        self.assertListEqual(sorted(dset.column_names), ["file", "number"])
                        with dset.select([1]) as dset:
                            self.assertEqual(dset[0]["file"], "my_name-train_1")
                            self.assertEqual(dset[0]["number"], 1)

                            self.assertEqual(dset._indices["indices"].to_pylist(), [1])
                            if not in_memory:
                                self.assertEqual(
                                    dset._data.replays,
                                    [("rename_columns", (["file", "number"],), {})],
                                )
                            if not in_memory:
                                dset._data.table = Unpicklable()  # check that we don't pickle the entire table

                            pickled = pickle.dumps(dset)
                            with pickle.loads(pickled) as loaded:
                                self.assertEqual(loaded[0]["file"], "my_name-train_1")
                                self.assertEqual(loaded[0]["number"], 1)

    def test_shuffle(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                tmp_file = os.path.join(tmp_dir, "test.arrow")
                fingerprint = dset._fingerprint
                with dset.shuffle(seed=1234, indices_cache_file_name=tmp_file) as dset_shuffled:
                    self.assertEqual(len(dset_shuffled), 30)
                    self.assertEqual(dset_shuffled[0]["filename"], "my_name-train_28")
                    self.assertEqual(dset_shuffled[2]["filename"], "my_name-train_10")
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_shuffled.features, Features({"filename": Value("string")}))
                    self.assertNotEqual(dset_shuffled._fingerprint, fingerprint)

                    # Reproducibility
                    tmp_file = os.path.join(tmp_dir, "test_2.arrow")
                    with dset.shuffle(seed=1234, indices_cache_file_name=tmp_file) as dset_shuffled_2:
                        self.assertListEqual(dset_shuffled["filename"], dset_shuffled_2["filename"])

                    # Compatible with temp_seed
                    with temp_seed(42), dset.shuffle() as d1:
                        with temp_seed(42), dset.shuffle() as d2, dset.shuffle() as d3:
                            self.assertListEqual(d1["filename"], d2["filename"])
                            self.assertEqual(d1._fingerprint, d2._fingerprint)
                            self.assertNotEqual(d3["filename"], d2["filename"])
                            self.assertNotEqual(d3._fingerprint, d2._fingerprint)

    def test_sort(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                # Keep only 10 examples
                tmp_file = os.path.join(tmp_dir, "test.arrow")
                with dset.select(range(10), indices_cache_file_name=tmp_file) as dset:
                    tmp_file = os.path.join(tmp_dir, "test_2.arrow")
                    with dset.shuffle(seed=1234, indices_cache_file_name=tmp_file) as dset:
                        self.assertEqual(len(dset), 10)
                        self.assertEqual(dset[0]["filename"], "my_name-train_8")
                        self.assertEqual(dset[1]["filename"], "my_name-train_9")
                        # Sort
                        tmp_file = os.path.join(tmp_dir, "test_3.arrow")
                        fingerprint = dset._fingerprint
                        with dset.sort("filename", indices_cache_file_name=tmp_file) as dset_sorted:
                            for i, row in enumerate(dset_sorted):
                                self.assertEqual(int(row["filename"][-1]), i)
                            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                            self.assertDictEqual(dset_sorted.features, Features({"filename": Value("string")}))
                            self.assertNotEqual(dset_sorted._fingerprint, fingerprint)
                            # Sort reversed
                            tmp_file = os.path.join(tmp_dir, "test_4.arrow")
                            fingerprint = dset._fingerprint
                            with dset.sort("filename", indices_cache_file_name=tmp_file, reverse=True) as dset_sorted:
                                for i, row in enumerate(dset_sorted):
                                    self.assertEqual(int(row["filename"][-1]), len(dset_sorted) - 1 - i)
                                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                                self.assertDictEqual(dset_sorted.features, Features({"filename": Value("string")}))
                                self.assertNotEqual(dset_sorted._fingerprint, fingerprint)
                            # formatted
                            dset.set_format("numpy")
                            with dset.sort("filename") as dset_sorted_formatted:
                                self.assertEqual(dset_sorted_formatted.format["type"], "numpy")

    @require_tf
    def test_export(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                # Export the data
                tfrecord_path = os.path.join(tmp_dir, "test.tfrecord")
                with dset.map(
                    lambda ex, i: {
                        "id": i,
                        "question": f"Question {i}",
                        "answers": {"text": [f"Answer {i}-0", f"Answer {i}-1"], "answer_start": [0, 1]},
                    },
                    with_indices=True,
                    remove_columns=["filename"],
                ) as formatted_dset:
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

    def test_to_csv(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # File path argument
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                file_path = os.path.join(tmp_dir, "test_path.csv")
                bytes_written = dset.to_csv(path_or_buf=file_path)

                self.assertTrue(os.path.isfile(file_path))
                self.assertEqual(bytes_written, os.path.getsize(file_path))
                csv_dset = pd.read_csv(file_path, header=0, index_col=0)

                self.assertEqual(csv_dset.shape, dset.shape)
                self.assertListEqual(list(csv_dset.columns), list(dset.column_names))

            # File buffer argument
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                file_path = os.path.join(tmp_dir, "test_buffer.csv")
                with open(file_path, "wb+") as buffer:
                    bytes_written = dset.to_csv(path_or_buf=buffer)

                self.assertTrue(os.path.isfile(file_path))
                self.assertEqual(bytes_written, os.path.getsize(file_path))
                csv_dset = pd.read_csv(file_path, header=0, index_col=0)

                self.assertEqual(csv_dset.shape, dset.shape)
                self.assertListEqual(list(csv_dset.columns), list(dset.column_names))

            # After a select/shuffle transform
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset = dset.select(range(0, len(dset), 2)).shuffle()
                file_path = os.path.join(tmp_dir, "test_path.csv")
                bytes_written = dset.to_csv(path_or_buf=file_path)

                self.assertTrue(os.path.isfile(file_path))
                self.assertEqual(bytes_written, os.path.getsize(file_path))
                csv_dset = pd.read_csv(file_path, header=0, index_col=0)

                self.assertEqual(csv_dset.shape, dset.shape)
                self.assertListEqual(list(csv_dset.columns), list(dset.column_names))

            # With array features
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True, array_features=True) as dset:
                file_path = os.path.join(tmp_dir, "test_path.csv")
                bytes_written = dset.to_csv(path_or_buf=file_path)

                self.assertTrue(os.path.isfile(file_path))
                self.assertEqual(bytes_written, os.path.getsize(file_path))
                csv_dset = pd.read_csv(file_path, header=0, index_col=0)

                self.assertEqual(csv_dset.shape, dset.shape)
                self.assertListEqual(list(csv_dset.columns), list(dset.column_names))

    def test_to_dict(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Batched
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                bacth_size = dset.num_rows - 1
                to_dict_generator = dset.to_dict(batched=True, batch_size=bacth_size)

                for batch in to_dict_generator:
                    self.assertIsInstance(batch, dict)
                    self.assertListEqual(sorted(batch.keys()), sorted(dset.column_names))
                    for col_name in dset.column_names:
                        self.assertIsInstance(batch[col_name], list)
                        self.assertLessEqual(len(batch[col_name]), bacth_size)

                # Full
                dset_to_dict = dset.to_dict()
                self.assertIsInstance(dset_to_dict, dict)
                self.assertListEqual(sorted(dset_to_dict.keys()), sorted(dset.column_names))

                for col_name in dset.column_names:
                    self.assertLessEqual(len(dset_to_dict[col_name]), len(dset))

                # With index mapping
                with dset.select([1, 0, 3]) as dset:
                    dset_to_dict = dset.to_dict()
                    self.assertIsInstance(dset_to_dict, dict)
                    self.assertEqual(len(dset_to_dict), 3)
                    self.assertListEqual(sorted(dset_to_dict.keys()), sorted(dset.column_names))

                    for col_name in dset.column_names:
                        self.assertIsInstance(dset_to_dict[col_name], list)
                        self.assertEqual(len(dset_to_dict[col_name]), len(dset))

    def test_to_pandas(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Batched
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                bacth_size = dset.num_rows - 1
                to_pandas_generator = dset.to_pandas(batched=True, batch_size=bacth_size)

                for batch in to_pandas_generator:
                    self.assertIsInstance(batch, pd.DataFrame)
                    self.assertListEqual(sorted(batch.columns), sorted(dset.column_names))
                    for col_name in dset.column_names:
                        self.assertLessEqual(len(batch[col_name]), bacth_size)

                # Full
                dset_to_pandas = dset.to_pandas()
                self.assertIsInstance(dset_to_pandas, pd.DataFrame)
                self.assertListEqual(sorted(dset_to_pandas.columns), sorted(dset.column_names))
                for col_name in dset.column_names:
                    self.assertEqual(len(dset_to_pandas[col_name]), len(dset))

                # With index mapping
                with dset.select([1, 0, 3]) as dset:
                    dset_to_pandas = dset.to_pandas()
                    self.assertIsInstance(dset_to_pandas, pd.DataFrame)
                    self.assertEqual(len(dset_to_pandas), 3)
                    self.assertListEqual(sorted(dset_to_pandas.columns), sorted(dset.column_names))

                    for col_name in dset.column_names:
                        self.assertEqual(len(dset_to_pandas[col_name]), dset.num_rows)

    def test_train_test_split(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
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
                del dset_test, dset_train, dset_dict  # DatasetDict

    def test_shard(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir, self._create_dummy_dataset(in_memory, tmp_dir) as dset:
            tmp_file = os.path.join(tmp_dir, "test.arrow")
            with dset.select(range(10), indices_cache_file_name=tmp_file) as dset:
                self.assertEqual(len(dset), 10)
                # Shard
                tmp_file_1 = os.path.join(tmp_dir, "test_1.arrow")
                fingerprint = dset._fingerprint
                with dset.shard(num_shards=8, index=1, indices_cache_file_name=tmp_file_1) as dset_sharded:
                    self.assertEqual(2, len(dset_sharded))
                    self.assertEqual(["my_name-train_1", "my_name-train_9"], dset_sharded["filename"])
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_sharded.features, Features({"filename": Value("string")}))
                    self.assertNotEqual(dset_sharded._fingerprint, fingerprint)
                # Shard contiguous
                tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
                with dset.shard(
                    num_shards=3, index=0, contiguous=True, indices_cache_file_name=tmp_file_2
                ) as dset_sharded_contiguous:
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
                with dset.shard(num_shards=3, index=0) as dset_sharded_formatted:
                    self.assertEqual(dset_sharded_formatted.format["type"], "numpy")

    def test_flatten_indices(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertEqual(dset._indices, None)

                tmp_file = os.path.join(tmp_dir, "test.arrow")
                with dset.select(range(10), indices_cache_file_name=tmp_file) as dset:
                    self.assertEqual(len(dset), 10)

                    self.assertNotEqual(dset._indices, None)

                    # Test unique fail
                    with self.assertRaises(ValueError):
                        dset.unique(dset.column_names[0])

                    tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
                    fingerprint = dset._fingerprint
                    dset.set_format("numpy")
                    with dset.flatten_indices(cache_file_name=tmp_file_2) as dset:
                        self.assertEqual(len(dset), 10)
                        self.assertEqual(dset._indices, None)
                        self.assertNotEqual(dset._fingerprint, fingerprint)
                        self.assertEqual(dset.format["type"], "numpy")
                        # Test unique works
                        dset.unique(dset.column_names[0])

    @require_tf
    @require_torch
    def test_format_vectors(self, in_memory):
        import numpy as np
        import tensorflow as tf
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir, self._create_dummy_dataset(
            in_memory, tmp_dir
        ) as dset, dset.map(lambda ex, i: {"vec": np.ones(3) * i}, with_indices=True) as dset:
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
            self.assertIsInstance(dset[0]["filename"], np.str_)
            self.assertIsInstance(dset[:2]["filename"], np.ndarray)
            self.assertIsInstance(dset["filename"], np.ndarray)
            self.assertIsInstance(dset[0]["vec"], np.ndarray)
            self.assertIsInstance(dset[:2]["vec"], np.ndarray)
            self.assertIsInstance(dset["vec"], np.ndarray)
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

    @require_tf
    @require_torch
    def test_format_ragged_vectors(self, in_memory):
        import numpy as np
        import tensorflow as tf
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir, self._create_dummy_dataset(
            in_memory, tmp_dir
        ) as dset, dset.map(lambda ex, i: {"vec": np.ones(3 + i) * i}, with_indices=True) as dset:
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
            self.assertIsInstance(dset[0]["filename"], np.str_)
            self.assertIsInstance(dset[:2]["filename"], np.ndarray)
            self.assertIsInstance(dset["filename"], np.ndarray)
            self.assertIsInstance(dset[0]["vec"], np.ndarray)
            self.assertIsInstance(dset[:2]["vec"], np.ndarray)
            self.assertIsInstance(dset["vec"], np.ndarray)
            # array is flat for ragged vectors in numpy
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

    @require_tf
    @require_torch
    def test_format_nested(self, in_memory):
        import numpy as np
        import tensorflow as tf
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir, self._create_dummy_dataset(
            in_memory, tmp_dir
        ) as dset, dset.map(lambda ex: {"nested": [{"foo": np.ones(3)}] * len(ex["filename"])}, batched=True) as dset:
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

    def test_format_pandas(self, in_memory):
        import pandas as pd

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.set_format("pandas")
                self.assertIsInstance(dset[0], pd.DataFrame)
                self.assertIsInstance(dset[:2], pd.DataFrame)
                self.assertIsInstance(dset["col_1"], pd.Series)

    def test_transmit_format_single(self, in_memory):
        @transmit_format
        def my_single_transform(self, return_factory, *args, **kwargs):
            return return_factory()

        with tempfile.TemporaryDirectory() as tmp_dir:
            return_factory = partial(
                self._create_dummy_dataset, in_memory=in_memory, tmp_dir=tmp_dir, multiple_columns=True
            )
            with return_factory() as dset:
                dset.set_format("numpy", columns=["col_1"])
                prev_format = dset.format
                with my_single_transform(dset, return_factory) as transformed_dset:
                    self.assertDictEqual(transformed_dset.format, prev_format)

    def test_transmit_format_dict(self, in_memory):
        @transmit_format
        def my_split_transform(self, return_factory, *args, **kwargs):
            return DatasetDict({"train": return_factory()})

        with tempfile.TemporaryDirectory() as tmp_dir:
            return_factory = partial(
                self._create_dummy_dataset, in_memory=in_memory, tmp_dir=tmp_dir, multiple_columns=True
            )
            with return_factory() as dset:
                dset.set_format("numpy", columns=["col_1"])
                prev_format = dset.format
                transformed_dset = my_split_transform(dset, return_factory)["train"]
                self.assertDictEqual(transformed_dset.format, prev_format)

                del transformed_dset  # DatasetDict

    def test_with_format(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                with dset.with_format("numpy", columns=["col_1"]) as dset2:
                    dset.set_format("numpy", columns=["col_1"])
                    self.assertDictEqual(dset.format, dset2.format)
                    self.assertEqual(dset._fingerprint, dset2._fingerprint)
                    # dset.reset_format()
                    # self.assertNotEqual(dset.format, dset2.format)
                    # self.assertNotEqual(dset._fingerprint, dset2._fingerprint)

    def test_with_transform(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                transform = lambda x: {"foo": x["col_1"]}  # noqa: E731
                with dset.with_transform(transform, columns=["col_1"]) as dset2:
                    dset.set_transform(transform, columns=["col_1"])
                    self.assertDictEqual(dset.format, dset2.format)
                    self.assertEqual(dset._fingerprint, dset2._fingerprint)
                    dset.reset_format()
                    self.assertNotEqual(dset.format, dset2.format)
                    self.assertNotEqual(dset._fingerprint, dset2._fingerprint)


class MiscellaneousDatasetTest(TestCase):
    def test_from_pandas(self):
        data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
        df = pd.DataFrame.from_dict(data)
        with Dataset.from_pandas(df) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
            self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("string")})
        with Dataset.from_pandas(df, features=features) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
            self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("string")})
        with Dataset.from_pandas(df, features=features, info=DatasetInfo(features=features)) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
            self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("string"), "col_2": Value("string")})
        self.assertRaises(pa.ArrowTypeError, Dataset.from_pandas, df, features=features)

    def test_from_dict(self):
        data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
        with Dataset.from_dict(data) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
            self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("string")})
        with Dataset.from_dict(data, features=features) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
            self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("string")})
        with Dataset.from_dict(data, features=features, info=DatasetInfo(features=features)) as dset:
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
            with Dataset.from_dict(data1, info=info1).map(
                cache_file_name=os.path.join(tmp_dir, "d1.arrow")
            ) as dset1, Dataset.from_dict(data2, info=info2).map(
                cache_file_name=os.path.join(tmp_dir, "d2.arrow")
            ) as dset2, Dataset.from_dict(
                data3
            ) as dset3:
                with concatenate_datasets([dset1, dset2, dset3]) as concatenated_dset:
                    self.assertEqual(len(concatenated_dset), len(dset1) + len(dset2) + len(dset3))
                    self.assertListEqual(concatenated_dset["id"], dset1["id"] + dset2["id"] + dset3["id"])

    @require_transformers
    def test_set_format_encode(self):
        from transformers import BertTokenizer

        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        def encode(batch):
            return tokenizer(batch["text"], padding="longest", return_tensors="np")

        with Dataset.from_dict({"text": ["hello there", "foo"]}) as dset:
            dset.set_transform(transform=encode)
            self.assertEqual(str(dset[:2]), str(encode({"text": ["hello there", "foo"]})))
