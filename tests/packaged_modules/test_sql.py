import pytest

from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.sql.sql import SqlConfig


def test_bound_parameters_change_the_cache_key() -> None:
    sqlalchemy = pytest.importorskip("sqlalchemy")
    items = sqlalchemy.table("items", sqlalchemy.column("id"))
    uri = "sqlite:///example.db"
    first = sqlalchemy.select(items).where(items.c.id == sqlalchemy.bindparam("id", 1))
    second = sqlalchemy.select(items).where(items.c.id == sqlalchemy.bindparam("id", 2))
    first_id = SqlConfig(name="items", sql=first, con=uri).create_config_id({"sql": first, "con": uri})
    second_id = SqlConfig(name="items", sql=second, con=uri).create_config_id({"sql": second, "con": uri})
    assert first_id != second_id


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = SqlConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = SqlConfig(name="name", data_files=data_files)
