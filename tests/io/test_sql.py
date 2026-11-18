import contextlib
import datetime
import os
import sqlite3
import time
import types
import unittest.mock

import numpy as np
import pyarrow as pa
import pytest

import datasets.config
from datasets import Dataset, Features, Value
from datasets.io import sql
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


def _dump(path):
    """Each table's DDL and rows: rowid, then typeof() and value of each column."""
    with contextlib.closing(sqlite3.connect(path)) as con:
        dump = {}
        for name, ddl in con.execute("SELECT name, sql FROM sqlite_master WHERE type = 'table' ORDER BY name"):
            columns = "".join(f', typeof("{c[1]}"), "{c[1]}"' for c in con.execute(f'PRAGMA table_info("{name}")'))
            dump[ddl] = con.execute(f'SELECT rowid{columns} FROM "{name}" ORDER BY rowid').fetchall()
    return dump


def _to_sql(path, dataset, grouped, setup=None, listener=None, name="dataset", **kwargs):
    """Exports with batch_size=2, grouped or with pandas only: the result or the chain of errors, and the database."""
    import sqlalchemy

    if setup:  # a table to append to
        with contextlib.closing(sqlite3.connect(path)) as con:
            con.executescript(setup)
        kwargs.setdefault("if_exists", "append")
    with contextlib.ExitStack() as stack:
        if not grouped:
            stack.enter_context(unittest.mock.patch.object(SqlDatasetWriter, "_sqlite_groups", return_value=False))
        if listener:
            sqlalchemy.event.listen(sqlalchemy.engine.Engine, "connect", listener)
            stack.callback(sqlalchemy.event.remove, sqlalchemy.engine.Engine, "connect", listener)
        try:
            result = SqlDatasetWriter(dataset, name, f"sqlite:///{path}", batch_size=2, **kwargs).write()
        except Exception as error:
            result = []
            while error is not None:
                result, error = [*result, (type(error), str(error))], error.__context__
    return result, _dump(path)


@require_sqlalchemy
def test_dataset_to_sql_grouped_writes_what_pandas_writes(tmp_path):
    n = 9
    columns = {
        "i8": pa.array([None, -128, 127] * 3, pa.int8()),
        "u32": pa.array(range(n), pa.uint32()),
        "i64": pa.array([2**53 + 1, None, 3] * 3),
        "f16": pa.array(np.array([0.1, 1.5, -2.25] * 3, dtype=np.float16)),
        "f64": [float("nan"), None, 0.1] * 3,
        "b": [True, None, False] * 3,
        "s": ["é", None, "a\x00b"] * 3,
        "ls": pa.array(["x"] * n, pa.large_string()),
        "bin": [b"\x00", None, b"z"] * 3,
        "lbin": pa.array([b"a"] * n, pa.large_binary()),
        "null": pa.nulls(n),
        "d": [datetime.date(1, 1, 1), None, datetime.date(9999, 12, 31)] * 3,
        "ts_s": pa.array([-62135596800, None, 253402300799] * 3, pa.timestamp("s")),
        "ts_ms": pa.array([0, None, 1_234_567] * 3, pa.timestamp("ms")),
        "ts_us": [datetime.datetime(2020, 1, 1, 0, 0, 0, 7), None, datetime.datetime(1, 1, 1)] * 3,
    }
    for i, dataset in enumerate([Dataset(pa.table(columns)), Dataset(pa.table(columns)).shuffle(seed=0)]):
        assert SqlDatasetWriter(dataset, "dataset", f"sqlite:///{tmp_path / 'x.sqlite'}")._sqlite_groups(index=False)
        grouped = _to_sql(tmp_path / f"grouped{i}.sqlite", dataset, True)
        assert grouped == _to_sql(tmp_path / f"pandas{i}.sqlite", dataset, False) and grouped[0] == n


_DDL = "CREATE TABLE dataset (a INTEGER {}, s TEXT);"
_CHECK = _DDL.format("CHECK (a < 6)")
_INVALID_UTF8 = pa.Array.from_buffers(  # its third string, in batch 1, is b"\xff"
    pa.string(), 5, [None, pa.py_buffer(np.arange(6, dtype=np.int32).tobytes()), pa.py_buffer(b"ab\xffde")]
)
_CASES = {  # after a failure in a group, pandas writes its batches again: today's error and rows, without duplicates
    "check fails in batch 3": {"setup": _CHECK},
    "ignored": {"setup": _DDL.format("UNIQUE ON CONFLICT IGNORE") + "INSERT INTO dataset (a) VALUES (4), (5), (7);"},
    "replace a table": {"setup": _DDL.format("") + "INSERT INTO dataset VALUES (-1, 'x');", "if_exists": "replace"},
    "autocommit": {"setup": _CHECK, "listener": lambda con, record: setattr(con, "isolation_level", None)},
    "date out of range in batch 1": {"dataset": {"a": pa.array([0, 1, 2, 253402300800 * 10**6], pa.timestamp("us"))}},
    "check fails in the group before": {  # the group is written before pandas writes batch 2: its error comes first
        "setup": "CREATE TABLE dataset (a TIMESTAMP CHECK (a < '1970-01-01 00:00:00.000002'));",
        "dataset": {"a": pa.array([0, 1, 2, 3, 253402300800 * 10**6, 5], pa.timestamp("us"))},
    },
    "invalid UTF-8 in batch 1": {"dataset": {"s": _INVALID_UTF8}},
}


@require_sqlalchemy
@pytest.mark.parametrize("case", _CASES)
def test_dataset_to_sql_grouped_errors_like_pandas(case, tmp_path):
    kwargs = dict(_CASES[case])
    dataset = Dataset.from_dict(kwargs.pop("dataset", {"a": list(range(10)), "s": [str(i) for i in range(10)]}))
    grouped = _to_sql(tmp_path / "grouped.sqlite", dataset, True, **kwargs)
    assert grouped == _to_sql(tmp_path / "pandas.sqlite", dataset, False, **kwargs)


@require_sqlalchemy
@pytest.mark.parametrize("cap, limit", [("_GROUP_ROWS", 5), ("_GROUP_BYTES", 40)])  # batches of 2 rows, 16 bytes
def test_dataset_to_sql_groups_and_pauses(cap, limit, tmp_path, monkeypatch):
    """Groups of two batches here, each but the last followed by a pause of _GROUP_PAUSE_PER_ROW per row."""
    sleeps = []
    monkeypatch.setattr(sql, "time", types.SimpleNamespace(perf_counter=time.perf_counter, sleep=sleeps.append))
    for name, value in {"_GROUP_SECONDS": 60, "_GROUP_PAUSE_PER_ROW": 1e-9, cap: limit}.items():
        monkeypatch.setattr(sql, name, value)
    dataset = Dataset.from_dict({"a": list(range(20))})
    assert SqlDatasetWriter(dataset, "t", f"sqlite:///{tmp_path / 'x.sqlite'}", batch_size=2).write() == 20
    assert [round(s * 1e9) for s in sleeps] == [4] * 4


@require_sqlalchemy
@pytest.mark.parametrize("name, column", [("", "a"), ("dataset", "")])  # pandas' error, not SQLAlchemy 2.0's
def test_dataset_to_sql_empty_names_raise_like_pandas(name, column, tmp_path):
    dataset = Dataset.from_dict({column: list(range(5))})
    grouped = _to_sql(tmp_path / "grouped.sqlite", dataset, True, name=name)
    assert grouped == _to_sql(tmp_path / "pandas.sqlite", dataset, False, name=name)


@require_sqlalchemy
def test_dataset_to_sql_without_journal_is_written_by_pandas(tmp_path):
    """With journal_mode=OFF (set by a connect listener) a rollback is undefined: pandas writes every batch."""
    dataset, batch_sql = Dataset.from_dict({"a": list(range(10))}), SqlDatasetWriter._batch_sql
    kwargs = {"listener": lambda con, _: con.execute("PRAGMA journal_mode=OFF")}
    with unittest.mock.patch.object(SqlDatasetWriter, "_batch_sql", autospec=True, side_effect=batch_sql) as spy:
        grouped = _to_sql(tmp_path / "grouped.sqlite", dataset, True, **kwargs)
    assert grouped == _to_sql(tmp_path / "pandas.sqlite", dataset, False, **kwargs)
    assert [call.args[1][0] for call in spy.call_args_list] == [0, 2, 4, 6, 8]


@require_sqlalchemy
def test_dataset_to_sql_large_batches_are_written_by_pandas(tmp_path, monkeypatch):
    monkeypatch.setattr(sql, "_GROUP_BYTES", 8)  # smaller than a batch of two int64
    dataset = Dataset.from_dict({"a": list(range(10))})
    with unittest.mock.patch.object(sql, "_sqlite_rows", wraps=sql._sqlite_rows) as convert:
        grouped = _to_sql(tmp_path / "grouped.sqlite", dataset, True)
    assert grouped == _to_sql(tmp_path / "pandas.sqlite", dataset, False) and not convert.called


@require_sqlalchemy
@pytest.mark.parametrize(
    "columns, con, kwargs",
    [
        ({"a": pa.array([1], pa.uint64())}, None, {}),
        ({"a": pa.array([1], pa.timestamp("ns"))}, None, {}),
        ({"a": [1]}, None, {"num_proc": 2}),
        ({"a": [1]}, None, {"index": True}),
        ({"a": [1]}, None, {"dtype": {"a": "TEXT"}}),
        ({"a": [1]}, "sqlite+aiosqlite:///x.sqlite", {}),
        ({"a": [1]}, "sqlite:///:memory:", {}),
        ({"a": [1]}, "a URL object", {}),
        ({"a": [1]}, "pandas 1", {}),  # it binds datetimes in nanoseconds
    ],
)
def test_dataset_to_sql_not_grouped(columns, con, kwargs, tmp_path, monkeypatch):
    """These exports keep today's path: pandas writes every batch."""
    import sqlalchemy

    url = f"sqlite:///{tmp_path / 'x.sqlite'}"
    if con == "pandas 1":
        monkeypatch.setattr(datasets.config, "PANDAS_VERSION", types.SimpleNamespace(major=1))
    url = sqlalchemy.engine.make_url(url) if con == "a URL object" else url if con in (None, "pandas 1") else con
    writer = SqlDatasetWriter(Dataset(pa.table(columns)), "dataset", url, **kwargs)
    assert not writer._sqlite_groups(index=writer.to_sql_kwargs.pop("index", False))
