import pytest

from datasets import Dataset, DatasetDict, Features, NamedSplit, Value
from datasets.io.text import TextDatasetReader

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


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
        dataset = TextDatasetReader(text_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
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
    dataset = TextDatasetReader(text_path, features=features, cache_dir=cache_dir).read()
    _check_text_dataset(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_text_split(split, text_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"text": "string"}
    dataset = TextDatasetReader(text_path, cache_dir=cache_dir, split=split).read()
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
    dataset = TextDatasetReader(path, cache_dir=cache_dir).read()
    _check_text_dataset(dataset, expected_features)


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
        dataset = TextDatasetReader({"train": text_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
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
    # CSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"text": "string"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = TextDatasetReader({"train": text_path}, features=features, cache_dir=cache_dir).read()
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
    dataset = TextDatasetReader(path, cache_dir=cache_dir).read()
    _check_text_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())
