import os

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.parquet.parquet import Parquet, ParquetConfig


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = ParquetConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = ParquetConfig(name="name", data_files=data_files)


@pytest.fixture
def parquet_file(tmp_path):
    filename = tmp_path / "file.parquet"
    table = pa.table({"col_1": [1, 2, 3], "col_2": ["a", "b", "c"]})
    pq.write_table(table, filename)
    return str(filename)


def test_parquet_no_file_name_by_default(parquet_file):
    """Ensure backward compatibility: file_name column is absent when return_file_name is not set."""
    parquet = Parquet()
    generator = parquet._generate_tables(files=[parquet_file], row_groups_list=[None])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert "file_name" not in pa_table.column_names


def test_parquet_return_file_name_enabled(parquet_file):
    """When return_file_name=True, the file_name column should be present."""
    parquet = Parquet(return_file_name=True)
    generator = parquet._generate_tables(files=[parquet_file], row_groups_list=[None])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert "file_name" in pa_table.column_names


def test_parquet_file_name_values(parquet_file):
    """The file_name column should contain the basename of the source file for every row."""
    parquet = Parquet(return_file_name=True)
    generator = parquet._generate_tables(files=[parquet_file], row_groups_list=[None])
    pa_table = pa.concat_tables([table for _, table in generator])
    data = pa_table.to_pydict()
    expected_name = os.path.basename(parquet_file)
    assert all(name == expected_name for name in data["file_name"])
