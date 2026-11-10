import contextlib
import multiprocessing
import os
import sqlite3
import types

import pytest

import datasets.config
import datasets.io.sql
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


def _table_rows(sqlite_path):
    with contextlib.closing(sqlite3.connect(sqlite_path)) as con:
        if con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='dataset'").fetchone() is None:
            return None
        return sorted(con.execute("SELECT a FROM dataset").fetchall())


@pytest.fixture
def rows_when_workers_get_batches(monkeypatch):
    """Records the table's rows each time the writer calls pool.imap, i.e. just before batches go to the workers."""

    def watch(sqlite_path):
        records = []

        def pool(*args, **kwargs):
            real_pool = multiprocessing.Pool(*args, **kwargs)
            real_imap = real_pool.imap

            def imap(*imap_args, **imap_kwargs):
                records.append(_table_rows(sqlite_path))
                return real_imap(*imap_args, **imap_kwargs)

            real_pool.imap = imap
            return real_pool

        monkeypatch.setattr(datasets.io.sql, "multiprocessing", types.SimpleNamespace(Pool=pool))
        return records

    return watch


@require_sqlalchemy
@pytest.mark.parametrize("if_exists", [None, "replace"])
def test_dataset_to_sql_multiproc_creates_the_table_before_the_workers_append(
    if_exists, tmp_path, rows_when_workers_get_batches, set_sqlalchemy_silence_uber_warning
):
    # With num_proc > 1 the batches run in a pool, and a later batch (if_exists="append") could
    # reach the database before the first one. The first one then either raised "table already
    # exists" (default if_exists="fail") or dropped the rows already appended (if_exists="replace").
    # The first batch must have applied if_exists before the later batches are handed to the workers.
    output_sqlite_path = os.path.join(tmp_path, "out.sqlite")
    if if_exists == "replace":
        with contextlib.closing(sqlite3.connect(output_sqlite_path)) as con, con:
            con.execute("CREATE TABLE dataset (a INTEGER)")
            con.execute("INSERT INTO dataset VALUES (-1)")
    records = rows_when_workers_get_batches(output_sqlite_path)
    to_sql_kwargs = {"if_exists": if_exists} if if_exists else {}
    dataset = Dataset.from_dict({"a": list(range(6))})
    writer = SqlDatasetWriter(
        dataset, "dataset", "sqlite:///" + output_sqlite_path, batch_size=2, num_proc=2, **to_sql_kwargs
    )
    assert writer.write() == 6
    assert records == [[(0,), (1,)]]
    assert _table_rows(output_sqlite_path) == [(i,) for i in range(6)]


@require_sqlalchemy
def test_dataset_to_sql_multiproc_leaves_an_existing_table_untouched_with_if_exists_fail(
    tmp_path, rows_when_workers_get_batches, set_sqlalchemy_silence_uber_warning
):
    output_sqlite_path = os.path.join(tmp_path, "out.sqlite")
    with contextlib.closing(sqlite3.connect(output_sqlite_path)) as con, con:
        con.execute("CREATE TABLE dataset (a INTEGER)")
        con.execute("INSERT INTO dataset VALUES (-1)")
    records = rows_when_workers_get_batches(output_sqlite_path)
    dataset = Dataset.from_dict({"a": list(range(6))})
    writer = SqlDatasetWriter(dataset, "dataset", "sqlite:///" + output_sqlite_path, batch_size=2, num_proc=2)
    with pytest.raises(ValueError, match="already exists"):
        writer.write()
    assert records == []
    assert _table_rows(output_sqlite_path) == [(-1,)]


@require_sqlalchemy
def test_dataset_to_sql_invalidproc(sqlite_path, tmp_path, set_sqlalchemy_silence_uber_warning):
    cache_dir = tmp_path / "cache"
    output_sqlite_path = os.path.join(cache_dir, "tmp.sql")
    dataset = SqlDatasetReader("dataset", "sqlite:///" + sqlite_path, cache_dir=cache_dir).read()
    with pytest.raises(ValueError):
        SqlDatasetWriter(dataset, "dataset", "sqlite:///" + output_sqlite_path, num_proc=0).write()


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
