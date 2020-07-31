import os
import tempfile
from typing import Dict
from unittest import TestCase

import numpy as np
import pandas as pd

from nlp.arrow_dataset import Dataset
from nlp.dataset_dict import DatasetDict
from nlp.features import Value

from .utils import require_tf, require_torch


class DatasetDictTest(TestCase):
    def _create_dummy_dataset(self, multiple_columns=False):
        if multiple_columns:
            data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
            dset = Dataset.from_dict(data)
        else:
            dset = Dataset.from_dict({"filename": ["my_name-train" + "_" + str(x) for x in np.arange(30).tolist()]})
        return dset

    def _create_dummy_dataset_dict(self, multiple_columns=False) -> DatasetDict:
        return DatasetDict(
            {
                "train": self._create_dummy_dataset(multiple_columns=multiple_columns),
                "test": self._create_dummy_dataset(multiple_columns=multiple_columns),
            }
        )

    def test_set_format_numpy(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.set_format(type="numpy", columns=["col_1"])
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0]), 1)
            self.assertIsInstance(dset_split[0]["col_1"], np.ndarray)
            self.assertListEqual(list(dset_split[0]["col_1"].shape), [])
            self.assertEqual(dset_split[0]["col_1"].item(), 3)

        dset.reset_format()
        with dset.formated_as(type="numpy", columns=["col_1"]):
            for dset_split in dset.values():
                self.assertEqual(len(dset_split[0]), 1)
                self.assertIsInstance(dset_split[0]["col_1"], np.ndarray)
                self.assertListEqual(list(dset_split[0]["col_1"].shape), [])
                self.assertEqual(dset_split[0]["col_1"].item(), 3)

        for dset_split in dset.values():
            self.assertEqual(dset_split.format["type"], "python")
            self.assertEqual(dset_split.format["format_kwargs"], {})
            self.assertEqual(dset_split.format["columns"], dset_split.column_names)
            self.assertEqual(dset_split.format["output_all_columns"], False)

        dset.set_format(type="numpy", columns=["col_1"], output_all_columns=True)
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0]), 2)
            self.assertIsInstance(dset_split[0]["col_2"], str)
            self.assertEqual(dset_split[0]["col_2"], "a")

        dset.set_format(type="numpy", columns=["col_1", "col_2"])
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0]), 2)
            self.assertEqual(dset_split[0]["col_2"].item(), "a")

    @require_torch
    def test_set_format_torch(self):
        import torch

        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.set_format(type="torch", columns=["col_1"])
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0]), 1)
            self.assertIsInstance(dset_split[0]["col_1"], torch.Tensor)
            self.assertListEqual(list(dset_split[0]["col_1"].shape), [])
            self.assertEqual(dset_split[0]["col_1"].item(), 3)

        dset.set_format(type="torch", columns=["col_1"], output_all_columns=True)
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0]), 2)
            self.assertIsInstance(dset_split[0]["col_2"], str)
            self.assertEqual(dset_split[0]["col_2"], "a")

        dset.set_format(type="torch", columns=["col_1", "col_2"])
        for dset_split in dset.values():
            with self.assertRaises(TypeError):
                dset_split[0]

    @require_tf
    def test_set_format_tf(self):
        import tensorflow as tf

        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.set_format(type="tensorflow", columns=["col_1"])
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0]), 1)
            self.assertIsInstance(dset_split[0]["col_1"], tf.Tensor)
            self.assertListEqual(list(dset_split[0]["col_1"].shape), [])
            self.assertEqual(dset_split[0]["col_1"].numpy().item(), 3)

        dset.set_format(type="tensorflow", columns=["col_1"], output_all_columns=True)
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0]), 2)
            self.assertIsInstance(dset_split[0]["col_2"], str)
            self.assertEqual(dset_split[0]["col_2"], "a")

        dset.set_format(type="tensorflow", columns=["col_1", "col_2"])
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0]), 2)
            self.assertEqual(dset_split[0]["col_2"].numpy().decode("utf-8"), "a")

    def test_set_format_pandas(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.set_format(type="pandas", columns=["col_1"])
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0].columns), 1)
            self.assertIsInstance(dset_split[0], pd.DataFrame)
            self.assertListEqual(list(dset_split[0].shape), [1, 1])
            self.assertEqual(dset_split[0]["col_1"].item(), 3)

        dset.set_format(type="pandas", columns=["col_1", "col_2"])
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0].columns), 2)
            self.assertEqual(dset_split[0]["col_2"].item(), "a")

    def test_cast_(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        features = dset["train"].features
        features["col_1"] = Value("float64")
        dset.cast_(features)
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 2)
            self.assertEqual(dset_split.features["col_1"], Value("float64"))
            self.assertIsInstance(dset_split[0]["col_1"], float)

    def test_remove_column_(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.remove_column_(column_name="col_1")
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 1)
            self.assertListEqual(list(dset_split.column_names), ["col_2"])

    def test_rename_column_(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.rename_column_(original_column_name="col_1", new_column_name="new_name")
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 2)
            self.assertListEqual(list(dset_split.column_names), ["new_name", "col_2"])

    def test_map(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dsets = self._create_dummy_dataset_dict()

            mapped_dsets_1: Dict[str, Dataset] = dsets.map(
                lambda ex: {"foo": ["bar"] * len(ex["filename"])}, batched=True
            )
            self.assertListEqual(list(dsets.keys()), list(mapped_dsets_1.keys()))
            self.assertListEqual(mapped_dsets_1["train"].column_names, ["filename", "foo"])

            cache_file_names = {
                "train": os.path.join(tmp_dir, "train.arrow"),
                "test": os.path.join(tmp_dir, "test.arrow"),
            }
            mapped_dsets_2: Dict[str, Dataset] = mapped_dsets_1.map(
                lambda ex: {"bar": ["foo"] * len(ex["filename"])}, batched=True, cache_file_names=cache_file_names
            )
            self.assertListEqual(list(dsets.keys()), list(mapped_dsets_2.keys()))
            self.assertListEqual(mapped_dsets_2["train"].column_names, ["filename", "foo", "bar"])

    def test_filter(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dsets = self._create_dummy_dataset_dict()

            filtered_dsets_1: Dict[str, Dataset] = dsets.filter(lambda ex: int(ex["filename"].split("_")[-1]) < 10)
            self.assertListEqual(list(dsets.keys()), list(filtered_dsets_1.keys()))
            self.assertEqual(len(filtered_dsets_1["train"]), 10)

            cache_file_names = {
                "train": os.path.join(tmp_dir, "train.arrow"),
                "test": os.path.join(tmp_dir, "test.arrow"),
            }
            filtered_dsets_2: Dict[str, Dataset] = filtered_dsets_1.filter(
                lambda ex: int(ex["filename"].split("_")[-1]) < 5, cache_file_names=cache_file_names
            )
            self.assertListEqual(list(dsets.keys()), list(filtered_dsets_2.keys()))
            self.assertEqual(len(filtered_dsets_2["train"]), 5)

    def test_sort(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dsets = self._create_dummy_dataset_dict()

            sorted_dsets_1: Dict[str, Dataset] = dsets.sort("filename")
            self.assertListEqual(list(dsets.keys()), list(sorted_dsets_1.keys()))
            self.assertListEqual(
                [f.split("_")[-1] for f in sorted_dsets_1["train"]["filename"]], sorted(str(x) for x in range(30))
            )

            cache_file_names = {
                "train": os.path.join(tmp_dir, "train.arrow"),
                "test": os.path.join(tmp_dir, "test.arrow"),
            }
            sorted_dsets_2: Dict[str, Dataset] = sorted_dsets_1.sort(
                "filename", cache_file_names=cache_file_names, reverse=True
            )
            self.assertListEqual(list(dsets.keys()), list(sorted_dsets_2.keys()))
            self.assertListEqual(
                [f.split("_")[-1] for f in sorted_dsets_2["train"]["filename"]],
                sorted((str(x) for x in range(30)), reverse=True),
            )

    def test_check_values_type(self):
        dsets = self._create_dummy_dataset_dict()
        dsets["bad_split"] = None
        self.assertRaises(TypeError, dsets.map, lambda x: x)
        self.assertRaises(TypeError, dsets.filter, lambda x: True)
        self.assertRaises(TypeError, dsets.shuffle)
        self.assertRaises(TypeError, dsets.sort, "filename")
