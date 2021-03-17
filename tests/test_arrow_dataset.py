import copy
import os
import pickle
import shutil
import tempfile
from functools import partial
from unittest import TestCase

import boto3
import numpy as np
import pandas as pd
import pyarrow as pa
import pytest
from absl.testing import parameterized
from moto import mock_s3

import datasets.arrow_dataset
from datasets import NamedSplit, concatenate_datasets, load_from_disk, temp_seed
from datasets.arrow_dataset import Dataset, transmit_format
from datasets.dataset_dict import DatasetDict
from datasets.features import Array2D, Array3D, ClassLabel, Features, Sequence, Value
from datasets.filesystems import S3FileSystem
from datasets.info import DatasetInfo
from datasets.utils.logging import WARNING

from .utils import (
    assert_arrow_memory_doesnt_increase,
    assert_arrow_memory_increases,
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

    def test_dummy_dataset(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:

            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
            self.assertEqual(dset[0]["filename"], "my_name-train_0")
            self.assertEqual(dset["filename"][0], "my_name-train_0")
            del dset

            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            self.assertDictEqual(
                dset.features, Features({"col_1": Value("int64"), "col_2": Value("string"), "col_3": Value("bool")})
            )
            self.assertEqual(dset[0]["col_1"], 3)
            self.assertEqual(dset["col_1"][0], 3)
            del dset

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True, array_features=True)
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

    def test_dummy_dataset_deepcopy(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir).select(range(10))
            with assert_arrow_memory_doesnt_increase():
                dset2 = copy.deepcopy(dset)
            # don't copy the underlying arrow data using memory
            self.assertEqual(len(dset2), 10)
            self.assertDictEqual(dset2.features, Features({"filename": Value("string")}))
            self.assertEqual(dset2[0]["filename"], "my_name-train_0")
            self.assertEqual(dset2["filename"][0], "my_name-train_0")
            del dset, dset2

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
                dset._data.table = Unpicklable()
            dset._indices.table = Unpicklable()

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
            with set_current_working_directory_to_temp_dir():
                dset = self._create_dummy_dataset(in_memory, tmp_dir).select(range(10))
                dataset_path = "my_dataset"  # rel path
                dset.save_to_disk(dataset_path)
                dset = dset.load_from_disk(dataset_path)

                self.assertEqual(len(dset), 10)
                self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
                self.assertEqual(dset[0]["filename"], "my_name-train_0")
                self.assertEqual(dset["filename"][0], "my_name-train_0")
                del dset

            dset = self._create_dummy_dataset(in_memory, tmp_dir).select(range(10))
            dataset_path = os.path.join(tmp_dir, "my_dataset")  # abs path
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

    @mock_s3
    def test_dummy_dataset_serialize_s3(self, in_memory):
        tmp_dir = tempfile.TemporaryDirectory()
        # Mocked AWS Credentials for moto.
        os.environ["AWS_ACCESS_KEY_ID"] = "fake_access_key"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "fake_secret_key"
        os.environ["AWS_SECURITY_TOKEN"] = "fake_secrurity_token"
        os.environ["AWS_SESSION_TOKEN"] = "fake_session_token"

        s3 = boto3.client("s3", region_name="us-east-1")
        mock_bucket = "moto-mock-s3-bucket"
        # We need to create the bucket since this is all in Moto's 'virtual' AWS account
        s3.create_bucket(Bucket=mock_bucket)

        if in_memory:
            prefix = "datasets/memory"
        else:
            prefix = "datasets/disk"

        dset = self._create_dummy_dataset(in_memory, tmp_dir.name).select(range(10))
        dataset_path = f"s3://{mock_bucket}/{prefix}"

        fs = S3FileSystem(key="fake_access_key", secret="fake_secret")

        dset.save_to_disk(dataset_path, fs)
        dset = dset.load_from_disk(dataset_path, fs)

        self.assertEqual(len(dset), 10)
        self.assertDictEqual(dset.features, Features({"filename": Value("string")}))
        self.assertEqual(dset[0]["filename"], "my_name-train_0")
        self.assertEqual(dset["filename"][0], "my_name-train_0")
        del dset

        shutil.rmtree(tmp_dir.name, ignore_errors=True)

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
            self.assertEqual(len(dset[0]), 3)
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
            self.assertEqual(len(dset[0]), 3)
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

    def test_set_transform(self, in_memory):
        def transform(batch):
            return {k: [str(i).upper() for i in v] for k, v in batch.items()}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
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
            del dset

    def test_transmit_format(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
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
            del dset

    def test_cast_in_place(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            features = dset.features
            features["col_1"] = Value("float64")
            features = Features({k: features[k] for k in list(features)[::-1]})
            fingerprint = dset._fingerprint
            dset.cast_(features)
            self.assertEqual(dset.num_columns, 3)
            self.assertEqual(dset.features["col_1"], Value("float64"))
            self.assertIsInstance(dset[0]["col_1"], float)
            self.assertNotEqual(dset._fingerprint, fingerprint)
            del dset

    def test_cast(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            features = dset.features
            features["col_1"] = Value("float64")
            features = Features({k: features[k] for k in list(features)[::-1]})
            fingerprint = dset._fingerprint
            casted_dset = dset.cast(features)
            self.assertEqual(casted_dset.num_columns, 3)
            self.assertEqual(casted_dset.features["col_1"], Value("float64"))
            self.assertIsInstance(casted_dset[0]["col_1"], float)
            self.assertNotEqual(casted_dset._fingerprint, fingerprint)
            self.assertNotEqual(casted_dset, dset)
            del dset
            del casted_dset

    def test_remove_columns_in_place(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            fingerprint = dset._fingerprint
            dset.remove_columns_(column_names="col_1")
            self.assertEqual(dset.num_columns, 2)
            self.assertListEqual(list(dset.column_names), ["col_2", "col_3"])
            del dset

            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            dset.remove_columns_(column_names=["col_1", "col_2", "col_3"])
            self.assertEqual(dset.num_columns, 0)
            self.assertNotEqual(dset._fingerprint, fingerprint)
            del dset

    def test_remove_columns(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            fingerprint = dset._fingerprint
            new_dset = dset.remove_columns(column_names="col_1")
            self.assertEqual(new_dset.num_columns, 2)
            self.assertListEqual(list(new_dset.column_names), ["col_2", "col_3"])
            self.assertNotEqual(new_dset._fingerprint, fingerprint)
            del dset
            del new_dset

            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            new_dset = dset.remove_columns(column_names=["col_1", "col_2", "col_3"])
            self.assertEqual(new_dset.num_columns, 0)
            self.assertNotEqual(new_dset._fingerprint, fingerprint)
            del dset
            del new_dset

    def test_rename_column_in_place(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            fingerprint = dset._fingerprint
            dset.rename_column_(original_column_name="col_1", new_column_name="new_name")
            self.assertEqual(dset.num_columns, 3)
            self.assertListEqual(list(dset.column_names), ["new_name", "col_2", "col_3"])
            self.assertNotEqual(dset._fingerprint, fingerprint)
            del dset

    def test_rename_column(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            fingerprint = dset._fingerprint
            new_dset = dset.rename_column(original_column_name="col_1", new_column_name="new_name")
            self.assertEqual(new_dset.num_columns, 3)
            self.assertListEqual(list(new_dset.column_names), ["new_name", "col_2", "col_3"])
            self.assertListEqual(list(dset.column_names), ["col_1", "col_2", "col_3"])
            self.assertNotEqual(new_dset._fingerprint, fingerprint)
            del dset
            del new_dset

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
            self.assertEqual(len(dset_concat.cache_files), 0 if in_memory else 3)
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
            # in_memory = False:
            # 3 cache files for the dset_concat._data table, and 1 for the dset_concat._indices_table
            # no cache file for the indices
            # in_memory = True:
            # no cache files since both dset_concat._data and dset_concat._indices are in memory
            self.assertEqual(len(dset_concat.cache_files), 0 if in_memory else 3)
            self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")

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
            # in_memory = False:
            # 3 cache files for the dset_concat._data table, and 1 for the dset_concat._indices_table
            # There is only 1 for the indices tables (i1.arrow)
            # Indeed, the others are brought to memory since an offset is applied to them.
            # in_memory = True:
            # 1 cache file for i1.arrow since both dset_concat._data and dset_concat._indices are in memory
            self.assertEqual(len(dset_concat.cache_files), 1 if in_memory else 3 + 1)
            self.assertEqual(dset_concat.info.description, "Dataset1\n\nDataset2\n\n")
            del dset_concat, dset1, dset2, dset3

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
            dset_concat = concatenate_datasets([dset1, dset2, dset3])
            if not in_memory:
                dset_concat._data.table = Unpicklable()
            dset_concat = pickle.loads(pickle.dumps(dset_concat))
            self.assertEqual((len(dset1), len(dset2), len(dset3)), (3, 3, 2))
            self.assertEqual(len(dset_concat), len(dset1) + len(dset2) + len(dset3))
            self.assertListEqual(dset_concat["id"], [0, 1, 2, 3, 4, 5, 6, 7])
            # in_memory = True: 1 cache file for dset3
            # in_memory = False: 2 caches files for dset1 and dset2, and 1 cache file for i1.arrow
            self.assertEqual(len(dset_concat.cache_files), 1 if in_memory else 2 + 1)
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

        # no transform
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir)
            fingerprint = dset._fingerprint
            dset_test = dset.map(lambda x: None)
            self.assertEqual(len(dset_test), 30)
            self.assertEqual(dset_test._fingerprint, fingerprint)
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

            dset_test = dset.map(lambda x: {"col_1_plus_one": x["col_1"] + 1})
            self.assertEqual(len(dset_test), 4)
            self.assertEqual(dset_test.format["type"], "numpy")
            self.assertIsInstance(dset_test["col_1"], np.ndarray)
            self.assertIsInstance(dset_test["col_1_plus_one"], np.ndarray)
            self.assertListEqual(sorted(dset_test[0].keys()), ["col_1", "col_1_plus_one"])
            self.assertListEqual(sorted(dset_test.column_names), ["col_1", "col_1_plus_one", "col_2", "col_3"])
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
            self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 2)
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
            self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 3)
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
            self.assertEqual(len(dset_test.cache_files), 0 if in_memory else 2)
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

    def test_map_caching(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(WARNING):
                dset = self._create_dummy_dataset(in_memory, tmp_dir)
                dset_test1 = dset.map(lambda x: {"foo": "bar"})
                dset_test1_data_files = list(dset_test1.cache_files)
                del dset_test1
                dset_test2 = dset.map(lambda x: {"foo": "bar"})
                self.assertEqual(dset_test1_data_files, dset_test2.cache_files)
                self.assertEqual(len(dset_test2.cache_files), 1 - int(in_memory))
                self.assertTrue(("Loading cached processed dataset" in self._caplog.text) ^ in_memory)
                del dset, dset_test2

        with tempfile.TemporaryDirectory() as tmp_dir:
            self._caplog.clear()
            with self._caplog.at_level(WARNING):
                dset = self._create_dummy_dataset(in_memory, tmp_dir)
                dset_test1 = dset.map(lambda x: {"foo": "bar"})
                dset_test1_data_files = list(dset_test1.cache_files)
                del dset_test1
                dset_test2 = dset.map(lambda x: {"foo": "bar"}, load_from_cache_file=False)
                self.assertEqual(dset_test1_data_files, dset_test2.cache_files)
                self.assertEqual(len(dset_test2.cache_files), 1 - int(in_memory))
                self.assertNotIn("Loading cached processed dataset", self._caplog.text)
                del dset, dset_test2

        if not in_memory:
            try:
                self._caplog.clear()
                with tempfile.TemporaryDirectory() as tmp_dir:
                    with self._caplog.at_level(WARNING):
                        dset = self._create_dummy_dataset(in_memory, tmp_dir)
                        datasets.set_caching_enabled(False)
                        dset_test1 = dset.map(lambda x: {"foo": "bar"})
                        dset_test2 = dset.map(lambda x: {"foo": "bar"})
                        self.assertNotEqual(dset_test1.cache_files, dset_test2.cache_files)
                        self.assertEqual(len(dset_test1.cache_files), 1)
                        self.assertEqual(len(dset_test2.cache_files), 1)
                        self.assertNotIn("Loading cached processed dataset", self._caplog.text)
                        # make sure the arrow files are going to be removed
                        self.assertIn("tmp", dset_test1.cache_files[0])
                        self.assertIn("tmp", dset_test2.cache_files[0])
                        del dset, dset_test2
            finally:
                datasets.set_caching_enabled(True)

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
            dset_filter_even_num = dset.filter(lambda x: (int(x["filename"][-1]) % 2 == 0))
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
            # only one cache file since the there is only 10 examples from the 1 processed shard
            self.assertEqual(len(dset_filter_first_ten.cache_files), 0 if in_memory else 1)
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
                self.assertEqual(int(row["filename"][-1]), i)
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
            self.assertEqual(len(dset.cache_files), 0 if in_memory else 1)
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
            if not in_memory:
                self.assertEqual(
                    dset._data.replay,
                    [("rename_columns", (["file", "number"],), {})],
                )
            if not in_memory:
                dset._data.table = Unpicklable()  # check that we don't pickle the entire table

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

    def test_to_csv(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # File path argument
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            file_path = os.path.join(tmp_dir, "test_path.csv")
            bytes_written = dset.to_csv(path_or_buf=file_path)

            self.assertTrue(os.path.isfile(file_path))
            self.assertEqual(bytes_written, os.path.getsize(file_path))
            csv_dset = pd.read_csv(file_path, header=0, index_col=0)

            self.assertEqual(csv_dset.shape, dset.shape)
            self.assertListEqual(list(csv_dset.columns), list(dset.column_names))
            del dset

            # File buffer argument
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            file_path = os.path.join(tmp_dir, "test_buffer.csv")
            with open(file_path, "wb+") as buffer:
                bytes_written = dset.to_csv(path_or_buf=buffer)

            self.assertTrue(os.path.isfile(file_path))
            self.assertEqual(bytes_written, os.path.getsize(file_path))
            csv_dset = pd.read_csv(file_path, header=0, index_col=0)

            self.assertEqual(csv_dset.shape, dset.shape)
            self.assertListEqual(list(csv_dset.columns), list(dset.column_names))
            del dset

            # After a select/shuffle transform
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            dset = dset.select(range(0, len(dset), 2)).shuffle()
            file_path = os.path.join(tmp_dir, "test_path.csv")
            bytes_written = dset.to_csv(path_or_buf=file_path)

            self.assertTrue(os.path.isfile(file_path))
            self.assertEqual(bytes_written, os.path.getsize(file_path))
            csv_dset = pd.read_csv(file_path, header=0, index_col=0)

            self.assertEqual(csv_dset.shape, dset.shape)
            self.assertListEqual(list(csv_dset.columns), list(dset.column_names))
            del dset

            # With array features
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True, array_features=True)
            file_path = os.path.join(tmp_dir, "test_path.csv")
            bytes_written = dset.to_csv(path_or_buf=file_path)

            self.assertTrue(os.path.isfile(file_path))
            self.assertEqual(bytes_written, os.path.getsize(file_path))
            csv_dset = pd.read_csv(file_path, header=0, index_col=0)

            self.assertEqual(csv_dset.shape, dset.shape)
            self.assertListEqual(list(csv_dset.columns), list(dset.column_names))

            del dset

    def test_to_dict(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Batched
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
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
            dset = dset.select([1, 0, 3])
            dset_to_dict = dset.to_dict()
            self.assertIsInstance(dset_to_dict, dict)
            self.assertEqual(len(dset_to_dict), 3)
            self.assertListEqual(sorted(dset_to_dict.keys()), sorted(dset.column_names))

            for col_name in dset.column_names:
                self.assertIsInstance(dset_to_dict[col_name], list)
                self.assertEqual(len(dset_to_dict[col_name]), len(dset))

            del dset

    def test_to_pandas(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Batched
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
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
            dset = dset.select([1, 0, 3])
            dset_to_pandas = dset.to_pandas()
            self.assertIsInstance(dset_to_pandas, pd.DataFrame)
            self.assertEqual(len(dset_to_pandas), 3)
            self.assertListEqual(sorted(dset_to_pandas.columns), sorted(dset.column_names))

            for col_name in dset.column_names:
                self.assertEqual(len(dset_to_pandas[col_name]), dset.num_rows)

            del dset

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

    def test_with_format(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            dset2 = dset.with_format("numpy", columns=["col_1"])
            dset.set_format("numpy", columns=["col_1"])
            self.assertDictEqual(dset.format, dset2.format)
            self.assertEqual(dset._fingerprint, dset2._fingerprint)
            # dset.reset_format()
            # self.assertNotEqual(dset.format, dset2.format)
            # self.assertNotEqual(dset._fingerprint, dset2._fingerprint)
            del dset, dset2

    def test_with_transform(self, in_memory):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dset = self._create_dummy_dataset(in_memory, tmp_dir, multiple_columns=True)
            transform = lambda x: {"foo": x["col_1"]}  # noqa: E731
            dset2 = dset.with_transform(transform, columns=["col_1"])
            dset.set_transform(transform, columns=["col_1"])
            self.assertDictEqual(dset.format, dset2.format)
            self.assertEqual(dset._fingerprint, dset2._fingerprint)
            dset.reset_format()
            self.assertNotEqual(dset.format, dset2.format)
            self.assertNotEqual(dset._fingerprint, dset2._fingerprint)
            del dset, dset2


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
            concatenated_dset = concatenate_datasets([dset1, dset2, dset3])
            self.assertEqual(len(concatenated_dset), len(dset1) + len(dset2) + len(dset3))
            self.assertListEqual(concatenated_dset["id"], dset1["id"] + dset2["id"] + dset3["id"])
            del dset1, dset2, dset3, concatenated_dset

    @require_transformers
    def test_set_format_encode(self):
        from transformers import BertTokenizer

        dset = Dataset.from_dict({"text": ["hello there", "foo"]})
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        def encode(batch):
            return tokenizer(batch["text"], padding="longest", return_tensors="np")

        dset.set_transform(transform=encode)
        self.assertEqual(str(dset[:2]), str(encode({"text": ["hello there", "foo"]})))


@pytest.mark.parametrize("keep_in_memory", [False, True])
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
@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_csv(path_type, split, features, keep_in_memory, csv_path, tmp_path):
    if issubclass(path_type, str):
        path = csv_path
    elif issubclass(path_type, list):
        path = [csv_path]
    cache_dir = tmp_path / "cache"
    expected_split = str(split) if split else "train"
    # CSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = Features({feature: Value(dtype) for feature, dtype in features.items()}) if features else None
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_csv(
            path, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        )
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    assert dataset.split == expected_split
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("in_memory", [False, True])
def test_dataset_from_file(in_memory, dataset, arrow_file):
    filename = arrow_file
    with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
        dataset_from_file = Dataset.from_file(filename, in_memory=in_memory)
    assert dataset_from_file.features.type == dataset.features.type
    assert dataset_from_file.features == dataset.features
    assert dataset_from_file.cache_files == ([filename] if not in_memory else [])


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
                    }
                )
            },
        ),
        ("flatten_", tuple(), {}),
    ],
)
def test_pickle_dataset_after_transforming_the_table(in_memory, method_and_params, arrow_file):
    method, args, kwargs = method_and_params
    dataset = Dataset.from_file(arrow_file, in_memory=in_memory)
    reference_dataset = Dataset.from_file(arrow_file, in_memory=in_memory)

    out = getattr(dataset, method)(*args, **kwargs)
    dataset = out if out is not None else dataset
    pickled_dataset = pickle.dumps(dataset)
    reloaded_dataset = pickle.loads(pickled_dataset)

    assert dataset._data != reference_dataset._data
    assert dataset._data.table == reloaded_dataset._data.table
