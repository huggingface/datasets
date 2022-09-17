import contextlib
import os
from sqlite3 import connect

import pandas as pd
import pytest

from datasets import Dataset, Features, Value
from datasets.io.sql import SqlDatasetReader, SqlDatasetWriter

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


SQLITE_TABLE_NAME = "TABLE_NAME"


def _check_sql_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_sql_keep_in_memory(keep_in_memory, sql_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = SqlDatasetReader(
            sql_path, table_name=SQLITE_TABLE_NAME, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        ).read()
    _check_sql_dataset(dataset, expected_features)


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
def test_dataset_from_sql_features(features, sql_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = SqlDatasetReader(sql_path, table_name=SQLITE_TABLE_NAME, features=features, cache_dir=cache_dir).read()
    _check_sql_dataset(dataset, expected_features)


@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_sql_path_type(path_type, sql_path, tmp_path):
    if issubclass(path_type, str):
        path = sql_path
    elif issubclass(path_type, list):
        path = [sql_path]
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = SqlDatasetReader(path, table_name=SQLITE_TABLE_NAME, cache_dir=cache_dir).read()
    _check_sql_dataset(dataset, expected_features)


def iter_sql_file(sql_path):
    with contextlib.closing(connect(sql_path)) as conn:
        return pd.read_sql(f"SELECT * FROM {SQLITE_TABLE_NAME}", conn).drop("index", axis=1, errors="ignore")


def test_dataset_to_sql(sql_path, tmp_path):
    cache_dir = tmp_path / "cache"
    output_sql = os.path.join(cache_dir, "tmp.sql")
    dataset = SqlDatasetReader(sql_path, table_name=SQLITE_TABLE_NAME, cache_dir=cache_dir).read()
    SqlDatasetWriter(dataset, output_sql, table_name=SQLITE_TABLE_NAME, index=False, num_proc=1).write()

    original_sql = iter_sql_file(sql_path)
    expected_sql = iter_sql_file(output_sql)

    for row1, row2 in zip(original_sql, expected_sql):
        assert row1 == row2


def test_dataset_to_sql_multiproc(sql_path, tmp_path):
    cache_dir = tmp_path / "cache"
    output_sql = os.path.join(cache_dir, "tmp.sql")
    dataset = SqlDatasetReader(sql_path, table_name=SQLITE_TABLE_NAME, cache_dir=cache_dir).read()
    SqlDatasetWriter(dataset, output_sql, table_name=SQLITE_TABLE_NAME, index=False, num_proc=2).write()

    original_sql = iter_sql_file(sql_path)
    expected_sql = iter_sql_file(output_sql)

    for row1, row2 in zip(original_sql, expected_sql):
        assert row1 == row2


def test_dataset_to_sql_invalidproc(sql_path, tmp_path):
    cache_dir = tmp_path / "cache"
    output_sql = os.path.join(cache_dir, "tmp.sql")
    dataset = SqlDatasetReader(sql_path, table_name=SQLITE_TABLE_NAME, cache_dir=cache_dir).read()
    with pytest.raises(ValueError):
        SqlDatasetWriter(dataset, output_sql, table_name=SQLITE_TABLE_NAME, index=False, num_proc=0)
