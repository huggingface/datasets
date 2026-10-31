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
@pytest.mark.parametrize("con_type", ["uri", "engine", "connection"])
@pytest.mark.parametrize("chunksize", [None, 2])
def test_dataset_from_sql_selectable(con_type, chunksize, tmp_path):
    import sqlalchemy

    uri = "sqlite:///" + str(tmp_path / "samples.db")
    engine = sqlalchemy.create_engine(uri)
    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table(
        "sample rows",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer),
        sqlalchemy.Column("text", sqlalchemy.String),
    )
    metadata.create_all(engine)
    try:
        with engine.begin() as connection:
            connection.execute(
                table.insert(), [{"id": 1, "text": "中文"}, {"id": 2, "text": None}, {"id": 3, "text": "end"}]
            )
        with engine.connect() as connection:
            con = {"uri": uri, "engine": engine, "connection": connection}[con_type]
            query = sqlalchemy.select(table).order_by(table.c.id)
            dataset = Dataset.from_sql(query, con, cache_dir=tmp_path / "cache", chunksize=chunksize)
            assert dataset.to_dict() == {"id": [1, 2, 3], "text": ["中文", None, "end"]}
            assert dataset.column_names == ["id", "text"]
            assert dataset.features == Features({"id": Value("int64"), "text": Value(STRING_FROM_PANDAS)})
            repeated = Dataset.from_sql(query, con, cache_dir=tmp_path / "cache", chunksize=chunksize)
            assert repeated.to_dict() == dataset.to_dict()
            assert repeated._fingerprint == dataset._fingerprint
    finally:
        engine.dispose()


@require_sqlalchemy
def test_dataset_from_sql_selectable_distinguishes_engines(tmp_path):
    import sqlalchemy

    engines = [sqlalchemy.create_engine("sqlite://"), sqlalchemy.create_engine("sqlite://")]
    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table("samples", metadata, sqlalchemy.Column("value", sqlalchemy.Integer))
    try:
        readers = []
        for value, engine in enumerate(engines):
            metadata.create_all(engine)
            with engine.begin() as connection:
                connection.execute(table.insert(), {"value": value})
            readers.append(SqlDatasetReader(sqlalchemy.select(table), engine, cache_dir=tmp_path / "cache"))
        assert readers[0].builder.config_id != readers[1].builder.config_id
        assert readers[0].read().to_dict() == {"value": [0]}
        assert readers[1].read().to_dict() == {"value": [1]}
    finally:
        for engine in engines:
            engine.dispose()
