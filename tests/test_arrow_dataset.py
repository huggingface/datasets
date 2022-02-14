import copy
import itertools
import json
import os
import pickle
import re
import tempfile
from functools import partial
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest
from absl.testing import parameterized

import datasets.arrow_dataset
from datasets import concatenate_datasets, interleave_datasets, load_from_disk, temp_seed
from datasets.arrow_dataset import Dataset, transmit_format, update_metadata_with_features
from datasets.dataset_dict import DatasetDict
from datasets.features import Array2D, Array3D, ClassLabel, Features, Sequence, Value
from datasets.filesystems import extract_path_from_uri
from datasets.info import DatasetInfo
from datasets.splits import NamedSplit
from datasets.table import ConcatenationTable, InMemoryTable, MemoryMappedTable
from datasets.tasks import (
    AutomaticSpeechRecognition,
    LanguageModeling,
    QuestionAnsweringExtractive,
    Summarization,
    TextClassification,
)
from datasets.utils.logging import WARNING

from .conftest import s3_test_bucket_name
from .utils import (
    assert_arrow_memory_doesnt_increase,
    assert_arrow_memory_increases,
    require_jax,
    require_s3,
    require_tf,
    require_torch,
    require_transformers,
    set_current_working_directory_to_temp_dir,
)


class Unpicklable:
    def __getstate__(self):
        raise pickle.PicklingError()


def picklable_map_function(x):
    return {"id": int(x["filename"].split("_")[-1])}


def picklable_map_function_with_indices(x, i):
    return {"id": i}


def picklable_map_function_with_rank(x, r):
    return {"rank": r}


def picklable_map_function_with_indices_and_rank(x, i, r):
    return {"id": i, "rank": r}


def picklable_filter_function(x):
    return int(x["filename"].split("_")[-1]) < 10


def assert_arrow_metadata_are_synced_with_dataset_features(dataset: Dataset):
    assert dataset.data.schema.metadata is not None
    assert b"huggingface" in dataset.data.schema.metadata
    metadata = json.loads(dataset.data.schema.metadata[b"huggingface"].decode())
    assert "info" in metadata
    features = DatasetInfo.from_dict(metadata["info"]).features
    assert features is not None
    assert dataset.features is not None
    assert sorted(features) == sorted(field.name for field in dataset.data.schema)


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
        self, in_memory: bool, tmp_dir: str, multiple_columns=False, array_features=False, nested_features=False
    ) -> Dataset:
        assert int(multiple_columns) + int(array_features) + int(nested_features) < 2
        if multiple_columns:
            data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"], "col_3": [False, True, False, True]}
            dset = Dataset.from_dict(data)
        elif array_features:
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
            dset = Dataset.from_dict(data, features=features)
        elif nested_features:
            data = {"nested": [{"a": i, "x": i * 10, "c": i * 100} for i in range(1, 11)]}
            features = Features({"nested": {"a": Value("int64"), "x": Value("int64"), "c": Value("int64")}})
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

    def test_dummy_dataset(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:

            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertEqual(dset[0]["filename"], "my_name-train_0")
                self.assertEqual(dset["filename"][0], "my_name-train_0")

            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                self.assertDictEqual(
                    dset.features,
                    Features({"col_1": Value("int64"), "col_2": Value("string"), "col_3": Value("bool")}),
                )
                self.assertEqual(dset[0]["col_1"], 3)
                self.assertEqual(dset["col_1"][0], 3)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, array_features=True) as dset:
                self.assertDictEqual(
                    dset.features,
                    Features(
                        {
                            "col_1": Array2D(shape=(2, 2), dtype="bool"),
                            "col_2": Array3D(shape=(2, 2, 2), dtype="string"),
                            "col_3": Sequence(feature=Value("int64")),
                        }
                    ),
                )
                self.assertEqual(dset[0]["col_2"], [[["a", "b"], ["c", "d"]], [["e", "f"], ["g", "h"]]])
                self.assertEqual(dset["col_2"][0], [[["a", "b"], ["c", "d"]], [["e", "f"], ["g", "h"]]])

    def test_dataset_getitem(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
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

                with dset.select(range(2)) as dset_subset:
                    self.assertListEqual(dset_subset[-1:]["filename"], ["my_name-train_1"])
                    self.assertListEqual(dset_subset["filename"][-1:], ["my_name-train_1"])

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

    def test_dummy_dataset_serialize(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with set_current_working_directory_to_temp_dir():
                with self._create_dummy_dataset(in_memory, tmp_dir).select(range(10)) as dset:
                    dataset_path = "my_dataset"  # rel path
                    dset.save_to_disk(dataset_path)

                with Dataset.load_from_disk(dataset_path) as dset:
                    self.assertEqual(len(dset), 10)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertEqual(dset[0]["filename"], "my_name-train_0")
                    self.assertEqual(dset["filename"][0], "my_name-train_0")

            with self._create_dummy_dataset(in_memory, tmp_dir).select(range(10)) as dset:
                dataset_path = os.path.join(tmp_dir, "my_dataset")  # abs path
                dset.save_to_disk(dataset_path)

            with Dataset.load_from_disk(dataset_path) as dset:
                self.assertEqual(len(dset), 10)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertEqual(dset[0]["filename"], "my_name-train_0")
                self.assertEqual(dset["filename"][0], "my_name-train_0")

            with self._create_dummy_dataset(in_memory, tmp_dir).select(
                range(10), indices_cache_file_name=os.path.join(tmp_dir, "ind.arrow")
            ) as dset:
                with assert_arrow_memory_doesnt_increase():
                    dset.save_to_disk(dataset_path)

            with Dataset.load_from_disk(dataset_path) as dset:
                self.assertEqual(len(dset), 10)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertEqual(dset[0]["filename"], "my_name-train_0")
                self.assertEqual(dset["filename"][0], "my_name-train_0")

            with self._create_dummy_dataset(in_memory, tmp_dir, nested_features=True) as dset:
                with assert_arrow_memory_doesnt_increase():
                    dset.save_to_disk(dataset_path)

            with Dataset.load_from_disk(dataset_path) as dset:
                self.assertEqual(len(dset), 10)
                self.assertDictEqual(
                    dset.features,
                    Features({"nested": {"a": Value("int64"), "x": Value("int64"), "c": Value("int64")}}),
                )
                self.assertDictEqual(dset[0]["nested"], {"a": 1, "c": 100, "x": 10})
                self.assertDictEqual(dset["nested"][0], {"a": 1, "c": 100, "x": 10})

    def test_dummy_dataset_load_from_disk(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:

            with self._create_dummy_dataset(in_memory, tmp_dir).select(range(10)) as dset:
                dataset_path = os.path.join(tmp_dir, "my_dataset")
                dset.save_to_disk(dataset_path)

            with load_from_disk(dataset_path) as dset:
                self.assertEqual(len(dset), 10)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertEqual(dset[0]["filename"], "my_name-train_0")
                self.assertEqual(dset["filename"][0], "my_name-train_0")

    def test_set_format_numpy_multiple_columns(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                fingerprint = dset._fingerprint
                dset.set_format(type="numpy", columns=["col_1"])
                self.assertEqual(len(dset[0]), 1)
                self.assertIsInstance(dset[0]["col_1"], np.int64)
                self.assertEqual(dset[0]["col_1"].item(), 3)
                self.assertIsInstance(dset["col_1"], np.ndarray)
                self.assertListEqual(list(dset["col_1"].shape), [4])
                np.testing.assert_array_equal(dset["col_1"], np.array([3, 2, 1, 0]))
                self.assertNotEqual(dset._fingerprint, fingerprint)

                dset.reset_format()
                with dset.formatted_as(type="numpy", columns=["col_1"]):
                    self.assertEqual(len(dset[0]), 1)
                    self.assertIsInstance(dset[0]["col_1"], np.int64)
                    self.assertEqual(dset[0]["col_1"].item(), 3)
                    self.assertIsInstance(dset["col_1"], np.ndarray)
                    self.assertListEqual(list(dset["col_1"].shape), [4])
                    np.testing.assert_array_equal(dset["col_1"], np.array([3, 2, 1, 0]))

                self.assertEqual(dset.format["type"], None)
                self.assertEqual(dset.format["format_kwargs"], {})
                self.assertEqual(dset.format["columns"], dset.column_names)
                self.assertEqual(dset.format["output_all_columns"], False)

                dset.set_format(type="numpy", columns=["col_1"], output_all_columns=True)
                self.assertEqual(len(dset[0]), 3)
                self.assertIsInstance(dset[0]["col_2"], str)
                self.assertEqual(dset[0]["col_2"], "a")

                dset.set_format(type="numpy", columns=["col_1", "col_2"])
                self.assertEqual(len(dset[0]), 2)
                self.assertIsInstance(dset[0]["col_2"], np.str_)
                self.assertEqual(dset[0]["col_2"].item(), "a")

    @require_torch
    def test_set_format_torch(self, in_memory):
        import torch

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.set_format(type="torch", columns=["col_1"])
                self.assertEqual(len(dset[0]), 1)
                self.assertIsInstance(dset[0]["col_1"], torch.Tensor)
                self.assertIsInstance(dset["col_1"], torch.Tensor)
                self.assertListEqual(list(dset[0]["col_1"].shape), [])
                self.assertEqual(dset[0]["col_1"].item(), 3)

                dset.set_format(type="torch", columns=["col_1"], output_all_columns=True)
                self.assertEqual(len(dset[0]), 3)
                self.assertIsInstance(dset[0]["col_2"], str)
                self.assertEqual(dset[0]["col_2"], "a")

                dset.set_format(type="torch", columns=["col_1", "col_2"])
                with self.assertRaises(TypeError):
                    dset[0]

    @require_tf
    def test_set_format_tf(self, in_memory):
        import tensorflow as tf

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.set_format(type="tensorflow", columns=["col_1"])
                self.assertEqual(len(dset[0]), 1)
                self.assertIsInstance(dset[0]["col_1"], tf.Tensor)
                self.assertListEqual(list(dset[0]["col_1"].shape), [])
                self.assertEqual(dset[0]["col_1"].numpy().item(), 3)

                dset.set_format(type="tensorflow", columns=["col_1"], output_all_columns=True)
                self.assertEqual(len(dset[0]), 3)
                self.assertIsInstance(dset[0]["col_2"], str)
                self.assertEqual(dset[0]["col_2"], "a")

                dset.set_format(type="tensorflow", columns=["col_1", "col_2"])
                self.assertEqual(len(dset[0]), 2)
                self.assertEqual(dset[0]["col_2"].numpy().decode("utf-8"), "a")

    def test_set_format_pandas(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.set_format(type="pandas", columns=["col_1"])
                self.assertEqual(len(dset[0].columns), 1)
                self.assertIsInstance(dset[0], pd.DataFrame)
                self.assertListEqual(list(dset[0].shape), [1, 1])
                self.assertEqual(dset[0]["col_1"].item(), 3)

                dset.set_format(type="pandas", columns=["col_1", "col_2"])
                self.assertEqual(len(dset[0].columns), 2)
                self.assertEqual(dset[0]["col_2"].item(), "a")

    def test_set_transform(self, in_memory):
        def transform(batch):
            return {k: [str(i).upper() for i in v] for k, v in batch.items()}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.set_transform(transform=transform, columns=["col_1"])
                self.assertEqual(dset.format["type"], "custom")
                self.assertEqual(len(dset[0].keys()), 1)
                self.assertEqual(dset[0]["col_1"], "3")
                self.assertEqual(dset[:2]["col_1"], ["3", "2"])
                self.assertEqual(dset["col_1"][:2], ["3", "2"])

                prev_format = dset.format
                dset.set_format(**dset.format)
                self.assertEqual(prev_format, dset.format)

                dset.set_transform(transform=transform, columns=["col_1", "col_2"])
                self.assertEqual(len(dset[0].keys()), 2)
                self.assertEqual(dset[0]["col_2"], "A")

    def test_transmit_format(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                transform = datasets.arrow_dataset.transmit_format(lambda x: x)
                # make sure identity transform doesn't apply unnecessary format
                self.assertEqual(dset._fingerprint, transform(dset)._fingerprint)
                dset.set_format(**dset.format)
                self.assertEqual(dset._fingerprint, transform(dset)._fingerprint)
                # check lists comparisons
                dset.set_format(columns=["col_1"])
                self.assertEqual(dset._fingerprint, transform(dset)._fingerprint)
                dset.set_format(columns=["col_1", "col_2"])
                self.assertEqual(dset._fingerprint, transform(dset)._fingerprint)
                dset.set_format("numpy", columns=["col_1", "col_2"])
                self.assertEqual(dset._fingerprint, transform(dset)._fingerprint)

    def test_cast_in_place(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                features = dset.features
                features["col_1"] = Value("float64")
                features = Features({k: features[k] for k in list(features)[::-1]})
                fingerprint = dset._fingerprint
                dset.cast_(features)
                self.assertEqual(dset.num_columns, 3)
                self.assertEqual(dset.features["col_1"], Value("float64"))
                self.assertIsInstance(dset[0]["col_1"], float)
                self.assertNotEqual(dset._fingerprint, fingerprint)
                assert_arrow_metadata_are_synced_with_dataset_features(dset)

    def test_cast(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                features = dset.features
                features["col_1"] = Value("float64")
                features = Features({k: features[k] for k in list(features)[::-1]})
                fingerprint = dset._fingerprint
                # TODO: with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
                with dset.cast(features) as casted_dset:
                    self.assertEqual(casted_dset.num_columns, 3)
                    self.assertEqual(casted_dset.features["col_1"], Value("float64"))
                    self.assertIsInstance(casted_dset[0]["col_1"], float)
                    self.assertNotEqual(casted_dset._fingerprint, fingerprint)
                    self.assertNotEqual(casted_dset, dset)
                    assert_arrow_metadata_are_synced_with_dataset_features(casted_dset)

    def test_class_encode_column(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                with self.assertRaises(ValueError):
                    dset.class_encode_column(column="does not exist")

                with dset.class_encode_column("col_1") as casted_dset:
                    self.assertIsInstance(casted_dset.features["col_1"], ClassLabel)
                    self.assertListEqual(casted_dset.features["col_1"].names, ["0", "1", "2", "3"])
                    self.assertListEqual(casted_dset["col_1"], [3, 2, 1, 0])
                    self.assertNotEqual(casted_dset._fingerprint, dset._fingerprint)
                    self.assertNotEqual(casted_dset, dset)
                    assert_arrow_metadata_are_synced_with_dataset_features(casted_dset)

                with dset.class_encode_column("col_2") as casted_dset:
                    self.assertIsInstance(casted_dset.features["col_2"], ClassLabel)
                    self.assertListEqual(casted_dset.features["col_2"].names, ["a", "b", "c", "d"])
                    self.assertListEqual(casted_dset["col_2"], [0, 1, 2, 3])
                    self.assertNotEqual(casted_dset._fingerprint, dset._fingerprint)
                    self.assertNotEqual(casted_dset, dset)
                    assert_arrow_metadata_are_synced_with_dataset_features(casted_dset)

                with dset.class_encode_column("col_3") as casted_dset:
                    self.assertIsInstance(casted_dset.features["col_3"], ClassLabel)
                    self.assertListEqual(casted_dset.features["col_3"].names, ["False", "True"])
                    self.assertListEqual(casted_dset["col_3"], [0, 1, 0, 1])
                    self.assertNotEqual(casted_dset._fingerprint, dset._fingerprint)
                    self.assertNotEqual(casted_dset, dset)
                    assert_arrow_metadata_are_synced_with_dataset_features(casted_dset)

            # Test raises if feature is an array / sequence
            with self._create_dummy_dataset(in_memory, tmp_dir, array_features=True) as dset:
                for column in dset.column_names:
                    with self.assertRaises(ValueError):
                        dset.class_encode_column(column)

    def test_remove_columns_in_place(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                fingerprint = dset._fingerprint
                with assert_arrow_memory_doesnt_increase():
                    dset.remove_columns_(column_names="col_1")
                self.assertEqual(dset.num_columns, 2)
                self.assertListEqual(list(dset.column_names), ["col_2", "col_3"])
                assert_arrow_metadata_are_synced_with_dataset_features(dset)

            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.remove_columns_(column_names=["col_1", "col_2", "col_3"])
                self.assertEqual(dset.num_columns, 0)
                self.assertNotEqual(dset._fingerprint, fingerprint)
                assert_arrow_metadata_are_synced_with_dataset_features(dset)

    def test_remove_columns(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                fingerprint = dset._fingerprint
                with dset.remove_columns(column_names="col_1") as new_dset:
                    self.assertEqual(new_dset.num_columns, 2)
                    self.assertListEqual(list(new_dset.column_names), ["col_2", "col_3"])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(new_dset)

            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                with dset.remove_columns(column_names=["col_1", "col_2", "col_3"]) as new_dset:
                    self.assertEqual(new_dset.num_columns, 0)
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(new_dset)

    def test_rename_column_in_place(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                fingerprint = dset._fingerprint
                dset.rename_column_(original_column_name="col_1", new_column_name="new_name")
                self.assertEqual(dset.num_columns, 3)
                self.assertListEqual(list(dset.column_names), ["new_name", "col_2", "col_3"])
                self.assertNotEqual(dset._fingerprint, fingerprint)
                assert_arrow_metadata_are_synced_with_dataset_features(dset)

    def test_rename_column(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                fingerprint = dset._fingerprint
                with dset.rename_column(original_column_name="col_1", new_column_name="new_name") as new_dset:
                    self.assertEqual(new_dset.num_columns, 3)
                    self.assertListEqual(list(new_dset.column_names), ["new_name", "col_2", "col_3"])
                    self.assertListEqual(list(dset.column_names), ["col_1", "col_2", "col_3"])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(new_dset)

    def test_rename_columns(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                fingerprint = dset._fingerprint
                with dset.rename_columns({"col_1": "new_name"}) as new_dset:
                    self.assertEqual(new_dset.num_columns, 3)
                    self.assertListEqual(list(new_dset.column_names), ["new_name", "col_2", "col_3"])
                    self.assertListEqual(list(dset.column_names), ["col_1", "col_2", "col_3"])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)

                with dset.rename_columns({"col_1": "new_name", "col_2": "new_name2"}) as new_dset:
                    self.assertEqual(new_dset.num_columns, 3)
                    self.assertListEqual(list(new_dset.column_names), ["new_name", "new_name2", "col_3"])
                    self.assertListEqual(list(dset.column_names), ["col_1", "col_2", "col_3"])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)

                # Original column not in dataset
                with self.assertRaises(ValueError):
                    dset.rename_columns({"not_there": "new_name"})

                # Empty new name
                with self.assertRaises(ValueError):
                    dset.rename_columns({"col_1": ""})

                # Duplicates
                with self.assertRaises(ValueError):
                    dset.rename_columns({"col_1": "new_name", "col_2": "new_name"})

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

            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
                self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
                self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
                self.assertEqual(len(dset_concat.cache_files), 0 if in_memory else 3)
                self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")
            del dset1, dset2, dset3

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
            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                self.assertEqual(dset_concat.format["type"], None)
            dset2.set_format("numpy")
            dset3.set_format("numpy")
            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                self.assertEqual(dset_concat.format["type"], "numpy")
            del dset1, dset2, dset3

    def test_concatenate_with_indices(self, in_memory):
        data1, data2, data3 = {"id": [0, 1, 2] * 2}, {"id": [3, 4, 5] * 2}, {"id": [6, 7, 8]}
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

            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 3))
                self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
                self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7, 8])
                # in_memory = False:
                # 3 cache files for the dset_concat._data table
                # no cache file for the indices because it's in memory
                # in_memory = True:
                # no cache files since both dset_concat._data and dset_concat._indices are in memory
                self.assertEqual(len(dset_concat.cache_files), 0 if in_memory else 3)
                self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")

            dset1 = dset1.rename_columns({"id": "id1"})
            dset2 = dset2.rename_columns({"id": "id2"})
            dset3 = dset3.rename_columns({"id": "id3"})
            with concatenate_datasets([dset1, dset2, dset3], axis=1) as dset_concat:
                self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 3))
                self.assertEqual(len(dset_concat), len(dset1))
                self.assertListEqual(dset_concat["id1"], [0, 1, 2])
                self.assertListEqual(dset_concat["id2"], [3, 4, 5])
                self.assertListEqual(dset_concat["id3"], [6, 7, 8])
                # in_memory = False:
                # 3 cache files for the dset_concat._data table
                # no cache file for the indices because it's None
                # in_memory = True:
                # no cache files since dset_concat._data is in memory and dset_concat._indices is None
                self.assertEqual(len(dset_concat.cache_files), 0 if in_memory else 3)
                self.assertIsNone(dset_concat._indices)
                self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")

            with concatenate_datasets([dset1], axis=1) as dset_concat:
                self.assertEqual(len(dset_concat), len(dset1))
                self.assertListEqual(dset_concat["id1"], [0, 1, 2])
                # in_memory = False:
                # 1 cache file for the dset_concat._data table
                # no cache file for the indices because it's in memory
                # in_memory = True:
                # no cache files since both dset_concat._data and dset_concat._indices are in memory
                self.assertEqual(len(dset_concat.cache_files), 0 if in_memory else 1)
                self.assertTrue(dset_concat._indices == dset1._indices)
                self.assertEqual(dset_concat.info.description, "Dataset1")
            del dset1, dset2, dset3

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

            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
                self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
                self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
                # in_memory = False:
                # 3 cache files for the dset_concat._data table, and 1 for the dset_concat._indices_table
                # There is only 1 for the indices tables (i1.arrow)
                # Indeed, the others are brought to memory since an offset is applied to them.
                # in_memory = True:
                # 1 cache file for i1.arrow since both dset_concat._data and dset_concat._indices are in memory
                self.assertEqual(len(dset_concat.cache_files), 1 if in_memory else 3 + 1)
                self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")
            del dset1, dset2, dset3

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
            dset1, dset2, dset3 = (pickle.loads(pickle.dumps(d)) for d in (dset1, dset2, dset3))
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

    def test_flatten(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10},
                features=Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")}),
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fingerprint = dset._fingerprint
                    dset.flatten_()
                    self.assertListEqual(sorted(dset.column_names), ["a.b.c", "foo"])
                    self.assertListEqual(sorted(dset.features.keys()), ["a.b.c", "foo"])
                    self.assertDictEqual(
                        dset.features, Features({"a.b.c": Sequence(Value("string")), "foo": Value("int64")})
                    )
                    self.assertNotEqual(dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset)

    def test_map(self, in_memory):
        # standard
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                fingerprint = dset._fingerprint
                with dset.map(
                    lambda x: {"name": x["filename"][:-2], "id": int(x["filename"].split("_")[-1])}
                ) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
                    )
                    self.assertListEqual(dset_test["id"], list(range(30)))
                    self.assertNotEqual(dset_test._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)

        # no transform
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.map(lambda x: None) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertEqual(dset_test._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)

        # with indices
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(
                    lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True
                ) as dset_test_with_indices:
                    self.assertEqual(len(dset_test_with_indices), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test_with_indices.features,
                        Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
                    )
                    self.assertListEqual(dset_test_with_indices["id"], list(range(30)))
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test_with_indices)

        # interrupted
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:

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
                with dset.map(
                    lambda x, i: {"name": x["filename"][:-2], "id": i},
                    with_indices=True,
                    cache_file_name=tmp_file,
                    writer_batch_size=2,
                ) as dset_test_with_indices:
                    self.assertTrue(os.path.exists(tmp_file))
                    self.assertEqual(len(dset_test_with_indices), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test_with_indices.features,
                        Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
                    )
                    self.assertListEqual(dset_test_with_indices["id"], list(range(30)))
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test_with_indices)

        # formatted
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.set_format("numpy", columns=["col_1"])
                with dset.map(lambda x: {"col_1_plus_one": x["col_1"] + 1}) as dset_test:
                    self.assertEqual(len(dset_test), 4)
                    self.assertEqual(dset_test.format["type"], "numpy")
                    self.assertIsInstance(dset_test["col_1"], np.ndarray)
                    self.assertIsInstance(dset_test["col_1_plus_one"], np.ndarray)
                    self.assertListEqual(sorted(dset_test[0].keys()), ["col_1", "col_1_plus_one"])
                    self.assertListEqual(sorted(dset_test.column_names), ["col_1", "col_1_plus_one", "col_2", "col_3"])
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)

    def test_map_multiprocessing(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:  # standard
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                fingerprint = dset._fingerprint
                with dset.map(picklable_map_function, num_proc=2) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "id": Value("int64")}),
                    )
                    self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 2)
                    self.assertListEqual(dset_test["id"], list(range(30)))
                    self.assertNotEqual(dset_test._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)

        with tempfile.TemporaryDirectory() as tmp_dir:  # num_proc > num rows
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                fingerprint = dset._fingerprint
                with dset.select([0, 1], keep_in_memory=True).map(picklable_map_function, num_proc=10) as dset_test:
                    self.assertEqual(len(dset_test), 2)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "id": Value("int64")}),
                    )
                    self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 2)
                    self.assertListEqual(dset_test["id"], list(range(2)))
                    self.assertNotEqual(dset_test._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)

        with tempfile.TemporaryDirectory() as tmp_dir:  # with_indices
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.map(picklable_map_function_with_indices, num_proc=3, with_indices=True) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "id": Value("int64")}),
                    )
                    self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 3)
                    self.assertListEqual(dset_test["id"], list(range(30)))
                    self.assertNotEqual(dset_test._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)

        with tempfile.TemporaryDirectory() as tmp_dir:  # with_rank
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.map(picklable_map_function_with_rank, num_proc=3, with_rank=True) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "rank": Value("int64")}),
                    )
                    self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 3)
                    self.assertListEqual(dset_test["rank"], [0] * 10 + [1] * 10 + [2] * 10)
                    self.assertNotEqual(dset_test._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)

        with tempfile.TemporaryDirectory() as tmp_dir:  # with_indices AND with_rank
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.map(
                    picklable_map_function_with_indices_and_rank, num_proc=3, with_indices=True, with_rank=True
                ) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "id": Value("int64"), "rank": Value("int64")}),
                    )
                    self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 3)
                    self.assertListEqual(dset_test["id"], list(range(30)))
                    self.assertListEqual(dset_test["rank"], [0] * 10 + [1] * 10 + [2] * 10)
                    self.assertNotEqual(dset_test._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)

        with tempfile.TemporaryDirectory() as tmp_dir:  # new_fingerprint
            new_fingerprint = "foobar"
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.map(picklable_map_function, num_proc=2, new_fingerprint=new_fingerprint) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "id": Value("int64")}),
                    )
                    self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 2)
                    self.assertListEqual(dset_test["id"], list(range(30)))
                    self.assertNotEqual(dset_test._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)
                    file_names = sorted(Path(cache_file["filename"]).name for cache_file in dset_test.cache_files)
                    for i, file_name in enumerate(file_names):
                        self.assertIn(new_fingerprint + f"_{i:05d}", file_name)

        with tempfile.TemporaryDirectory() as tmp_dir:  # lambda (requires multiprocess from pathos)
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.map(lambda x: {"id": int(x["filename"].split("_")[-1])}, num_proc=2) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "id": Value("int64")}),
                    )
                    self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 2)
                    self.assertListEqual(dset_test["id"], list(range(30)))
                    self.assertNotEqual(dset_test._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test)

    def test_new_features(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                features = Features({"filename": Value("string"), "label": ClassLabel(names=["positive", "negative"])})
                with dset.map(
                    lambda x, i: {"label": i % 2}, with_indices=True, features=features
                ) as dset_test_with_indices:
                    self.assertEqual(len(dset_test_with_indices), 30)
                    self.assertDictEqual(
                        dset_test_with_indices.features,
                        features,
                    )
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test_with_indices)

    def test_map_batched(self, in_memory):
        def map_batched(example):
            return {"filename_new": [x + "_extension" for x in example["filename"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(map_batched, batched=True) as dset_test_batched:
                    self.assertEqual(len(dset_test_batched), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test_batched.features,
                        Features({"filename": Value("string"), "filename_new": Value("string")}),
                    )
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test_batched)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.formatted_as("numpy", columns=["filename"]):
                    with dset.map(map_batched, batched=True) as dset_test_batched:
                        self.assertEqual(len(dset_test_batched), 30)
                        self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                        self.assertDictEqual(
                            dset_test_batched.features,
                            Features({"filename": Value("string"), "filename_new": Value("string")}),
                        )
                        assert_arrow_metadata_are_synced_with_dataset_features(dset_test_batched)

        def map_batched_with_indices(example, idx):
            return {"filename_new": [x + "_extension_" + str(idx) for x in example["filename"]]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(
                    map_batched_with_indices, batched=True, with_indices=True
                ) as dset_test_with_indices_batched:
                    self.assertEqual(len(dset_test_with_indices_batched), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test_with_indices_batched.features,
                        Features({"filename": Value("string"), "filename_new": Value("string")}),
                    )
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test_with_indices_batched)

    def test_map_nested(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict({"field": ["a", "b"]}) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    with dset.map(lambda example: {"otherfield": {"capital": example["field"].capitalize()}}) as dset:
                        with dset.map(lambda example: {"otherfield": {"append_x": example["field"] + "x"}}) as dset:
                            self.assertEqual(dset[0], {"field": "a", "otherfield": {"append_x": "ax"}})

    def test_map_fn_kwargs(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict({"id": range(10)}) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fn_kwargs = {"offset": 3}
                    with dset.map(
                        lambda example, offset: {"id+offset": example["id"] + offset}, fn_kwargs=fn_kwargs
                    ) as mapped_dset:
                        assert mapped_dset["id+offset"] == list(range(3, 13))
                    with dset.map(
                        lambda id, offset: {"id+offset": id + offset}, fn_kwargs=fn_kwargs, input_columns="id"
                    ) as mapped_dset:
                        assert mapped_dset["id+offset"] == list(range(3, 13))
                    with dset.map(
                        lambda id, i, offset: {"id+offset": i + offset},
                        fn_kwargs=fn_kwargs,
                        input_columns="id",
                        with_indices=True,
                    ) as mapped_dset:
                        assert mapped_dset["id+offset"] == list(range(3, 13))

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

        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(WARNING):
                with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                    with patch("datasets.arrow_dataset.Pool", side_effect=datasets.arrow_dataset.Pool) as mock_pool:
                        with dset.map(lambda x: {"foo": "bar"}, num_proc=2) as dset_test1:
                            dset_test1_data_files = list(dset_test1.cache_files)
                        self.assertEqual(mock_pool.call_count, 1)
                        with dset.map(lambda x: {"foo": "bar"}, num_proc=2) as dset_test2:
                            self.assertEqual(dset_test1_data_files, dset_test2.cache_files)
                            self.assertTrue(
                                (len(re.findall("Loading cached processed dataset", self._caplog.text)) == 2)
                                ^ in_memory
                            )
                        self.assertEqual(mock_pool.call_count, 2 if in_memory else 1)

        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(WARNING):
                with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                    with dset.map(lambda x: {"foo": "bar"}, num_proc=2) as dset_test1:
                        dset_test1_data_files = list(dset_test1.cache_files)
                    with dset.map(lambda x: {"foo": "bar"}, num_proc=2, load_from_cache_file=False) as dset_test2:
                        self.assertEqual(dset_test1_data_files, dset_test2.cache_files)
                        self.assertEqual(len(dset_test2.cache_files), (1 - int(in_memory)) * 2)
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
                                    self.assertIn("tmp", dset_test1.cache_files[0]["filename"])
                                    self.assertIn("tmp", dset_test2.cache_files[0]["filename"])
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
                        Features({"filename": Value("string"), "tensor": Sequence(Value("float32"))}),
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
                        Features({"filename": Value("string"), "tensor": Sequence(Value("float32"))}),
                    )
                    self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])

    @require_jax
    def test_map_jax(self, in_memory):
        import jax.numpy as jnp

        def func(example):
            return {"tensor": jnp.asarray([1.0, 2, 3])}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "tensor": Sequence(Value("float32"))}),
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

    def test_map_remove_columns(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True) as dset:
                    self.assertTrue("id" in dset[0])
                    self.assertDictEqual(
                        dset.features,
                        Features({"filename": Value("string"), "name": Value("string"), "id": Value("int64")}),
                    )
                    assert_arrow_metadata_are_synced_with_dataset_features(dset)
                    with dset.map(lambda x: x, remove_columns=["id"]) as dset:
                        self.assertTrue("id" not in dset[0])
                        self.assertDictEqual(
                            dset.features, Features({"filename": Value("string"), "name": Value("string")})
                        )
                        assert_arrow_metadata_are_synced_with_dataset_features(dset)
                        with dset.with_format("numpy", columns=dset.column_names) as dset:
                            with dset.map(lambda x: {"name": 1}, remove_columns=dset.column_names) as dset:
                                self.assertTrue("filename" not in dset[0])
                                self.assertTrue("name" in dset[0])
                                self.assertDictEqual(dset.features, Features({"name": Value(dtype="int64")}))
                                assert_arrow_metadata_are_synced_with_dataset_features(dset)

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

    def test_filter_with_indices_mapping(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"col": [0, 1, 2]})
            with self._to(in_memory, tmp_dir, dset) as dset:
                with dset.filter(lambda x: x["col"] > 0) as dset:
                    self.assertListEqual(dset["col"], [1, 2])
                    with dset.filter(lambda x: x["col"] < 2) as dset:
                        self.assertListEqual(dset["col"], [1])

    def test_filter_batched(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"col": [0, 1, 2]})
            with self._to(in_memory, tmp_dir, dset) as dset:
                with dset.filter(lambda x: [i > 0 for i in x["col"]], batched=True) as dset:
                    self.assertListEqual(dset["col"], [1, 2])
                    with dset.filter(lambda x: [i < 2 for i in x["col"]], batched=True) as dset:
                        self.assertListEqual(dset["col"], [1])

    def test_filter_fn_kwargs(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict({"id": range(10)}) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fn_kwargs = {"max_offset": 3}
                    with dset.filter(
                        lambda example, max_offset: example["id"] < max_offset, fn_kwargs=fn_kwargs
                    ) as filtered_dset:
                        assert len(filtered_dset) == 3
                    with dset.filter(
                        lambda id, max_offset: id < max_offset, fn_kwargs=fn_kwargs, input_columns="id"
                    ) as filtered_dset:
                        assert len(filtered_dset) == 3
                    with dset.filter(
                        lambda id, i, max_offset: i < max_offset,
                        fn_kwargs=fn_kwargs,
                        input_columns="id",
                        with_indices=True,
                    ) as filtered_dset:
                        assert len(filtered_dset) == 3

    def test_filter_multiprocessing(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.filter(picklable_filter_function, num_proc=2) as dset_filter_first_ten:
                    self.assertEqual(len(dset_filter_first_ten), 10)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_filter_first_ten.features, Features({"filename": Value("string")}))
                    self.assertEqual(len(dset_filter_first_ten.cache_files), 0 if in_memory else 2)
                    self.assertNotEqual(dset_filter_first_ten._fingerprint, fingerprint)

    def test_filter_caching(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(WARNING):
                with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                    with dset.filter(lambda x, i: i < 5, with_indices=True) as dset_filter_first_five1:
                        dset_test1_data_files = list(dset_filter_first_five1.cache_files)
                    with dset.filter(lambda x, i: i < 5, with_indices=True) as dset_filter_first_five2:
                        self.assertEqual(dset_test1_data_files, dset_filter_first_five2.cache_files)
                        self.assertEqual(len(dset_filter_first_five2.cache_files), 0 if in_memory else 2)
                        self.assertTrue(("Loading cached processed dataset" in self._caplog.text) ^ in_memory)

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
                        assert_arrow_metadata_are_synced_with_dataset_features(inverted_dset)

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
                        assert_arrow_metadata_are_synced_with_dataset_features(inverted_dset)

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
                        assert_arrow_metadata_are_synced_with_dataset_features(inverted_dset)

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
                bad_indices[-1] = len(dset) + 10  # out of bounds
                tmp_file = os.path.join(tmp_dir, "test.arrow")
                self.assertRaises(
                    Exception,
                    dset.select,
                    indices=bad_indices,
                    indices_cache_file_name=tmp_file,
                    writer_batch_size=2,
                )
                self.assertFalse(os.path.exists(tmp_file))

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                bad_indices = list(range(5))
                bad_indices[3] = "foo"  # wrong type
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
                                self.assertIn(
                                    ("rename_columns", (["file", "number"],), {}),
                                    dset._data.replays,
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
            with self._create_dummy_dataset(in_memory, tmp_dir, array_features=True) as dset:
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

    def test_to_parquet(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # File path argument
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                file_path = os.path.join(tmp_dir, "test_path.parquet")
                dset.to_parquet(path_or_buf=file_path)

                self.assertTrue(os.path.isfile(file_path))
                # self.assertEqual(bytes_written, os.path.getsize(file_path))  # because of compression, the number of bytes doesn't match
                parquet_dset = pd.read_parquet(file_path)

                self.assertEqual(parquet_dset.shape, dset.shape)
                self.assertListEqual(list(parquet_dset.columns), list(dset.column_names))

            # File buffer argument
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                file_path = os.path.join(tmp_dir, "test_buffer.parquet")
                with open(file_path, "wb+") as buffer:
                    dset.to_parquet(path_or_buf=buffer)

                self.assertTrue(os.path.isfile(file_path))
                # self.assertEqual(bytes_written, os.path.getsize(file_path))  # because of compression, the number of bytes doesn't match
                parquet_dset = pd.read_parquet(file_path)

                self.assertEqual(parquet_dset.shape, dset.shape)
                self.assertListEqual(list(parquet_dset.columns), list(dset.column_names))

            # After a select/shuffle transform
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset = dset.select(range(0, len(dset), 2)).shuffle()
                file_path = os.path.join(tmp_dir, "test_path.parquet")
                dset.to_parquet(path_or_buf=file_path)

                self.assertTrue(os.path.isfile(file_path))
                # self.assertEqual(bytes_written, os.path.getsize(file_path))  # because of compression, the number of bytes doesn't match
                parquet_dset = pd.read_parquet(file_path)

                self.assertEqual(parquet_dset.shape, dset.shape)
                self.assertListEqual(list(parquet_dset.columns), list(dset.column_names))

            # With array features
            with self._create_dummy_dataset(in_memory, tmp_dir, array_features=True) as dset:
                file_path = os.path.join(tmp_dir, "test_path.parquet")
                dset.to_parquet(path_or_buf=file_path)

                self.assertTrue(os.path.isfile(file_path))
                # self.assertEqual(bytes_written, os.path.getsize(file_path))  # because of compression, the number of bytes doesn't match
                parquet_dset = pd.read_parquet(file_path)

                self.assertEqual(parquet_dset.shape, dset.shape)
                self.assertListEqual(list(parquet_dset.columns), list(dset.column_names))

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
                        assert_arrow_metadata_are_synced_with_dataset_features(dset)

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
            self.assertEqual(tuple(dset[:2]["vec"].shape), (2, 3))
            self.assertEqual(tuple(dset["vec"][:2].shape), (2, 3))

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

    @require_tf
    def test_tf_dataset_conversion(self, in_memory):
        def tf_default_data_collator(features):
            """This is the tf_default_data_collator from transformers, copied so we avoid depending on that library."""
            import numpy as np
            import tensorflow as tf

            first = features[0]
            batch = {}

            # Special handling for labels.
            # Ensure that tensor is created with the correct type
            # (it should be automatically the case, but let's make sure of it.)
            if "label" in first and first["label"] is not None:
                if isinstance(first["label"], tf.Tensor):
                    dtype = tf.int64 if first["label"].dtype.is_integer() else tf.float32
                elif isinstance(first["label"], np.ndarray):
                    dtype = tf.int64 if np.issubdtype(first["label"].dtype, np.integer) else tf.float32
                elif isinstance(first["label"], (tuple, list)):
                    dtype = tf.int64 if isinstance(first["label"][0], int) else tf.float32
                else:
                    dtype = tf.int64 if isinstance(first["label"], int) else tf.float32
                batch["labels"] = tf.convert_to_tensor([f["label"] for f in features], dtype=dtype)
            elif "label_ids" in first and first["label_ids"] is not None:
                if isinstance(first["label_ids"], tf.Tensor):
                    batch["labels"] = tf.stack([f["label_ids"] for f in features])
                else:
                    dtype = tf.int64 if type(first["label_ids"][0]) is int else tf.float32
                    batch["labels"] = tf.convert_to_tensor([f["label_ids"] for f in features], dtype=dtype)

            # Handling of all other possible keys.
            # Again, we will use the first element to figure out which key/values are not None for this model.
            for k, v in first.items():
                if k not in ("label", "label_ids") and v is not None and not isinstance(v, str):
                    if isinstance(v, (tf.Tensor, np.ndarray)):
                        batch[k] = tf.stack([f[k] for f in features])
                    else:
                        batch[k] = tf.convert_to_tensor([f[k] for f in features])

            return batch

        tmp_dir = tempfile.TemporaryDirectory()
        with self._create_dummy_dataset(in_memory, tmp_dir.name, array_features=True) as dset:
            tf_dataset = dset.to_tf_dataset(
                columns="col_3", batch_size=4, shuffle=False, dummy_labels=False, collate_fn=tf_default_data_collator
            )
            batch = next(iter(tf_dataset))
            self.assertEqual(batch.shape.as_list(), [4, 4])
            self.assertEqual(batch.dtype.name, "int64")
        with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
            tf_dataset = dset.to_tf_dataset(
                columns="col_1", batch_size=4, shuffle=False, dummy_labels=False, collate_fn=tf_default_data_collator
            )
            batch = next(iter(tf_dataset))
            self.assertEqual(batch.shape.as_list(), [4])
            self.assertEqual(batch.dtype.name, "int64")
        del tf_dataset  # For correct cleanup


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
        with Dataset.from_dict(data, features=features) as dset:
            # the integers are converted to strings
            self.assertListEqual(dset["col_1"], [str(x) for x in data["col_1"]])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
            self.assertDictEqual(dset.features, Features({"col_1": Value("string"), "col_2": Value("string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("int64")})
        self.assertRaises(ValueError, Dataset.from_dict, data, features=features)

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


def test_cast_with_sliced_list():
    old_features = Features({"foo": Sequence(Value("int64"))})
    new_features = Features({"foo": Sequence(Value("int32"))})
    dataset = Dataset.from_dict({"foo": [[i] * (i % 3) for i in range(20)]}, features=old_features)
    casted_dataset = dataset.cast(new_features, batch_size=2)  # small batch size to slice the ListArray
    assert dataset["foo"] == casted_dataset["foo"]
    assert casted_dataset.features == new_features


@pytest.mark.parametrize("include_nulls", [False, True])
def test_class_encode_column_with_none(include_nulls):
    dataset = Dataset.from_dict({"col_1": ["a", "b", "c", None, "d", None]})
    dataset = dataset.class_encode_column("col_1", include_nulls=include_nulls)
    class_names = ["a", "b", "c", "d"]
    if include_nulls:
        class_names += ["None"]
    assert isinstance(dataset.features["col_1"], ClassLabel)
    assert set(dataset.features["col_1"].names) == set(class_names)
    assert (None in dataset.unique("col_1")) == (not include_nulls)


@pytest.mark.parametrize("null_placement", ["first", "last"])
def test_sort_with_none(null_placement):
    dataset = Dataset.from_dict({"col_1": ["item_2", "item_3", "item_1", None, "item_4", None]})
    dataset = dataset.sort("col_1", null_placement=null_placement)
    if null_placement == "first":
        assert dataset["col_1"] == [None, None, "item_1", "item_2", "item_3", "item_4"]
    else:
        assert dataset["col_1"] == ["item_1", "item_2", "item_3", "item_4", None, None]


def test_update_metadata_with_features(dataset_dict):
    table1 = pa.Table.from_pydict(dataset_dict)
    features1 = Features.from_arrow_schema(table1.schema)
    features2 = features1.copy()
    features2["col_2"] = ClassLabel(num_classes=len(table1))
    assert features1 != features2

    table2 = update_metadata_with_features(table1, features2)
    metadata = json.loads(table2.schema.metadata[b"huggingface"].decode())
    assert features2 == Features.from_dict(metadata["info"]["features"])

    with Dataset(table1) as dset1, Dataset(table2) as dset2:
        assert dset1.features == features1
        assert dset2.features == features2


@pytest.mark.parametrize("dataset_type", ["in_memory", "memory_mapped", "mixed"])
@pytest.mark.parametrize("axis, expected_shape", [(0, (4, 3)), (1, (2, 6))])
def test_concatenate_datasets(dataset_type, axis, expected_shape, dataset_dict, arrow_path):
    table = {
        "in_memory": InMemoryTable.from_pydict(dataset_dict),
        "memory_mapped": MemoryMappedTable.from_file(arrow_path),
    }
    tables = [
        table[dataset_type if dataset_type != "mixed" else "memory_mapped"].slice(0, 2),  # shape = (2, 3)
        table[dataset_type if dataset_type != "mixed" else "in_memory"].slice(2, 4),  # shape = (2, 3)
    ]
    if axis == 1:  # don't duplicate columns
        tables[1] = tables[1].rename_columns([col + "_bis" for col in tables[1].column_names])
    datasets = [Dataset(table) for table in tables]
    dataset = concatenate_datasets(datasets, axis=axis)
    assert dataset.shape == expected_shape
    assert_arrow_metadata_are_synced_with_dataset_features(dataset)


def test_concatenate_datasets_new_columns():
    dataset1 = Dataset.from_dict({"col_1": ["a", "b", "c"]})
    dataset2 = Dataset.from_dict({"col_1": ["d", "e", "f"], "col_2": [True, False, True]})
    dataset = concatenate_datasets([dataset1, dataset2])
    assert dataset.data.shape == (6, 2)
    assert dataset.features == Features({"col_1": Value("string"), "col_2": Value("bool")})
    assert dataset[:] == {"col_1": ["a", "b", "c", "d", "e", "f"], "col_2": [None, None, None, True, False, True]}
    dataset3 = Dataset.from_dict({"col_3": ["a_1"]})
    dataset = concatenate_datasets([dataset, dataset3])
    assert dataset.data.shape == (7, 3)
    assert dataset.features == Features({"col_1": Value("string"), "col_2": Value("bool"), "col_3": Value("string")})
    assert dataset[:] == {
        "col_1": ["a", "b", "c", "d", "e", "f", None],
        "col_2": [None, None, None, True, False, True, None],
        "col_3": [None, None, None, None, None, None, "a_1"],
    }


@pytest.mark.parametrize("axis", [0, 1])
def test_concatenate_datasets_complex_features(axis):
    n = 5
    dataset1 = Dataset.from_dict(
        {"col_1": [0] * n, "col_2": list(range(n))},
        features=Features({"col_1": Value("int32"), "col_2": ClassLabel(num_classes=n)}),
    )
    if axis == 1:
        dataset2 = dataset1.rename_columns({col: col + "_" for col in dataset1.column_names})
        expected_features = Features({**dataset1.features, **dataset2.features})
    else:
        dataset2 = dataset1
        expected_features = dataset1.features
    assert concatenate_datasets([dataset1, dataset2], axis=axis).features == expected_features


@pytest.mark.parametrize("other_dataset_type", ["in_memory", "memory_mapped", "concatenation"])
@pytest.mark.parametrize("axis, expected_shape", [(0, (8, 3)), (1, (4, 6))])
def test_concatenate_datasets_with_concatenation_tables(
    axis, expected_shape, other_dataset_type, dataset_dict, arrow_path
):
    def _create_concatenation_table(axis):
        if axis == 0:  # shape: (4, 3) = (4, 1) + (4, 2)
            concatenation_table = ConcatenationTable.from_blocks(
                [
                    [
                        InMemoryTable.from_pydict({"col_1": dataset_dict["col_1"]}),
                        MemoryMappedTable.from_file(arrow_path).remove_column(0),
                    ]
                ]
            )
        elif axis == 1:  # shape: (4, 3) = (1, 3) + (3, 3)
            concatenation_table = ConcatenationTable.from_blocks(
                [
                    [InMemoryTable.from_pydict(dataset_dict).slice(0, 1)],
                    [MemoryMappedTable.from_file(arrow_path).slice(1, 4)],
                ]
            )
        return concatenation_table

    concatenation_table = _create_concatenation_table(axis)
    assert concatenation_table.shape == (4, 3)

    if other_dataset_type == "in_memory":
        other_table = InMemoryTable.from_pydict(dataset_dict)
    elif other_dataset_type == "memory_mapped":
        other_table = MemoryMappedTable.from_file(arrow_path)
    elif other_dataset_type == "concatenation":
        other_table = _create_concatenation_table(axis)
    assert other_table.shape == (4, 3)

    tables = [concatenation_table, other_table]

    if axis == 1:  # don't duplicate columns
        tables[1] = tables[1].rename_columns([col + "_bis" for col in tables[1].column_names])

    for tables in [tables, reversed(tables)]:
        datasets = [Dataset(table) for table in tables]
        dataset = concatenate_datasets(datasets, axis=axis)
        assert dataset.shape == expected_shape


def test_concatenate_datasets_duplicate_columns(dataset):
    with pytest.raises(ValueError) as excinfo:
        concatenate_datasets([dataset, dataset], axis=1)
    assert "duplicated" in str(excinfo.value)


def test_interleave_datasets():
    d1 = Dataset.from_dict({"a": [0, 1, 2]})
    d2 = Dataset.from_dict({"a": [10, 11, 12, 13]})
    d3 = Dataset.from_dict({"a": [22, 21, 20]}).select([2, 1, 0])
    dataset = interleave_datasets([d1, d2, d3])
    expected_length = 3 * min(len(d1), len(d2), len(d3))
    expected_values = [x["a"] for x in itertools.chain(*zip(d1, d2, d3))]
    assert isinstance(dataset, Dataset)
    assert len(dataset) == expected_length
    assert dataset["a"] == expected_values
    assert dataset._fingerprint == interleave_datasets([d1, d2, d3])._fingerprint


def test_interleave_datasets_probabilities():
    seed = 42
    probabilities = [0.3, 0.5, 0.2]
    d1 = Dataset.from_dict({"a": [0, 1, 2]})
    d2 = Dataset.from_dict({"a": [10, 11, 12, 13]})
    d3 = Dataset.from_dict({"a": [22, 21, 20]}).select([2, 1, 0])
    dataset = interleave_datasets([d1, d2, d3], probabilities=probabilities, seed=seed)
    expected_length = 7  # hardcoded
    expected_values = [10, 11, 20, 12, 0, 21, 13]  # hardcoded
    assert isinstance(dataset, Dataset)
    assert len(dataset) == expected_length
    assert dataset["a"] == expected_values
    assert (
        dataset._fingerprint == interleave_datasets([d1, d2, d3], probabilities=probabilities, seed=seed)._fingerprint
    )


@pytest.mark.parametrize(
    "column, expected_dtype",
    [(["a", "b", "c", "d"], "string"), ([1, 2, 3, 4], "int64"), ([1.0, 2.0, 3.0, 4.0], "float64")],
)
@pytest.mark.parametrize("in_memory", [False, True])
@pytest.mark.parametrize(
    "transform",
    [
        None,
        ("shuffle", (42,), {}),
        ("with_format", ("pandas",), {}),
        ("class_encode_column", ("col_2",), {}),
        ("select", (range(3),), {}),
    ],
)
def test_dataset_add_column(column, expected_dtype, in_memory, transform, dataset_dict, arrow_path):
    column_name = "col_4"
    original_dataset = (
        Dataset(InMemoryTable.from_pydict(dataset_dict))
        if in_memory
        else Dataset(MemoryMappedTable.from_file(arrow_path))
    )
    if transform is not None:
        transform_name, args, kwargs = transform
        original_dataset: Dataset = getattr(original_dataset, transform_name)(*args, **kwargs)
    column = column[:3] if transform is not None and transform_name == "select" else column
    dataset = original_dataset.add_column(column_name, column)
    assert dataset.data.shape == (3, 4) if transform is not None and transform_name == "select" else (4, 4)
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    # Sort expected features as in the original dataset
    expected_features = {feature: expected_features[feature] for feature in original_dataset.features}
    # Add new column feature
    expected_features[column_name] = expected_dtype
    assert dataset.data.column_names == list(expected_features.keys())
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype
    assert len(dataset.data.blocks) == 1 if in_memory else 2  # multiple InMemoryTables are consolidated as one
    assert dataset.format["type"] == original_dataset.format["type"]
    assert dataset._fingerprint != original_dataset._fingerprint
    dataset.reset_format()
    original_dataset.reset_format()
    assert all(dataset[col] == original_dataset[col] for col in original_dataset.column_names)
    assert set(dataset["col_4"]) == set(column)
    if dataset._indices is not None:
        dataset_indices = dataset._indices["indices"].to_pylist()
        expected_dataset_indices = original_dataset._indices["indices"].to_pylist()
        assert dataset_indices == expected_dataset_indices
    assert_arrow_metadata_are_synced_with_dataset_features(dataset)


@pytest.mark.parametrize(
    "transform",
    [None, ("shuffle", (42,), {}), ("with_format", ("pandas",), {}), ("class_encode_column", ("col_2",), {})],
)
@pytest.mark.parametrize("in_memory", [False, True])
@pytest.mark.parametrize(
    "item",
    [
        {"col_1": "4", "col_2": 4, "col_3": 4.0},
        {"col_1": "4", "col_2": "4", "col_3": "4"},
        {"col_1": 4, "col_2": 4, "col_3": 4},
        {"col_1": 4.0, "col_2": 4.0, "col_3": 4.0},
    ],
)
def test_dataset_add_item(item, in_memory, dataset_dict, arrow_path, transform):
    dataset_to_test = (
        Dataset(InMemoryTable.from_pydict(dataset_dict))
        if in_memory
        else Dataset(MemoryMappedTable.from_file(arrow_path))
    )
    if transform is not None:
        transform_name, args, kwargs = transform
        dataset_to_test: Dataset = getattr(dataset_to_test, transform_name)(*args, **kwargs)
    dataset = dataset_to_test.add_item(item)
    assert dataset.data.shape == (5, 3)
    expected_features = dataset_to_test.features
    assert sorted(dataset.data.column_names) == sorted(expected_features.keys())
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature] == expected_dtype
    assert len(dataset.data.blocks) == 1 if in_memory else 2  # multiple InMemoryTables are consolidated as one
    assert dataset.format["type"] == dataset_to_test.format["type"]
    assert dataset._fingerprint != dataset_to_test._fingerprint
    dataset.reset_format()
    dataset_to_test.reset_format()
    assert dataset[:-1] == dataset_to_test[:]
    assert {k: int(v) for k, v in dataset[-1].items()} == {k: int(v) for k, v in item.items()}
    if dataset._indices is not None:
        dataset_indices = dataset._indices["indices"].to_pylist()
        dataset_to_test_indices = dataset_to_test._indices["indices"].to_pylist()
        assert dataset_indices == dataset_to_test_indices + [len(dataset_to_test._data)]


def test_dataset_add_item_new_columns():
    dataset = Dataset.from_dict({"col_1": [0, 1, 2]}, features=Features({"col_1": Value("uint8")}))
    dataset = dataset.add_item({"col_1": 3, "col_2": "a"})
    assert dataset.data.shape == (4, 2)
    assert dataset.features == Features({"col_1": Value("uint8"), "col_2": Value("string")})
    assert dataset[:] == {"col_1": [0, 1, 2, 3], "col_2": [None, None, None, "a"]}
    dataset = dataset.add_item({"col_3": True})
    assert dataset.data.shape == (5, 3)
    assert dataset.features == Features({"col_1": Value("uint8"), "col_2": Value("string"), "col_3": Value("bool")})
    assert dataset[:] == {
        "col_1": [0, 1, 2, 3, None],
        "col_2": [None, None, None, "a", None],
        "col_3": [None, None, None, None, True],
    }


def test_dataset_add_item_introduce_feature_type():
    dataset = Dataset.from_dict({"col_1": [None, None, None]})
    dataset = dataset.add_item({"col_1": "a"})
    assert dataset.data.shape == (4, 1)
    assert dataset.features == Features({"col_1": Value("string")})
    assert dataset[:] == {"col_1": [None, None, None, "a"]}


@pytest.mark.parametrize("in_memory", [False, True])
def test_dataset_from_file(in_memory, dataset, arrow_file):
    filename = arrow_file
    with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
        dataset_from_file = Dataset.from_file(filename, in_memory=in_memory)
    assert dataset_from_file.features.type == dataset.features.type
    assert dataset_from_file.features == dataset.features
    assert dataset_from_file.cache_files == ([{"filename": filename}] if not in_memory else [])


def _check_csv_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_csv_keep_in_memory(keep_in_memory, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_csv(csv_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory)
    _check_csv_dataset(dataset, expected_features)


@pytest.mark.parametrize(
    "features",
    [
        None,
        {"col_1": "string", "col_2": "int64", "col_3": "float64"},
        {"col_1": "string", "col_2": "string", "col_3": "string"},
        {"col_1": "int32", "col_2": "int32", "col_3": "int32"},
        {"col_1": "float32", "col_2": "float32", "col_3": "float32"},
    ],
)
def test_dataset_from_csv_features(features, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    # CSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = Dataset.from_csv(csv_path, features=features, cache_dir=cache_dir)
    _check_csv_dataset(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_csv_split(split, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    dataset = Dataset.from_csv(csv_path, cache_dir=cache_dir, split=split)
    _check_csv_dataset(dataset, expected_features)
    assert dataset.split == str(split) if split else "train"


@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_csv_path_type(path_type, csv_path, tmp_path):
    if issubclass(path_type, str):
        path = csv_path
    elif issubclass(path_type, list):
        path = [csv_path]
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    dataset = Dataset.from_csv(path, cache_dir=cache_dir)
    _check_csv_dataset(dataset, expected_features)


def _check_json_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_json_keep_in_memory(keep_in_memory, jsonl_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_json(jsonl_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory)
    _check_json_dataset(dataset, expected_features)


@pytest.mark.parametrize(
    "features",
    [
        None,
        {"col_1": "string", "col_2": "int64", "col_3": "float64"},
        {"col_1": "string", "col_2": "string", "col_3": "string"},
        {"col_1": "int32", "col_2": "int32", "col_3": "int32"},
        {"col_1": "float32", "col_2": "float32", "col_3": "float32"},
    ],
)
def test_dataset_from_json_features(features, jsonl_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = Dataset.from_json(jsonl_path, features=features, cache_dir=cache_dir)
    _check_json_dataset(dataset, expected_features)


def test_dataset_from_json_with_class_label_feature(jsonl_str_path, tmp_path):
    features = Features(
        {"col_1": ClassLabel(names=["s0", "s1", "s2", "s3"]), "col_2": Value("int64"), "col_3": Value("float64")}
    )
    cache_dir = tmp_path / "cache"
    dataset = Dataset.from_json(jsonl_str_path, features=features, cache_dir=cache_dir)
    assert dataset.features["col_1"].dtype == "int64"


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_json_split(split, jsonl_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = Dataset.from_json(jsonl_path, cache_dir=cache_dir, split=split)
    _check_json_dataset(dataset, expected_features)
    assert dataset.split == str(split) if split else "train"


@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_json_path_type(path_type, jsonl_path, tmp_path):
    if issubclass(path_type, str):
        path = jsonl_path
    elif issubclass(path_type, list):
        path = [jsonl_path]
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = Dataset.from_json(path, cache_dir=cache_dir)
    _check_json_dataset(dataset, expected_features)


def _check_parquet_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_parquet_keep_in_memory(keep_in_memory, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_parquet(parquet_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory)
    _check_parquet_dataset(dataset, expected_features)


@pytest.mark.parametrize(
    "features",
    [
        None,
        {"col_1": "string", "col_2": "int64", "col_3": "float64"},
        {"col_1": "string", "col_2": "string", "col_3": "string"},
        {"col_1": "int32", "col_2": "int32", "col_3": "int32"},
        {"col_1": "float32", "col_2": "float32", "col_3": "float32"},
    ],
)
def test_dataset_from_parquet_features(features, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = Dataset.from_parquet(parquet_path, features=features, cache_dir=cache_dir)
    _check_parquet_dataset(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_parquet_split(split, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = Dataset.from_parquet(parquet_path, cache_dir=cache_dir, split=split)
    _check_parquet_dataset(dataset, expected_features)
    assert dataset.split == str(split) if split else "train"


@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_parquet_path_type(path_type, parquet_path, tmp_path):
    if issubclass(path_type, str):
        path = parquet_path
    elif issubclass(path_type, list):
        path = [parquet_path]
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = Dataset.from_parquet(path, cache_dir=cache_dir)
    _check_parquet_dataset(dataset, expected_features)


def _check_text_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 1
    assert dataset.column_names == ["text"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_text_keep_in_memory(keep_in_memory, text_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"text": "string"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_text(text_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory)
    _check_text_dataset(dataset, expected_features)


@pytest.mark.parametrize(
    "features",
    [
        None,
        {"text": "string"},
        {"text": "int32"},
        {"text": "float32"},
    ],
)
def test_dataset_from_text_features(features, text_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"text": "string"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = Dataset.from_text(text_path, features=features, cache_dir=cache_dir)
    _check_text_dataset(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_text_split(split, text_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"text": "string"}
    dataset = Dataset.from_text(text_path, cache_dir=cache_dir, split=split)
    _check_text_dataset(dataset, expected_features)
    assert dataset.split == str(split) if split else "train"


@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_text_path_type(path_type, text_path, tmp_path):
    if issubclass(path_type, str):
        path = text_path
    elif issubclass(path_type, list):
        path = [text_path]
    cache_dir = tmp_path / "cache"
    expected_features = {"text": "string"}
    dataset = Dataset.from_text(path, cache_dir=cache_dir)
    _check_text_dataset(dataset, expected_features)


def test_dataset_to_json(dataset, tmp_path):
    file_path = tmp_path / "test_path.jsonl"
    bytes_written = dataset.to_json(path_or_buf=file_path)
    assert file_path.is_file()
    assert bytes_written == file_path.stat().st_size
    df = pd.read_json(file_path, orient="records", lines=True)
    assert df.shape == dataset.shape
    assert list(df.columns) == list(dataset.column_names)


@pytest.mark.parametrize("in_memory", [False, True])
@pytest.mark.parametrize(
    "method_and_params",
    [
        ("rename_column", tuple(), {"original_column_name": "labels", "new_column_name": "label"}),
        ("remove_columns", tuple(), {"column_names": "labels"}),
        (
            "cast",
            tuple(),
            {
                "features": Features(
                    {
                        "tokens": Sequence(Value("string")),
                        "labels": Sequence(Value("int16")),
                        "answers": Sequence(
                            {
                                "text": Value("string"),
                                "answer_start": Value("int32"),
                            }
                        ),
                        "id": Value("int32"),
                    }
                )
            },
        ),
        ("flatten", tuple(), {}),
        ("rename_column_", tuple(), {"original_column_name": "labels", "new_column_name": "label"}),
        ("remove_columns_", tuple(), {"column_names": "labels"}),
        (
            "cast_",
            tuple(),
            {
                "features": Features(
                    {
                        "tokens": Sequence(Value("string")),
                        "labels": Sequence(Value("int16")),
                        "answers": Sequence(
                            {
                                "text": Value("string"),
                                "answer_start": Value("int32"),
                            }
                        ),
                        "id": Value("int32"),
                    }
                )
            },
        ),
        ("flatten_", tuple(), {}),
    ],
)
def test_pickle_dataset_after_transforming_the_table(in_memory, method_and_params, arrow_file):
    method, args, kwargs = method_and_params
    with Dataset.from_file(arrow_file, in_memory=in_memory) as dataset, Dataset.from_file(
        arrow_file, in_memory=in_memory
    ) as reference_dataset:
        out = getattr(dataset, method)(*args, **kwargs)
        dataset = out if out is not None else dataset
        pickled_dataset = pickle.dumps(dataset)
        reloaded_dataset = pickle.loads(pickled_dataset)

        assert dataset._data != reference_dataset._data
        assert dataset._data.table == reloaded_dataset._data.table


@require_s3
def test_dummy_dataset_serialize_s3(s3, dataset):
    mock_bucket = s3_test_bucket_name
    dataset_path = f"s3://{mock_bucket}/my_dataset"
    features = dataset.features
    dataset.save_to_disk(dataset_path, s3)
    dataset = dataset.load_from_disk(dataset_path, s3)
    assert os.path.isfile(dataset.cache_files[0]["filename"])

    assert len(dataset) == 10
    assert len(dataset.shuffle()) == 10
    assert dataset.features == features
    assert dataset[0]["id"] == 0
    assert dataset["id"][0] == 0


@pytest.mark.parametrize(
    "uri_or_path",
    [
        "relative/path",
        "/absolute/path",
        "s3://bucket/relative/path",
        "hdfs://relative/path",
        "hdfs:///absolute/path",
    ],
)
def test_build_local_temp_path(uri_or_path):
    extracted_path = extract_path_from_uri(uri_or_path)
    local_temp_path = Dataset._build_local_temp_path(extracted_path)
    path_relative_to_tmp_dir = local_temp_path.as_posix().split("tmp")[-1].split("/", 1)[1]

    assert (
        "tmp" in local_temp_path.as_posix()
        and "hdfs" not in path_relative_to_tmp_dir
        and "s3" not in path_relative_to_tmp_dir
        and not local_temp_path.as_posix().startswith(extracted_path)
        and local_temp_path.as_posix().endswith(extracted_path)
    ), f"Local temp path: {local_temp_path.as_posix()}"


class TaskTemplatesTest(TestCase):
    def test_task_text_classification(self):
        labels = sorted(["pos", "neg"])
        features_before_cast = Features(
            {
                "input_text": Value("string"),
                "input_labels": ClassLabel(names=labels),
            }
        )
        # Labels are cast to tuple during `TextClassification.__post_init_`, so we do the same here
        features_after_cast = Features(
            {
                "text": Value("string"),
                "labels": ClassLabel(names=labels),
            }
        )
        # Label names are added in `DatasetInfo.__post_init__` so not needed here
        task_without_labels = TextClassification(text_column="input_text", label_column="input_labels")
        info1 = DatasetInfo(
            features=features_before_cast,
            task_templates=task_without_labels,
        )
        # Label names are required when passing a TextClassification template directly to `Dataset.prepare_for_task`
        # However they also can be used to define `DatasetInfo` so we include a test for this too
        task_with_labels = TextClassification(text_column="input_text", label_column="input_labels")
        info2 = DatasetInfo(
            features=features_before_cast,
            task_templates=task_with_labels,
        )
        data = {"input_text": ["i love transformers!"], "input_labels": [1]}
        # Test we can load from task name when label names not included in template (default behaviour)
        with Dataset.from_dict(data, info=info1) as dset:
            self.assertSetEqual({"input_text", "input_labels"}, set(dset.column_names))
            self.assertDictEqual(features_before_cast, dset.features)
            with dset.prepare_for_task(task="text-classification") as dset:
                self.assertSetEqual({"labels", "text"}, set(dset.column_names))
                self.assertDictEqual(features_after_cast, dset.features)
        # Test we can load from task name when label names included in template
        with Dataset.from_dict(data, info=info2) as dset:
            self.assertSetEqual({"input_text", "input_labels"}, set(dset.column_names))
            self.assertDictEqual(features_before_cast, dset.features)
            with dset.prepare_for_task(task="text-classification") as dset:
                self.assertSetEqual({"labels", "text"}, set(dset.column_names))
                self.assertDictEqual(features_after_cast, dset.features)
        # Test we can load from TextClassification template
        info1.task_templates = None
        with Dataset.from_dict(data, info=info1) as dset:
            with dset.prepare_for_task(task=task_with_labels) as dset:
                self.assertSetEqual({"labels", "text"}, set(dset.column_names))
                self.assertDictEqual(features_after_cast, dset.features)

    def test_task_question_answering(self):
        features_before_cast = Features(
            {
                "input_context": Value("string"),
                "input_question": Value("string"),
                "input_answers": Sequence(
                    {
                        "text": Value("string"),
                        "answer_start": Value("int32"),
                    }
                ),
            }
        )
        features_after_cast = Features(
            {
                "context": Value("string"),
                "question": Value("string"),
                "answers": Sequence(
                    {
                        "text": Value("string"),
                        "answer_start": Value("int32"),
                    }
                ),
            }
        )
        task = QuestionAnsweringExtractive(
            context_column="input_context", question_column="input_question", answers_column="input_answers"
        )
        info = DatasetInfo(features=features_before_cast, task_templates=task)
        data = {
            "input_context": ["huggingface is going to the moon!"],
            "input_question": ["where is huggingface going?"],
            "input_answers": [{"text": ["to the moon!"], "answer_start": [2]}],
        }
        # Test we can load from task name
        with Dataset.from_dict(data, info=info) as dset:
            self.assertSetEqual(
                {"input_context", "input_question", "input_answers.text", "input_answers.answer_start"},
                set(dset.flatten().column_names),
            )
            self.assertDictEqual(features_before_cast, dset.features)
            with dset.prepare_for_task(task="question-answering-extractive") as dset:
                self.assertSetEqual(
                    {"context", "question", "answers.text", "answers.answer_start"},
                    set(dset.flatten().column_names),
                )
                self.assertDictEqual(features_after_cast, dset.features)
        # Test we can load from QuestionAnsweringExtractive template
        info.task_templates = None
        with Dataset.from_dict(data, info=info) as dset:
            with dset.prepare_for_task(task=task) as dset:
                self.assertSetEqual(
                    {"context", "question", "answers.text", "answers.answer_start"},
                    set(dset.flatten().column_names),
                )
                self.assertDictEqual(features_after_cast, dset.features)

    def test_task_summarization(self):
        # Include a dummy extra column `dummy` to test we drop it correctly
        features_before_cast = Features(
            {"input_text": Value("string"), "input_summary": Value("string"), "dummy": Value("string")}
        )
        features_after_cast = Features({"text": Value("string"), "summary": Value("string")})
        task = Summarization(text_column="input_text", summary_column="input_summary")
        info = DatasetInfo(features=features_before_cast, task_templates=task)
        data = {
            "input_text": ["jack and jill took a taxi to attend a super duper party in the city."],
            "input_summary": ["jack and jill attend party"],
            "dummy": ["123456"],
        }
        # Test we can load from task name
        with Dataset.from_dict(data, info=info) as dset:
            with dset.prepare_for_task(task="summarization") as dset:
                self.assertSetEqual(
                    {"text", "summary"},
                    set(dset.column_names),
                )
                self.assertDictEqual(features_after_cast, dset.features)
        # Test we can load from Summarization template
        info.task_templates = None
        with Dataset.from_dict(data, info=info) as dset:
            with dset.prepare_for_task(task=task) as dset:
                self.assertSetEqual(
                    {"text", "summary"},
                    set(dset.column_names),
                )
                self.assertDictEqual(features_after_cast, dset.features)

    def test_task_automatic_speech_recognition(self):
        # Include a dummy extra column `dummy` to test we drop it correctly
        features_before_cast = Features(
            {
                "input_audio_file_path": Value("string"),
                "input_transcription": Value("string"),
                "dummy": Value("string"),
            }
        )
        features_after_cast = Features({"audio_file_path": Value("string"), "transcription": Value("string")})
        task = AutomaticSpeechRecognition(
            audio_file_path_column="input_audio_file_path", transcription_column="input_transcription"
        )
        info = DatasetInfo(features=features_before_cast, task_templates=task)
        data = {
            "input_audio_file_path": ["path/to/some/audio/file.wav"],
            "input_transcription": ["hello, my name is bob!"],
            "dummy": ["123456"],
        }
        # Test we can load from task name
        with Dataset.from_dict(data, info=info) as dset:
            with dset.prepare_for_task(task="automatic-speech-recognition") as dset:
                self.assertSetEqual(
                    {"audio_file_path", "transcription"},
                    set(dset.column_names),
                )
                self.assertDictEqual(features_after_cast, dset.features)
        # Test we can load from Summarization template
        info.task_templates = None
        with Dataset.from_dict(data, info=info) as dset:
            with dset.prepare_for_task(task=task) as dset:
                self.assertSetEqual(
                    {"audio_file_path", "transcription"},
                    set(dset.column_names),
                )
                self.assertDictEqual(features_after_cast, dset.features)

    def test_task_with_no_template(self):
        data = {"input_text": ["i love transformers!"], "input_labels": [1]}
        with Dataset.from_dict(data) as dset:
            with self.assertRaises(ValueError):
                dset.prepare_for_task("text-classification")

    def test_task_with_incompatible_templates(self):
        labels = sorted(["pos", "neg"])
        features = Features(
            {
                "input_text": Value("string"),
                "input_labels": ClassLabel(names=labels),
            }
        )
        task = TextClassification(text_column="input_text", label_column="input_labels")
        info = DatasetInfo(
            features=features,
            task_templates=task,
        )
        data = {"input_text": ["i love transformers!"], "input_labels": [1]}
        with Dataset.from_dict(data, info=info) as dset:
            # Invalid task name
            self.assertRaises(ValueError, dset.prepare_for_task, "this-task-does-not-exist")
            # Invalid task type
            self.assertRaises(ValueError, dset.prepare_for_task, 1)

    def test_task_with_multiple_compatible_task_templates(self):
        features = Features(
            {
                "text1": Value("string"),
                "text2": Value("string"),
            }
        )
        task1 = LanguageModeling(text_column="text1")
        task2 = LanguageModeling(text_column="text2")
        info = DatasetInfo(
            features=features,
            task_templates=[task1, task2],
        )
        data = {"text1": ["i love transformers!"], "text2": ["i love datasets!"]}
        with Dataset.from_dict(data, info=info) as dset:
            self.assertRaises(ValueError, dset.prepare_for_task, "language-modeling", id=3)
            with dset.prepare_for_task("language-modeling") as dset1:
                self.assertEqual(dset1[0]["text"], "i love transformers!")
            with dset.prepare_for_task("language-modeling", id=1) as dset2:
                self.assertEqual(dset2[0]["text"], "i love datasets!")

    def test_task_templates_empty_after_preparation(self):
        features = Features(
            {
                "input_text": Value("string"),
                "input_labels": ClassLabel(names=["pos", "neg"]),
            }
        )
        task = TextClassification(text_column="input_text", label_column="input_labels")
        info = DatasetInfo(
            features=features,
            task_templates=task,
        )
        data = {"input_text": ["i love transformers!"], "input_labels": [1]}
        with Dataset.from_dict(data, info=info) as dset:
            with dset.prepare_for_task(task="text-classification") as dset:
                self.assertIsNone(dset.info.task_templates)

    def test_align_labels_with_mapping(self):
        features = Features(
            {
                "input_text": Value("string"),
                "input_labels": ClassLabel(num_classes=3, names=["entailment", "neutral", "contradiction"]),
            }
        )
        data = {"input_text": ["a", "a", "b", "b", "c", "c"], "input_labels": [0, 0, 1, 1, 2, 2]}
        label2id = {"CONTRADICTION": 0, "ENTAILMENT": 2, "NEUTRAL": 1}
        id2label = {v: k for k, v in label2id.items()}
        expected_labels = [2, 2, 1, 1, 0, 0]
        expected_label_names = [id2label[idx] for idx in expected_labels]
        with Dataset.from_dict(data, features=features) as dset:
            with dset.align_labels_with_mapping(label2id, "input_labels") as dset:
                self.assertListEqual(expected_labels, dset["input_labels"])
                aligned_label_names = [dset.features["input_labels"].int2str(idx) for idx in dset["input_labels"]]
                self.assertListEqual(expected_label_names, aligned_label_names)

    def test_concatenate_with_no_task_templates(self):
        info = DatasetInfo(task_templates=None)
        data = {"text": ["i love transformers!"], "labels": [1]}
        with Dataset.from_dict(data, info=info) as dset1, Dataset.from_dict(
            data, info=info
        ) as dset2, Dataset.from_dict(data, info=info) as dset3:
            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                self.assertEqual(dset_concat.info.task_templates, None)

    def test_concatenate_with_equal_task_templates(self):
        labels = ["neg", "pos"]
        task_template = TextClassification(text_column="text", label_column="labels")
        info = DatasetInfo(
            features=Features({"text": Value("string"), "labels": ClassLabel(names=labels)}),
            # Label names are added in `DatasetInfo.__post_init__` so not included here
            task_templates=TextClassification(text_column="text", label_column="labels"),
        )
        data = {"text": ["i love transformers!"], "labels": [1]}
        with Dataset.from_dict(data, info=info) as dset1, Dataset.from_dict(
            data, info=info
        ) as dset2, Dataset.from_dict(data, info=info) as dset3:
            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                self.assertListEqual(dset_concat.info.task_templates, [task_template])

    def test_concatenate_with_mixed_task_templates_in_common(self):
        tc_template = TextClassification(text_column="text", label_column="labels")
        qa_template = QuestionAnsweringExtractive(
            question_column="question", context_column="context", answers_column="answers"
        )
        info1 = DatasetInfo(
            task_templates=[qa_template],
            features=Features(
                {
                    "text": Value("string"),
                    "labels": ClassLabel(names=["pos", "neg"]),
                    "context": Value("string"),
                    "question": Value("string"),
                    "answers": Sequence(
                        {
                            "text": Value("string"),
                            "answer_start": Value("int32"),
                        }
                    ),
                }
            ),
        )
        info2 = DatasetInfo(
            task_templates=[qa_template, tc_template],
            features=Features(
                {
                    "text": Value("string"),
                    "labels": ClassLabel(names=["pos", "neg"]),
                    "context": Value("string"),
                    "question": Value("string"),
                    "answers": Sequence(
                        {
                            "text": Value("string"),
                            "answer_start": Value("int32"),
                        }
                    ),
                }
            ),
        )
        data = {
            "text": ["i love transformers!"],
            "labels": [1],
            "context": ["huggingface is going to the moon!"],
            "question": ["where is huggingface going?"],
            "answers": [{"text": ["to the moon!"], "answer_start": [2]}],
        }
        with Dataset.from_dict(data, info=info1) as dset1, Dataset.from_dict(
            data, info=info2
        ) as dset2, Dataset.from_dict(data, info=info2) as dset3:
            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                self.assertListEqual(dset_concat.info.task_templates, [qa_template])

    def test_concatenate_with_no_mixed_task_templates_in_common(self):
        tc_template1 = TextClassification(text_column="text", label_column="labels")
        tc_template2 = TextClassification(text_column="text", label_column="sentiment")
        qa_template = QuestionAnsweringExtractive(
            question_column="question", context_column="context", answers_column="answers"
        )
        info1 = DatasetInfo(
            features=Features(
                {
                    "text": Value("string"),
                    "labels": ClassLabel(names=["pos", "neg"]),
                    "sentiment": ClassLabel(names=["pos", "neg", "neutral"]),
                    "context": Value("string"),
                    "question": Value("string"),
                    "answers": Sequence(
                        {
                            "text": Value("string"),
                            "answer_start": Value("int32"),
                        }
                    ),
                }
            ),
            task_templates=[tc_template1],
        )
        info2 = DatasetInfo(
            features=Features(
                {
                    "text": Value("string"),
                    "labels": ClassLabel(names=["pos", "neg"]),
                    "sentiment": ClassLabel(names=["pos", "neg", "neutral"]),
                    "context": Value("string"),
                    "question": Value("string"),
                    "answers": Sequence(
                        {
                            "text": Value("string"),
                            "answer_start": Value("int32"),
                        }
                    ),
                }
            ),
            task_templates=[tc_template2],
        )
        info3 = DatasetInfo(
            features=Features(
                {
                    "text": Value("string"),
                    "labels": ClassLabel(names=["pos", "neg"]),
                    "sentiment": ClassLabel(names=["pos", "neg", "neutral"]),
                    "context": Value("string"),
                    "question": Value("string"),
                    "answers": Sequence(
                        {
                            "text": Value("string"),
                            "answer_start": Value("int32"),
                        }
                    ),
                }
            ),
            task_templates=[qa_template],
        )
        data = {
            "text": ["i love transformers!"],
            "labels": [1],
            "sentiment": [0],
            "context": ["huggingface is going to the moon!"],
            "question": ["where is huggingface going?"],
            "answers": [{"text": ["to the moon!"], "answer_start": [2]}],
        }
        with Dataset.from_dict(data, info=info1) as dset1, Dataset.from_dict(
            data, info=info2
        ) as dset2, Dataset.from_dict(data, info=info3) as dset3:
            with concatenate_datasets([dset1, dset2, dset3]) as dset_concat:
                self.assertEqual(dset_concat.info.task_templates, None)

    def test_task_text_classification_when_columns_removed(self):
        labels = sorted(["pos", "neg"])
        features_before_map = Features(
            {
                "input_text": Value("string"),
                "input_labels": ClassLabel(names=labels),
            }
        )
        features_after_map = Features({"new_column": Value("int64")})
        # Label names are added in `DatasetInfo.__post_init__` so not needed here
        task = TextClassification(text_column="input_text", label_column="input_labels")
        info = DatasetInfo(
            features=features_before_map,
            task_templates=task,
        )
        data = {"input_text": ["i love transformers!"], "input_labels": [1]}
        with Dataset.from_dict(data, info=info) as dset:
            with dset.map(lambda x: {"new_column": 0}, remove_columns=dset.column_names) as dset:
                self.assertDictEqual(dset.features, features_after_map)
