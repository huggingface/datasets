import io
import json

import fsspec
import pyarrow as pa
import pytest

from datasets import Dataset, DatasetDict, Features, Json, List, NamedSplit, Value
from datasets.io.json import JsonDatasetReader, JsonDatasetWriter

from ..fixtures.files import DATA_MIXED_TYPES
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


def test_dataset_from_json_with_missing_fields(jsonl_missing_fields_path, tmp_path):
    expected_features = {"col_1": Value("int64"), "col_2": Value("int64"), "col_3": Value("int64")}

    cache_dir = tmp_path / "cache"
    dataset = JsonDatasetReader(jsonl_missing_fields_path, cache_dir=cache_dir).read()
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 2
    assert dataset.num_columns == 3
    assert dataset.features == expected_features
    assert list(dataset) == [
        {"col_1": 1, "col_2": 2, "col_3": None},
        {"col_1": 1, "col_2": None, "col_3": 3},
    ]


def test_dataset_from_json_with_mixed_types(jsonl_mixed_types_path, tmp_path):
    expected_features = {"col_1": Json(), "col_2": Json(), "col_3": List(Json())}

    cache_dir = tmp_path / "cache"
    dataset = JsonDatasetReader(jsonl_mixed_types_path, cache_dir=cache_dir).read()
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 3
    assert dataset.num_columns == 3
    assert dataset.features == expected_features
    assert list(dataset) == DATA_MIXED_TYPES


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_json_split(split, jsonl_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = JsonDatasetReader(jsonl_path, cache_dir=cache_dir, split=split).read()
    _check_json_dataset(dataset, expected_features)
    assert dataset.split == split if split else "train"


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
            ("split", dict, {"columns", "data"}, "data"),
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
            ("split", dict, {"columns", "data"}, "data"),
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

    @pytest.mark.parametrize("compression, extension", [("gzip", "gz"), ("bz2", "bz2"), ("xz", "xz")])
    def test_dataset_to_json_compression(self, shared_datadir, tmp_path_factory, extension, compression, dataset):
        path = tmp_path_factory.mktemp("data") / f"test.json.{extension}"
        original_path = str(shared_datadir / f"test_file.json.{extension}")
        JsonDatasetWriter(dataset, path, compression=compression).write()

        with fsspec.open(path, "rb", compression="infer") as f:
            exported_content = f.read()
        with fsspec.open(original_path, "rb", compression="infer") as f:
            original_content = f.read()
        assert exported_content == original_content

    def test_dataset_to_json_fsspec(self, dataset, mockfs):
        dataset_path = "mock://my_dataset.json"
        writer = JsonDatasetWriter(dataset, dataset_path, storage_options=mockfs.storage_options)
        assert writer.write() > 0
        assert mockfs.isfile(dataset_path)

        with fsspec.open(dataset_path, "rb", **mockfs.storage_options) as f:
            assert f.read()

    @pytest.mark.parametrize(
        "dtype, big",
        [("int64", 9007199254740993), ("uint64", 9007199254740993), ("int32", 2147483647)],
    )
    def test_dataset_to_json_preserves_nullable_int(self, dtype, big):
        # A nullable integer column must be written as JSON integers. batch.to_pandas()
        # defaults to integer_object_nulls=False, which casts an integer column that
        # contains a null to float64, dropping the integer type and any precision beyond
        # 2**53 (9007199254740993 becomes 9007199254740992.0).
        dataset = Dataset.from_dict({"a": [big, None, 5]}, features=Features({"a": Value(dtype)}))
        with io.BytesIO() as buffer:
            JsonDatasetWriter(dataset, buffer, lines=True).write()
            buffer.seek(0)
            rows = load_json_lines(buffer)
        assert [row["a"] for row in rows] == [big, None, 5]
        assert all(isinstance(row["a"], int) for row in rows if row["a"] is not None)

    @pytest.mark.parametrize("num_proc", [None, 2])
    @pytest.mark.parametrize(
        "orient, lines, batch_size",
        [("records", True, 2), ("records", False, 10), ("split", False, 10), ("values", False, 10)],
    )
    def test_dataset_to_json_selected_rows(self, num_proc, orient, lines, batch_size):
        features = Features(
            {"id": Value("int64"), "amount": Value("uint64"), "answers": List(Value("string")), "payload": Json()}
        )
        records = [
            {
                "id": i,
                "amount": None if i == 1 else 2**54 + i,
                "answers": [f"answer {i}", "中文"],
                "payload": {"nested": [i, None]},
            }
            for i in range(5)
        ]
        original = Dataset.from_list(records, features=features)
        chunked = pa.Table.from_batches(original.data.table.to_batches(max_chunksize=2))
        selected_indices = [4, 1, 4, 0, 3]
        selected = Dataset(chunked, info=original.info).select(selected_indices)
        reference = Dataset.from_list([records[i] for i in selected_indices], features=features)
        options = {
            "num_proc": num_proc,
            "orient": orient,
            "lines": lines,
            "batch_size": batch_size,
            "force_ascii": False,
        }
        with io.BytesIO() as actual, io.BytesIO() as expected:
            written = selected.to_json(actual, **options)
            reference.to_json(expected, **options)
            assert actual.getvalue() == expected.getvalue()
            assert written == len(actual.getvalue())

    @pytest.mark.parametrize("error", [pa.ArrowInvalid, pa.ArrowNotImplementedError])
    def test_dataset_to_json_when_chunks_cannot_be_combined(self, monkeypatch, error):
        # A failed optional Arrow concatenation must not prevent exporting a valid batch.
        dataset = Dataset.from_dict({"value": [2**54 + 1, None, 3]}).select([2, 0, 1])
        table = pa.table({"value": pa.array([3, 2**54 + 1, None], type=pa.int64())})

        class UncombinableTable:
            def combine_chunks(self):
                raise error("cannot combine this nested array")

            def to_pandas(self, **kwargs):
                return table.to_pandas(**kwargs)

        monkeypatch.setattr("datasets.io.json.query_table", lambda **kwargs: UncombinableTable())
        with io.BytesIO() as buffer:
            dataset.to_json(buffer)
            buffer.seek(0)
            assert load_json_lines(buffer) == [{"value": 3}, {"value": 2**54 + 1}, {"value": None}]
