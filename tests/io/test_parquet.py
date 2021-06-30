import pyarrow.parquet as pq
import pytest

from datasets import Dataset, DatasetDict, Features, NamedSplit, Value
from datasets.io.parquet import ParquetDatasetReader, ParquetDatasetWriter

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


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
        dataset = ParquetDatasetReader(parquet_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
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
    dataset = ParquetDatasetReader(parquet_path, features=features, cache_dir=cache_dir).read()
    _check_parquet_dataset(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_parquet_split(split, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = ParquetDatasetReader(parquet_path, cache_dir=cache_dir, split=split).read()
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
    dataset = ParquetDatasetReader(path, cache_dir=cache_dir).read()
    _check_parquet_dataset(dataset, expected_features)


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
def test_parquet_datasetdict_reader_keep_in_memory(keep_in_memory, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = ParquetDatasetReader(
            {"train": parquet_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        ).read()
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
def test_parquet_datasetdict_reader_features(features, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = ParquetDatasetReader({"train": parquet_path}, features=features, cache_dir=cache_dir).read()
    _check_parquet_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_parquet_datasetdict_reader_split(split, parquet_path, tmp_path):
    if split:
        path = {split: parquet_path}
    else:
        split = "train"
        path = {"train": parquet_path, "test": parquet_path}
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = ParquetDatasetReader(path, cache_dir=cache_dir).read()
    _check_parquet_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())


def test_parquer_write(dataset, tmp_path):
    writer = ParquetDatasetWriter(dataset, tmp_path / "foo.parquet")
    assert writer.write() > 0
    pf = pq.ParquetFile(tmp_path / "foo.parquet")
    output_table = pf.read()
    assert dataset.data.table == output_table
