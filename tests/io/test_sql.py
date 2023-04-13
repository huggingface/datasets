import contextlib
import os
import sqlite3

import pytest

from datasets import Dataset, Features, Value
from datasets.io.sql import SqlDatasetReader, SqlDatasetWriter

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases, require_sqlalchemy


def _check_sql_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@require_sqlalchemy
@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_sql_keep_in_memory(keep_in_memory, sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = SqlDatasetReader(
            "dataset", "sqlite:///" + sqlite_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        ).read()
    _check_sql_dataset(dataset, expected_features)


@require_sqlalchemy
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
def test_dataset_from_sql_features(features, sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = SqlDatasetReader("dataset", "sqlite:///" + sqlite_path, features=features, cache_dir=cache_dir).read()
    _check_sql_dataset(dataset, expected_features)


def iter_sql_file(sqlite_path):
    with contextlib.closing(sqlite3.connect(sqlite_path)) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM dataset")
        for row in cur:
            yield row


@require_sqlalchemy
def test_dataset_to_sql(sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning):
    cache_dir = tmp_path / "cache"
    output_sqlite_path = os.path.join(cache_dir, "tmp.sql")
    dataset = SqlDatasetReader("dataset", "sqlite:///" + sqlite_path, cache_dir=cache_dir).read()
    SqlDatasetWriter(dataset, "dataset", "sqlite:///" + output_sqlite_path, num_proc=1).write()

    original_sql = iter_sql_file(sqlite_path)
    expected_sql = iter_sql_file(output_sqlite_path)

    for row1, row2 in zip(original_sql, expected_sql):
        assert row1 == row2


@require_sqlalchemy
def test_dataset_to_sql_multiproc(sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning):
    cache_dir = tmp_path / "cache"
    output_sqlite_path = os.path.join(cache_dir, "tmp.sql")
    dataset = SqlDatasetReader("dataset", "sqlite:///" + sqlite_path, cache_dir=cache_dir).read()
    SqlDatasetWriter(dataset, "dataset", "sqlite:///" + output_sqlite_path, num_proc=2).write()

    original_sql = iter_sql_file(sqlite_path)
    expected_sql = iter_sql_file(output_sqlite_path)

    for row1, row2 in zip(original_sql, expected_sql):
        assert row1 == row2


@require_sqlalchemy
def test_dataset_to_sql_invalidproc(sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning):
    cache_dir = tmp_path / "cache"
    output_sqlite_path = os.path.join(cache_dir, "tmp.sql")
    dataset = SqlDatasetReader("dataset", "sqlite:///" + sqlite_path, cache_dir=cache_dir).read()
    with pytest.raises(ValueError):
        SqlDatasetWriter(dataset, "dataset", "sqlite:///" + output_sqlite_path, num_proc=0).write()
