import h5py
import numpy as np
import pytest

from datasets import Array2D, Array3D, Array4D, Features, Sequence, Value
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesDict, DataFilesList
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.hdf5.hdf5 import HDF5, HDF5Config


@pytest.fixture
def hdf5_file(tmp_path):
    """Create a basic HDF5 file with numeric datasets."""
    filename = tmp_path / "basic.h5"
    n_rows = 5

    with h5py.File(filename, "w") as f:
        f.create_dataset("int32", data=np.arange(n_rows, dtype=np.int32))
        f.create_dataset("float32", data=np.arange(n_rows, dtype=np.float32) / 10.0)
        f.create_dataset("bool", data=np.array([True, False, True, False, True]))

    return str(filename)


@pytest.fixture
def hdf5_file_with_groups(tmp_path):
    """Create an HDF5 file with nested groups."""
    filename = tmp_path / "nested.h5"
    n_rows = 3

    with h5py.File(filename, "w") as f:
        f.create_dataset("root_data", data=np.arange(n_rows, dtype=np.int32))
        grp = f.create_group("group1")
        grp.create_dataset("group_data", data=np.arange(n_rows, dtype=np.float32))
        subgrp = grp.create_group("subgroup")
        subgrp.create_dataset("sub_data", data=np.arange(n_rows, dtype=np.int64))

    return str(filename)


@pytest.fixture
def hdf5_file_with_arrays(tmp_path):
    """Create an HDF5 file with multi-dimensional arrays."""
    filename = tmp_path / "arrays.h5"
    n_rows = 4

    with h5py.File(filename, "w") as f:
        # 2D array (should become Array2D)
        f.create_dataset("matrix_2d", data=np.random.randn(n_rows, 3, 4).astype(np.float32))
        # 3D array (should become Array3D)
        f.create_dataset("tensor_3d", data=np.random.randn(n_rows, 2, 3, 4).astype(np.float64))
        # 4D array (should become Array4D)
        f.create_dataset("tensor_4d", data=np.random.randn(n_rows, 2, 3, 4, 5).astype(np.float32))
        # 5D array (should become Array5D)
        f.create_dataset("tensor_5d", data=np.random.randn(n_rows, 2, 3, 4, 5, 6).astype(np.float64))
        # 1D array (should become Value)
        f.create_dataset("vector_1d", data=np.random.randn(n_rows, 10).astype(np.float32))

    return str(filename)


@pytest.fixture
def hdf5_file_with_different_dtypes(tmp_path):
    """Create an HDF5 file with various numeric dtypes."""
    filename = tmp_path / "dtypes.h5"
    n_rows = 3

    with h5py.File(filename, "w") as f:
        f.create_dataset("int8", data=np.arange(n_rows, dtype=np.int8))
        f.create_dataset("int16", data=np.arange(n_rows, dtype=np.int16))
        f.create_dataset("int64", data=np.arange(n_rows, dtype=np.int64))
        f.create_dataset("uint8", data=np.arange(n_rows, dtype=np.uint8))
        f.create_dataset("uint16", data=np.arange(n_rows, dtype=np.uint16))
        f.create_dataset("uint32", data=np.arange(n_rows, dtype=np.uint32))
        f.create_dataset("uint64", data=np.arange(n_rows, dtype=np.uint64))
        f.create_dataset("float16", data=np.arange(n_rows, dtype=np.float16) / 10.0)
        f.create_dataset("float64", data=np.arange(n_rows, dtype=np.float64) / 10.0)
        f.create_dataset("bytes", data=np.array([b"row_%d" % i for i in range(n_rows)], dtype="S10"))

    return str(filename)


@pytest.fixture
def hdf5_file_with_mismatched_lengths(tmp_path):
    """Create an HDF5 file with datasets of different lengths (should raise error)."""
    filename = tmp_path / "mismatched.h5"

    with h5py.File(filename, "w") as f:
        f.create_dataset("data1", data=np.arange(5, dtype=np.int32))
        f.create_dataset("data2", data=np.arange(3, dtype=np.int32))  # Different length

    return str(filename)


@pytest.fixture
def hdf5_file_with_zero_dimensions(tmp_path):
    """Create an HDF5 file with zero dimensions (should be handled gracefully)."""
    filename = tmp_path / "zero_dims.h5"

    with h5py.File(filename, "w") as f:
        # Create a dataset with a zero dimension
        f.create_dataset("zero_dim", data=np.zeros((3, 0, 2), dtype=np.float32))
        # Create a dataset with zero in the middle dimension
        f.create_dataset("zero_middle", data=np.zeros((3, 0), dtype=np.int32))
        # Create a dataset with zero in the last dimension
        f.create_dataset("zero_last", data=np.zeros((3, 2, 0), dtype=np.float64))

    return str(filename)


@pytest.fixture
def hdf5_file_with_unsupported_dtypes(tmp_path):
    """Create an HDF5 file with unsupported dtypes (complex)."""
    filename = tmp_path / "unsupported.h5"

    with h5py.File(filename, "w") as f:
        # Complex dtype (should be rejected)
        complex_data = np.array([1 + 2j, 3 + 4j, 5 + 6j], dtype=np.complex64)
        f.create_dataset("complex_data", data=complex_data)

    return str(filename)


@pytest.fixture
def empty_hdf5_file(tmp_path):
    """Create an HDF5 file with no datasets (should warn and skip)."""
    filename = tmp_path / "empty.h5"

    with h5py.File(filename, "w") as f:
        # Create only groups, no datasets
        f.create_group("empty_group")
        grp = f.create_group("another_group")
        grp.create_group("subgroup")

    return str(filename)


def test_config_raises_when_invalid_name():
    """Test that invalid config names raise an error."""
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = HDF5Config(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files):
    """Test that invalid data_files parameter raises an error."""
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = HDF5Config(name="name", data_files=data_files)


def test_hdf5_basic_functionality(hdf5_file):
    """Test basic HDF5 loading with simple numeric datasets."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[hdf5_file]])

    tables = list(generator)
    assert len(tables) == 1

    _, table = tables[0]
    assert "int32" in table.column_names
    assert "float32" in table.column_names
    assert "bool" in table.column_names

    # Check data
    int32_data = table["int32"].to_pylist()
    assert int32_data == [0, 1, 2, 3, 4]

    float32_data = table["float32"].to_pylist()
    expected_float32 = [0.0, 0.1, 0.2, 0.3, 0.4]
    np.testing.assert_allclose(float32_data, expected_float32, rtol=1e-6)


def test_hdf5_nested_groups(hdf5_file_with_groups):
    """Test HDF5 loading with nested groups."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[hdf5_file_with_groups]])

    tables = list(generator)
    assert len(tables) == 1

    _, table = tables[0]
    expected_columns = {"root_data", "group1/group_data", "group1/subgroup/sub_data"}
    assert set(table.column_names) == expected_columns

    # Check data
    root_data = table["root_data"].to_pylist()
    assert root_data == [0, 1, 2]

    group_data = table["group1/group_data"].to_pylist()
    expected_group_data = [0.0, 1.0, 2.0]
    np.testing.assert_allclose(group_data, expected_group_data, rtol=1e-6)


def test_hdf5_multi_dimensional_arrays(hdf5_file_with_arrays):
    """Test HDF5 loading with multi-dimensional arrays."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[hdf5_file_with_arrays]])

    tables = list(generator)
    assert len(tables) == 1

    _, table = tables[0]
    expected_columns = {"matrix_2d", "tensor_3d", "tensor_4d", "tensor_5d", "vector_1d"}
    assert set(table.column_names) == expected_columns

    # Check shapes
    matrix_2d = table["matrix_2d"].to_pylist()
    assert len(matrix_2d) == 4  # 4 rows
    assert len(matrix_2d[0]) == 3  # 3 rows in each matrix
    assert len(matrix_2d[0][0]) == 4  # 4 columns in each matrix


def test_hdf5_different_dtypes(hdf5_file_with_different_dtypes):
    """Test HDF5 loading with various numeric dtypes."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[hdf5_file_with_different_dtypes]])

    tables = list(generator)
    assert len(tables) == 1

    _, table = tables[0]
    expected_columns = {"int8", "int16", "int64", "uint8", "uint16", "uint32", "uint64", "float16", "float64", "bytes"}
    assert set(table.column_names) == expected_columns

    # Check specific dtypes
    int8_data = table["int8"].to_pylist()
    assert int8_data == [0, 1, 2]

    bytes_data = table["bytes"].to_pylist()
    assert bytes_data == [b"row_0", b"row_1", b"row_2"]


def test_hdf5_batch_processing(hdf5_file):
    """Test HDF5 loading with custom batch size."""
    config = HDF5Config(batch_size=2)
    hdf5 = HDF5()
    hdf5.config = config
    generator = hdf5._generate_tables([[hdf5_file]])

    tables = list(generator)
    # Should have 3 batches: [0,1], [2,3], [4]
    assert len(tables) == 3

    # Check first batch
    _, first_batch = tables[0]
    assert len(first_batch) == 2

    # Check last batch
    _, last_batch = tables[2]
    assert len(last_batch) == 1


def test_hdf5_column_filtering(hdf5_file_with_groups):
    """Test HDF5 loading with column filtering."""
    config = HDF5Config(columns=["root_data", "group1/group_data"])
    hdf5 = HDF5()
    hdf5.config = config
    generator = hdf5._generate_tables([[hdf5_file_with_groups]])

    tables = list(generator)
    assert len(tables) == 1

    _, table = tables[0]
    expected_columns = {"root_data", "group1/group_data"}
    assert set(table.column_names) == expected_columns
    assert "group1/subgroup/sub_data" not in table.column_names


def test_hdf5_feature_specification(hdf5_file):
    """Test HDF5 loading with explicit feature specification."""
    features = Features({"int32": Value("int32"), "float32": Value("float32"), "bool": Value("bool")})

    config = HDF5Config(features=features)
    hdf5 = HDF5()
    hdf5.config = config
    generator = hdf5._generate_tables([[hdf5_file]])

    tables = list(generator)
    assert len(tables) == 1

    _, table = tables[0]
    # Check that features are properly cast
    assert table.schema.field("int32").type == features["int32"].pa_type
    assert table.schema.field("float32").type == features["float32"].pa_type
    assert table.schema.field("bool").type == features["bool"].pa_type


def test_hdf5_mismatched_lengths_error(hdf5_file_with_mismatched_lengths):
    """Test that mismatched dataset lengths raise an error."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[hdf5_file_with_mismatched_lengths]])

    with pytest.raises(ValueError, match="length.*differs from"):
        for _ in generator:
            pass


def test_hdf5_zero_dimensions_handling(hdf5_file_with_zero_dimensions, caplog):
    """Test that zero dimensions are handled gracefully."""
    # Trigger feature inference
    data_files = DataFilesDict({"train": [hdf5_file_with_zero_dimensions]})
    config = HDF5Config(data_files=data_files)
    hdf5 = HDF5()
    hdf5.config = config

    # Trigger feature inference
    dl_manager = StreamingDownloadManager()
    hdf5._split_generators(dl_manager)

    # Check that features were inferred
    assert hdf5.info.features is not None

    # Test that the data can be loaded
    generator = hdf5._generate_tables([[hdf5_file_with_zero_dimensions]])
    tables = list(generator)
    assert len(tables) == 1

    _, table = tables[0]
    expected_columns = {"zero_dim", "zero_middle", "zero_last"}
    assert set(table.column_names) == expected_columns

    # Check that the data is loaded (should be empty arrays)
    zero_dim_data = table["zero_dim"].to_pylist()
    assert len(zero_dim_data) == 3  # 3 rows
    assert all(len(row) == 0 for row in zero_dim_data)  # Each row is empty


def test_hdf5_unsupported_dtypes_error(hdf5_file_with_unsupported_dtypes):
    """Test that unsupported dtypes raise an error."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[hdf5_file_with_unsupported_dtypes]])

    # Complex dtypes cause ArrowNotImplementedError during conversion
    with pytest.raises(Exception):  # Either ValueError or ArrowNotImplementedError
        for _ in generator:
            pass


def test_hdf5_empty_file_warning(empty_hdf5_file, caplog):
    """Test that empty files (no datasets) are skipped with a warning."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[empty_hdf5_file]])

    tables = list(generator)
    assert len(tables) == 0  # No tables should be generated

    # Check that warning was logged
    assert any(
        record.levelname == "WARNING" and "contains no datasets, skipping" in record.message
        for record in caplog.records
    )


def test_hdf5_feature_inference(hdf5_file_with_arrays):
    """Test automatic feature inference from HDF5 datasets."""
    data_files = DataFilesDict({"train": [hdf5_file_with_arrays]})
    config = HDF5Config(data_files=data_files)
    hdf5 = HDF5()
    hdf5.config = config

    # Trigger feature inference
    dl_manager = StreamingDownloadManager()
    hdf5._split_generators(dl_manager)

    # Check that features were inferred
    assert hdf5.info.features is not None

    # Check specific feature types
    features = hdf5.info.features
    # (n_rows, 3, 4) -> Array2D with shape (3, 4)
    assert isinstance(features["matrix_2d"], Array2D)
    assert features["matrix_2d"].shape == (3, 4)
    # (n_rows, 2, 3, 4) -> Array3D with shape (2, 3, 4)
    assert isinstance(features["tensor_3d"], Array3D)
    assert features["tensor_3d"].shape == (2, 3, 4)
    # (n_rows, 2, 3, 4, 5) -> Array4D with shape (2, 3, 4, 5)
    assert isinstance(features["tensor_4d"], Array4D)
    assert features["tensor_4d"].shape == (2, 3, 4, 5)
    # (n_rows, 10) -> Sequence of length 10
    assert isinstance(features["vector_1d"], Sequence)
    assert features["vector_1d"].length == 10


def test_hdf5_columns_features_mismatch():
    """Test that mismatched columns and features raise an error."""
    features = Features({"col1": Value("int32"), "col2": Value("float32")})

    config = HDF5Config(
        name="test",
        columns=["col1", "col3"],  # col3 not in features
        features=features,
    )

    hdf5 = HDF5()
    hdf5.config = config

    with pytest.raises(ValueError, match="must contain the same columns"):
        hdf5._info()


def test_hdf5_no_data_files_error():
    """Test that missing data_files raises an error."""
    config = HDF5Config(name="test", data_files=None)
    hdf5 = HDF5()
    hdf5.config = config

    with pytest.raises(ValueError, match="At least one data file must be specified"):
        hdf5._split_generators(None)
