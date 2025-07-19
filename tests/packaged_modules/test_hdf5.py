import numpy as np
import pytest

import h5py
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
def hdf5_file_with_vlen_arrays(tmp_path):
    """Create an HDF5 file with variable-length arrays using HDF5's vlen_dtype."""
    filename = tmp_path / "vlen.h5"
    n_rows = 4

    with h5py.File(filename, "w") as f:
        # Variable-length arrays of different sizes using vlen_dtype
        vlen_arrays = [[1, 2, 3], [4, 5], [6, 7, 8, 9], [10]]
        # Create variable-length int dataset using vlen_dtype
        dt = h5py.vlen_dtype(np.dtype("int32"))
        dset = f.create_dataset("vlen_ints", (n_rows,), dtype=dt)
        for i, arr in enumerate(vlen_arrays):
            dset[i] = arr

        # Mixed types (some empty arrays) - use variable-length with empty arrays
        mixed_data = [
            [1, 2, 3],
            [],  # Empty array
            [4, 5],
            [6],
        ]
        dt_mixed = h5py.vlen_dtype(np.dtype("int32"))
        dset_mixed = f.create_dataset("mixed_data", (n_rows,), dtype=dt_mixed)
        for i, arr in enumerate(mixed_data):
            dset_mixed[i] = arr

    return str(filename)


@pytest.fixture
def hdf5_file_with_variable_length_strings(tmp_path):
    """Create an HDF5 file with variable-length string datasets."""
    filename = tmp_path / "var_strings.h5"
    n_rows = 4

    with h5py.File(filename, "w") as f:
        # Variable-length string dataset
        var_strings = ["short", "medium length string", "very long string with many characters", "tiny"]
        # Create variable-length string dataset using vlen_dtype
        dt = h5py.vlen_dtype(str)
        dset = f.create_dataset("var_strings", (n_rows,), dtype=dt)
        for i, s in enumerate(var_strings):
            dset[i] = s

        # Variable-length bytes dataset
        var_bytes = [b"short", b"medium length bytes", b"very long bytes with many characters", b"tiny"]
        dt_bytes = h5py.vlen_dtype(bytes)
        dset_bytes = f.create_dataset("var_bytes", (n_rows,), dtype=dt_bytes)
        for i, b in enumerate(var_bytes):
            dset_bytes[i] = b

    return str(filename)


@pytest.fixture
def hdf5_file_with_complex_data(tmp_path):
    """Create an HDF5 file with complex number datasets."""
    filename = tmp_path / "complex.h5"

    with h5py.File(filename, "w") as f:
        # Complex numbers
        complex_data = np.array([1 + 2j, 3 + 4j, 5 + 6j, 7 + 8j], dtype=np.complex64)
        f.create_dataset("complex_64", data=complex_data)

        # Complex double precision
        complex_double = np.array([1.5 + 2.5j, 3.5 + 4.5j, 5.5 + 6.5j, 7.5 + 8.5j], dtype=np.complex128)
        f.create_dataset("complex_128", data=complex_double)

        # Complex array
        complex_array = np.array(
            [[1 + 2j, 3 + 4j], [5 + 6j, 7 + 8j], [9 + 10j, 11 + 12j], [13 + 14j, 15 + 16j]], dtype=np.complex64
        )
        f.create_dataset("complex_array", data=complex_array)

    return str(filename)


@pytest.fixture
def hdf5_file_with_compound_data(tmp_path):
    """Create an HDF5 file with compound/structured datasets."""
    filename = tmp_path / "compound.h5"

    with h5py.File(filename, "w") as f:
        # Simple compound type
        dt_simple = np.dtype([("x", "i4"), ("y", "f8")])
        compound_simple = np.array([(1, 2.5), (3, 4.5), (5, 6.5)], dtype=dt_simple)
        f.create_dataset("simple_compound", data=compound_simple)

        # Compound type with complex numbers
        dt_complex = np.dtype([("real", "f4"), ("imag", "f4")])
        compound_complex = np.array([(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)], dtype=dt_complex)
        f.create_dataset("complex_compound", data=compound_complex)

        # Nested compound type
        dt_nested = np.dtype([("position", [("x", "i4"), ("y", "i4")]), ("velocity", [("vx", "f4"), ("vy", "f4")])])
        compound_nested = np.array([((1, 2), (1.5, 2.5)), ((3, 4), (3.5, 4.5)), ((5, 6), (5.5, 6.5))], dtype=dt_nested)
        f.create_dataset("nested_compound", data=compound_nested)

    return str(filename)


@pytest.fixture
def hdf5_file_with_mismatched_lengths(tmp_path):
    """Create an HDF5 file with datasets of different lengths (should raise error)."""
    filename = tmp_path / "mismatched.h5"

    with h5py.File(filename, "w") as f:
        f.create_dataset("data1", data=np.arange(5, dtype=np.int32))
        # Dataset with 3 rows (mismatched)
        f.create_dataset("data2", data=np.arange(3, dtype=np.int32))
        f.create_dataset("data3", data=np.random.randn(5, 3, 4).astype(np.float32))
        f.create_dataset("data4", data=np.arange(5, dtype=np.float64) / 10.0)
        f.create_dataset("data5", data=np.array([True, False, True, False, True]))
        var_strings = ["short", "medium length", "very long string", "tiny", "another string"]
        dt = h5py.vlen_dtype(str)
        dset = f.create_dataset("data6", (5,), dtype=dt)
        for i, s in enumerate(var_strings):
            dset[i] = s

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
def empty_hdf5_file(tmp_path):
    """Create an HDF5 file with no datasets (should warn and skip)."""
    filename = tmp_path / "empty.h5"

    with h5py.File(filename, "w") as f:
        # Create only groups, no datasets
        f.create_group("empty_group")
        grp = f.create_group("another_group")
        grp.create_group("subgroup")

    return str(filename)


@pytest.fixture
def hdf5_file_with_mixed_data_types(tmp_path):
    """Create an HDF5 file with mixed data types in the same file."""
    filename = tmp_path / "mixed.h5"
    n_rows = 3

    with h5py.File(filename, "w") as f:
        # Regular numeric data
        f.create_dataset("regular_int", data=np.arange(n_rows, dtype=np.int32))
        f.create_dataset("regular_float", data=np.arange(n_rows, dtype=np.float32))

        # Complex data
        complex_data = np.array([1 + 2j, 3 + 4j, 5 + 6j], dtype=np.complex64)
        f.create_dataset("complex_data", data=complex_data)

        # Compound data
        dt_compound = np.dtype([("x", "i4"), ("y", "f8")])
        compound_data = np.array([(1, 2.5), (3, 4.5), (5, 6.5)], dtype=dt_compound)
        f.create_dataset("compound_data", data=compound_data)

    return str(filename)


@pytest.fixture
def hdf5_file_with_complex_collision(tmp_path):
    """Create an HDF5 file where complex dataset would collide with existing dataset name."""
    filename = tmp_path / "collision.h5"

    with h5py.File(filename, "w") as f:
        # Create a complex dataset
        complex_data = np.array([1 + 2j, 3 + 4j], dtype=np.complex64)
        f.create_dataset("data", data=complex_data)

        # Create a regular dataset that would collide with the complex real part
        regular_data = np.array([1.0, 2.0], dtype=np.float32)
        f.create_dataset("data_real", data=regular_data)  # This should cause a collision

    return str(filename)


@pytest.fixture
def hdf5_file_with_compound_collision(tmp_path):
    """Create an HDF5 file where compound dataset would collide with existing dataset name."""
    filename = tmp_path / "compound_collision.h5"

    with h5py.File(filename, "w") as f:
        # Create a compound dataset
        dt_compound = np.dtype([("x", "i4"), ("y", "f8")])
        compound_data = np.array([(1, 2.5), (3, 4.5)], dtype=dt_compound)
        f.create_dataset("position", data=compound_data)

        # Create a regular dataset that would collide with compound field
        regular_data = np.array([10, 20], dtype=np.int32)
        f.create_dataset("position_x", data=regular_data)  # This should cause a collision

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


def test_hdf5_vlen_arrays(hdf5_file_with_vlen_arrays):
    """Test HDF5 loading with variable-length arrays (int32)."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[hdf5_file_with_vlen_arrays]])

    tables = list(generator)
    assert len(tables) == 1

    _, table = tables[0]
    expected_columns = {"vlen_ints", "mixed_data"}
    assert set(table.column_names) == expected_columns

    # Check vlen_ints data
    vlen_ints = table["vlen_ints"].to_pylist()
    assert len(vlen_ints) == 4
    assert vlen_ints[0] == [1, 2, 3]
    assert vlen_ints[1] == [4, 5]
    assert vlen_ints[2] == [6, 7, 8, 9]
    assert vlen_ints[3] == [10]

    # Check mixed_data (with None values)
    mixed_data = table["mixed_data"].to_pylist()
    assert len(mixed_data) == 4
    assert mixed_data[0] == [1, 2, 3]
    assert mixed_data[1] == []  # Empty array instead of None
    assert mixed_data[2] == [4, 5]
    assert mixed_data[3] == [6]


def test_hdf5_variable_length_strings(hdf5_file_with_variable_length_strings):
    """Test HDF5 loading with variable-length string datasets."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[hdf5_file_with_variable_length_strings]])

    tables = list(generator)
    assert len(tables) == 1

    _, table = tables[0]
    expected_columns = {"var_strings", "var_bytes"}
    assert set(table.column_names) == expected_columns

    # Check variable-length strings (converted to strings for usability)
    var_strings = table["var_strings"].to_pylist()
    assert len(var_strings) == 4
    assert var_strings[0] == "short"
    assert var_strings[1] == "medium length string"
    assert var_strings[2] == "very long string with many characters"
    assert var_strings[3] == "tiny"

    # Check variable-length bytes (converted to strings for usability)
    var_bytes = table["var_bytes"].to_pylist()
    assert len(var_bytes) == 4
    assert var_bytes[0] == "short"
    assert var_bytes[1] == "medium length bytes"
    assert var_bytes[2] == "very long bytes with many characters"
    assert var_bytes[3] == "tiny"


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


def test_hdf5_empty_file_warning(empty_hdf5_file, caplog):
    """Test that empty files (no datasets) are skipped with a warning."""
    hdf5 = HDF5()
    generator = hdf5._generate_tables([[empty_hdf5_file]])

    tables = list(generator)
    assert len(tables) == 0  # No tables should be generated

    # Check that warning was logged
    assert any(
        record.levelname == "WARNING" and "contains no data, skipping" in record.message for record in caplog.records
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


def test_hdf5_vlen_feature_inference(hdf5_file_with_vlen_arrays):
    """Test automatic feature inference from variable-length HDF5 datasets."""
    data_files = DataFilesDict({"train": [hdf5_file_with_vlen_arrays]})
    config = HDF5Config(data_files=data_files)
    hdf5 = HDF5()
    hdf5.config = config

    # Trigger feature inference
    dl_manager = StreamingDownloadManager()
    hdf5._split_generators(dl_manager)

    # Check that features were inferred
    assert hdf5.info.features is not None

    # Check specific feature types for variable-length arrays
    features = hdf5.info.features
    # Variable-length arrays should become Sequence features by default (for small datasets)
    assert isinstance(features["vlen_ints"], Sequence)
    assert isinstance(features["mixed_data"], Sequence)

    # Check that the inner feature types are correct
    assert isinstance(features["vlen_ints"].feature, Value)
    assert features["vlen_ints"].feature.dtype == "int32"
    assert isinstance(features["mixed_data"].feature, Value)
    assert features["mixed_data"].feature.dtype == "int32"


def test_hdf5_variable_string_feature_inference(hdf5_file_with_variable_length_strings):
    """Test automatic feature inference from variable-length string datasets."""
    data_files = DataFilesDict({"train": [hdf5_file_with_variable_length_strings]})
    config = HDF5Config(data_files=data_files)
    hdf5 = HDF5()
    hdf5.config = config

    # Trigger feature inference
    dl_manager = StreamingDownloadManager()
    hdf5._split_generators(dl_manager)

    # Check that features were inferred
    assert hdf5.info.features is not None

    # Check specific feature types for variable-length strings
    features = hdf5.info.features
    # Variable-length strings should become Value("string") features
    assert isinstance(features["var_strings"], Value)
    assert isinstance(features["var_bytes"], Value)

    # Check that the feature types are correct
    assert features["var_strings"].dtype == "string"
    assert features["var_bytes"].dtype == "string"


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


def test_hdf5_complex_numbers(hdf5_file_with_complex_data):
    """Test HDF5 loading with complex number datasets."""
    config = HDF5Config()
    hdf5 = HDF5()
    hdf5.config = config

    generator = hdf5._generate_tables([[hdf5_file_with_complex_data]])
    tables = list(generator)

    assert len(tables) == 1
    _, table = tables[0]

    # Check that complex numbers are split into real/imaginary parts
    expected_columns = {
        "complex_64_real",
        "complex_64_imag",
        "complex_128_real",
        "complex_128_imag",
        "complex_array_real",
        "complex_array_imag",
    }
    assert set(table.column_names) == expected_columns

    # Check complex_64 data
    real_data = table["complex_64_real"].to_pylist()
    imag_data = table["complex_64_imag"].to_pylist()

    assert real_data == [1.0, 3.0, 5.0, 7.0]
    assert imag_data == [2.0, 4.0, 6.0, 8.0]


def test_hdf5_compound_types(hdf5_file_with_compound_data):
    """Test HDF5 loading with compound/structured datasets."""
    config = HDF5Config()
    hdf5 = HDF5()
    hdf5.config = config

    generator = hdf5._generate_tables([[hdf5_file_with_compound_data]])
    tables = list(generator)

    assert len(tables) == 1
    _, table = tables[0]

    # Check that compound types are flattened into separate columns
    expected_columns = {
        "simple_compound_x",
        "simple_compound_y",
        "complex_compound_real",
        "complex_compound_imag",
        "nested_compound_position_x",
        "nested_compound_position_y",
        "nested_compound_velocity_vx",
        "nested_compound_velocity_vy",
    }
    assert set(table.column_names) == expected_columns

    # Check simple compound data
    x_data = table["simple_compound_x"].to_pylist()
    y_data = table["simple_compound_y"].to_pylist()

    assert x_data == [1, 3, 5]
    assert y_data == [2.5, 4.5, 6.5]


def test_hdf5_feature_inference_complex(hdf5_file_with_complex_data):
    """Test automatic feature inference for complex datasets."""
    config = HDF5Config()
    hdf5 = HDF5()
    hdf5.config = config
    hdf5.config.data_files = DataFilesDict({"train": [hdf5_file_with_complex_data]})

    # Trigger feature inference
    dl_manager = StreamingDownloadManager()
    hdf5._split_generators(dl_manager)

    # Check that features were inferred correctly
    assert hdf5.info.features is not None
    features = hdf5.info.features

    # Check complex number features
    assert "complex_64_real" in features
    assert "complex_64_imag" in features
    assert features["complex_64_real"] == Value("float64")
    assert features["complex_64_imag"] == Value("float64")


def test_hdf5_feature_inference_compound(hdf5_file_with_compound_data):
    """Test automatic feature inference for compound datasets."""
    config = HDF5Config()
    hdf5 = HDF5()
    hdf5.config = config
    hdf5.config.data_files = DataFilesDict({"train": [hdf5_file_with_compound_data]})

    # Trigger feature inference
    dl_manager = StreamingDownloadManager()
    hdf5._split_generators(dl_manager)

    # Check that features were inferred correctly
    assert hdf5.info.features is not None
    features = hdf5.info.features

    # Check compound type features
    assert "simple_compound_x" in features
    assert "simple_compound_y" in features
    assert features["simple_compound_x"] == Value("int32")
    assert features["simple_compound_y"] == Value("float64")


def test_hdf5_mixed_data_types(hdf5_file_with_mixed_data_types):
    """Test HDF5 loading with mixed data types in the same file."""
    config = HDF5Config()
    hdf5 = HDF5()
    hdf5.config = config

    generator = hdf5._generate_tables([[hdf5_file_with_mixed_data_types]])
    tables = list(generator)

    assert len(tables) == 1
    _, table = tables[0]

    # Check all expected columns are present
    expected_columns = {
        "regular_int",
        "regular_float",
        "complex_data_real",
        "complex_data_imag",
        "compound_data_x",
        "compound_data_y",
    }
    assert set(table.column_names) == expected_columns

    # Check data types
    assert table["regular_int"].to_pylist() == [0, 1, 2]
    assert len(table["complex_data_real"].to_pylist()) == 3
    assert len(table["compound_data_x"].to_pylist()) == 3


def test_hdf5_column_name_collision_detection(hdf5_file_with_complex_collision):
    """Test that column name collision detection works correctly."""
    config = HDF5Config()
    hdf5 = HDF5()
    hdf5.config = config
    hdf5.config.data_files = DataFilesDict({"train": [hdf5_file_with_complex_collision]})

    # This should raise a ValueError due to column name collision
    dl_manager = StreamingDownloadManager()
    with pytest.raises(ValueError, match="Column name collision detected"):
        hdf5._split_generators(dl_manager)


def test_hdf5_compound_collision_detection(hdf5_file_with_compound_collision):
    """Test collision detection with compound types."""
    config = HDF5Config()
    hdf5 = HDF5()
    hdf5.config = config
    hdf5.config.data_files = DataFilesDict({"train": [hdf5_file_with_compound_collision]})

    # This should raise a ValueError due to column name collision
    dl_manager = StreamingDownloadManager()
    with pytest.raises(ValueError, match="Column name collision detected"):
        hdf5._split_generators(dl_manager)


def test_hdf5_mismatched_lengths_with_column_filtering(hdf5_file_with_mismatched_lengths):
    """Test that mismatched dataset lengths are ignored when the mismatched dataset is excluded via columns config."""
    config = HDF5Config(columns=["data1"])
    hdf5 = HDF5()
    hdf5.config = config

    generator = hdf5._generate_tables([[hdf5_file_with_mismatched_lengths]])
    tables = list(generator)

    # Should work without error since we're only including the first dataset
    assert len(tables) == 1
    _, table = tables[0]

    # Check that only the specified column is present
    expected_columns = {"data1"}
    assert set(table.column_names) == expected_columns
    assert "data2" not in table.column_names

    # Check the data
    data1_values = table["data1"].to_pylist()
    assert data1_values == [0, 1, 2, 3, 4]

    # Test 2: Include multiple compatible datasets (all with 5 rows)
    config2 = HDF5Config(columns=["data1", "data3", "data4", "data5", "data6"])
    hdf5.config = config2

    generator2 = hdf5._generate_tables([[hdf5_file_with_mismatched_lengths]])
    tables2 = list(generator2)

    # Should work without error since we're excluding the mismatched dataset
    assert len(tables2) == 1
    _, table2 = tables2[0]

    # Check that all specified columns are present
    expected_columns2 = {"data1", "data3", "data4", "data5", "data6"}
    assert set(table2.column_names) == expected_columns2
    assert "data2" not in table2.column_names

    # Check data types and values
    assert table2["data1"].to_pylist() == [0, 1, 2, 3, 4]  # int32
    assert len(table2["data3"].to_pylist()) == 5  # Array2D
    assert len(table2["data3"].to_pylist()[0]) == 3  # 3 rows in each 2D array
    assert len(table2["data3"].to_pylist()[0][0]) == 4  # 4 columns in each 2D array
    np.testing.assert_allclose(table2["data4"].to_pylist(), [0.0, 0.1, 0.2, 0.3, 0.4], rtol=1e-6)  # float64
    assert table2["data5"].to_pylist() == [True, False, True, False, True]  # boolean
    assert table2["data6"].to_pylist() == [
        "short",
        "medium length",
        "very long string",
        "tiny",
        "another string",
    ]  # vlen string
