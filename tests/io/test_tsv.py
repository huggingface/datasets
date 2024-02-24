import csv
import os

import pytest

from datasets import Dataset, DatasetDict, Features, NamedSplit, Value
from datasets.io.csv import CsvDatasetReader, CsvDatasetWriter

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


def _check_tsv_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_tsv_keep_in_memory(keep_in_memory, tsv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = CsvDatasetReader(tsv_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory,delimiter="\t").read()
    _check_tsv_dataset(dataset, expected_features)


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
def test_dataset_from_tsv_features(features, tsv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    # TSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = CsvDatasetReader(tsv_path, features=features, cache_dir=cache_dir,delimiter="\t").read()
    _check_tsv_dataset(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_tsv_split(split, tsv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    dataset = CsvDatasetReader(tsv_path, cache_dir=cache_dir, split=split,delimiter="\t").read()
    _check_tsv_dataset(dataset, expected_features)
    assert dataset.split == split if split else "train"


@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_tsv_path_type(path_type, tsv_path, tmp_path):
    if issubclass(path_type, str):
        path = tsv_path
    elif issubclass(path_type, list):
        path = [tsv_path]
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    dataset = CsvDatasetReader(path, cache_dir=cache_dir,delimiter="\t").read()
    _check_tsv_dataset(dataset, expected_features)


def _check_tsv_datasetdict(dataset_dict, expected_features, splits=("train",)):
    assert isinstance(dataset_dict, DatasetDict)
    for split in splits:
        dataset = dataset_dict[split]
        assert dataset.num_rows == 4
        assert dataset.num_columns == 3
        assert dataset.column_names == ["col_1", "col_2", "col_3"]
        for feature, expected_dtype in expected_features.items():
            assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_tsv_datasetdict_reader_keep_in_memory(keep_in_memory, tsv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = CsvDatasetReader({"train": tsv_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory,delimiter="\t").read()
    _check_tsv_datasetdict(dataset, expected_features)


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
def test_tsv_datasetdict_reader_features(features, tsv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    # TSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = CsvDatasetReader({"train": tsv_path}, features=features, cache_dir=cache_dir,delimiter="\t").read()
    _check_tsv_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_tsv_datasetdict_reader_split(split, tsv_path, tmp_path):
    if split:
        path = {split: tsv_path}
    else:
        path = {"train": tsv_path, "test": tsv_path}
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    dataset = CsvDatasetReader(path, cache_dir=cache_dir,delimiter="\t").read()
    _check_tsv_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())


def iter_tsv_file(tsv_path):
    with open(tsv_path, encoding="utf-8") as tsvfile:
        yield from csv.reader(tsvfile, delimiter="\t")


def test_dataset_to_tsv(tsv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    output_tsv = os.path.join(cache_dir, "tmp.tsv")
    dataset = CsvDatasetReader({"train": tsv_path}, cache_dir=cache_dir,delimiter="\t").read()
    CsvDatasetWriter(dataset["train"], output_tsv, num_proc=1,delimiter="\t").write()

    original_tsv = iter_tsv_file(tsv_path)
    expected_tsv = iter_tsv_file(output_tsv)

    for row1, row2 in zip(original_tsv, expected_tsv):
        assert row1 == row2


def test_dataset_to_tsv_multiproc(tsv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    output_tsv = os.path.join(cache_dir, "tmp.tsv")
    dataset = CsvDatasetReader({"train": tsv_path}, cache_dir=cache_dir,delimiter="\t").read()
    CsvDatasetWriter(dataset["train"], output_tsv, num_proc=2,delimiter="\t").write()

    original_tsv = iter_tsv_file(tsv_path)
    expected_tsv = iter_tsv_file(output_tsv)

    for row1, row2 in zip(original_tsv, expected_tsv):
        assert row1 == row2


def test_dataset_to_tsv_invalidproc(tsv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    output_tsv = os.path.join(cache_dir, "tmp.tsv")
    dataset = CsvDatasetReader({"train": tsv_path}, cache_dir=cache_dir,delimiter="\t").read()
    with pytest.raises(ValueError):
        CsvDatasetWriter(dataset["train"], output_tsv, num_proc=0,delimiter="\t")
