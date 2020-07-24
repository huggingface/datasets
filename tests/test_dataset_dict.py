import os
import tempfile
from typing import Dict
from unittest import TestCase

import numpy as np
import pyarrow as pa

from nlp.arrow_dataset import Dataset
from nlp.dataset_dict import DatasetDict


class DatasetDictTest(TestCase):
    def _create_dummy_dataset(self) -> Dataset:
        dset = Dataset(
            pa.Table.from_pydict({"filename": ["my_name-train" + "_" + str(x) for x in np.arange(30).tolist()]})
        )
        return dset

    def _create_dummy_dataset_dict(self) -> DatasetDict:
        return DatasetDict({"train": self._create_dummy_dataset(), "test": self._create_dummy_dataset()})

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
