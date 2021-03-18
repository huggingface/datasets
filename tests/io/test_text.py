import pytest

from datasets import Dataset, DatasetDict, Features, NamedSplit, Value
from datasets.io.text import TextDatasetReader

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


@pytest.mark.parametrize("keep_in_memory", [False, True])
@pytest.mark.parametrize(
    "features",
    [
        None,
        {"text": "string"},
        {"text": "int32"},
        {"text": "float32"},
    ],
)
@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
@pytest.mark.parametrize("path_type", [str, list])
def test_text_dataset_reader(path_type, split, features, keep_in_memory, text_path, tmp_path):
    if issubclass(path_type, str):
        path = text_path
    elif issubclass(path_type, list):
        path = [text_path]
    cache_dir = tmp_path / "cache"

    expected_split = str(split) if split else "train"

    default_expected_features = {"text": "string"}
    expected_features = features.copy() if features else default_expected_features
    features = Features({feature: Value(dtype) for feature, dtype in features.items()}) if features else None
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = TextDatasetReader(
            path, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        ).read()
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 1
    assert dataset.column_names == ["text"]
    assert dataset.split == expected_split
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
@pytest.mark.parametrize(
    "features",
    [
        None,
        {"text": "string"},
        {"text": "int32"},
        {"text": "float32"},
    ],
)
@pytest.mark.parametrize("split", [None, "train", "test"])
def test_text_datasetdict_reader(split, features, keep_in_memory, text_path, tmp_path):
    if split:
        path = {split: text_path}
    else:
        split = "train"
        path = {"train": text_path, "test": text_path}
    cache_dir = tmp_path / "cache"

    default_expected_features = {"text": "string"}
    expected_features = features.copy() if features else default_expected_features
    features = Features({feature: Value(dtype) for feature, dtype in features.items()}) if features else None
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = TextDatasetReader(path, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
    assert isinstance(dataset, DatasetDict)
    dataset = dataset[split]
    assert dataset.num_rows == 4
    assert dataset.num_columns == 1
    assert dataset.column_names == ["text"]
    assert dataset.split == split
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype
