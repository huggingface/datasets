"""Tests for the TsFile packaged module."""

import pytest

from datasets import Features, Value, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.tsfile.tsfile import TsFile, TsFileConfig


# ============================================================================
# Fixtures for creating test TsFile files
# ============================================================================


@pytest.fixture
def tsfile_table_model(tmp_path):
    """Create a TsFile with table-model data."""
    from tsfile import ColumnCategory, ColumnSchema, TableSchema, Tablet, TSDataType, TsFileTableWriter

    filename = tmp_path / "table_model.tsfile"
    n_rows = 10

    # Define schema
    table_schema = TableSchema(
        table_name="sensor_data",
        columns=[
            ColumnSchema("temperature", TSDataType.FLOAT, ColumnCategory.FIELD),
            ColumnSchema("humidity", TSDataType.DOUBLE, ColumnCategory.FIELD),
            ColumnSchema("status", TSDataType.BOOLEAN, ColumnCategory.FIELD),
        ],
    )

    with TsFileTableWriter(str(filename), table_schema) as writer:
        # Create a tablet with data
        tablet = Tablet(
            column_name_list=["temperature", "humidity", "status"],
            type_list=[TSDataType.FLOAT, TSDataType.DOUBLE, TSDataType.BOOLEAN],
            max_row_num=n_rows,
        )
        tablet.set_table_name("sensor_data")

        for i in range(n_rows):
            tablet.add_timestamp(i, i * 1000)  # timestamps in milliseconds
            tablet.add_value_by_name("temperature", i, 20.0 + i * 0.5)
            tablet.add_value_by_name("humidity", i, 45.0 + i * 1.0)
            tablet.add_value_by_name("status", i, i % 2 == 0)

        writer.write_table(tablet)

    return str(filename)


@pytest.fixture
def simple_tsfile(tmp_path):
    """Create a simple TsFile for basic tests."""
    from tsfile import ColumnCategory, ColumnSchema, TableSchema, Tablet, TSDataType, TsFileTableWriter

    filename = tmp_path / "simple.tsfile"
    n_rows = 5

    table_schema = TableSchema(
        table_name="test_table",
        columns=[
            ColumnSchema("value_int", TSDataType.INT32, ColumnCategory.FIELD),
            ColumnSchema("value_float", TSDataType.FLOAT, ColumnCategory.FIELD),
        ],
    )

    with TsFileTableWriter(str(filename), table_schema) as writer:
        tablet = Tablet(
            column_name_list=["value_int", "value_float"],
            type_list=[TSDataType.INT32, TSDataType.FLOAT],
            max_row_num=n_rows,
        )
        tablet.set_table_name("test_table")

        for i in range(n_rows):
            tablet.add_timestamp(i, i * 1000)
            tablet.add_value_by_name("value_int", i, i * 10)
            tablet.add_value_by_name("value_float", i, float(i) * 1.5)

        writer.write_table(tablet)

    return str(filename)


# ============================================================================
# Configuration Tests
# ============================================================================


def test_config_raises_when_invalid_name():
    """Test that invalid config names raise an error."""
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = TsFileConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files):
    """Test that invalid data_files parameter raises an error."""
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = TsFileConfig(name="name", data_files=data_files)


def test_config_default_values():
    """Test that TsFileConfig has expected default values."""
    config = TsFileConfig()
    assert config.batch_size == 10000
    assert config.features is None
    assert config.table_name is None
    assert config.columns is None
    assert config.start_time is None
    assert config.end_time is None


# ============================================================================
# Basic Functionality Tests
# ============================================================================


def test_tsfile_load_simple(simple_tsfile):
    """Test loading a simple TsFile."""
    dataset = load_dataset("tsfile", data_files=[simple_tsfile], split="train")

    assert len(dataset) == 5
    assert "value_int" in dataset.column_names
    assert "value_float" in dataset.column_names
    assert "time" in dataset.column_names


def test_tsfile_load_table_model(tsfile_table_model):
    """Test loading a table-model TsFile."""
    dataset = load_dataset("tsfile", data_files=[tsfile_table_model], split="train")

    assert len(dataset) == 10
    assert "temperature" in dataset.column_names
    assert "humidity" in dataset.column_names
    assert "status" in dataset.column_names
    assert "time" in dataset.column_names


def test_tsfile_data_values(simple_tsfile):
    """Test that data values are correctly loaded from TsFile."""
    dataset = load_dataset("tsfile", data_files=[simple_tsfile], split="train")

    # Check timestamps
    assert dataset["time"] == [0, 1000, 2000, 3000, 4000]

    # Check int values
    assert dataset["value_int"] == [0, 10, 20, 30, 40]

    # Check float values (with tolerance)
    import numpy as np
    np.testing.assert_allclose(dataset["value_float"], [0.0, 1.5, 3.0, 4.5, 6.0], rtol=1e-5)


# ============================================================================
# Feature Tests
# ============================================================================


def test_tsfile_feature_inference(simple_tsfile):
    """Test automatic feature inference from TsFile schema."""
    dataset = load_dataset("tsfile", data_files=[simple_tsfile], split="train")

    assert dataset.features is not None
    assert "value_int" in dataset.features
    assert "value_float" in dataset.features
    assert "time" in dataset.features

    # Check inferred types
    assert dataset.features["value_int"].dtype == "int32"
    assert dataset.features["value_float"].dtype == "float32"
    assert dataset.features["time"].dtype == "int64"


def test_tsfile_custom_features(simple_tsfile):
    """Test loading with explicit feature specification."""
    features = Features(
        {"value_int": Value("int64"), "value_float": Value("float64"), "time": Value("int64")}
    )
    dataset = load_dataset("tsfile", data_files=[simple_tsfile], split="train", features=features)

    assert dataset.features is not None


# ============================================================================
# Error Handling Tests
# ============================================================================


def test_tsfile_no_data_files_error():
    """Test that missing data_files raises an error."""
    config = TsFileConfig(name="test", data_files=None)
    tsfile_builder = TsFile()
    tsfile_builder.config = config

    with pytest.raises(ValueError, match="At least one data file must be specified"):
        tsfile_builder._split_generators(None)
