import os
import tempfile
from unittest import TestCase

import numpy as np
import pandas as pd
import pytest

from datasets import load_from_disk
from datasets.arrow_dataset import Dataset
from datasets.dataset_dict import DatasetDict
from datasets.features import ClassLabel, Features, Sequence, Value
from datasets.splits import NamedSplit

from .conftest import s3_test_bucket_name
from .utils import (
    assert_arrow_memory_doesnt_increase,
    assert_arrow_memory_increases,
    require_s3,
    require_tf,
    require_torch,
)


class DatasetDictTest(TestCase):
    def _create_dummy_dataset(self, multiple_columns=False):
        if multiple_columns:
            data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
            dset = Dataset.from_dict(data)
        else:
            dset = Dataset.from_dict(
                {"filename": ["my_name-train" + "_" + f"{x:03d}" for x in np.arange(30).tolist()]}
            )
        return dset

    def _create_dummy_dataset_dict(self, multiple_columns=False) -> DatasetDict:
        return DatasetDict(
            {
                "train": self._create_dummy_dataset(multiple_columns=multiple_columns),
                "test": self._create_dummy_dataset(multiple_columns=multiple_columns),
            }
        )

    def test_flatten_in_place(self):
        dset_split = Dataset.from_dict(
            {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10},
            features=Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")}),
        )
        dset = DatasetDict({"train": dset_split, "test": dset_split})
        dset.flatten_()
        self.assertDictEqual(dset.column_names, {"train": ["a.b.c", "foo"], "test": ["a.b.c", "foo"]})
        self.assertListEqual(sorted(dset["train"].features.keys()), ["a.b.c", "foo"])
        self.assertDictEqual(
            dset["train"].features, Features({"a.b.c": Sequence(Value("string")), "foo": Value("int64")})
        )
        del dset

    def test_flatten(self):
        dset_split = Dataset.from_dict(
            {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10},
            features=Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")}),
        )
        dset = DatasetDict({"train": dset_split, "test": dset_split})
        dset = dset.flatten()
        self.assertDictEqual(dset.column_names, {"train": ["a.b.c", "foo"], "test": ["a.b.c", "foo"]})
        self.assertListEqual(sorted(dset["train"].features.keys()), ["a.b.c", "foo"])
        self.assertDictEqual(
            dset["train"].features, Features({"a.b.c": Sequence(Value("string")), "foo": Value("int64")})
        )
        del dset

    def test_set_format_numpy(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.set_format(type="numpy", columns=["col_1"])
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0]), 1)
            self.assertIsInstance(dset_split[0]["col_1"], np.int64)
            self.assertEqual(dset_split[0]["col_1"].item(), 3)

        dset.reset_format()
        with dset.formatted_as(type="numpy", columns=["col_1"]):
            for dset_split in dset.values():
                self.assertEqual(len(dset_split[0]), 1)
                self.assertIsInstance(dset_split[0]["col_1"], np.int64)
                self.assertEqual(dset_split[0]["col_1"].item(), 3)

        for dset_split in dset.values():
            self.assertEqual(dset_split.format["type"], None)
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
            self.assertIsInstance(dset_split[0]["col_2"], np.str_)
            self.assertEqual(dset_split[0]["col_2"].item(), "a")
        del dset

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
        del dset

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
        del dset

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
        del dset

    def test_set_transform(self):
        def transform(batch):
            return {k: [str(i).upper() for i in v] for k, v in batch.items()}

        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.set_transform(transform=transform, columns=["col_1"])
        for dset_split in dset.values():
            self.assertEqual(dset_split.format["type"], "custom")
            self.assertEqual(len(dset_split[0].keys()), 1)
            self.assertEqual(dset_split[0]["col_1"], "3")
            self.assertEqual(dset_split[:2]["col_1"], ["3", "2"])
            self.assertEqual(dset_split["col_1"][:2], ["3", "2"])

        prev_format = dset[list(dset.keys())[0]].format
        for dset_split in dset.values():
            dset_split.set_format(**dset_split.format)
            self.assertEqual(prev_format, dset_split.format)

        dset.set_transform(transform=transform, columns=["col_1", "col_2"])
        for dset_split in dset.values():
            self.assertEqual(len(dset_split[0].keys()), 2)
            self.assertEqual(dset_split[0]["col_2"], "A")
        del dset

    def test_with_format(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset2 = dset.with_format("numpy", columns=["col_1"])
        dset.set_format("numpy", columns=["col_1"])
        for dset_split, dset_split2 in zip(dset.values(), dset2.values()):
            self.assertDictEqual(dset_split.format, dset_split2.format)
        del dset, dset2

    def test_with_transform(self):
        def transform(batch):
            return {k: [str(i).upper() for i in v] for k, v in batch.items()}

        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset2 = dset.with_transform(transform, columns=["col_1"])
        dset.set_transform(transform, columns=["col_1"])
        for dset_split, dset_split2 in zip(dset.values(), dset2.values()):
            self.assertDictEqual(dset_split.format, dset_split2.format)
        del dset, dset2

    def test_cast_in_place(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        features = dset["train"].features
        features["col_1"] = Value("float64")
        dset.cast_(features)
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 2)
            self.assertEqual(dset_split.features["col_1"], Value("float64"))
            self.assertIsInstance(dset_split[0]["col_1"], float)
        del dset

    def test_cast(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        features = dset["train"].features
        features["col_1"] = Value("float64")
        dset = dset.cast(features)
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 2)
            self.assertEqual(dset_split.features["col_1"], Value("float64"))
            self.assertIsInstance(dset_split[0]["col_1"], float)
        del dset

    def test_remove_columns_in_place(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.remove_columns_(column_names="col_1")
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 1)
            self.assertListEqual(list(dset_split.column_names), ["col_2"])

        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.remove_columns_(column_names=["col_1", "col_2"])
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 0)
        del dset

    def test_remove_columns(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset = dset.remove_columns(column_names="col_1")
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 1)
            self.assertListEqual(list(dset_split.column_names), ["col_2"])

        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset = dset.remove_columns(column_names=["col_1", "col_2"])
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 0)
        del dset

    def test_rename_column_in_place(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset.rename_column_(original_column_name="col_1", new_column_name="new_name")
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 2)
            self.assertListEqual(list(dset_split.column_names), ["new_name", "col_2"])
        del dset

    def test_rename_column(self):
        dset = self._create_dummy_dataset_dict(multiple_columns=True)
        dset = dset.rename_column(original_column_name="col_1", new_column_name="new_name")
        for dset_split in dset.values():
            self.assertEqual(dset_split.num_columns, 2)
            self.assertListEqual(list(dset_split.column_names), ["new_name", "col_2"])
        del dset

    def test_map(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dsets = self._create_dummy_dataset_dict()

            mapped_dsets_1: DatasetDict = dsets.map(lambda ex: {"foo": ["bar"] * len(ex["filename"])}, batched=True)
            self.assertListEqual(list(dsets.keys()), list(mapped_dsets_1.keys()))
            self.assertListEqual(mapped_dsets_1["train"].column_names, ["filename", "foo"])

            cache_file_names = {
                "train": os.path.join(tmp_dir, "train.arrow"),
                "test": os.path.join(tmp_dir, "test.arrow"),
            }
            mapped_dsets_2: DatasetDict = mapped_dsets_1.map(
                lambda ex: {"bar": ["foo"] * len(ex["filename"])}, batched=True, cache_file_names=cache_file_names
            )
            self.assertListEqual(list(dsets.keys()), list(mapped_dsets_2.keys()))
            self.assertListEqual(sorted(mapped_dsets_2["train"].column_names), sorted(["filename", "foo", "bar"]))
            del dsets, mapped_dsets_1, mapped_dsets_2

    def test_filter(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dsets = self._create_dummy_dataset_dict()

            filtered_dsets_1: DatasetDict = dsets.filter(lambda ex: int(ex["filename"].split("_")[-1]) < 10)
            self.assertListEqual(list(dsets.keys()), list(filtered_dsets_1.keys()))
            self.assertEqual(len(filtered_dsets_1["train"]), 10)

            cache_file_names = {
                "train": os.path.join(tmp_dir, "train.arrow"),
                "test": os.path.join(tmp_dir, "test.arrow"),
            }
            filtered_dsets_2: DatasetDict = filtered_dsets_1.filter(
                lambda ex: int(ex["filename"].split("_")[-1]) < 5, cache_file_names=cache_file_names
            )
            self.assertListEqual(list(dsets.keys()), list(filtered_dsets_2.keys()))
            self.assertEqual(len(filtered_dsets_2["train"]), 5)

            filtered_dsets_3: DatasetDict = dsets.filter(
                lambda examples: [int(ex.split("_")[-1]) < 10 for ex in examples["filename"]], batched=True
            )
            self.assertListEqual(list(dsets.keys()), list(filtered_dsets_3.keys()))
            self.assertEqual(len(filtered_dsets_3["train"]), 10)
            del dsets, filtered_dsets_1, filtered_dsets_2, filtered_dsets_3

    def test_sort(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dsets = self._create_dummy_dataset_dict()

            sorted_dsets_1: DatasetDict = dsets.sort("filename")
            self.assertListEqual(list(dsets.keys()), list(sorted_dsets_1.keys()))
            self.assertListEqual(
                [f.split("_")[-1] for f in sorted_dsets_1["train"]["filename"]],
                sorted(f"{x:03d}" for x in range(30)),
            )

            indices_cache_file_names = {
                "train": os.path.join(tmp_dir, "train.arrow"),
                "test": os.path.join(tmp_dir, "test.arrow"),
            }
            sorted_dsets_2: DatasetDict = sorted_dsets_1.sort(
                "filename", indices_cache_file_names=indices_cache_file_names, reverse=True
            )
            self.assertListEqual(list(dsets.keys()), list(sorted_dsets_2.keys()))
            self.assertListEqual(
                [f.split("_")[-1] for f in sorted_dsets_2["train"]["filename"]],
                sorted((f"{x:03d}" for x in range(30)), reverse=True),
            )
            del dsets, sorted_dsets_1, sorted_dsets_2

    def test_shuffle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dsets = self._create_dummy_dataset_dict()

            indices_cache_file_names = {
                "train": os.path.join(tmp_dir, "train.arrow"),
                "test": os.path.join(tmp_dir, "test.arrow"),
            }
            seeds = {
                "train": 1234,
                "test": 1234,
            }
            dsets_shuffled = dsets.shuffle(
                seeds=seeds, indices_cache_file_names=indices_cache_file_names, load_from_cache_file=False
            )
            self.assertListEqual(dsets_shuffled["train"]["filename"], dsets_shuffled["test"]["filename"])

            self.assertEqual(len(dsets_shuffled["train"]), 30)
            self.assertEqual(dsets_shuffled["train"][0]["filename"], "my_name-train_028")
            self.assertEqual(dsets_shuffled["train"][2]["filename"], "my_name-train_010")
            self.assertDictEqual(dsets["train"].features, Features({"filename": Value("string")}))
            self.assertDictEqual(dsets_shuffled["train"].features, Features({"filename": Value("string")}))

            # Reproducibility
            indices_cache_file_names_2 = {
                "train": os.path.join(tmp_dir, "train_2.arrow"),
                "test": os.path.join(tmp_dir, "test_2.arrow"),
            }
            dsets_shuffled_2 = dsets.shuffle(
                seeds=seeds, indices_cache_file_names=indices_cache_file_names_2, load_from_cache_file=False
            )
            self.assertListEqual(dsets_shuffled["train"]["filename"], dsets_shuffled_2["train"]["filename"])

            seeds = {
                "train": 1234,
                "test": 1,
            }
            indices_cache_file_names_3 = {
                "train": os.path.join(tmp_dir, "train_3.arrow"),
                "test": os.path.join(tmp_dir, "test_3.arrow"),
            }
            dsets_shuffled_3 = dsets.shuffle(
                seeds=seeds, indices_cache_file_names=indices_cache_file_names_3, load_from_cache_file=False
            )
            self.assertNotEqual(dsets_shuffled_3["train"]["filename"], dsets_shuffled_3["test"]["filename"])

            # other input types
            dsets_shuffled_int = dsets.shuffle(42)
            dsets_shuffled_alias = dsets.shuffle(seed=42)
            dsets_shuffled_none = dsets.shuffle()
            self.assertEqual(len(dsets_shuffled_int["train"]), 30)
            self.assertEqual(len(dsets_shuffled_alias["train"]), 30)
            self.assertEqual(len(dsets_shuffled_none["train"]), 30)

            del dsets, dsets_shuffled, dsets_shuffled_2, dsets_shuffled_3
            del dsets_shuffled_int, dsets_shuffled_alias, dsets_shuffled_none

    def test_check_values_type(self):
        dsets = self._create_dummy_dataset_dict()
        dsets["bad_split"] = None
        self.assertRaises(TypeError, dsets.map, lambda x: x)
        self.assertRaises(TypeError, dsets.filter, lambda x: True)
        self.assertRaises(TypeError, dsets.shuffle)
        self.assertRaises(TypeError, dsets.sort, "filename")
        del dsets

    def test_serialization(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dsets = self._create_dummy_dataset_dict()
            dsets.save_to_disk(tmp_dir)
            reloaded_dsets = DatasetDict.load_from_disk(tmp_dir)
            self.assertListEqual(sorted(reloaded_dsets), ["test", "train"])
            self.assertEqual(len(reloaded_dsets["train"]), 30)
            self.assertListEqual(reloaded_dsets["train"].column_names, ["filename"])
            self.assertEqual(len(reloaded_dsets["test"]), 30)
            self.assertListEqual(reloaded_dsets["test"].column_names, ["filename"])
            del reloaded_dsets

            del dsets["test"]
            dsets.save_to_disk(tmp_dir)
            reloaded_dsets = DatasetDict.load_from_disk(tmp_dir)
            self.assertListEqual(sorted(reloaded_dsets), ["train"])
            self.assertEqual(len(reloaded_dsets["train"]), 30)
            self.assertListEqual(reloaded_dsets["train"].column_names, ["filename"])
            del dsets, reloaded_dsets

    def test_load_from_disk(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dsets = self._create_dummy_dataset_dict()
            dsets.save_to_disk(tmp_dir)
            del dsets
            dsets = load_from_disk(tmp_dir)
            self.assertListEqual(sorted(dsets), ["test", "train"])
            self.assertEqual(len(dsets["train"]), 30)
            self.assertListEqual(dsets["train"].column_names, ["filename"])
            self.assertEqual(len(dsets["test"]), 30)
            self.assertListEqual(dsets["test"].column_names, ["filename"])
            del dsets

    def test_align_labels_with_mapping(self):
        train_features = Features(
            {
                "input_text": Value("string"),
                "input_labels": ClassLabel(num_classes=3, names=["entailment", "neutral", "contradiction"]),
            }
        )
        test_features = Features(
            {
                "input_text": Value("string"),
                "input_labels": ClassLabel(num_classes=3, names=["entailment", "contradiction", "neutral"]),
            }
        )
        train_data = {"input_text": ["a", "a", "b", "b", "c", "c"], "input_labels": [0, 0, 1, 1, 2, 2]}
        test_data = {"input_text": ["a", "a", "c", "c", "b", "b"], "input_labels": [0, 0, 1, 1, 2, 2]}
        label2id = {"CONTRADICTION": 0, "ENTAILMENT": 2, "NEUTRAL": 1}
        id2label = {v: k for k, v in label2id.items()}
        train_expected_labels = [2, 2, 1, 1, 0, 0]
        test_expected_labels = [2, 2, 0, 0, 1, 1]
        train_expected_label_names = [id2label[idx] for idx in train_expected_labels]
        test_expected_label_names = [id2label[idx] for idx in test_expected_labels]
        dsets = DatasetDict(
            {
                "train": Dataset.from_dict(train_data, features=train_features),
                "test": Dataset.from_dict(test_data, features=test_features),
            }
        )
        dsets = dsets.align_labels_with_mapping(label2id, "input_labels")
        self.assertListEqual(train_expected_labels, dsets["train"]["input_labels"])
        self.assertListEqual(test_expected_labels, dsets["test"]["input_labels"])
        train_aligned_label_names = [
            dsets["train"].features["input_labels"].int2str(idx) for idx in dsets["train"]["input_labels"]
        ]
        test_aligned_label_names = [
            dsets["test"].features["input_labels"].int2str(idx) for idx in dsets["test"]["input_labels"]
        ]
        self.assertListEqual(train_expected_label_names, train_aligned_label_names)
        self.assertListEqual(test_expected_label_names, test_aligned_label_names)


def _check_csv_datasetdict(dataset_dict, expected_features, splits=("train",)):
    assert isinstance(dataset_dict, DatasetDict)
    for split in splits:
        dataset = dataset_dict[split]
        assert dataset.num_rows == 4
        assert dataset.num_columns == 3
        assert dataset.column_names == ["col_1", "col_2", "col_3"]
        for feature, expected_dtype in expected_features.items():
            assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_datasetdict_from_csv_keep_in_memory(keep_in_memory, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = DatasetDict.from_csv({"train": csv_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory)
    _check_csv_datasetdict(dataset, expected_features)


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
def test_datasetdict_from_csv_features(features, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    # CSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = DatasetDict.from_csv({"train": csv_path}, features=features, cache_dir=cache_dir)
    _check_csv_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_datasetdict_from_csv_split(split, csv_path, tmp_path):
    if split:
        path = {split: csv_path}
    else:
        split = "train"
        path = {"train": csv_path, "test": csv_path}
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    dataset = DatasetDict.from_csv(path, cache_dir=cache_dir)
    _check_csv_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())


def _check_json_datasetdict(dataset_dict, expected_features, splits=("train",)):
    assert isinstance(dataset_dict, DatasetDict)
    for split in splits:
        dataset = dataset_dict[split]
        assert dataset.num_rows == 4
        assert dataset.num_columns == 3
        assert dataset.column_names == ["col_1", "col_2", "col_3"]
        for feature, expected_dtype in expected_features.items():
            assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_datasetdict_from_json_keep_in_memory(keep_in_memory, jsonl_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = DatasetDict.from_json({"train": jsonl_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory)
    _check_json_datasetdict(dataset, expected_features)


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
def test_datasetdict_from_json_features(features, jsonl_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = DatasetDict.from_json({"train": jsonl_path}, features=features, cache_dir=cache_dir)
    _check_json_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_datasetdict_from_json_splits(split, jsonl_path, tmp_path):
    if split:
        path = {split: jsonl_path}
    else:
        split = "train"
        path = {"train": jsonl_path, "test": jsonl_path}
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = DatasetDict.from_json(path, cache_dir=cache_dir)
    _check_json_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())


def _check_parquet_datasetdict(dataset_dict, expected_features, splits=("train",)):
    assert isinstance(dataset_dict, DatasetDict)
    for split in splits:
        dataset = dataset_dict[split]
        assert dataset.num_rows == 4
        assert dataset.num_columns == 3
        assert dataset.column_names == ["col_1", "col_2", "col_3"]
        for feature, expected_dtype in expected_features.items():
            assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_datasetdict_from_parquet_keep_in_memory(keep_in_memory, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = DatasetDict.from_parquet({"train": parquet_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory)
    _check_parquet_datasetdict(dataset, expected_features)


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
def test_datasetdict_from_parquet_features(features, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = DatasetDict.from_parquet({"train": parquet_path}, features=features, cache_dir=cache_dir)
    _check_parquet_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_datasetdict_from_parquet_split(split, parquet_path, tmp_path):
    if split:
        path = {split: parquet_path}
    else:
        split = "train"
        path = {"train": parquet_path, "test": parquet_path}
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = DatasetDict.from_parquet(path, cache_dir=cache_dir)
    _check_parquet_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())


def _check_text_datasetdict(dataset_dict, expected_features, splits=("train",)):
    assert isinstance(dataset_dict, DatasetDict)
    for split in splits:
        dataset = dataset_dict[split]
        assert dataset.num_rows == 4
        assert dataset.num_columns == 1
        assert dataset.column_names == ["text"]
        for feature, expected_dtype in expected_features.items():
            assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_datasetdict_from_text_keep_in_memory(keep_in_memory, text_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"text": "string"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = DatasetDict.from_text({"train": text_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory)
    _check_text_datasetdict(dataset, expected_features)


@pytest.mark.parametrize(
    "features",
    [
        None,
        {"text": "string"},
        {"text": "int32"},
        {"text": "float32"},
    ],
)
def test_datasetdict_from_text_features(features, text_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"text": "string"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = DatasetDict.from_text({"train": text_path}, features=features, cache_dir=cache_dir)
    _check_text_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_datasetdict_from_text_split(split, text_path, tmp_path):
    if split:
        path = {split: text_path}
    else:
        split = "train"
        path = {"train": text_path, "test": text_path}
    cache_dir = tmp_path / "cache"
    expected_features = {"text": "string"}
    dataset = DatasetDict.from_text(path, cache_dir=cache_dir)
    _check_text_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())


@require_s3
def test_dummy_dataset_serialize_s3(s3, dataset):
    dsets = DatasetDict({"train": dataset, "test": dataset.select(range(2))})
    mock_bucket = s3_test_bucket_name
    dataset_path = f"s3://{mock_bucket}/datasets/dict"
    column_names = dsets["train"].column_names
    lengths = [len(dset) for dset in dsets.values()]
    dataset.save_to_disk(dataset_path, s3)
    dataset = dataset.load_from_disk(dataset_path, s3)

    assert sorted(dsets) == ["test", "train"]
    assert [len(dset) for dset in dsets.values()] == lengths
    assert dsets["train"].column_names == column_names
    assert dsets["test"].column_names == column_names
