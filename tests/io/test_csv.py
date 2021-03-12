import pytest

from datasets import Dataset, DatasetDict, Features, NamedSplit, Value
from datasets.io.csv import CsvDatasetReader

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


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
def test_csv_dataset_reader(path_type, split, features, keep_in_memory, csv_path, tmp_path):
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
        dataset = CsvDatasetReader(
            path, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        ).read()
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    assert dataset.split == expected_split
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


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
@pytest.mark.parametrize("split", [None, "train", "test"])
def test_csv_datasetdict_reader(split, features, keep_in_memory, csv_path, tmp_path):
    if split:
        path = {split: csv_path}
    else:
        split = "train"
        path = {"train": csv_path, "test": csv_path}
    cache_dir = tmp_path / "cache"

    # CSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = Features({feature: Value(dtype) for feature, dtype in features.items()}) if features else None
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = CsvDatasetReader(path, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
    assert isinstance(dataset, DatasetDict)
    dataset = dataset[split]
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    assert dataset.split == split
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype
