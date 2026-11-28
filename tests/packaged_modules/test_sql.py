from functools import partial
from uuid import UUID

import pytest

from datasets.builder import BuilderConfig, InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.sql.sql import SqlConfig

from ..utils import require_sqlalchemy


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = SqlConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = SqlConfig(name="name", data_files=data_files)


@require_sqlalchemy
@pytest.mark.parametrize("uri", ["postgresql://", "mysql://", "oracle://"])
def test_config_id_bound_parameters(uri, monkeypatch):
    import sqlalchemy as sa

    # Exercise real dialect compilers without requiring external servers or DBAPI drivers.
    monkeypatch.setattr(sa, "create_engine", partial(sa.create_mock_engine, executor=None))

    def config_id(value):
        # Nested native values need deterministic hashing, not SQL literal rendering.
        payload = {"uuid": UUID(int=value), "nested": (None, "λ'?:%", memoryview(b"\x00\xff"))}
        query = sa.select(sa.bindparam("value", payload, type_=sa.types.NullType()))
        kwargs = {"sql": query, "con": uri}
        return SqlConfig(**kwargs).create_config_id(kwargs)

    assert config_id(1) != config_id(2)
    assert config_id(1) == config_id(1)


@require_sqlalchemy
def test_config_id_expanding_parameters():
    import sqlalchemy as sa

    def config_id(values):
        query = sa.select(sa.column("id")).where(sa.column("id").in_(values))
        kwargs = {"sql": query, "con": "sqlite://"}
        return SqlConfig(**kwargs).create_config_id(kwargs)

    assert len({config_id(values) for values in [[], [1], [2], [1, 2]]}) == 4
    assert config_id([]) == config_id([])


@require_sqlalchemy
def test_config_id_explicit_params_order():
    import sqlalchemy as sa

    def config_id(params):
        query = sa.select(sa.bindparam("first"), sa.bindparam("second"))
        kwargs = {"sql": query, "con": "sqlite://", "params": params}
        result = SqlConfig(**kwargs).create_config_id(kwargs)
        assert kwargs["sql"] is query
        assert kwargs["params"] is params
        return result

    assert config_id({"first": 1, "second": 2}) == config_id({"second": 2, "first": 1})
    assert config_id({"first": 1, "second": 2}) != config_id({"first": 2, "second": 1})


@require_sqlalchemy
def test_config_id_raw_sql_unchanged():
    kwargs = {"sql": "SELECT id FROM items WHERE id = ?", "con": "sqlite://", "params": (1,)}
    config = SqlConfig(**kwargs)
    assert config.create_config_id(kwargs) == BuilderConfig.create_config_id(config, kwargs)
