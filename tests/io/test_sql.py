import contextlib
import os
import sqlite3

import pytest

import datasets.config
from datasets import Dataset, Features, Value
from datasets.io.sql import SqlDatasetReader, SqlDatasetWriter

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases, require_sqlalchemy


STRING_FROM_PANDAS = "large_string" if datasets.config.PANDAS_VERSION.major >= 3 else "string"


def _check_sql_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


def _insert_or_ignore_sqlalchemy(table, con, keys, data_iter):
    from sqlalchemy.dialects.sqlite import insert

    rows = [dict(zip(keys, row)) for row in data_iter]
    statement = insert(table.table).values(rows).on_conflict_do_nothing()
    return con.execute(statement).rowcount


@require_sqlalchemy
@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_sql_keep_in_memory(keep_in_memory, sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": STRING_FROM_PANDAS, "col_2": "int64", "col_3": "float64"}
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
    default_expected_features = {"col_1": STRING_FROM_PANDAS, "col_2": "int64", "col_3": "float64"}
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


@pytest.mark.parametrize(
    "existing_values, return_count, expected_written",
    [([], True, 4), ([1, 2], True, 2), ([1, 2, 3, 4], True, 0), ([1, 2, 3, 4], False, 4)],
    ids=["all-inserted", "some-ignored", "all-ignored", "unknown-count"],
)
def test_dataset_to_sql_returns_method_rowcount(existing_values, return_count, expected_written):
    dataset = Dataset.from_dict({"value": [1, 2, 3, 4]})

    def insert_or_ignore(_table, cursor, _keys, data_iter):
        cursor.executemany("INSERT OR IGNORE INTO items (value) VALUES (?)", data_iter)
        return cursor.rowcount if return_count else None

    with contextlib.closing(sqlite3.connect(":memory:")) as con:
        con.execute("CREATE TABLE items (value INTEGER PRIMARY KEY)")
        con.executemany("INSERT INTO items (value) VALUES (?)", [(value,) for value in existing_values])

        written = dataset.to_sql("items", con, batch_size=2, if_exists="append", method=insert_or_ignore)

        assert written == expected_written
        assert con.execute("SELECT value FROM items ORDER BY value").fetchall() == [(1,), (2,), (3,), (4,)]


@require_sqlalchemy
def test_dataset_to_sql_returns_zero_with_multiproc(tmp_path):
    path = tmp_path / "counts.sqlite"
    with contextlib.closing(sqlite3.connect(path)) as con:
        con.execute("CREATE TABLE items (value INTEGER PRIMARY KEY)")
        con.executemany("INSERT INTO items (value) VALUES (?)", [(1,), (2,), (3,), (4,)])
        con.commit()

    dataset = Dataset.from_dict({"value": [1, 2, 3, 4]})
    written = dataset.to_sql(
        "items",
        f"sqlite:///{path.as_posix()}",
        batch_size=2,
        num_proc=2,
        if_exists="append",
        method=_insert_or_ignore_sqlalchemy,
    )

    with contextlib.closing(sqlite3.connect(path)) as con:
        assert con.execute("SELECT value FROM items ORDER BY value").fetchall() == [(1,), (2,), (3,), (4,)]
    assert written == 0


@require_sqlalchemy
@pytest.mark.parametrize("dtype, big", [("int64", 9007199254740993), ("uint64", 9007199254740993)])
def test_dataset_to_sql_preserves_nullable_int(dtype, big, tmp_path, set_sqlalchemy_silence_uber_warning):
    # A nullable integer column must land in an INTEGER SQL column with its exact value.
    # batch.to_pandas() defaults to integer_object_nulls=False, casting an integer column
    # that contains a null to float64, so the value is stored as REAL and precision beyond
    # 2**53 is lost.
    dataset = Dataset.from_dict({"a": [big, None, 5]}, features=Features({"a": Value(dtype)}))
    output_sqlite_path = os.path.join(tmp_path, "tmp.sql")
    SqlDatasetWriter(dataset, "dataset", "sqlite:///" + output_sqlite_path, num_proc=1).write()
    with contextlib.closing(sqlite3.connect(output_sqlite_path)) as con:
        rows = con.execute("SELECT a, typeof(a) FROM dataset").fetchall()
    assert rows == [(big, "integer"), (None, "null"), (5, "integer")]
