import pytest

from datasets import load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.parquet.parquet import ParquetConfig


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = ParquetConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = ParquetConfig(name="name", data_files=data_files)


def test_parquet_reshard(multi_row_groups_parquet_path):
    ds = load_dataset("parquet", data_files=multi_row_groups_parquet_path, split="train", streaming=True)
    assert ds.num_shards == 1
    expected = list(ds)
    resharded_ds = ds.reshard()
    assert resharded_ds.num_shards == 4
    assert list(resharded_ds) == expected


def test_parquet_columns(parquet_path):
    ds = load_dataset("parquet", data_files=parquet_path, split="train", streaming=True)
    full_features = ds.features
    assert len(ds.features) == 3
    assert len(next(iter(ds))) == 3
    ds = load_dataset("parquet", data_files=parquet_path, split="train", streaming=True, columns=["col_1"])
    assert len(ds.features) == 1
    assert len(next(iter(ds))) == 1
    ds = load_dataset(
        "parquet", data_files=parquet_path, split="train", streaming=True, columns=["col_1"], features=full_features
    )
    assert len(ds.features) == 1
    assert len(next(iter(ds))) == 1
