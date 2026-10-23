import contextlib
import os
import sqlite3
from collections import UserDict
from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

import datasets.config
from datasets import Dataset, Features, Value
from datasets.io.sql import SqlDatasetReader, SqlDatasetWriter

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases, require_sqlalchemy


STRING_FROM_PANDAS = "large_string" if datasets.config.PANDAS_VERSION.major >= 3 else "string"


@pytest.fixture
def sql_items(tmp_path):
    import sqlalchemy as sa

    uri = "sqlite:///" + str(tmp_path / "items.db")
    engine = sa.create_engine(uri)
    items = sa.Table("items", sa.MetaData(), sa.Column("id", sa.Integer, primary_key=True))
    items.metadata.create_all(engine)
    try:
        with engine.begin() as connection:
            connection.execute(items.insert(), [{"id": i} for i in range(1, 5)])
        yield uri, items
    finally:
        engine.dispose()


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


@require_sqlalchemy
@pytest.mark.parametrize(
    "query_kind,reverse,chunksize",
    [
        ("where", False, None),
        ("limit", False, None),
        ("limit", True, None),
        ("offset", False, None),
        ("in", False, 2),
        ("in", True, 2),
        ("tuple_in", False, None),
        ("literal_execute", False, None),
    ],
)
def test_dataset_from_sql_bound_parameters(query_kind, reverse, chunksize, sql_items, tmp_path):
    import sqlalchemy as sa

    uri, items = sql_items
    query = sa.select(items).order_by(items.c.id)
    if query_kind == "where":
        queries = [query.where(items.c.id == value) for value in (1, 2)]
        expected_ids = [[1], [2]]
    elif query_kind == "limit":
        queries = [query.limit(value) for value in (1, 2)]
        expected_ids = [[1], [1, 2]]
    elif query_kind == "offset":
        queries = [query.limit(2).offset(value) for value in (0, 1)]
        expected_ids = [[1, 2], [2, 3]]
    elif query_kind == "in":
        queries = [query.where(items.c.id.in_(values)) for values in ([1], [2, 3])]
        expected_ids = [[1], [2, 3]]
    elif query_kind == "tuple_in":
        queries = [query.where(sa.tuple_(items.c.id, items.c.id).in_(values)) for values in ([(1, 1)], [(2, 2)])]
        expected_ids = [[1], [2]]
    else:
        queries = [query.where(items.c.id == sa.bindparam("id", value, literal_execute=True)) for value in (1, 2)]
        expected_ids = [[1], [2]]
    if reverse:
        queries.reverse()
        expected_ids.reverse()

    # Different queries must not reuse one another's cached rows (#8877).
    first = Dataset.from_sql(queries[0], uri, cache_dir=tmp_path / "cache", chunksize=chunksize)
    second = Dataset.from_sql(queries[1], uri, cache_dir=tmp_path / "cache", chunksize=chunksize)
    assert first.to_dict() == {"id": expected_ids[0]}
    assert second.to_dict() == {"id": expected_ids[1]}
    assert first.cache_files != second.cache_files
    assert first._fingerprint != second._fingerprint


@require_sqlalchemy
def test_dataset_from_sql_equivalent_queries_reuse_cache(sql_items, tmp_path):
    import sqlalchemy as sa

    uri, items = sql_items

    def read():
        query = sa.select(items).where(items.c.id > 1).where(items.c.id.in_([2, 3])).order_by(items.c.id)
        return Dataset.from_sql(query, uri, cache_dir=tmp_path / "cache")

    first = read()
    # Rebuild the statement so SQLAlchemy object identities cannot determine the cache key.
    with patch("datasets.packaged_modules.sql.sql.pd.read_sql", side_effect=AssertionError("cache miss")):
        second = read()
    assert first.to_dict() == second.to_dict() == {"id": [2, 3]}
    assert first.cache_files == second.cache_files
    assert first._fingerprint == second._fingerprint


@require_sqlalchemy
@pytest.mark.parametrize("query_kind", ["selectable", "string"])
def test_dataset_from_sql_explicit_params(query_kind, sql_items, tmp_path):
    import sqlalchemy as sa

    uri, items = sql_items
    query = (
        sa.select(items).where(items.c.id == sa.bindparam("id", 4))
        if query_kind == "selectable"
        else "SELECT id FROM items WHERE id = :id"
    )
    # SQLAlchemy accepts parameter mappings beyond plain dictionaries.
    params = UserDict(id=1) if query_kind == "selectable" else {"id": 1}
    first = Dataset.from_sql(query, uri, cache_dir=tmp_path / "cache", params=params)
    second = Dataset.from_sql(query, uri, cache_dir=tmp_path / "cache", params=type(params)(id=2))
    assert first.to_dict() == {"id": [1]}
    assert second.to_dict() == {"id": [2]}
    assert first.cache_files != second.cache_files
    assert params == {"id": 1}
    if query_kind == "selectable":
        # An overridden default must not prevent reuse of the effective query's cache.
        query = sa.select(items).where(items.c.id == sa.bindparam("id", 3))
        with patch("datasets.packaged_modules.sql.sql.pd.read_sql", side_effect=AssertionError("cache miss")):
            repeated = Dataset.from_sql(query, uri, cache_dir=tmp_path / "cache", params=params)
        assert repeated.to_dict() == first.to_dict()


@require_sqlalchemy
def test_dataset_from_sql_bound_and_explicit_params(sql_items, tmp_path):
    import sqlalchemy as sa

    uri, items = sql_items
    datasets = [
        Dataset.from_sql(
            sa.select(items).where(items.c.id == value).where(items.c.id > sa.bindparam("minimum")),
            uri,
            cache_dir=tmp_path / "cache",
            params={"minimum": 0},
        )
        for value in (1, 2)
    ]
    assert [dataset.to_dict() for dataset in datasets] == [{"id": [1]}, {"id": [2]}]


@require_sqlalchemy
def test_dataset_from_sql_callable_parameters(sql_items, tmp_path):
    import sqlalchemy as sa

    uri, items = sql_items
    values = iter([1, 2])
    query = sa.select(items).where(items.c.id == sa.bindparam("id", callable_=lambda: next(values)))
    first = Dataset.from_sql(query, uri, cache_dir=tmp_path / "cache")
    second = Dataset.from_sql(query, uri, cache_dir=tmp_path / "cache")
    assert first.to_dict() == {"id": [1]}
    assert second.to_dict() == {"id": [2]}
    # Cache identity must not evaluate the callable in addition to SQL execution.
    assert next(values, None) is None


@require_sqlalchemy
def test_dataset_from_sql_explicit_params_override_callable(sql_items, tmp_path):
    import sqlalchemy as sa

    uri, items = sql_items
    value = Mock(side_effect=AssertionError("overridden callable was evaluated"))
    query = sa.select(items).where(items.c.id == sa.bindparam("id", callable_=value))
    dataset = Dataset.from_sql(query, uri, cache_dir=tmp_path / "cache", params={"id": 2})
    assert dataset.to_dict() == {"id": [2]}
    with patch("datasets.packaged_modules.sql.sql.pd.read_sql", side_effect=AssertionError("cache miss")):
        repeated = Dataset.from_sql(query, uri, cache_dir=tmp_path / "cache", params={"id": 2})
    assert repeated.to_dict() == {"id": [2]}


@require_sqlalchemy
@pytest.mark.parametrize(
    "sql_type,values,explicit",
    [
        ("DateTime", [datetime(2024, 1, 1), datetime(2024, 1, 2)], False),
        ("Numeric", [Decimal("1.25"), Decimal("2.50")], False),
        ("LargeBinary", [memoryview(b"\x00\xff"), memoryview(b"\x00\xfe")], False),
        ("LargeBinary", [memoryview(b"\x00\xff"), memoryview(b"\x00\xfe")], True),
    ],
)
def test_dataset_from_sql_typed_bound_parameters(sql_type, values, explicit, tmp_path):
    import sqlalchemy as sa

    def read(value):
        bound = sa.bindparam("value", None if explicit else value, type_=getattr(sa, sql_type)())
        params = {"value": value} if explicit else None
        return Dataset.from_sql(
            sa.select(bound.label("value")),
            "sqlite://",
            cache_dir=tmp_path / "cache",
            params=params,
            coerce_float=False,
        )

    datasets = [read(value) for value in values]
    expected = [bytes(value) if isinstance(value, memoryview) else value for value in values]
    assert [dataset.to_dict() for dataset in datasets] == [{"value": [value]} for value in expected]
    assert datasets[0].cache_files != datasets[1].cache_files
    with patch("datasets.packaged_modules.sql.sql.pd.read_sql", side_effect=AssertionError("cache miss")):
        # Buffer contents identify the query, independently of the buffer object or representation.
        repeated = read(expected[0])
    assert repeated.to_dict() == datasets[0].to_dict()
