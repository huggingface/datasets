import io
import json

import pytest

from datasets import Dataset, DatasetDict, Features, NamedSplit, Value
from datasets.io.json import JsonDatasetReader, JsonDatasetWriter

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


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
        dataset = JsonDatasetReader(jsonl_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
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
    dataset = JsonDatasetReader(jsonl_path, features=features, cache_dir=cache_dir).read()
    _check_json_dataset(dataset, expected_features)


@pytest.mark.parametrize(
    "features",
    [
        None,
        {"col_3": "float64", "col_1": "string", "col_2": "int64"},
    ],
)
def test_dataset_from_json_with_unsorted_column_names(features, jsonl_312_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_3": "float64", "col_1": "string", "col_2": "int64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = JsonDatasetReader(jsonl_312_path, features=features, cache_dir=cache_dir).read()
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 2
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_3", "col_1", "col_2"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


def test_dataset_from_json_with_mismatched_features(jsonl_312_path, tmp_path):
    # jsonl_312_path features are {"col_3": "float64", "col_1": "string", "col_2": "int64"}
    features = {"col_2": "int64", "col_3": "float64", "col_1": "string"}
    expected_features = features.copy()
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    cache_dir = tmp_path / "cache"
    dataset = JsonDatasetReader(jsonl_312_path, features=features, cache_dir=cache_dir).read()
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 2
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_2", "col_3", "col_1"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_json_split(split, jsonl_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = JsonDatasetReader(jsonl_path, cache_dir=cache_dir, split=split).read()
    _check_json_dataset(dataset, expected_features)
    assert dataset.split == str(split) if split else "train"


@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_json_path_type(path_type, jsonl_path, tmp_path):
    if issubclass(path_type, str):
        path = jsonl_path
    elif issubclass(path_type, list):
        path = [jsonl_path]
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = JsonDatasetReader(path, cache_dir=cache_dir).read()
    _check_json_dataset(dataset, expected_features)


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
        dataset = JsonDatasetReader({"train": jsonl_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
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
    dataset = JsonDatasetReader({"train": jsonl_path}, features=features, cache_dir=cache_dir).read()
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
    dataset = JsonDatasetReader(path, cache_dir=cache_dir).read()
    _check_json_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())


def load_json(buffer):
    return json.load(buffer)


def load_json_lines(buffer):
    return [json.loads(line) for line in buffer]


class TestJsonDatasetWriter:
    @pytest.mark.parametrize("lines, load_json_function", [(True, load_json_lines), (False, load_json)])
    def test_dataset_to_json_lines(self, lines, load_json_function, dataset):
        with io.BytesIO() as buffer:
            JsonDatasetWriter(dataset, buffer, lines=lines).write()
            buffer.seek(0)
            exported_content = load_json_function(buffer)
        assert isinstance(exported_content, list)
        assert isinstance(exported_content[0], dict)
        assert len(exported_content) == 10

    @pytest.mark.parametrize(
        "orient, container, keys, len_at",
        [
            ("records", list, {"tokens", "labels", "answers", "id"}, None),
            ("split", dict, {"index", "columns", "data"}, "data"),
            ("index", dict, set("0123456789"), None),
            ("columns", dict, {"tokens", "labels", "answers", "id"}, "tokens"),
            ("values", list, None, None),
            ("table", dict, {"schema", "data"}, "data"),
        ],
    )
    def test_dataset_to_json_orient(self, orient, container, keys, len_at, dataset):
        with io.BytesIO() as buffer:
            JsonDatasetWriter(dataset, buffer, lines=False, orient=orient).write()
            buffer.seek(0)
            exported_content = load_json(buffer)
        assert isinstance(exported_content, container)
        if keys:
            if container is dict:
                assert exported_content.keys() == keys
            else:
                assert exported_content[0].keys() == keys
        else:
            assert not hasattr(exported_content, "keys") and not hasattr(exported_content[0], "keys")
        if len_at:
            assert len(exported_content[len_at]) == 10
        else:
            assert len(exported_content) == 10

    @pytest.mark.parametrize("lines, load_json_function", [(True, load_json_lines), (False, load_json)])
    def test_dataset_to_json_lines_multiproc(self, lines, load_json_function, dataset):
        with io.BytesIO() as buffer:
            JsonDatasetWriter(dataset, buffer, lines=lines, num_proc=2).write()
            buffer.seek(0)
            exported_content = load_json_function(buffer)
        assert isinstance(exported_content, list)
        assert isinstance(exported_content[0], dict)
        assert len(exported_content) == 10

    @pytest.mark.parametrize(
        "orient, container, keys, len_at",
        [
            ("records", list, {"tokens", "labels", "answers", "id"}, None),
            ("split", dict, {"index", "columns", "data"}, "data"),
            ("index", dict, set("0123456789"), None),
            ("columns", dict, {"tokens", "labels", "answers", "id"}, "tokens"),
            ("values", list, None, None),
            ("table", dict, {"schema", "data"}, "data"),
        ],
    )
    def test_dataset_to_json_orient_multiproc(self, orient, container, keys, len_at, dataset):
        with io.BytesIO() as buffer:
            JsonDatasetWriter(dataset, buffer, lines=False, orient=orient, num_proc=2).write()
            buffer.seek(0)
            exported_content = load_json(buffer)
        assert isinstance(exported_content, container)
        if keys:
            if container is dict:
                assert exported_content.keys() == keys
            else:
                assert exported_content[0].keys() == keys
        else:
            assert not hasattr(exported_content, "keys") and not hasattr(exported_content[0], "keys")
        if len_at:
            assert len(exported_content[len_at]) == 10
        else:
            assert len(exported_content) == 10

    def test_dataset_to_json_orient_invalidproc(self, dataset):
        with pytest.raises(ValueError):
            with io.BytesIO() as buffer:
                JsonDatasetWriter(dataset, buffer, num_proc=0)
