import asyncio
import contextlib
import copy
import itertools
import json
import os
import pickle
import re
import sys
import tempfile
import time
from functools import partial
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

import numpy as np
import numpy.testing as npt
import pandas as pd
import pyarrow as pa
import pytest
from absl.testing import parameterized
from fsspec.core import strip_protocol
from packaging import version

import datasets.arrow_dataset
from datasets import concatenate_datasets, interleave_datasets, load_from_disk
from datasets.arrow_dataset import Dataset, transmit_format, update_metadata_with_features
from datasets.dataset_dict import DatasetDict
from datasets.features import (
    Array2D,
    Array3D,
    ClassLabel,
    Features,
    Image,
    LargeList,
    Sequence,
    Translation,
    TranslationVariableLanguages,
    Value,
)
from datasets.info import DatasetInfo
from datasets.iterable_dataset import IterableDataset
from datasets.splits import NamedSplit
from datasets.table import ConcatenationTable, InMemoryTable, MemoryMappedTable
from datasets.utils.logging import INFO, get_logger
from datasets.utils.py_utils import temp_seed

from .utils import (
    assert_arrow_memory_doesnt_increase,
    assert_arrow_memory_increases,
    require_dill_gt_0_3_2,
    require_jax,
    require_not_windows,
    require_numpy1_on_windows,
    require_pil,
    require_polars,
    require_pyspark,
    require_sqlalchemy,
    require_tf,
    require_torch,
    require_transformers,
    set_current_working_directory_to_temp_dir,
)


class PickableMagicMock(MagicMock):
    def __reduce__(self):
        return MagicMock, ()


class Unpicklable:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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


def picklable_filter_function_with_rank(x, r):
    return r == 0


def assert_arrow_metadata_are_synced_with_dataset_features(dataset: Dataset):
    assert dataset.data.schema.metadata is not None
    assert b"huggingface" in dataset.data.schema.metadata
    metadata = json.loads(dataset.data.schema.metadata[b"huggingface"].decode())
    assert "info" in metadata
    features = DatasetInfo.from_dict(metadata["info"]).features
    assert features is not None
    assert features == dataset.features
    assert features == Features.from_arrow_schema(dataset.data.schema)
    assert list(features) == dataset.data.column_names
    assert list(features) == list(dataset.features)


IN_MEMORY_PARAMETERS = [
    {"testcase_name": name, "in_memory": im} for im, name in [(True, "in_memory"), (False, "on_disk")]
]


@parameterized.named_parameters(IN_MEMORY_PARAMETERS)
class BaseDatasetTest(TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, set_sqlalchemy_silence_uber_warning):
        self._caplog = caplog

    def _create_dummy_dataset(
        self,
        in_memory: bool,
        tmp_dir: str,
        multiple_columns=False,
        array_features=False,
        nested_features=False,
        int_to_float=False,
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
        elif int_to_float:
            data = {
                "text": ["text1", "text2", "text3", "text4"],
                "labels": [[1, 1, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 0]],
            }
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
                self.assertListEqual(dset[range(0, -2, -1)]["filename"], ["my_name-train_0", "my_name-train_29"])
                self.assertListEqual(dset[np.array([0, -1])]["filename"], ["my_name-train_0", "my_name-train_29"])
                self.assertListEqual(dset[pd.Series([0, -1])]["filename"], ["my_name-train_0", "my_name-train_29"])

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

            with self._create_dummy_dataset(in_memory, tmp_dir).select(range(0, 10, 2)) as dset:
                with open(tmp_file, "wb") as f:
                    pickle.dump(dset, f)

            with open(tmp_file, "rb") as f:
                with pickle.load(f) as dset:
                    self.assertEqual(len(dset), 5)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertEqual(dset[0]["filename"], "my_name-train_0")
                    self.assertEqual(dset["filename"][0], "my_name-train_0")

            with self._create_dummy_dataset(in_memory, tmp_dir).select(
                range(0, 10, 2), indices_cache_file_name=os.path.join(tmp_dir, "ind.arrow")
            ) as dset:
                if not in_memory:
                    dset._data.table = Unpicklable()
                dset._indices.table = Unpicklable()
                with open(tmp_file, "wb") as f:
                    pickle.dump(dset, f)

            with open(tmp_file, "rb") as f:
                with pickle.load(f) as dset:
                    self.assertEqual(len(dset), 5)
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
                    expected = dset.to_dict()

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

            with self._create_dummy_dataset(in_memory, tmp_dir).select(range(10)) as dset:
                with assert_arrow_memory_doesnt_increase():
                    dset.save_to_disk(dataset_path, num_shards=4)

            with Dataset.load_from_disk(dataset_path) as dset:
                self.assertEqual(len(dset), 10)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertDictEqual(dset.to_dict(), expected)
                self.assertEqual(len(dset.cache_files), 4)

            with self._create_dummy_dataset(in_memory, tmp_dir).select(range(10)) as dset:
                with assert_arrow_memory_doesnt_increase():
                    dset.save_to_disk(dataset_path, num_proc=2)

            with Dataset.load_from_disk(dataset_path) as dset:
                self.assertEqual(len(dset), 10)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertDictEqual(dset.to_dict(), expected)
                self.assertEqual(len(dset.cache_files), 2)

            with self._create_dummy_dataset(in_memory, tmp_dir).select(range(10)) as dset:
                with assert_arrow_memory_doesnt_increase():
                    dset.save_to_disk(dataset_path, num_shards=7, num_proc=2)

            with Dataset.load_from_disk(dataset_path) as dset:
                self.assertEqual(len(dset), 10)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertDictEqual(dset.to_dict(), expected)
                self.assertEqual(len(dset.cache_files), 7)

            with self._create_dummy_dataset(in_memory, tmp_dir).select(range(10)) as dset:
                with assert_arrow_memory_doesnt_increase():
                    max_shard_size = dset._estimate_nbytes() // 2 + 1
                    dset.save_to_disk(dataset_path, max_shard_size=max_shard_size)

            with Dataset.load_from_disk(dataset_path) as dset:
                self.assertEqual(len(dset), 10)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertDictEqual(dset.to_dict(), expected)
                self.assertEqual(len(dset.cache_files), 2)

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

    def test_restore_saved_format(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.set_format(type="numpy", columns=["col_1"], output_all_columns=True)
                dataset_path = os.path.join(tmp_dir, "my_dataset")
                dset.save_to_disk(dataset_path)

                with load_from_disk(dataset_path) as loaded_dset:
                    self.assertEqual(dset.format, loaded_dset.format)

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

    @require_numpy1_on_windows
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

                dset.set_format(type="torch")
                self.assertEqual(len(dset[0]), 3)
                self.assertIsInstance(dset[0]["col_1"], torch.Tensor)
                self.assertIsInstance(dset["col_1"], torch.Tensor)
                self.assertListEqual(list(dset[0]["col_1"].shape), [])
                self.assertEqual(dset[0]["col_1"].item(), 3)
                self.assertIsInstance(dset[0]["col_2"], str)
                self.assertEqual(dset[0]["col_2"], "a")
                self.assertIsInstance(dset[0]["col_3"], torch.Tensor)
                self.assertIsInstance(dset["col_3"], torch.Tensor)
                self.assertListEqual(list(dset[0]["col_3"].shape), [])

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

    @require_polars
    def test_set_format_polars(self, in_memory):
        import polars as pl

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.set_format(type="polars", columns=["col_1"])
                self.assertEqual(len(dset[0].columns), 1)
                self.assertIsInstance(dset[0], pl.DataFrame)
                self.assertListEqual(list(dset[0].shape), [1, 1])
                self.assertEqual(dset[0]["col_1"].item(), 3)

                dset.set_format(type="polars", columns=["col_1", "col_2"])
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

            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset._format_columns = ["col_1", "col_2", "col_3"]
                with dset.remove_columns(column_names=["col_1"]) as new_dset:
                    self.assertListEqual(new_dset._format_columns, ["col_2", "col_3"])
                    self.assertEqual(new_dset.num_columns, 2)
                    self.assertListEqual(list(new_dset.column_names), ["col_2", "col_3"])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(new_dset)

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

    def test_select_columns(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                fingerprint = dset._fingerprint
                with dset.select_columns(column_names=[]) as new_dset:
                    self.assertEqual(new_dset.num_columns, 0)
                    self.assertListEqual(list(new_dset.column_names), [])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(new_dset)

            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                fingerprint = dset._fingerprint
                with dset.select_columns(column_names="col_1") as new_dset:
                    self.assertEqual(new_dset.num_columns, 1)
                    self.assertListEqual(list(new_dset.column_names), ["col_1"])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(new_dset)

            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                with dset.select_columns(column_names=["col_1", "col_2", "col_3"]) as new_dset:
                    self.assertEqual(new_dset.num_columns, 3)
                    self.assertListEqual(list(new_dset.column_names), ["col_1", "col_2", "col_3"])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(new_dset)

            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                with dset.select_columns(column_names=["col_3", "col_2", "col_1"]) as new_dset:
                    self.assertEqual(new_dset.num_columns, 3)
                    self.assertListEqual(list(new_dset.column_names), ["col_3", "col_2", "col_1"])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(new_dset)

            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset._format_columns = ["col_1", "col_2", "col_3"]
                with dset.select_columns(column_names=["col_1"]) as new_dset:
                    self.assertListEqual(new_dset._format_columns, ["col_1"])
                    self.assertEqual(new_dset.num_columns, 1)
                    self.assertListEqual(list(new_dset.column_names), ["col_1"])
                    self.assertNotEqual(new_dset._fingerprint, fingerprint)
                    assert_arrow_metadata_are_synced_with_dataset_features(new_dset)

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
                self.assertTupleEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
                self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
                self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
                self.assertEqual(len(dset_concat.cache_files), 0 if in_memory else 3)
                self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2")
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
            dset1, dset2, dset3 = dset1.select([2, 1, 0]), dset2.select([2, 1, 0]), dset3

            with concatenate_datasets([dset3, dset2, dset1]) as dset_concat:
                self.assertTupleEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 3))
                self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
                self.assertListEqual(dset_concat["id"], [6, 7, 8, 5, 4, 3, 2, 1, 0])
                # in_memory = False:
                # 3 cache files for the dset_concat._data table
                # no cache file for the indices because it's in memory
                # in_memory = True:
                # no cache files since both dset_concat._data and dset_concat._indices are in memory
                self.assertEqual(len(dset_concat.cache_files), 0 if in_memory else 3)
                self.assertEqual(dset_concat.info.description, "Dataset2\n\nDataset1")

            dset1 = dset1.rename_columns({"id": "id1"})
            dset2 = dset2.rename_columns({"id": "id2"})
            dset3 = dset3.rename_columns({"id": "id3"})
            with concatenate_datasets([dset1, dset2, dset3], axis=1) as dset_concat:
                self.assertTupleEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 3))
                self.assertEqual(len(dset_concat), len(dset1))
                self.assertListEqual(dset_concat["id1"], [2, 1, 0])
                self.assertListEqual(dset_concat["id2"], [5, 4, 3])
                self.assertListEqual(dset_concat["id3"], [6, 7, 8])
                # in_memory = False:
                # 3 cache files for the dset_concat._data table
                # no cache file for the indices because it's None
                # in_memory = True:
                # no cache files since dset_concat._data is in memory and dset_concat._indices is None
                self.assertEqual(len(dset_concat.cache_files), 0 if in_memory else 3)
                self.assertIsNone(dset_concat._indices)
                self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2")

            with concatenate_datasets([dset1], axis=1) as dset_concat:
                self.assertEqual(len(dset_concat), len(dset1))
                self.assertListEqual(dset_concat["id1"], [2, 1, 0])
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
                dset1.select([2, 1, 0], indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow")),
                dset2.select([2, 1, 0], indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow")),
                dset3.select([1, 0], indices_cache_file_name=os.path.join(tmp_dir, "i3.arrow")),
            )

            with concatenate_datasets([dset3, dset2, dset1]) as dset_concat:
                self.assertTupleEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
                self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
                self.assertListEqual(dset_concat["id"], [7, 6, 5, 4, 3, 2, 1, 0])
                # in_memory = False:
                # 3 cache files for the dset_concat._data table, and 1 for the dset_concat._indices_table
                # There is only 1 for the indices tables (i1.arrow)
                # Indeed, the others are brought to memory since an offset is applied to them.
                # in_memory = True:
                # 1 cache file for i1.arrow since both dset_concat._data and dset_concat._indices are in memory
                self.assertEqual(len(dset_concat.cache_files), 1 if in_memory else 3 + 1)
                self.assertEqual(dset_concat.info.description, "Dataset2\n\nDataset1")
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
            schema = dset1.data.schema
            # mix from in-memory and on-disk datasets
            dset1, dset2 = self._to(in_memory, tmp_dir, dset1, dset2)
            dset3 = self._to(not in_memory, tmp_dir, dset3)
            dset1, dset2, dset3 = (
                dset1.select(
                    [2, 1, 0],
                    keep_in_memory=in_memory,
                    indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow") if not in_memory else None,
                ),
                dset2.select(
                    [2, 1, 0],
                    keep_in_memory=in_memory,
                    indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow") if not in_memory else None,
                ),
                dset3.select(
                    [1, 0],
                    keep_in_memory=in_memory,
                    indices_cache_file_name=os.path.join(tmp_dir, "i3.arrow") if not in_memory else None,
                ),
            )

            dset3 = dset3.rename_column("foo", "new_foo")
            dset3 = dset3.remove_columns("new_foo")
            if in_memory:
                dset3._data.table = Unpicklable(schema=schema)
            else:
                dset1._data.table, dset2._data.table = Unpicklable(schema=schema), Unpicklable(schema=schema)
            dset1, dset2, dset3 = (pickle.loads(pickle.dumps(d)) for d in (dset1, dset2, dset3))
            with concatenate_datasets([dset3, dset2, dset1]) as dset_concat:
                if not in_memory:
                    dset_concat._data.table = Unpicklable(schema=schema)
                with pickle.loads(pickle.dumps(dset_concat)) as dset_concat:
                    self.assertTupleEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
                    self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
                    self.assertListEqual(dset_concat["id"], [7, 6, 5, 4, 3, 2, 1, 0])
                    # in_memory = True: 1 cache file for dset3
                    # in_memory = False: 2 caches files for dset1 and dset2, and 1 cache file for i1.arrow
                    self.assertEqual(len(dset_concat.cache_files), 1 if in_memory else 2 + 1)
                    self.assertEqual(dset_concat.info.description, "Dataset2\n\nDataset1")
            del dset1, dset2, dset3

    def test_repeat(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                repeated_dset = dset.repeat(3)
                column_values_dict = {col: dset[col] for col in dset.column_names}
                for col, single_values in column_values_dict.items():
                    self.assertListEqual(repeated_dset[col], single_values * 3)
                del repeated_dset

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                with pytest.raises(ValueError):
                    dset.repeat(None)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                repeated_dset = dset.repeat(0)
                self.assertEqual(len(repeated_dset), 0)
                del repeated_dset

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                repeated_dset = dset.repeat(-1)
                self.assertEqual(len(repeated_dset), 0)
                del repeated_dset

    def test_flatten(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10},
                features=Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")}),
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fingerprint = dset._fingerprint
                    with dset.flatten() as dset:
                        self.assertListEqual(sorted(dset.column_names), ["a.b.c", "foo"])
                        self.assertListEqual(sorted(dset.features.keys()), ["a.b.c", "foo"])
                        self.assertDictEqual(
                            dset.features, Features({"a.b.c": Sequence(Value("string")), "foo": Value("int64")})
                        )
                        self.assertNotEqual(dset._fingerprint, fingerprint)
                        assert_arrow_metadata_are_synced_with_dataset_features(dset)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"a": [{"en": "Thank you", "fr": "Merci"}] * 10, "foo": [1] * 10},
                features=Features({"a": Translation(languages=["en", "fr"]), "foo": Value("int64")}),
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fingerprint = dset._fingerprint
                    with dset.flatten() as dset:
                        self.assertListEqual(sorted(dset.column_names), ["a.en", "a.fr", "foo"])
                        self.assertListEqual(sorted(dset.features.keys()), ["a.en", "a.fr", "foo"])
                        self.assertDictEqual(
                            dset.features,
                            Features({"a.en": Value("string"), "a.fr": Value("string"), "foo": Value("int64")}),
                        )
                        self.assertNotEqual(dset._fingerprint, fingerprint)
                        assert_arrow_metadata_are_synced_with_dataset_features(dset)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"a": [{"en": "the cat", "fr": ["le chat", "la chatte"], "de": "die katze"}] * 10, "foo": [1] * 10},
                features=Features(
                    {
                        "a": TranslationVariableLanguages(languages=["en", "fr", "de"]),
                        "foo": Value("int64"),
                    }
                ),
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fingerprint = dset._fingerprint
                    with dset.flatten() as dset:
                        self.assertListEqual(sorted(dset.column_names), ["a.language", "a.translation", "foo"])
                        self.assertListEqual(sorted(dset.features.keys()), ["a.language", "a.translation", "foo"])
                        self.assertDictEqual(
                            dset.features,
                            Features(
                                {
                                    "a.language": Sequence(Value("string")),
                                    "a.translation": Sequence(Value("string")),
                                    "foo": Value("int64"),
                                }
                            ),
                        )
                        self.assertNotEqual(dset._fingerprint, fingerprint)
                        assert_arrow_metadata_are_synced_with_dataset_features(dset)

    @require_pil
    def test_flatten_complex_image(self, in_memory):
        # decoding turned on
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"a": [np.arange(4 * 4 * 3, dtype=np.uint8).reshape(4, 4, 3)] * 10, "foo": [1] * 10},
                features=Features({"a": Image(), "foo": Value("int64")}),
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fingerprint = dset._fingerprint
                    with dset.flatten() as dset:
                        self.assertListEqual(sorted(dset.column_names), ["a", "foo"])
                        self.assertListEqual(sorted(dset.features.keys()), ["a", "foo"])
                        self.assertDictEqual(dset.features, Features({"a": Image(), "foo": Value("int64")}))
                        self.assertNotEqual(dset._fingerprint, fingerprint)
                        assert_arrow_metadata_are_synced_with_dataset_features(dset)

        # decoding turned on + nesting
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"a": [{"b": np.arange(4 * 4 * 3, dtype=np.uint8).reshape(4, 4, 3)}] * 10, "foo": [1] * 10},
                features=Features({"a": {"b": Image()}, "foo": Value("int64")}),
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fingerprint = dset._fingerprint
                    with dset.flatten() as dset:
                        self.assertListEqual(sorted(dset.column_names), ["a.b", "foo"])
                        self.assertListEqual(sorted(dset.features.keys()), ["a.b", "foo"])
                        self.assertDictEqual(dset.features, Features({"a.b": Image(), "foo": Value("int64")}))
                        self.assertNotEqual(dset._fingerprint, fingerprint)
                        assert_arrow_metadata_are_synced_with_dataset_features(dset)

        # decoding turned off
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"a": [np.arange(4 * 4 * 3, dtype=np.uint8).reshape(4, 4, 3)] * 10, "foo": [1] * 10},
                features=Features({"a": Image(decode=False), "foo": Value("int64")}),
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fingerprint = dset._fingerprint
                    with dset.flatten() as dset:
                        self.assertListEqual(sorted(dset.column_names), ["a.bytes", "a.path", "foo"])
                        self.assertListEqual(sorted(dset.features.keys()), ["a.bytes", "a.path", "foo"])
                        self.assertDictEqual(
                            dset.features,
                            Features({"a.bytes": Value("binary"), "a.path": Value("string"), "foo": Value("int64")}),
                        )
                        self.assertNotEqual(dset._fingerprint, fingerprint)
                        assert_arrow_metadata_are_synced_with_dataset_features(dset)

        # decoding turned off + nesting
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict(
                {"a": [{"b": np.arange(4 * 4 * 3, dtype=np.uint8).reshape(4, 4, 3)}] * 10, "foo": [1] * 10},
                features=Features({"a": {"b": Image(decode=False)}, "foo": Value("int64")}),
            ) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    fingerprint = dset._fingerprint
                    with dset.flatten() as dset:
                        self.assertListEqual(sorted(dset.column_names), ["a.b.bytes", "a.b.path", "foo"])
                        self.assertListEqual(sorted(dset.features.keys()), ["a.b.bytes", "a.b.path", "foo"])
                        self.assertDictEqual(
                            dset.features,
                            Features(
                                {
                                    "a.b.bytes": Value("binary"),
                                    "a.b.path": Value("string"),
                                    "foo": Value("int64"),
                                }
                            ),
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
        # casting int labels to float labels
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, int_to_float=True) as dset:

                def _preprocess(examples):
                    result = {"labels": [list(map(float, labels)) for labels in examples["labels"]]}
                    return result

                with dset.map(
                    _preprocess, remove_columns=["labels", "text"], batched=True, try_original_type=True
                ) as dset_test:
                    for labels in dset_test["labels"]:
                        for label in labels:
                            self.assertIsInstance(label, int)

                with dset.map(
                    _preprocess, remove_columns=["labels", "text"], batched=True, try_original_type=False
                ) as dset_test:
                    for labels in dset_test["labels"]:
                        for label in labels:
                            self.assertIsInstance(label, float)

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
                    if not in_memory:
                        self.assertIn("_of_00002.arrow", dset_test.cache_files[0]["filename"])
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
            invalid_new_fingerprint = "foobar/hey"
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                self.assertRaises(
                    ValueError, dset.map, picklable_map_function, num_proc=2, new_fingerprint=invalid_new_fingerprint
                )
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
                    self.assertEqual(dset_test._fingerprint, new_fingerprint)
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

    def test_map_new_features(self, in_memory):
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

        # change batch size and drop the last batch
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                batch_size = 4
                with dset.map(
                    map_batched, batched=True, batch_size=batch_size, drop_last_batch=True
                ) as dset_test_batched:
                    self.assertEqual(len(dset_test_batched), 30 // batch_size * batch_size)
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

        # check remove columns for even if the function modifies input in-place
        def map_batched_modifying_inputs_inplace(example):
            result = {"filename_new": [x + "_extension" for x in example["filename"]]}
            del example["filename"]
            return result

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(
                    map_batched_modifying_inputs_inplace, batched=True, remove_columns="filename"
                ) as dset_test_modifying_inputs_inplace:
                    self.assertEqual(len(dset_test_modifying_inputs_inplace), 30)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(
                        dset_test_modifying_inputs_inplace.features,
                        Features({"filename_new": Value("string")}),
                    )
                    assert_arrow_metadata_are_synced_with_dataset_features(dset_test_modifying_inputs_inplace)

    def test_map_nested(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict({"field": ["a", "b"]}) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    with dset.map(lambda example: {"otherfield": {"capital": example["field"].capitalize()}}) as dset:
                        with dset.map(lambda example: {"otherfield": {"append_x": example["field"] + "x"}}) as dset:
                            self.assertEqual(dset[0], {"field": "a", "otherfield": {"append_x": "ax"}})

    def test_map_return_example_as_dict_value(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with Dataset.from_dict({"en": ["aa", "bb"], "fr": ["cc", "dd"]}) as dset:
                with self._to(in_memory, tmp_dir, dset) as dset:
                    with dset.map(lambda example: {"translation": example}) as dset:
                        self.assertEqual(dset[0], {"en": "aa", "fr": "cc", "translation": {"en": "aa", "fr": "cc"}})

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
            with self._caplog.at_level(INFO, logger=get_logger().name):
                with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                    with patch(
                        "datasets.arrow_dataset.Dataset._map_single",
                        autospec=Dataset._map_single,
                        side_effect=Dataset._map_single,
                    ) as mock_map_single:
                        with dset.map(lambda x: {"foo": "bar"}) as dset_test1:
                            dset_test1_data_files = list(dset_test1.cache_files)
                        self.assertEqual(mock_map_single.call_count, 1)
                        with dset.map(lambda x: {"foo": "bar"}) as dset_test2:
                            self.assertEqual(dset_test1_data_files, dset_test2.cache_files)
                            self.assertEqual(len(dset_test2.cache_files), 1 - int(in_memory))
                            self.assertTrue(("Loading cached processed dataset" in self._caplog.text) ^ in_memory)
                        self.assertEqual(mock_map_single.call_count, 2 if in_memory else 1)

        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(INFO, logger=get_logger().name):
                with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                    with dset.map(lambda x: {"foo": "bar"}) as dset_test1:
                        dset_test1_data_files = list(dset_test1.cache_files)
                    with dset.map(lambda x: {"foo": "bar"}, load_from_cache_file=False) as dset_test2:
                        self.assertEqual(dset_test1_data_files, dset_test2.cache_files)
                        self.assertEqual(len(dset_test2.cache_files), 1 - int(in_memory))
                        self.assertNotIn("Loading cached processed dataset", self._caplog.text)

        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(INFO, logger=get_logger().name):
                with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                    with patch(
                        "datasets.arrow_dataset.Pool",
                        new_callable=PickableMagicMock,
                        side_effect=datasets.arrow_dataset.Pool,
                    ) as mock_pool:
                        with dset.map(lambda x: {"foo": "bar"}, num_proc=2) as dset_test1:
                            dset_test1_data_files = list(dset_test1.cache_files)
                        self.assertEqual(mock_pool.call_count, 1)
                        with dset.map(lambda x: {"foo": "bar"}, num_proc=2) as dset_test2:
                            self.assertEqual(dset_test1_data_files, dset_test2.cache_files)
                            self.assertTrue(
                                (len(re.findall("Loading cached processed dataset", self._caplog.text)) == 1)
                                ^ in_memory
                            )
                        self.assertEqual(mock_pool.call_count, 2 if in_memory else 1)

        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(INFO, logger=get_logger().name):
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
                    with self._caplog.at_level(INFO, logger=get_logger().name):
                        with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                            datasets.disable_caching()
                            with dset.map(lambda x: {"foo": "bar"}) as dset_test1:
                                with dset.map(lambda x: {"foo": "bar"}) as dset_test2:
                                    self.assertNotEqual(dset_test1.cache_files, dset_test2.cache_files)
                                    self.assertEqual(len(dset_test1.cache_files), 1)
                                    self.assertEqual(len(dset_test2.cache_files), 1)
                                    self.assertNotIn("Loading cached processed dataset", self._caplog.text)
                                    # make sure the arrow files are going to be removed
                                    self.assertIn(
                                        Path(tempfile.gettempdir()),
                                        Path(dset_test1.cache_files[0]["filename"]).parents,
                                    )
                                    self.assertIn(
                                        Path(tempfile.gettempdir()),
                                        Path(dset_test2.cache_files[0]["filename"]).parents,
                                    )
            finally:
                datasets.enable_caching()

    def test_map_return_pa_table(self, in_memory):
        def func_return_single_row_pa_table(x):
            return pa.table({"id": [0], "text": ["a"]})

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func_return_single_row_pa_table) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"id": Value("int64"), "text": Value("string")}),
                    )
                    self.assertEqual(dset_test[0]["id"], 0)
                    self.assertEqual(dset_test[0]["text"], "a")

        # Batched
        def func_return_single_row_pa_table_batched(x):
            batch_size = len(x[next(iter(x))])
            return pa.table({"id": [0] * batch_size, "text": ["a"] * batch_size})

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func_return_single_row_pa_table_batched, batched=True) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"id": Value("int64"), "text": Value("string")}),
                    )
                    self.assertEqual(dset_test[0]["id"], 0)
                    self.assertEqual(dset_test[0]["text"], "a")

        # Error when returning a table with more than one row in the non-batched mode
        def func_return_multi_row_pa_table(x):
            return pa.table({"id": [0, 1], "text": ["a", "b"]})

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertRaises(ValueError, dset.map, func_return_multi_row_pa_table)

        # arrow formatted dataset
        def func_return_table_from_expression(t):
            import pyarrow.dataset as pds

            return pds.dataset(t).to_table(
                columns={"new_column": pds.field("")._call("ascii_capitalize", [pds.field("filename")])}
            )

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.with_format("arrow").map(func_return_table_from_expression, batched=True) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"new_column": Value("string")}),
                    )
                    self.assertEqual(dset_test.with_format(None)[0]["new_column"], dset[0]["filename"].capitalize())

    def test_map_return_pd_dataframe(self, in_memory):
        def func_return_single_row_pd_dataframe(x):
            return pd.DataFrame({"id": [0], "text": ["a"]})

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func_return_single_row_pd_dataframe) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"id": Value("int64"), "text": Value("string")}),
                    )
                    self.assertEqual(dset_test[0]["id"], 0)
                    self.assertEqual(dset_test[0]["text"], "a")

        # Batched
        def func_return_single_row_pd_dataframe_batched(x):
            batch_size = len(x[next(iter(x))])
            return pd.DataFrame({"id": [0] * batch_size, "text": ["a"] * batch_size})

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func_return_single_row_pd_dataframe_batched, batched=True) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"id": Value("int64"), "text": Value("string")}),
                    )
                    self.assertEqual(dset_test[0]["id"], 0)
                    self.assertEqual(dset_test[0]["text"], "a")

        # Error when returning a table with more than one row in the non-batched mode
        def func_return_multi_row_pd_dataframe(x):
            return pd.DataFrame({"id": [0, 1], "text": ["a", "b"]})

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertRaises(ValueError, dset.map, func_return_multi_row_pd_dataframe)

    @require_polars
    def test_map_return_pl_dataframe(self, in_memory):
        import polars as pl

        def func_return_single_row_pl_dataframe(x):
            return pl.DataFrame({"id": [0], "text": ["a"]})

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func_return_single_row_pl_dataframe) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"id": Value("int64"), "text": Value("large_string")}),
                    )
                    self.assertEqual(dset_test[0]["id"], 0)
                    self.assertEqual(dset_test[0]["text"], "a")

        # Batched
        def func_return_single_row_pl_dataframe_batched(x):
            batch_size = len(x[next(iter(x))])
            return pl.DataFrame({"id": [0] * batch_size, "text": ["a"] * batch_size})

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func_return_single_row_pl_dataframe_batched, batched=True) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"id": Value("int64"), "text": Value("large_string")}),
                    )
                    self.assertEqual(dset_test[0]["id"], 0)
                    self.assertEqual(dset_test[0]["text"], "a")

        # Error when returning a table with more than one row in the non-batched mode
        def func_return_multi_row_pl_dataframe(x):
            return pl.DataFrame({"id": [0, 1], "text": ["a", "b"]})

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertRaises(ValueError, dset.map, func_return_multi_row_pl_dataframe)

    @require_numpy1_on_windows
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

    @require_numpy1_on_windows
    @require_torch
    def test_map_tensor_batched(self, in_memory):
        import torch

        def func(batch):
            return {"tensor": torch.tensor([[1.0, 2, 3]] * len(batch["filename"]))}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with dset.map(func, batched=True) as dset_test:
                    self.assertEqual(len(dset_test), 30)
                    self.assertDictEqual(
                        dset_test.features,
                        Features({"filename": Value("string"), "tensor": Sequence(Value("float32"))}),
                    )
                    self.assertListEqual(dset_test[0]["tensor"], [1, 2, 3])

    def test_map_input_columns(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                with dset.map(lambda col_1: {"label": col_1 % 2}, input_columns="col_1") as mapped_dset:
                    self.assertEqual(mapped_dset[0].keys(), {"col_1", "col_2", "col_3", "label"})
                    self.assertEqual(
                        mapped_dset.features,
                        Features(
                            {
                                "col_1": Value("int64"),
                                "col_2": Value("string"),
                                "col_3": Value("bool"),
                                "label": Value("int64"),
                            }
                        ),
                    )

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
                    with dset.map(lambda x: x, remove_columns=["id"]) as mapped_dset:
                        self.assertTrue("id" not in mapped_dset[0])
                        self.assertDictEqual(
                            mapped_dset.features, Features({"filename": Value("string"), "name": Value("string")})
                        )
                        assert_arrow_metadata_are_synced_with_dataset_features(mapped_dset)
                        with mapped_dset.with_format("numpy", columns=mapped_dset.column_names) as mapped_dset:
                            with mapped_dset.map(
                                lambda x: {"name": 1}, remove_columns=mapped_dset.column_names
                            ) as mapped_dset:
                                self.assertTrue("filename" not in mapped_dset[0])
                                self.assertTrue("name" in mapped_dset[0])
                                self.assertDictEqual(mapped_dset.features, Features({"name": Value(dtype="int64")}))
                                assert_arrow_metadata_are_synced_with_dataset_features(mapped_dset)
                    # empty dataset
                    columns_names = dset.column_names
                    with dset.select([]) as empty_dset:
                        self.assertEqual(len(empty_dset), 0)
                        with empty_dset.map(lambda x: {}, remove_columns=columns_names[0]) as mapped_dset:
                            self.assertListEqual(columns_names[1:], mapped_dset.column_names)
                            assert_arrow_metadata_are_synced_with_dataset_features(mapped_dset)

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

    @require_not_windows
    def test_map_crash_subprocess(self, in_memory):
        # be sure that a crash in one of the subprocess will not
        # hang dataset.map() call forever

        def do_crash(row):
            import os

            os.kill(os.getpid(), 9)
            return row

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                with pytest.raises(RuntimeError) as excinfo:
                    dset.map(do_crash, num_proc=2)
                assert str(excinfo.value) == (
                    "One of the subprocesses has abruptly died during map operation."
                    "To debug the error, disable multiprocessing."
                )

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

    def test_filter_empty(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertIsNone(dset._indices, None)

                tmp_file = os.path.join(tmp_dir, "test.arrow")
                with dset.filter(lambda _: False, cache_file_name=tmp_file) as dset:
                    self.assertEqual(len(dset), 0)
                    self.assertIsNotNone(dset._indices, None)

                    tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
                    with dset.filter(lambda _: False, cache_file_name=tmp_file_2) as dset2:
                        self.assertEqual(len(dset2), 0)
                        self.assertEqual(dset._indices, dset2._indices)

    def test_filter_batched(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"col": [0, 1, 2]})
            with self._to(in_memory, tmp_dir, dset) as dset:
                with dset.filter(lambda x: [i > 0 for i in x["col"]], batched=True) as dset:
                    self.assertListEqual(dset["col"], [1, 2])
                    with dset.filter(lambda x: [i < 2 for i in x["col"]], batched=True) as dset:
                        self.assertListEqual(dset["col"], [1])

    def test_filter_input_columns(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = Dataset.from_dict({"col_1": [0, 1, 2], "col_2": ["a", "b", "c"]})
            with self._to(in_memory, tmp_dir, dset) as dset:
                with dset.filter(lambda x: x > 0, input_columns=["col_1"]) as filtered_dset:
                    self.assertListEqual(filtered_dset.column_names, dset.column_names)
                    self.assertListEqual(filtered_dset["col_1"], [1, 2])
                    self.assertListEqual(filtered_dset["col_2"], ["b", "c"])

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

        with tempfile.TemporaryDirectory() as tmp_dir:  # with_rank
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                fingerprint = dset._fingerprint
                with dset.filter(
                    picklable_filter_function_with_rank, num_proc=2, with_rank=True
                ) as dset_filter_first_rank:
                    self.assertEqual(len(dset_filter_first_rank), min(len(dset) // 2, len(dset)))
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_filter_first_rank.features, Features({"filename": Value("string")}))
                    self.assertEqual(len(dset_filter_first_rank.cache_files), 0 if in_memory else 2)
                    self.assertNotEqual(dset_filter_first_rank._fingerprint, fingerprint)

    def test_filter_caching(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(INFO, logger=get_logger().name):
                with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                    with dset.filter(lambda x, i: i < 5, with_indices=True) as dset_filter_first_five1:
                        dset_test1_data_files = list(dset_filter_first_five1.cache_files)
                    with dset.filter(lambda x, i: i < 5, with_indices=True) as dset_filter_first_five2:
                        self.assertEqual(dset_test1_data_files, dset_filter_first_five2.cache_files)
                        self.assertEqual(len(dset_filter_first_five2.cache_files), 0 if in_memory else 2)
                        self.assertTrue(("Loading cached processed dataset" in self._caplog.text) ^ in_memory)

    def test_keep_features_after_transform_specified(self, in_memory):
        features = Features(
            {
                "tokens": Sequence(Value("string")),
                "labels": Sequence(ClassLabel(names=["negative", "positive"])),
            }
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
            {
                "tokens": Sequence(Value("string")),
                "labels": Sequence(ClassLabel(names=["negative", "positive"])),
            }
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
            {
                "tokens": Sequence(Value("string")),
                "labels": Sequence(ClassLabel(names=["negative", "positive"])),
            }
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
            {
                "tokens": Sequence(Value("string")),
                "labels": Sequence(ClassLabel(names=["negative", "positive"])),
            }
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
            {
                "tokens": Sequence(Value("string")),
                "labels": Sequence(ClassLabel(names=["negative", "positive"])),
            }
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
            {
                "tokens": Sequence(Value("string")),
                "labels": Sequence(ClassLabel(names=["negative", "positive"])),
            }
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
                    self.assertIsNotNone(dset_select_even._indices)  # an indices mapping is created
                    self.assertTrue(os.path.exists(tmp_file))
                    self.assertEqual(len(dset_select_even), 15)
                    for row in dset_select_even:
                        self.assertEqual(int(row["filename"][-1]) % 2, 0)
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_select_even.features, Features({"filename": Value("string")}))
                    self.assertNotEqual(dset_select_even._fingerprint, fingerprint)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                indices = list(range(0, len(dset)))
                with dset.select(indices) as dset_select_all:
                    # no indices mapping, since the indices are contiguous
                    # (in this case the arrow table is simply sliced, which is more efficient)
                    self.assertIsNone(dset_select_all._indices)
                    self.assertEqual(len(dset_select_all), len(dset))
                    self.assertListEqual(list(dset_select_all), list(dset))
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_select_all.features, Features({"filename": Value("string")}))
                    self.assertNotEqual(dset_select_all._fingerprint, fingerprint)
                indices = range(0, len(dset))
                with dset.select(indices) as dset_select_all:
                    # same but with range
                    self.assertIsNone(dset_select_all._indices)
                    self.assertEqual(len(dset_select_all), len(dset))
                    self.assertListEqual(list(dset_select_all), list(dset))
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_select_all.features, Features({"filename": Value("string")}))
                    self.assertNotEqual(dset_select_all._fingerprint, fingerprint)

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
                indices = iter(range(len(dset)))  # iterator of contiguous indices
                with dset.select(indices) as dset_select_all:
                    # no indices mapping, since the indices are contiguous
                    self.assertIsNone(dset_select_all._indices)
                    self.assertEqual(len(dset_select_all), len(dset))
                indices = reversed(range(len(dset)))  # iterator of not contiguous indices
                tmp_file = os.path.join(tmp_dir, "test.arrow")
                with dset.select(indices, indices_cache_file_name=tmp_file) as dset_select_all:
                    # new indices mapping, since the indices are not contiguous
                    self.assertIsNotNone(dset_select_all._indices)
                    self.assertEqual(len(dset_select_all), len(dset))

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
                    self.assertIsNone(dset_select_five._indices)
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
                with dset.rename_column("filename", "file") as dset:
                    self.assertListEqual(dset.column_names, ["file"])
                    with dset.select(range(5)) as dset:
                        self.assertEqual(len(dset), 5)
                        with dset.map(lambda x: {"id": int(x["file"][-1])}) as dset:
                            self.assertListEqual(sorted(dset.column_names), ["file", "id"])
                            with dset.rename_column("id", "number") as dset:
                                self.assertListEqual(sorted(dset.column_names), ["file", "number"])
                                with dset.select([1, 0]) as dset:
                                    self.assertEqual(dset[0]["file"], "my_name-train_1")
                                    self.assertEqual(dset[0]["number"], 1)

                                    self.assertEqual(dset._indices["indices"].to_pylist(), [1, 0])
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

                with dset.shuffle(seed=1234, keep_in_memory=True) as dset_shuffled:
                    self.assertEqual(len(dset_shuffled), 30)
                    self.assertEqual(dset_shuffled[0]["filename"], "my_name-train_28")
                    self.assertEqual(dset_shuffled[2]["filename"], "my_name-train_10")
                    self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                    self.assertDictEqual(dset_shuffled.features, Features({"filename": Value("string")}))
                    self.assertNotEqual(dset_shuffled._fingerprint, fingerprint)

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
            # Sort on a single key
            with self._create_dummy_dataset(in_memory=in_memory, tmp_dir=tmp_dir) as dset:
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
            # Sort on multiple keys
            with self._create_dummy_dataset(in_memory=in_memory, tmp_dir=tmp_dir, multiple_columns=True) as dset:
                tmp_file = os.path.join(tmp_dir, "test_5.arrow")
                fingerprint = dset._fingerprint
                # Throw error when reverse is a list of bools that does not match the length of column_names
                with pytest.raises(ValueError):
                    dset.sort(["col_1", "col_2", "col_3"], reverse=[False])
                with dset.shuffle(seed=1234, indices_cache_file_name=tmp_file) as dset:
                    # Sort
                    with dset.sort(["col_1", "col_2", "col_3"], reverse=[False, True, False]) as dset_sorted:
                        for i, row in enumerate(dset_sorted):
                            self.assertEqual(row["col_1"], i)
                        self.assertDictEqual(
                            dset.features,
                            Features(
                                {
                                    "col_1": Value("int64"),
                                    "col_2": Value("string"),
                                    "col_3": Value("bool"),
                                }
                            ),
                        )
                        self.assertDictEqual(
                            dset_sorted.features,
                            Features(
                                {
                                    "col_1": Value("int64"),
                                    "col_2": Value("string"),
                                    "col_3": Value("bool"),
                                }
                            ),
                        )
                        self.assertNotEqual(dset_sorted._fingerprint, fingerprint)
                        # Sort reversed
                        with dset.sort(["col_1", "col_2", "col_3"], reverse=[True, False, True]) as dset_sorted:
                            for i, row in enumerate(dset_sorted):
                                self.assertEqual(row["col_1"], len(dset_sorted) - 1 - i)
                            self.assertDictEqual(
                                dset.features,
                                Features(
                                    {
                                        "col_1": Value("int64"),
                                        "col_2": Value("string"),
                                        "col_3": Value("bool"),
                                    }
                                ),
                            )
                            self.assertDictEqual(
                                dset_sorted.features,
                                Features(
                                    {
                                        "col_1": Value("int64"),
                                        "col_2": Value("string"),
                                        "col_3": Value("bool"),
                                    }
                                ),
                            )
                            self.assertNotEqual(dset_sorted._fingerprint, fingerprint)
                            # formatted
                            dset.set_format("numpy")
                            with dset.sort(
                                ["col_1", "col_2", "col_3"], reverse=[False, True, False]
                            ) as dset_sorted_formatted:
                                self.assertEqual(dset_sorted_formatted.format["type"], "numpy")

    def test_to_csv(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # File path argument
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                file_path = os.path.join(tmp_dir, "test_path.csv")
                bytes_written = dset.to_csv(path_or_buf=file_path)

                self.assertTrue(os.path.isfile(file_path))
                self.assertEqual(bytes_written, os.path.getsize(file_path))
                csv_dset = pd.read_csv(file_path)

                self.assertEqual(csv_dset.shape, dset.shape)
                self.assertListEqual(list(csv_dset.columns), list(dset.column_names))

            # File buffer argument
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                file_path = os.path.join(tmp_dir, "test_buffer.csv")
                with open(file_path, "wb+") as buffer:
                    bytes_written = dset.to_csv(path_or_buf=buffer)

                self.assertTrue(os.path.isfile(file_path))
                self.assertEqual(bytes_written, os.path.getsize(file_path))
                csv_dset = pd.read_csv(file_path)

                self.assertEqual(csv_dset.shape, dset.shape)
                self.assertListEqual(list(csv_dset.columns), list(dset.column_names))

            # After a select/shuffle transform
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset = dset.select(range(0, len(dset), 2)).shuffle()
                file_path = os.path.join(tmp_dir, "test_path.csv")
                bytes_written = dset.to_csv(path_or_buf=file_path)

                self.assertTrue(os.path.isfile(file_path))
                self.assertEqual(bytes_written, os.path.getsize(file_path))
                csv_dset = pd.read_csv(file_path)

                self.assertEqual(csv_dset.shape, dset.shape)
                self.assertListEqual(list(csv_dset.columns), list(dset.column_names))

            # With array features
            with self._create_dummy_dataset(in_memory, tmp_dir, array_features=True) as dset:
                file_path = os.path.join(tmp_dir, "test_path.csv")
                bytes_written = dset.to_csv(path_or_buf=file_path)

                self.assertTrue(os.path.isfile(file_path))
                self.assertEqual(bytes_written, os.path.getsize(file_path))
                csv_dset = pd.read_csv(file_path)

                self.assertEqual(csv_dset.shape, dset.shape)
                self.assertListEqual(list(csv_dset.columns), list(dset.column_names))

    def test_to_dict(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
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

    def test_to_list(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset_to_list = dset.to_list()
                self.assertIsInstance(dset_to_list, list)
                for row in dset_to_list:
                    self.assertIsInstance(row, dict)
                    self.assertListEqual(sorted(row.keys()), sorted(dset.column_names))

                # With index mapping
                with dset.select([1, 0, 3]) as dset:
                    dset_to_list = dset.to_list()
                    self.assertIsInstance(dset_to_list, list)
                    self.assertEqual(len(dset_to_list), 3)
                    for row in dset_to_list:
                        self.assertIsInstance(row, dict)
                        self.assertListEqual(sorted(row.keys()), sorted(dset.column_names))

    def test_to_pandas(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Batched
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                batch_size = dset.num_rows - 1
                to_pandas_generator = dset.to_pandas(batched=True, batch_size=batch_size)

                for batch in to_pandas_generator:
                    self.assertIsInstance(batch, pd.DataFrame)
                    self.assertListEqual(sorted(batch.columns), sorted(dset.column_names))
                    for col_name in dset.column_names:
                        self.assertLessEqual(len(batch[col_name]), batch_size)

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

    @require_polars
    def test_to_polars(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Batched
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                batch_size = dset.num_rows - 1
                to_polars_generator = dset.to_polars(batched=True, batch_size=batch_size)

                for batch in to_polars_generator:
                    self.assertIsInstance(batch, sys.modules["polars"].DataFrame)
                    self.assertListEqual(sorted(batch.columns), sorted(dset.column_names))
                    for col_name in dset.column_names:
                        self.assertLessEqual(len(batch[col_name]), batch_size)
                    del batch

                # Full
                dset_to_polars = dset.to_polars()
                self.assertIsInstance(dset_to_polars, sys.modules["polars"].DataFrame)
                self.assertListEqual(sorted(dset_to_polars.columns), sorted(dset.column_names))
                for col_name in dset.column_names:
                    self.assertEqual(len(dset_to_polars[col_name]), len(dset))

                # With index mapping
                with dset.select([1, 0, 3]) as dset:
                    dset_to_polars = dset.to_polars()
                    self.assertIsInstance(dset_to_polars, sys.modules["polars"].DataFrame)
                    self.assertEqual(len(dset_to_polars), 3)
                    self.assertListEqual(sorted(dset_to_polars.columns), sorted(dset.column_names))

                    for col_name in dset.column_names:
                        self.assertEqual(len(dset_to_polars[col_name]), dset.num_rows)

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

    @require_sqlalchemy
    def test_to_sql(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Destionation specified as database URI string
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                file_path = os.path.join(tmp_dir, "test_path.sqlite")
                _ = dset.to_sql("data", "sqlite:///" + file_path)

                self.assertTrue(os.path.isfile(file_path))
                sql_dset = pd.read_sql("data", "sqlite:///" + file_path)

                self.assertEqual(sql_dset.shape, dset.shape)
                self.assertListEqual(list(sql_dset.columns), list(dset.column_names))

            # Destionation specified as sqlite3 connection
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                import sqlite3

                file_path = os.path.join(tmp_dir, "test_path.sqlite")
                with contextlib.closing(sqlite3.connect(file_path)) as con:
                    _ = dset.to_sql("data", con, if_exists="replace")

                self.assertTrue(os.path.isfile(file_path))
                sql_dset = pd.read_sql("data", "sqlite:///" + file_path)

                self.assertEqual(sql_dset.shape, dset.shape)
                self.assertListEqual(list(sql_dset.columns), list(dset.column_names))

            # Test writing to a database in chunks
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                file_path = os.path.join(tmp_dir, "test_path.sqlite")
                _ = dset.to_sql("data", "sqlite:///" + file_path, batch_size=1, if_exists="replace")

                self.assertTrue(os.path.isfile(file_path))
                sql_dset = pd.read_sql("data", "sqlite:///" + file_path)

                self.assertEqual(sql_dset.shape, dset.shape)
                self.assertListEqual(list(sql_dset.columns), list(dset.column_names))

            # After a select/shuffle transform
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset = dset.select(range(0, len(dset), 2)).shuffle()
                file_path = os.path.join(tmp_dir, "test_path.sqlite")
                _ = dset.to_sql("data", "sqlite:///" + file_path, if_exists="replace")

                self.assertTrue(os.path.isfile(file_path))
                sql_dset = pd.read_sql("data", "sqlite:///" + file_path)

                self.assertEqual(sql_dset.shape, dset.shape)
                self.assertListEqual(list(sql_dset.columns), list(dset.column_names))

            # With array features
            with self._create_dummy_dataset(in_memory, tmp_dir, array_features=True) as dset:
                file_path = os.path.join(tmp_dir, "test_path.sqlite")
                _ = dset.to_sql("data", "sqlite:///" + file_path, if_exists="replace")

                self.assertTrue(os.path.isfile(file_path))
                sql_dset = pd.read_sql("data", "sqlite:///" + file_path)

                self.assertEqual(sql_dset.shape, dset.shape)
                self.assertListEqual(list(sql_dset.columns), list(dset.column_names))

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
                # Shard non-contiguous
                tmp_file_1 = os.path.join(tmp_dir, "test_1.arrow")
                fingerprint = dset._fingerprint
                with dset.shard(
                    num_shards=8, index=1, contiguous=False, indices_cache_file_name=tmp_file_1
                ) as dset_sharded:
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
                self.assertIsNone(dset._indices)

                tmp_file = os.path.join(tmp_dir, "test.arrow")
                with dset.select(range(0, 10, 2), indices_cache_file_name=tmp_file) as dset:
                    self.assertEqual(len(dset), 5)

                    self.assertIsNotNone(dset._indices)

                    tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
                    fingerprint = dset._fingerprint
                    dset.set_format("numpy")
                    with dset.flatten_indices(cache_file_name=tmp_file_2) as dset:
                        self.assertEqual(len(dset), 5)
                        self.assertEqual(len(dset.data), len(dset))
                        self.assertIsNone(dset._indices)
                        self.assertNotEqual(dset._fingerprint, fingerprint)
                        self.assertEqual(dset.format["type"], "numpy")
                        # Test unique works
                        dset.unique(dset.column_names[0])
                        assert_arrow_metadata_are_synced_with_dataset_features(dset)

        # Empty indices mapping
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir) as dset:
                self.assertIsNone(dset._indices, None)

                tmp_file = os.path.join(tmp_dir, "test.arrow")
                with dset.filter(lambda _: False, cache_file_name=tmp_file) as dset:
                    self.assertEqual(len(dset), 0)

                    self.assertIsNotNone(dset._indices, None)

                    tmp_file_2 = os.path.join(tmp_dir, "test_2.arrow")
                    fingerprint = dset._fingerprint
                    dset.set_format("numpy")
                    with dset.flatten_indices(cache_file_name=tmp_file_2) as dset:
                        self.assertEqual(len(dset), 0)
                        self.assertEqual(len(dset.data), len(dset))
                        self.assertIsNone(dset._indices, None)
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

        with (
            tempfile.TemporaryDirectory() as tmp_dir,
            self._create_dummy_dataset(in_memory, tmp_dir) as dset,
            dset.map(lambda ex, i: {"vec": np.ones(3) * i}, with_indices=True) as dset,
        ):
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
            self.assertTupleEqual(tuple(dset[:2]["vec"].shape), (2, 3))
            self.assertTupleEqual(tuple(dset["vec"][:2].shape), (2, 3))

            dset.set_format("numpy")
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            self.assertIsInstance(dset[0]["filename"], np.str_)
            self.assertIsInstance(dset[:2]["filename"], np.ndarray)
            self.assertIsInstance(dset["filename"], np.ndarray)
            self.assertIsInstance(dset[0]["vec"], np.ndarray)
            self.assertIsInstance(dset[:2]["vec"], np.ndarray)
            self.assertIsInstance(dset["vec"], np.ndarray)
            self.assertTupleEqual(dset[:2]["vec"].shape, (2, 3))
            self.assertTupleEqual(dset["vec"][:2].shape, (2, 3))

            dset.set_format("torch", columns=["vec"])
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            # torch.Tensor is only for numerical columns
            self.assertIsInstance(dset[0]["vec"], torch.Tensor)
            self.assertIsInstance(dset[:2]["vec"], torch.Tensor)
            self.assertIsInstance(dset["vec"][:2], torch.Tensor)
            self.assertTupleEqual(dset[:2]["vec"].shape, (2, 3))
            self.assertTupleEqual(dset["vec"][:2].shape, (2, 3))

    @require_tf
    @require_torch
    def test_format_ragged_vectors(self, in_memory):
        import numpy as np
        import tensorflow as tf
        import torch

        with (
            tempfile.TemporaryDirectory() as tmp_dir,
            self._create_dummy_dataset(in_memory, tmp_dir) as dset,
            dset.map(lambda ex, i: {"vec": np.ones(3 + i) * i}, with_indices=True) as dset,
        ):
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
                self.assertIsInstance(dset[0][col], tf.Tensor)
                self.assertIsInstance(dset[:2][col], tf.RaggedTensor if col == "vec" else tf.Tensor)
                self.assertIsInstance(dset[col], tf.RaggedTensor if col == "vec" else tf.Tensor)
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
            self.assertTupleEqual(dset[:2]["vec"].shape, (2,))
            self.assertTupleEqual(dset["vec"][:2].shape, (2,))

            dset.set_format("torch")
            self.assertIsNotNone(dset[0])
            self.assertIsNotNone(dset[:2])
            self.assertIsInstance(dset[0]["filename"], str)
            self.assertIsInstance(dset[:2]["filename"], list)
            self.assertIsInstance(dset["filename"], list)
            self.assertIsInstance(dset[0]["vec"], torch.Tensor)
            self.assertIsInstance(dset[:2]["vec"][0], torch.Tensor)
            self.assertIsInstance(dset["vec"][0], torch.Tensor)
            # pytorch doesn't support ragged tensors, so we should have lists
            self.assertIsInstance(dset[:2]["vec"], list)
            self.assertIsInstance(dset[:2]["vec"][0], torch.Tensor)
            self.assertIsInstance(dset["vec"][:2], list)
            self.assertIsInstance(dset["vec"][0], torch.Tensor)

    @require_tf
    @require_torch
    def test_format_nested(self, in_memory):
        import numpy as np
        import tensorflow as tf
        import torch

        with (
            tempfile.TemporaryDirectory() as tmp_dir,
            self._create_dummy_dataset(in_memory, tmp_dir) as dset,
            dset.map(lambda ex: {"nested": [{"foo": np.ones(3)}] * len(ex["filename"])}, batched=True) as dset,
        ):
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

    @require_polars
    def test_format_polars(self, in_memory):
        import polars as pl

        with tempfile.TemporaryDirectory() as tmp_dir:
            with self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True) as dset:
                dset.set_format("polars")
                self.assertIsInstance(dset[0], pl.DataFrame)
                self.assertIsInstance(dset[:2], pl.DataFrame)
                self.assertIsInstance(dset["col_1"], pl.Series)

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
        tmp_dir = tempfile.TemporaryDirectory()
        for num_workers in [0, 1, 2]:
            if num_workers > 0 and sys.platform == "win32" and not in_memory:
                continue  # This test hangs on the Py3.10 test worker, but it runs fine locally on my Windows machine
            with self._create_dummy_dataset(in_memory, tmp_dir.name, array_features=True) as dset:
                tf_dataset = dset.to_tf_dataset(columns="col_3", batch_size=2, num_workers=num_workers)
                batch = next(iter(tf_dataset))
                self.assertEqual(batch.shape.as_list(), [2, 4])
                self.assertEqual(batch.dtype.name, "int64")
            with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
                tf_dataset = dset.to_tf_dataset(columns="col_1", batch_size=2, num_workers=num_workers)
                batch = next(iter(tf_dataset))
                self.assertEqual(batch.shape.as_list(), [2])
                self.assertEqual(batch.dtype.name, "int64")
            with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
                # Check that it works with all default options (except batch_size because the dummy dataset only has 4)
                tf_dataset = dset.to_tf_dataset(batch_size=2, num_workers=num_workers)
                batch = next(iter(tf_dataset))
                self.assertEqual(batch["col_1"].shape.as_list(), [2])
                self.assertEqual(batch["col_2"].shape.as_list(), [2])
                self.assertEqual(batch["col_1"].dtype.name, "int64")
                self.assertEqual(batch["col_2"].dtype.name, "string")  # Assert that we're converting strings properly
            with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
                # Check that when we use a transform that creates a new column from existing column values
                # but don't load the old columns that the new column depends on in the final dataset,
                # that they're still kept around long enough to be used in the transform
                transform_dset = dset.with_transform(
                    lambda x: {"new_col": [val * 2 for val in x["col_1"]], "col_1": x["col_1"]}
                )
                tf_dataset = transform_dset.to_tf_dataset(columns="new_col", batch_size=2, num_workers=num_workers)
                batch = next(iter(tf_dataset))
                self.assertEqual(batch.shape.as_list(), [2])
                self.assertEqual(batch.dtype.name, "int64")
                del transform_dset
        del tf_dataset  # For correct cleanup

    @require_tf
    def test_tf_index_reshuffling(self, in_memory):
        # This test checks that when we do two epochs over a tf.data.Dataset from to_tf_dataset
        # that we get a different shuffle order each time
        # It also checks that when we aren't shuffling, that the dataset order is fully preserved
        # even when loading is split across multiple workers
        data = {"col_1": list(range(20))}
        for num_workers in [0, 1, 2, 3]:
            with Dataset.from_dict(data) as dset:
                tf_dataset = dset.to_tf_dataset(batch_size=10, shuffle=True, num_workers=num_workers)
                indices = []
                for batch in tf_dataset:
                    indices.append(batch["col_1"])
                indices = np.concatenate([arr.numpy() for arr in indices])
                second_indices = []
                for batch in tf_dataset:
                    second_indices.append(batch["col_1"])
                second_indices = np.concatenate([arr.numpy() for arr in second_indices])
                self.assertFalse(np.array_equal(indices, second_indices))
                self.assertEqual(len(indices), len(np.unique(indices)))
                self.assertEqual(len(second_indices), len(np.unique(second_indices)))

                tf_dataset = dset.to_tf_dataset(batch_size=1, shuffle=False, num_workers=num_workers)
                for i, batch in enumerate(tf_dataset):
                    # Assert that the unshuffled order is fully preserved even when multiprocessing
                    self.assertEqual(i, batch["col_1"].numpy())

    @require_tf
    def test_tf_label_renaming(self, in_memory):
        # Protect TF-specific imports in here
        import tensorflow as tf

        from datasets.utils.tf_utils import minimal_tf_collate_fn_with_renaming

        tmp_dir = tempfile.TemporaryDirectory()
        with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
            with dset.rename_columns({"col_1": "features", "col_2": "label"}) as new_dset:
                tf_dataset = new_dset.to_tf_dataset(collate_fn=minimal_tf_collate_fn_with_renaming, batch_size=4)
                batch = next(iter(tf_dataset))
                self.assertTrue("labels" in batch and "features" in batch)

                tf_dataset = new_dset.to_tf_dataset(
                    columns=["features", "labels"], collate_fn=minimal_tf_collate_fn_with_renaming, batch_size=4
                )
                batch = next(iter(tf_dataset))
                self.assertTrue("labels" in batch and "features" in batch)

                tf_dataset = new_dset.to_tf_dataset(
                    columns=["features", "label"], collate_fn=minimal_tf_collate_fn_with_renaming, batch_size=4
                )
                batch = next(iter(tf_dataset))
                self.assertTrue("labels" in batch and "features" in batch)  # Assert renaming was handled correctly

                tf_dataset = new_dset.to_tf_dataset(
                    columns=["features"],
                    label_cols=["labels"],
                    collate_fn=minimal_tf_collate_fn_with_renaming,
                    batch_size=4,
                )
                batch = next(iter(tf_dataset))
                self.assertEqual(len(batch), 2)
                # Assert that we don't have any empty entries here
                self.assertTrue(isinstance(batch[0], tf.Tensor) and isinstance(batch[1], tf.Tensor))

                tf_dataset = new_dset.to_tf_dataset(
                    columns=["features"],
                    label_cols=["label"],
                    collate_fn=minimal_tf_collate_fn_with_renaming,
                    batch_size=4,
                )
                batch = next(iter(tf_dataset))
                self.assertEqual(len(batch), 2)
                # Assert that we don't have any empty entries here
                self.assertTrue(isinstance(batch[0], tf.Tensor) and isinstance(batch[1], tf.Tensor))

                tf_dataset = new_dset.to_tf_dataset(
                    columns=["features"],
                    collate_fn=minimal_tf_collate_fn_with_renaming,
                    batch_size=4,
                )
                batch = next(iter(tf_dataset))
                # Assert that labels didn't creep in when we don't ask for them
                # just because the collate_fn added them
                self.assertTrue(isinstance(batch, tf.Tensor))

        del tf_dataset  # For correct cleanup

    @require_tf
    def test_tf_dataset_options(self, in_memory):
        tmp_dir = tempfile.TemporaryDirectory()
        # Test that batch_size option works as expected
        with self._create_dummy_dataset(in_memory, tmp_dir.name, array_features=True) as dset:
            tf_dataset = dset.to_tf_dataset(columns="col_3", batch_size=2)
            batch = next(iter(tf_dataset))
            self.assertEqual(batch.shape.as_list(), [2, 4])
            self.assertEqual(batch.dtype.name, "int64")
        # Test that batch_size=None (optional) works as expected
        with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
            tf_dataset = dset.to_tf_dataset(columns="col_3", batch_size=None)
            single_example = next(iter(tf_dataset))
            self.assertEqual(single_example.shape.as_list(), [])
            self.assertEqual(single_example.dtype.name, "int64")
            # Assert that we can batch it with `tf.data.Dataset.batch` method
            batched_dataset = tf_dataset.batch(batch_size=2)
            batch = next(iter(batched_dataset))
            self.assertEqual(batch.shape.as_list(), [2])
            self.assertEqual(batch.dtype.name, "int64")
        # Test that batching a batch_size=None dataset produces the same results as using batch_size arg
        with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
            batch_size = 2
            tf_dataset_no_batch = dset.to_tf_dataset(columns="col_3")
            tf_dataset_batch = dset.to_tf_dataset(columns="col_3", batch_size=batch_size)
            self.assertEqual(tf_dataset_no_batch.element_spec, tf_dataset_batch.unbatch().element_spec)
            self.assertEqual(tf_dataset_no_batch.cardinality(), tf_dataset_batch.cardinality() * batch_size)
            for batch_1, batch_2 in zip(tf_dataset_no_batch.batch(batch_size=batch_size), tf_dataset_batch):
                self.assertEqual(batch_1.shape, batch_2.shape)
                self.assertEqual(batch_1.dtype, batch_2.dtype)
                self.assertListEqual(batch_1.numpy().tolist(), batch_2.numpy().tolist())
        # Test that requesting label_cols works as expected
        with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
            tf_dataset = dset.to_tf_dataset(columns="col_1", label_cols=["col_2", "col_3"], batch_size=4)
            batch = next(iter(tf_dataset))
            self.assertEqual(len(batch), 2)
            self.assertEqual(set(batch[1].keys()), {"col_2", "col_3"})
            self.assertEqual(batch[0].dtype.name, "int64")
            # Assert data comes out as expected and isn't shuffled
            self.assertEqual(batch[0].numpy().tolist(), [3, 2, 1, 0])
            self.assertEqual(batch[1]["col_2"].numpy().tolist(), [b"a", b"b", b"c", b"d"])
            self.assertEqual(batch[1]["col_3"].numpy().tolist(), [0, 1, 0, 1])
        # Check that incomplete batches are dropped if requested
        with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
            tf_dataset = dset.to_tf_dataset(columns="col_1", batch_size=3)
            tf_dataset_with_drop = dset.to_tf_dataset(columns="col_1", batch_size=3, drop_remainder=True)
            self.assertEqual(len(tf_dataset), 2)  # One batch of 3 and one batch of 1
            self.assertEqual(len(tf_dataset_with_drop), 1)  # Incomplete batch of 1 is dropped
        # Test that `NotImplementedError` is raised `batch_size` is None and `num_workers` is > 0
        with self._create_dummy_dataset(in_memory, tmp_dir.name, multiple_columns=True) as dset:
            with self.assertRaisesRegex(
                NotImplementedError, "`batch_size` must be specified when using multiple workers"
            ):
                dset.to_tf_dataset(columns="col_1", batch_size=None, num_workers=2)
        del tf_dataset  # For correct cleanup
        del tf_dataset_with_drop


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

        features = Features({"col_1": Sequence(Value("string")), "col_2": Value("string")})
        self.assertRaises(TypeError, Dataset.from_pandas, df, features=features)

    @require_polars
    def test_from_polars(self):
        import polars as pl

        data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
        df = pl.from_dict(data)
        with Dataset.from_polars(df) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
            self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("large_string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("large_string")})
        with Dataset.from_polars(df, features=features) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
            self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("large_string")}))

        features = Features({"col_1": Value("int64"), "col_2": Value("large_string")})
        with Dataset.from_polars(df, features=features, info=DatasetInfo(features=features)) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2"])
            self.assertDictEqual(dset.features, Features({"col_1": Value("int64"), "col_2": Value("large_string")}))

        features = Features({"col_1": Sequence(Value("string")), "col_2": Value("large_string")})
        self.assertRaises(TypeError, Dataset.from_polars, df, features=features)

    def test_from_dict(self):
        data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"], "col_3": pa.array([True, False, True, False])}
        with Dataset.from_dict(data) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(dset["col_3"], data["col_3"].to_pylist())
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2", "col_3"])
            self.assertDictEqual(
                dset.features, Features({"col_1": Value("int64"), "col_2": Value("string"), "col_3": Value("bool")})
            )

        features = Features({"col_1": Value("int64"), "col_2": Value("string"), "col_3": Value("bool")})
        with Dataset.from_dict(data, features=features) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(dset["col_3"], data["col_3"].to_pylist())
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2", "col_3"])
            self.assertDictEqual(
                dset.features, Features({"col_1": Value("int64"), "col_2": Value("string"), "col_3": Value("bool")})
            )

        features = Features({"col_1": Value("int64"), "col_2": Value("string"), "col_3": Value("bool")})
        with Dataset.from_dict(data, features=features, info=DatasetInfo(features=features)) as dset:
            self.assertListEqual(dset["col_1"], data["col_1"])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(dset["col_3"], data["col_3"].to_pylist())
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2", "col_3"])
            self.assertDictEqual(
                dset.features, Features({"col_1": Value("int64"), "col_2": Value("string"), "col_3": Value("bool")})
            )

        features = Features({"col_1": Value("string"), "col_2": Value("string"), "col_3": Value("int32")})
        with Dataset.from_dict(data, features=features) as dset:
            # the integers are converted to strings
            self.assertListEqual(dset["col_1"], [str(x) for x in data["col_1"]])
            self.assertListEqual(dset["col_2"], data["col_2"])
            self.assertListEqual(dset["col_3"], [int(x) for x in data["col_3"].to_pylist()])
            self.assertListEqual(list(dset.features.keys()), ["col_1", "col_2", "col_3"])
            self.assertDictEqual(
                dset.features, Features({"col_1": Value("string"), "col_2": Value("string"), "col_3": Value("int32")})
            )

        features = Features({"col_1": Value("int64"), "col_2": Value("int64"), "col_3": Value("bool")})
        self.assertRaises(ValueError, Dataset.from_dict, data, features=features)

    def test_concatenate_mixed_memory_and_disk(self):
        data1, data2, data3 = {"id": [0, 1, 2]}, {"id": [3, 4, 5]}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        with tempfile.TemporaryDirectory() as tmp_dir:
            with (
                Dataset.from_dict(data1, info=info1).map(cache_file_name=os.path.join(tmp_dir, "d1.arrow")) as dset1,
                Dataset.from_dict(data2, info=info2).map(cache_file_name=os.path.join(tmp_dir, "d2.arrow")) as dset2,
                Dataset.from_dict(data3) as dset3,
            ):
                with concatenate_datasets([dset1, dset2, dset3]) as concatenated_dset:
                    self.assertEqual(len(concatenated_dset), len(dset1) + len(dset2) + len(dset3))
                    self.assertListEqual(concatenated_dset["id"], dset1["id"] + dset2["id"] + dset3["id"])

    @require_transformers
    @pytest.mark.integration
    def test_set_format_encode(self):
        from transformers import BertTokenizer

        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        def encode(batch):
            return tokenizer(batch["text"], padding="longest", return_tensors="np")

        with Dataset.from_dict({"text": ["hello there", "foo"]}) as dset:
            dset.set_transform(transform=encode)
            self.assertEqual(str(dset[:2]), str(encode({"text": ["hello there", "foo"]})))

    @require_tf
    def test_tf_string_encoding(self):
        data = {"col_1": ["á", "é", "í", "ó", "ú"], "col_2": ["à", "è", "ì", "ò", "ù"]}
        with Dataset.from_dict(data) as dset:
            tf_dset_wo_batch = dset.to_tf_dataset(columns=["col_1", "col_2"])
            for tf_row, row in zip(tf_dset_wo_batch, dset):
                self.assertEqual(tf_row["col_1"].numpy().decode("utf-8"), row["col_1"])
                self.assertEqual(tf_row["col_2"].numpy().decode("utf-8"), row["col_2"])

            tf_dset_w_batch = dset.to_tf_dataset(columns=["col_1", "col_2"], batch_size=2)
            for tf_row, row in zip(tf_dset_w_batch.unbatch(), dset):
                self.assertEqual(tf_row["col_1"].numpy().decode("utf-8"), row["col_1"])
                self.assertEqual(tf_row["col_2"].numpy().decode("utf-8"), row["col_2"])

            self.assertEqual(tf_dset_w_batch.unbatch().element_spec, tf_dset_wo_batch.element_spec)
            self.assertEqual(tf_dset_w_batch.element_spec, tf_dset_wo_batch.batch(2).element_spec)


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


def test_interleave_datasets_oversampling_strategy():
    d1 = Dataset.from_dict({"a": [0, 1, 2]})
    d2 = Dataset.from_dict({"a": [10, 11, 12, 13]})
    d3 = Dataset.from_dict({"a": [22, 21, 20]}).select([2, 1, 0])
    dataset = interleave_datasets([d1, d2, d3], stopping_strategy="all_exhausted")
    expected_length = 3 * max(len(d1), len(d2), len(d3))
    expected_values = [0, 10, 20, 1, 11, 21, 2, 12, 22, 0, 13, 20]  # hardcoded
    assert isinstance(dataset, Dataset)
    assert len(dataset) == expected_length
    assert dataset["a"] == expected_values
    assert dataset._fingerprint == interleave_datasets([d1, d2, d3], stopping_strategy="all_exhausted")._fingerprint


def test_interleave_datasets_probabilities_oversampling_strategy():
    seed = 42
    probabilities = [0.3, 0.5, 0.2]
    d1 = Dataset.from_dict({"a": [0, 1, 2]})
    d2 = Dataset.from_dict({"a": [10, 11, 12, 13]})
    d3 = Dataset.from_dict({"a": [22, 21, 20]}).select([2, 1, 0])
    dataset = interleave_datasets(
        [d1, d2, d3], stopping_strategy="all_exhausted", probabilities=probabilities, seed=seed
    )
    expected_length = 16  # hardcoded
    expected_values = [10, 11, 20, 12, 0, 21, 13, 10, 1, 11, 12, 22, 13, 20, 10, 2]  # hardcoded
    assert isinstance(dataset, Dataset)
    assert len(dataset) == expected_length
    assert dataset["a"] == expected_values
    assert (
        dataset._fingerprint
        == interleave_datasets(
            [d1, d2, d3], stopping_strategy="all_exhausted", probabilities=probabilities, seed=seed
        )._fingerprint
    )


@pytest.mark.parametrize("batch_size", [4, 5])
@pytest.mark.parametrize("drop_last_batch", [False, True])
def test_dataset_iter_batch(batch_size, drop_last_batch):
    n = 25
    dset = Dataset.from_dict({"i": list(range(n))})
    all_col_values = list(range(n))
    batches = []
    for i, batch in enumerate(dset.iter(batch_size, drop_last_batch=drop_last_batch)):
        assert batch == {"i": all_col_values[i * batch_size : (i + 1) * batch_size]}
        batches.append(batch)
    if drop_last_batch:
        assert all(len(batch["i"]) == batch_size for batch in batches)
    else:
        assert all(len(batch["i"]) == batch_size for batch in batches[:-1])
        assert len(batches[-1]["i"]) <= batch_size


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
        {"col_1": "2", "col_2": 2, "col_3": 2.0},
        {"col_1": "2", "col_2": "2", "col_3": "2"},
        {"col_1": 2, "col_2": 2, "col_3": 2},
        {"col_1": 2.0, "col_2": 2.0, "col_3": 2.0},
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


def test_dataset_filter_batched_indices():
    ds = Dataset.from_dict({"num": [0, 1, 2, 3]})
    ds = ds.filter(lambda num: num % 2 == 0, input_columns="num", batch_size=2)
    assert all(item["num"] % 2 == 0 for item in ds)


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
    assert dataset.split == split if split else "train"


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
        {
            "col_1": ClassLabel(names=["s0", "s1", "s2", "s3"]),
            "col_2": Value("int64"),
            "col_3": Value("float64"),
        }
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
    assert dataset.split == split if split else "train"


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
    assert dataset.split == split if split else "train"


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
    assert dataset.split == split if split else "train"


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


@pytest.fixture
def data_generator():
    def _gen():
        data = [
            {"col_1": "0", "col_2": 0, "col_3": 0.0},
            {"col_1": "1", "col_2": 1, "col_3": 1.0},
            {"col_1": "2", "col_2": 2, "col_3": 2.0},
            {"col_1": "3", "col_2": 3, "col_3": 3.0},
        ]
        for item in data:
            yield item

    return _gen


def _check_generator_dataset(dataset, expected_features, split):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.split == split
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_generator_keep_in_memory(keep_in_memory, data_generator, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_generator(data_generator, cache_dir=cache_dir, keep_in_memory=keep_in_memory)
    _check_generator_dataset(dataset, expected_features, NamedSplit("train"))


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
def test_dataset_from_generator_features(features, data_generator, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = Dataset.from_generator(data_generator, features=features, cache_dir=cache_dir)
    _check_generator_dataset(dataset, expected_features, NamedSplit("train"))


@pytest.mark.parametrize(
    "split",
    [None, NamedSplit("train"), "train", NamedSplit("foo"), "foo"],
)
def test_dataset_from_generator_split(split, data_generator, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_split = "train"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_split = split if split else default_expected_split
    if split:
        dataset = Dataset.from_generator(data_generator, cache_dir=cache_dir, split=split)
    else:
        dataset = Dataset.from_generator(data_generator, cache_dir=cache_dir)
    _check_generator_dataset(dataset, expected_features, expected_split)


@require_not_windows
@require_dill_gt_0_3_2
@require_pyspark
def test_from_spark():
    import pyspark

    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    data = [
        ("0", 0, 0.0),
        ("1", 1, 1.0),
        ("2", 2, 2.0),
        ("3", 3, 3.0),
    ]
    df = spark.createDataFrame(data, "col_1: string, col_2: int, col_3: float")
    dataset = Dataset.from_spark(df)
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]


@require_not_windows
@require_dill_gt_0_3_2
@require_pyspark
def test_from_spark_features():
    import PIL.Image
    import pyspark

    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    data = [(0, np.arange(4 * 4 * 3).reshape(4, 4, 3).tolist())]
    df = spark.createDataFrame(data, "idx: int, image: array<array<array<int>>>")
    features = Features({"idx": Value("int64"), "image": Image()})
    dataset = Dataset.from_spark(
        df,
        features=features,
    )
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 1
    assert dataset.num_columns == 2
    assert dataset.column_names == ["idx", "image"]
    assert isinstance(dataset[0]["image"], PIL.Image.Image)
    assert dataset.features == features
    assert_arrow_metadata_are_synced_with_dataset_features(dataset)


@require_not_windows
@require_dill_gt_0_3_2
@require_pyspark
def test_from_spark_different_cache():
    import pyspark

    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    df = spark.createDataFrame([("0", 0)], "col_1: string, col_2: int")
    dataset = Dataset.from_spark(df)
    assert isinstance(dataset, Dataset)
    different_df = spark.createDataFrame([("1", 1)], "col_1: string, col_2: int")
    different_dataset = Dataset.from_spark(different_df)
    assert isinstance(different_dataset, Dataset)
    assert dataset[0]["col_1"] == "0"
    # Check to make sure that the second dataset wasn't read from the cache.
    assert different_dataset[0]["col_1"] == "1"


def _check_sql_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@require_sqlalchemy
@pytest.mark.parametrize("con_type", ["string", "engine"])
def test_dataset_from_sql_con_type(con_type, sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning, caplog):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    if con_type == "string":
        con = "sqlite:///" + sqlite_path
    elif con_type == "engine":
        import sqlalchemy

        con = sqlalchemy.create_engine("sqlite:///" + sqlite_path)
    with caplog.at_level(INFO, logger=get_logger().name):
        dataset = Dataset.from_sql(
            "dataset",
            con,
            cache_dir=cache_dir,
        )
    if con_type == "string":
        assert "couldn't be hashed properly" not in caplog.text
    elif con_type == "engine":
        assert "couldn't be hashed properly" in caplog.text
    dataset = Dataset.from_sql(
        "dataset",
        con,
        cache_dir=cache_dir,
    )
    _check_sql_dataset(dataset, expected_features)


@require_sqlalchemy
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
def test_dataset_from_sql_features(features, sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = Dataset.from_sql("dataset", "sqlite:///" + sqlite_path, features=features, cache_dir=cache_dir)
    _check_sql_dataset(dataset, expected_features)


@require_sqlalchemy
@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_sql_keep_in_memory(keep_in_memory, sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_sql(
            "dataset", "sqlite:///" + sqlite_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        )
    _check_sql_dataset(dataset, expected_features)


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
        ("rename_column", (), {"original_column_name": "labels", "new_column_name": "label"}),
        ("remove_columns", (), {"column_names": "labels"}),
        (
            "cast",
            (),
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
        ("flatten", (), {}),
    ],
)
def test_pickle_dataset_after_transforming_the_table(in_memory, method_and_params, arrow_file):
    method, args, kwargs = method_and_params
    with (
        Dataset.from_file(arrow_file, in_memory=in_memory) as dataset,
        Dataset.from_file(arrow_file, in_memory=in_memory) as reference_dataset,
    ):
        out = getattr(dataset, method)(*args, **kwargs)
        dataset = out if out is not None else dataset
        pickled_dataset = pickle.dumps(dataset)
        reloaded_dataset = pickle.loads(pickled_dataset)

        assert dataset._data != reference_dataset._data
        assert dataset._data.table == reloaded_dataset._data.table


def test_dummy_dataset_serialize_fs(dataset, mockfs):
    dataset_path = "mock://my_dataset"
    dataset.save_to_disk(dataset_path, storage_options=mockfs.storage_options)
    assert mockfs.isdir(dataset_path)
    assert mockfs.glob(dataset_path + "/*")
    reloaded = Dataset.load_from_disk(dataset_path, storage_options=mockfs.storage_options)
    assert len(reloaded) == len(dataset)
    assert reloaded.features == dataset.features
    assert reloaded.to_dict() == dataset.to_dict()


@pytest.mark.parametrize(
    "uri_or_path",
    [
        "relative/path",
        "/absolute/path",
        "hf://bucket/relative/path",
        "hdfs://relative/path",
        "hdfs:///absolute/path",
    ],
)
def test_build_local_temp_path(uri_or_path):
    extracted_path = strip_protocol(uri_or_path)
    local_temp_path = Dataset._build_local_temp_path(extracted_path).as_posix()
    extracted_path_without_anchor = Path(extracted_path).relative_to(Path(extracted_path).anchor).as_posix()
    # Check that the local temp path is relative to the system temp dir
    path_relative_to_tmp_dir = Path(local_temp_path).relative_to(Path(tempfile.gettempdir())).as_posix()

    assert (
        "hdfs://" not in path_relative_to_tmp_dir
        and "hf://" not in path_relative_to_tmp_dir
        and not local_temp_path.startswith(extracted_path_without_anchor)
        and local_temp_path.endswith(extracted_path_without_anchor)
    ), f"Local temp path: {local_temp_path}"


class StratifiedTest(TestCase):
    def test_errors_train_test_split_stratify(self):
        ys = [
            np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2]),
            np.array([0, 1, 1, 1, 2, 2, 2, 3, 3, 3]),
            np.array([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2] * 2),
            np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]),
            np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]),
        ]
        for i in range(len(ys)):
            features = Features({"text": Value("int64"), "label": ClassLabel(len(np.unique(ys[i])))})
            data = {"text": np.ones(len(ys[i])), "label": ys[i]}
            d1 = Dataset.from_dict(data, features=features)

            # For checking stratify_by_column exist as key in self.features.keys()
            if i == 0:
                self.assertRaises(ValueError, d1.train_test_split, 0.33, stratify_by_column="labl")

            # For checking minimum class count error
            elif i == 1:
                self.assertRaises(ValueError, d1.train_test_split, 0.33, stratify_by_column="label")

            # For check typeof label as ClassLabel type
            elif i == 2:
                d1 = Dataset.from_dict(data)
                self.assertRaises(ValueError, d1.train_test_split, 0.33, stratify_by_column="label")

            # For checking test_size should be greater than or equal to number of classes
            elif i == 3:
                self.assertRaises(ValueError, d1.train_test_split, 0.30, stratify_by_column="label")

            # For checking train_size should be greater than or equal to number of classes
            elif i == 4:
                self.assertRaises(ValueError, d1.train_test_split, 0.60, stratify_by_column="label")

    def test_train_test_split_startify(self):
        ys = [
            np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2]),
            np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]),
            np.array([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2] * 2),
            np.array([0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3]),
            np.array([0] * 800 + [1] * 50),
        ]
        for y in ys:
            features = Features({"text": Value("int64"), "label": ClassLabel(len(np.unique(y)))})
            data = {"text": np.ones(len(y)), "label": y}
            d1 = Dataset.from_dict(data, features=features)
            d1 = d1.train_test_split(test_size=0.33, stratify_by_column="label")
            y = np.asanyarray(y)  # To make it indexable for y[train]
            test_size = np.ceil(0.33 * len(y))
            train_size = len(y) - test_size
            npt.assert_array_equal(np.unique(d1["train"]["label"]), np.unique(d1["test"]["label"]))

            # checking classes proportion
            p_train = np.bincount(np.unique(d1["train"]["label"], return_inverse=True)[1]) / float(
                len(d1["train"]["label"])
            )
            p_test = np.bincount(np.unique(d1["test"]["label"], return_inverse=True)[1]) / float(
                len(d1["test"]["label"])
            )
            npt.assert_array_almost_equal(p_train, p_test, 1)
            assert len(d1["train"]["text"]) + len(d1["test"]["text"]) == y.size
            assert len(d1["train"]["text"]) == train_size
            assert len(d1["test"]["text"]) == test_size


def test_dataset_estimate_nbytes():
    ds = Dataset.from_dict({"a": ["0" * 100] * 100})
    assert 0.9 * ds._estimate_nbytes() < 100 * 100, "must be smaller than full dataset size"

    ds = Dataset.from_dict({"a": ["0" * 100] * 100}).select([0])
    assert 0.9 * ds._estimate_nbytes() < 100 * 100, "must be smaller than one chunk"

    ds = Dataset.from_dict({"a": ["0" * 100] * 100})
    ds = concatenate_datasets([ds] * 100)
    assert 0.9 * ds._estimate_nbytes() < 100 * 100 * 100, "must be smaller than full dataset size"
    assert 1.1 * ds._estimate_nbytes() > 100 * 100 * 100, "must be bigger than full dataset size"

    ds = Dataset.from_dict({"a": ["0" * 100] * 100})
    ds = concatenate_datasets([ds] * 100).select([0])
    assert 0.9 * ds._estimate_nbytes() < 100 * 100, "must be smaller than one chunk"


def test_dataset_to_iterable_dataset(dataset: Dataset):
    iterable_dataset = dataset.to_iterable_dataset()
    assert isinstance(iterable_dataset, IterableDataset)
    assert list(iterable_dataset) == list(dataset)
    assert iterable_dataset.features == dataset.features
    iterable_dataset = dataset.to_iterable_dataset(num_shards=3)
    assert isinstance(iterable_dataset, IterableDataset)
    assert list(iterable_dataset) == list(dataset)
    assert iterable_dataset.features == dataset.features
    assert iterable_dataset.num_shards == 3
    with pytest.raises(ValueError):
        dataset.to_iterable_dataset(num_shards=len(dataset) + 1)
    assert dataset.with_format("torch").to_iterable_dataset()._formatting.format_type == "torch"
    with pytest.raises(NotImplementedError):
        dataset.with_format("torch", columns=[dataset.column_names[0]]).to_iterable_dataset()


@require_pil
def test_dataset_format_with_unformatted_image():
    import PIL

    ds = Dataset.from_dict(
        {"a": [np.arange(4 * 4 * 3).reshape(4, 4, 3)] * 10, "b": [[0, 1]] * 10},
        Features({"a": Image(), "b": Sequence(Value("int64"))}),
    )
    ds.set_format("np", columns=["b"], output_all_columns=True)
    assert isinstance(ds[0]["a"], PIL.Image.Image)
    assert isinstance(ds[0]["b"], np.ndarray)


@pytest.mark.parametrize("batch_size", [1, 4])
@require_torch
def test_dataset_with_torch_dataloader(dataset, batch_size):
    from torch.utils.data import DataLoader

    from datasets import config

    dataloader = DataLoader(dataset, batch_size=batch_size)
    with patch.object(dataset, "_getitem", wraps=dataset._getitem) as mock_getitem:
        out = list(dataloader)
        getitem_call_count = mock_getitem.call_count
    assert len(out) == len(dataset) // batch_size + int(len(dataset) % batch_size > 0)
    # calling dataset[list_of_indices] is much more efficient than [dataset[idx] for idx in list of indices]
    if config.TORCH_VERSION >= version.parse("1.13.0"):
        assert getitem_call_count == len(dataset) // batch_size + int(len(dataset) % batch_size > 0)


@pytest.mark.parametrize("return_lazy_dict", [True, False, "mix"])
def test_map_cases(return_lazy_dict):
    def f(x):
        """May return a mix of LazyDict and regular Dict"""
        if x["a"] < 2:
            x["a"] = -1
            return dict(x) if return_lazy_dict is False else x
        else:
            return x if return_lazy_dict is True else {}

    ds = Dataset.from_dict({"a": [0, 1, 2, 3]})
    ds = ds.map(f)
    outputs = ds[:]
    assert outputs == {"a": [-1, -1, 2, 3]}

    def f(x):
        """May return a mix of LazyDict and regular Dict, but sometimes with None values"""
        if x["a"] < 2:
            x["a"] = None
            return dict(x) if return_lazy_dict is False else x
        else:
            return x if return_lazy_dict is True else {}

    ds = Dataset.from_dict({"a": [0, 1, 2, 3]})
    ds = ds.map(f)
    outputs = ds[:]
    assert outputs == {"a": [None, None, 2, 3]}

    def f(x):
        """Return a LazyDict, but we remove a lazy column and add a new one"""
        if x["a"] < 2:
            x["b"] = -1
            return x
        else:
            x["b"] = x["a"]
            return x

    ds = Dataset.from_dict({"a": [0, 1, 2, 3]})
    ds = ds.map(f, remove_columns=["a"])
    outputs = ds[:]
    assert outputs == {"b": [-1, -1, 2, 3]}

    # The formatted dataset version removes the lazy column from a different dictionary, hence it should be preserved in the output
    ds = Dataset.from_dict({"a": [0, 1, 2, 3]})
    ds = ds.with_format("numpy")
    ds = ds.map(f, remove_columns=["a"])
    ds = ds.with_format(None)
    outputs = ds[:]
    assert outputs == {"a": [0, 1, 2, 3], "b": [-1, -1, 2, 3]}

    def f(x):
        """May return a mix of LazyDict and regular Dict, but we replace a lazy column"""
        if x["a"] < 2:
            x["a"] = -1
            return dict(x) if return_lazy_dict is False else x
        else:
            x["a"] = x["a"]
            return x if return_lazy_dict is True else {"a": x["a"]}

    ds = Dataset.from_dict({"a": [0, 1, 2, 3]})
    ds = ds.map(f, remove_columns=["a"])
    outputs = ds[:]
    assert outputs == ({"a": [-1, -1, 2, 3]} if return_lazy_dict is False else {})

    def f(x):
        """May return a mix of LazyDict and regular Dict, but we modify a nested lazy column in-place"""
        if x["a"]["b"] < 2:
            x["a"]["c"] = -1
            return dict(x) if return_lazy_dict is False else x
        else:
            x["a"]["c"] = x["a"]["b"]
            return x if return_lazy_dict is True else {}

    ds = Dataset.from_dict({"a": [{"b": 0}, {"b": 1}, {"b": 2}, {"b": 3}]})
    ds = ds.map(f)
    outputs = ds[:]
    assert outputs == {"a": [{"b": 0, "c": -1}, {"b": 1, "c": -1}, {"b": 2, "c": 2}, {"b": 3, "c": 3}]}

    def f(x):
        """May return a mix of LazyDict and regular Dict, but using an extension type"""
        if x["a"][0][0] < 2:
            x["a"] = [[-1]]
            return dict(x) if return_lazy_dict is False else x
        else:
            return x if return_lazy_dict is True else {}

    features = Features({"a": Array2D(shape=(1, 1), dtype="int32")})
    ds = Dataset.from_dict({"a": [[[i]] for i in [0, 1, 2, 3]]}, features=features)
    ds = ds.map(f)
    outputs = ds[:]
    assert outputs == {"a": [[[i]] for i in [-1, -1, 2, 3]]}

    def f(x):
        """May return a mix of LazyDict and regular Dict, but using a nested extension type"""
        if x["a"]["nested"][0][0] < 2:
            x["a"] = {"nested": [[-1]]}
            return dict(x) if return_lazy_dict is False else x
        else:
            return x if return_lazy_dict is True else {}

    features = Features({"a": {"nested": Array2D(shape=(1, 1), dtype="int64")}})
    ds = Dataset.from_dict({"a": [{"nested": [[i]]} for i in [0, 1, 2, 3]]}, features=features)
    ds = ds.map(f)
    outputs = ds[:]
    assert outputs == {"a": [{"nested": [[i]]} for i in [-1, -1, 2, 3]]}


def test_map_async():
    dset = Dataset.from_dict({"x": range(100)})

    async def f(example):
        await asyncio.sleep(0.1)
        return {"y": 1}

    _start = time.time()
    out = dset.map(f)
    assert time.time() - _start < 2.0
    assert out[0]["y"] == 1

    async def f(batch):
        await asyncio.sleep(0.1)
        return {"y": [1] * len(batch["x"])}

    _start = time.time()
    out = dset.map(f, batched=True)
    assert time.time() - _start < 2.0
    assert out[0]["y"] == 1


def test_filter_async():
    dset = Dataset.from_dict({"x": range(100)})

    async def f(example):
        await asyncio.sleep(0.1)
        return example["x"] == 42

    _start = time.time()
    out = dset.filter(f)
    assert time.time() - _start < 2.0
    assert len(out) == 1

    async def f(batch):
        await asyncio.sleep(0.1)
        return [x == 42 for x in batch["x"]]

    _start = time.time()
    out = dset.filter(f, batched=True)
    assert time.time() - _start < 2.0
    assert len(out) == 1


def test_dataset_getitem_raises():
    ds = Dataset.from_dict({"a": [0, 1, 2, 3]})
    with pytest.raises(TypeError):
        ds[False]
    with pytest.raises(TypeError):
        ds._getitem(True)


def test_categorical_dataset(tmpdir):
    n_legs = pa.array([2, 4, 5, 100])
    animals = pa.array(["Flamingo", "Horse", "Brittle stars", "Centipede"]).cast(
        pa.dictionary(pa.int32(), pa.string())
    )
    names = ["n_legs", "animals"]

    table = pa.Table.from_arrays([n_legs, animals], names=names)
    table_path = str(tmpdir / "data.parquet")
    pa.parquet.write_table(table, table_path)

    dataset = Dataset.from_parquet(table_path)
    entry = dataset[0]

    # Categorical types get transparently converted to string
    assert entry["animals"] == "Flamingo"


def test_dataset_batch():
    # Create a simple Dataset
    data = {"id": list(range(10)), "text": [f"Text {i}" for i in range(10)]}
    ds = Dataset.from_dict(data)

    # Test with batch_size=3, drop_last_batch=False
    batched_ds = ds.batch(batch_size=3, drop_last_batch=False)
    batches = list(batched_ds)

    assert len(batches) == 4  # 3 full batches and 1 partial batch
    for i, batch in enumerate(batches[:3]):  # Check full batches
        assert len(batch["id"]) == 3
        assert len(batch["text"]) == 3
        assert batch["id"] == [3 * i, 3 * i + 1, 3 * i + 2]
        assert batch["text"] == [f"Text {3 * i}", f"Text {3 * i + 1}", f"Text {3 * i + 2}"]

    # Check last partial batch
    assert len(batches[3]["id"]) == 1
    assert len(batches[3]["text"]) == 1
    assert batches[3]["id"] == [9]
    assert batches[3]["text"] == ["Text 9"]

    # Test with batch_size=3, drop_last_batch=True
    batched_ds = ds.batch(batch_size=3, drop_last_batch=True)
    batches = list(batched_ds)

    assert len(batches) == 3  # Only full batches
    for i, batch in enumerate(batches):
        assert len(batch["id"]) == 3
        assert len(batch["text"]) == 3
        assert batch["id"] == [3 * i, 3 * i + 1, 3 * i + 2]
        assert batch["text"] == [f"Text {3 * i}", f"Text {3 * i + 1}", f"Text {3 * i + 2}"]

    # Test with batch_size=4 (doesn't evenly divide dataset size)
    batched_ds = ds.batch(batch_size=4, drop_last_batch=False)
    batches = list(batched_ds)

    assert len(batches) == 3  # 2 full batches and 1 partial batch
    for i, batch in enumerate(batches[:2]):  # Check full batches
        assert len(batch["id"]) == 4
        assert len(batch["text"]) == 4
        assert batch["id"] == [4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3]
        assert batch["text"] == [f"Text {4 * i}", f"Text {4 * i + 1}", f"Text {4 * i + 2}", f"Text {4 * i + 3}"]

    # Check last partial batch
    assert len(batches[2]["id"]) == 2
    assert len(batches[2]["text"]) == 2
    assert batches[2]["id"] == [8, 9]
    assert batches[2]["text"] == ["Text 8", "Text 9"]


def test_dataset_from_dict_with_large_list():
    data = {"col_1": [[1, 2], [3, 4]]}
    features = Features({"col_1": LargeList(Value("int64"))})
    ds = Dataset.from_dict(data, features=features)
    assert isinstance(ds, Dataset)
    assert pa.types.is_large_list(ds.data.schema.field("col_1").type)


def test_dataset_save_to_disk_with_large_list(tmp_path):
    data = {"col_1": [[1, 2], [3, 4]]}
    features = Features({"col_1": LargeList(Value("int64"))})
    ds = Dataset.from_dict(data, features=features)
    dataset_path = tmp_path / "dataset_dir"
    ds.save_to_disk(dataset_path)
    assert (dataset_path / "data-00000-of-00001.arrow").exists()


def test_dataset_save_to_disk_and_load_from_disk_round_trip_with_large_list(tmp_path):
    data = {"col_1": [[1, 2], [3, 4]]}
    features = Features({"col_1": LargeList(Value("int64"))})
    ds = Dataset.from_dict(data, features=features)
    dataset_path = tmp_path / "dataset_dir"
    ds.save_to_disk(dataset_path)
    assert (dataset_path / "data-00000-of-00001.arrow").exists()
    loaded_ds = load_from_disk(dataset_path)
    assert len(loaded_ds) == len(ds)
    assert loaded_ds.features == ds.features
    assert loaded_ds.to_dict() == ds.to_dict()


@require_polars
def test_from_polars_with_large_list():
    import polars as pl

    df = pl.from_dict({"col_1": [[1, 2], [3, 4]]})
    ds = Dataset.from_polars(df)
    assert isinstance(ds, Dataset)


@require_polars
def test_from_polars_save_to_disk_with_large_list(tmp_path):
    import polars as pl

    df = pl.from_dict({"col_1": [[1, 2], [3, 4]]})
    ds = Dataset.from_polars(df)
    dataset_path = tmp_path / "dataset_dir"
    ds.save_to_disk(dataset_path)
    assert (dataset_path / "data-00000-of-00001.arrow").exists()


@require_polars
def test_from_polars_save_to_disk_and_load_from_disk_round_trip_with_large_list(tmp_path):
    import polars as pl

    df = pl.from_dict({"col_1": [[1, 2], [3, 4]]})
    ds = Dataset.from_polars(df)
    dataset_path = tmp_path / "dataset_dir"
    ds.save_to_disk(dataset_path)
    assert (dataset_path / "data-00000-of-00001.arrow").exists()
    loaded_ds = load_from_disk(dataset_path)
    assert len(loaded_ds) == len(ds)
    assert loaded_ds.features == ds.features
    assert loaded_ds.to_dict() == ds.to_dict()


@require_polars
def test_polars_round_trip():
    ds = Dataset.from_dict({"x": [[1, 2], [3, 4, 5]], "y": ["a", "b"]})
    assert isinstance(Dataset.from_polars(ds.to_polars()), Dataset)
