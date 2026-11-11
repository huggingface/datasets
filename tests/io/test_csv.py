import csv
import io
import os

import fsspec
import pyarrow as pa
import pytest

from datasets import Dataset, DatasetDict, Features, NamedSplit, Value, load_dataset
from datasets.io.csv import CsvDatasetReader, CsvDatasetWriter

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


@pytest.mark.parametrize("num_proc", [None, 2])
@pytest.mark.parametrize("header", [True, False, ["prompt", "reward"]])
def test_dataset_to_csv_empty(num_proc, header):
    dataset = Dataset.from_dict(
        {"text": [], "label": []}, features=Features({"text": Value("string"), "label": Value("int64")})
    )
    with io.BytesIO() as buffer:
        written = dataset.to_csv(buffer, num_proc=num_proc, header=header)
        content = buffer.getvalue()
    assert written == len(content)
    expected_header = ["text", "label"] if header is True else header
    assert list(csv.reader(io.StringIO(content.decode("utf-8")))) == ([expected_header] if header else [])


def _check_csv_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_csv_keep_in_memory(keep_in_memory, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = CsvDatasetReader(csv_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
    _check_csv_dataset(dataset, expected_features)


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
def test_dataset_from_csv_features(features, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    # CSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = CsvDatasetReader(csv_path, features=features, cache_dir=cache_dir).read()
    _check_csv_dataset(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_csv_split(split, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    dataset = CsvDatasetReader(csv_path, cache_dir=cache_dir, split=split).read()
    _check_csv_dataset(dataset, expected_features)
    assert dataset.split == split if split else "train"


@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_csv_path_type(path_type, csv_path, tmp_path):
    if issubclass(path_type, str):
        path = csv_path
    elif issubclass(path_type, list):
        path = [csv_path]
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    dataset = CsvDatasetReader(path, cache_dir=cache_dir).read()
    _check_csv_dataset(dataset, expected_features)


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
def test_csv_datasetdict_reader_keep_in_memory(keep_in_memory, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = CsvDatasetReader({"train": csv_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
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
def test_csv_datasetdict_reader_features(features, csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    # CSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = CsvDatasetReader({"train": csv_path}, features=features, cache_dir=cache_dir).read()
    _check_csv_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_csv_datasetdict_reader_split(split, csv_path, tmp_path):
    if split:
        path = {split: csv_path}
    else:
        path = {"train": csv_path, "test": csv_path}
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    dataset = CsvDatasetReader(path, cache_dir=cache_dir).read()
    _check_csv_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())


def iter_csv_file(csv_path):
    with open(csv_path, encoding="utf-8") as csvfile:
        yield from csv.reader(csvfile)


def test_dataset_to_csv(csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    output_csv = os.path.join(cache_dir, "tmp.csv")
    dataset = CsvDatasetReader({"train": csv_path}, cache_dir=cache_dir).read()
    CsvDatasetWriter(dataset["train"], output_csv, num_proc=1).write()

    original_csv = iter_csv_file(csv_path)
    expected_csv = iter_csv_file(output_csv)

    for row1, row2 in zip(original_csv, expected_csv):
        assert row1 == row2


def test_dataset_to_csv_multiproc(csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    output_csv = os.path.join(cache_dir, "tmp.csv")
    dataset = CsvDatasetReader({"train": csv_path}, cache_dir=cache_dir).read()
    CsvDatasetWriter(dataset["train"], output_csv, num_proc=2).write()

    original_csv = iter_csv_file(csv_path)
    expected_csv = iter_csv_file(output_csv)

    for row1, row2 in zip(original_csv, expected_csv):
        assert row1 == row2


def test_dataset_to_csv_invalidproc(csv_path, tmp_path):
    cache_dir = tmp_path / "cache"
    output_csv = os.path.join(cache_dir, "tmp.csv")
    dataset = CsvDatasetReader({"train": csv_path}, cache_dir=cache_dir).read()
    with pytest.raises(ValueError):
        CsvDatasetWriter(dataset["train"], output_csv, num_proc=0)


def test_dataset_to_csv_fsspec(dataset, mockfs):
    dataset_path = "mock://my_dataset.csv"
    writer = CsvDatasetWriter(dataset, dataset_path, storage_options=mockfs.storage_options)
    assert writer.write() > 0
    assert mockfs.isfile(dataset_path)

    with fsspec.open(dataset_path, "rb", **mockfs.storage_options) as f:
        assert f.read()


@pytest.mark.parametrize(
    "dtype, big",
    [("int64", 9007199254740993), ("uint64", 9007199254740993), ("int32", 2147483647)],
)
def test_dataset_to_csv_preserves_nullable_int(dtype, big, tmp_path):
    # A nullable integer column must be written as integers, not float64-coerced values.
    # batch.to_pandas() defaults to integer_object_nulls=False, casting an integer column
    # that contains a null to float64 and losing precision beyond 2**53.
    dataset = Dataset.from_dict({"a": [big, None, 5]}, features=Features({"a": Value(dtype)}))
    output_csv = os.path.join(tmp_path, "out.csv")
    CsvDatasetWriter(dataset, output_csv, num_proc=1).write()
    with open(output_csv, newline="") as f:
        rows = list(csv.DictReader(f))
    assert [row["a"] for row in rows] == [str(big), "", "5"]


@pytest.mark.parametrize(
    "dtype, values",
    [
        ("int64", [-9223372036854775808, None, 9007199254740993, 9223372036854775807]),
        ("uint64", [18446744073709551615, None, 9007199254740993, 0]),
        ("bool", [True, None, False]),
        ("string", ["001", None, "003"]),
    ],
)
@pytest.mark.parametrize("chunksize", [1, 10])
@pytest.mark.parametrize("reader", ["from_csv", "load_dataset"])
def test_dataset_csv_nullable_scalar_roundtrip(dtype, values, chunksize, reader, tmp_path):
    features = Features({"value": Value(dtype), "text": Value("string")})
    expected = {"value": values, "text": ["row"] * len(values)}
    dataset = Dataset(pa.Table.from_pydict(expected, schema=features.arrow_schema))
    path = tmp_path / "nullable.csv"
    dataset.to_csv(path)
    kwargs = {"features": features, "chunksize": chunksize, "cache_dir": str(tmp_path / "cache")}
    if reader == "from_csv":
        result = Dataset.from_csv(str(path), **kwargs)
    else:
        result = load_dataset("csv", data_files=str(path), split="train", **kwargs)
    assert result.features == features
    assert result.to_dict() == expected
    assert result.data.schema == dataset.data.schema
    assert result.data.column("value").null_count == 1


@pytest.mark.parametrize("dtype", ["string", "large_string"])
@pytest.mark.parametrize("engine", ["c", "python"])
@pytest.mark.parametrize("chunksize", [1, 10])
@pytest.mark.parametrize("reader", ["from_csv", "load_dataset"])
@pytest.mark.parametrize("with_null", [False, True])
def test_dataset_from_csv_declared_strings(dtype, engine, chunksize, reader, with_null, tmp_path):
    path = tmp_path / "strings.csv"
    # Hand-authored cells must retain their spelling, including in a wholly numeric column.
    path.write_text('value,tag\n"001",row\n' + (",row\n" if with_null else "") + '"003",row\n')
    values = ["001", None, "003"] if with_null else ["001", "003"]
    expected = {"tag": ["row"] * len(values), "value": values}
    features = Features({"tag": Value("string"), "value": Value(dtype)})
    kwargs = {
        "features": features,
        "engine": engine,
        "chunksize": chunksize,
        "cache_dir": str(tmp_path / "cache"),
    }
    if reader == "from_csv":
        result = Dataset.from_csv(str(path), **kwargs)
    else:
        result = load_dataset("csv", data_files=str(path), split="train", **kwargs)
    assert result.features == features
    assert result.to_dict() == expected
    assert result.data.schema == features.arrow_schema
    assert result.data.column("value").is_null().to_pylist() == [value is None for value in values]
