import h5py
import numpy as np
import pytest

from datasets import Array2D, Array3D, Array4D, Features, List, Value, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.exceptions import DatasetGenerationError
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
def hdf5_file_with_compound_complex_arrays(tmp_path):
    """Create an HDF5 file with compound datasets containing complex arrays."""
    filename = tmp_path / "compound_complex_arrays.h5"

    with h5py.File(filename, "w") as f:
        # Compound type with complex arrays
        dt_complex_arrays = np.dtype(
            [
                ("position", [("x", "i4"), ("y", "i4")]),
                ("complex_field", "c8"),
                ("complex_array", "c8", (2, 3)),
                ("nested_complex", [("real", "f4"), ("imag", "f4")]),
            ]
        )

        # Create data with complex numbers
        compound_data = np.array(
            [
                (
                    (1, 2),
                    1.0 + 2.0j,
                    [[1.0 + 2.0j, 3.0 + 4.0j, 5.0 + 6.0j], [7.0 + 8.0j, 9.0 + 10.0j, 11.0 + 12.0j]],
                    (1.5, 2.5),
                ),
                (
                    (3, 4),
                    3.0 + 4.0j,
                    [[13.0 + 14.0j, 15.0 + 16.0j, 17.0 + 18.0j], [19.0 + 20.0j, 21.0 + 22.0j, 23.0 + 24.0j]],
                    (3.5, 4.5),
                ),
                (
                    (5, 6),
                    5.0 + 6.0j,
                    [[25.0 + 26.0j, 27.0 + 28.0j, 29.0 + 30.0j], [31.0 + 32.0j, 33.0 + 34.0j, 35.0 + 36.0j]],
                    (5.5, 6.5),
                ),
            ],
            dtype=dt_complex_arrays,
        )

        f.create_dataset("compound_with_complex", data=compound_data)

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
    dataset = load_dataset("hdf5", data_files=[hdf5_file], split="train")

    assert "int32" in dataset.column_names
    assert "float32" in dataset.column_names
    assert "bool" in dataset.column_names

    assert np.asarray(dataset.data["int32"]).dtype == np.int32
    assert np.asarray(dataset.data["float32"]).dtype == np.float32
    assert np.asarray(dataset.data["bool"]).dtype == np.bool_

    assert dataset["int32"] == [0, 1, 2, 3, 4]
    float32_data = dataset["float32"]
    expected_float32 = [0.0, 0.1, 0.2, 0.3, 0.4]
    np.testing.assert_allclose(float32_data, expected_float32, rtol=1e-6)


def test_hdf5_nested_groups(hdf5_file_with_groups):
    """Test HDF5 loading with nested groups."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_groups], split="train")

    expected_columns = {"root_data", "group1"}
    assert set(dataset.column_names) == expected_columns

    # Check data
    root_data = dataset["root_data"]
    group1_data = dataset["group1"]
    assert root_data == [0, 1, 2]
    assert group1_data == [
        {"group_data": 0.0, "subgroup": {"sub_data": 0}},
        {"group_data": 1.0, "subgroup": {"sub_data": 1}},
        {"group_data": 2.0, "subgroup": {"sub_data": 2}},
    ]


def test_hdf5_multi_dimensional_arrays(hdf5_file_with_arrays):
    """Test HDF5 loading with multi-dimensional arrays."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_arrays], split="train")

    expected_columns = {"matrix_2d", "tensor_3d", "tensor_4d", "tensor_5d", "vector_1d"}
    assert set(dataset.column_names) == expected_columns

    # Check shapes
    matrix_2d = dataset["matrix_2d"]
    assert len(matrix_2d) == 4  # 4 rows
    assert len(matrix_2d[0]) == 3  # 3 rows in each matrix
    assert len(matrix_2d[0][0]) == 4  # 4 columns in each matrix


def test_hdf5_vlen_arrays(hdf5_file_with_vlen_arrays):
    """Test HDF5 loading with variable-length arrays (int32)."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_vlen_arrays], split="train")

    expected_columns = {"vlen_ints", "mixed_data"}
    assert set(dataset.column_names) == expected_columns

    # Check vlen_ints data
    vlen_ints = dataset["vlen_ints"]
    assert len(vlen_ints) == 4
    assert vlen_ints[0] == [1, 2, 3]
    assert vlen_ints[1] == [4, 5]
    assert vlen_ints[2] == [6, 7, 8, 9]
    assert vlen_ints[3] == [10]

    # Check mixed_data (with None values)
    mixed_data = dataset["mixed_data"]
    assert len(mixed_data) == 4
    assert mixed_data[0] == [1, 2, 3]
    assert mixed_data[1] == []  # Empty array instead of None
    assert mixed_data[2] == [4, 5]
    assert mixed_data[3] == [6]


def test_hdf5_variable_length_strings(hdf5_file_with_variable_length_strings):
    """Test HDF5 loading with variable-length string datasets."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_variable_length_strings], split="train")
    expected_columns = {"var_strings", "var_bytes"}
    assert set(dataset.column_names) == expected_columns

    # Check variable-length strings (converted to strings for usability)
    var_strings = dataset["var_strings"]
    assert len(var_strings) == 4
    assert var_strings[0] == "short"
    assert var_strings[1] == "medium length string"
    assert var_strings[2] == "very long string with many characters"
    assert var_strings[3] == "tiny"

    # Check variable-length bytes (converted to strings for usability)
    var_bytes = dataset["var_bytes"]
    assert len(var_bytes) == 4
    assert var_bytes[0] == "short"
    assert var_bytes[1] == "medium length bytes"
    assert var_bytes[2] == "very long bytes with many characters"
    assert var_bytes[3] == "tiny"


def test_hdf5_different_dtypes(hdf5_file_with_different_dtypes):
    """Test HDF5 loading with various numeric dtypes."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_different_dtypes], split="train")
    expected_columns = {"int8", "int16", "int64", "uint8", "uint16", "uint32", "uint64", "float16", "float64", "bytes"}
    assert set(dataset.column_names) == expected_columns

    # Check specific dtypes
    int8_data = dataset["int8"]
    assert int8_data == [0, 1, 2]

    bytes_data = dataset["bytes"]
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
    features = Features({"root_data": Value("int32"), "group1": Features({"group_data": Value("float32")})})
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_groups], split="train", features=features)

    expected_columns = {"root_data", "group1"}
    assert set(dataset.column_names) == expected_columns

    # Check that subgroup is filtered out
    group1_data = dataset["group1"]
    assert group1_data == [
        {"group_data": 0.0},
        {"group_data": 1.0},
        {"group_data": 2.0},
    ]


def test_hdf5_feature_specification(hdf5_file):
    """Test HDF5 loading with explicit feature specification."""
    features = Features({"int32": Value("int32"), "float32": Value("float64"), "bool": Value("bool")})
    dataset = load_dataset("hdf5", data_files=[hdf5_file], split="train", features=features)

    # Check that features are properly cast
    assert np.asarray(dataset.data["float32"]).dtype == np.float64
    assert np.asarray(dataset.data["int32"]).dtype == np.int32
    assert np.asarray(dataset.data["bool"]).dtype == np.bool_


def test_hdf5_mismatched_lengths_error(hdf5_file_with_mismatched_lengths):
    """Test that mismatched dataset lengths raise an error."""
    with pytest.raises(DatasetGenerationError) as exc_info:
        load_dataset("hdf5", data_files=[hdf5_file_with_mismatched_lengths], split="train")

    assert isinstance(exc_info.value.__cause__, ValueError)
    assert "3 but expected 5" in str(exc_info.value.__cause__)


def test_hdf5_zero_dimensions_handling(hdf5_file_with_zero_dimensions, caplog):
    """Test that zero dimensions are handled gracefully."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_zero_dimensions], split="train")

    expected_columns = {"zero_dim", "zero_middle", "zero_last"}
    assert set(dataset.column_names) == expected_columns

    # Check that the data is loaded (should be empty arrays)
    zero_dim_data = dataset["zero_dim"]
    assert len(zero_dim_data) == 3  # 3 rows
    assert all(len(row) == 0 for row in zero_dim_data)  # Each row is empty

    # Check that shape info is lost
    assert all(isinstance(col, List) and col.length == -1 for col in dataset.features.values())

    # Check for the warnings
    assert (
        len(
            [
                record.message
                for record in caplog.records
                if record.levelname == "WARNING" and "dimension with size 0" in record.message
            ]
        )
        == 3
    )


def test_hdf5_empty_file_warning(empty_hdf5_file, caplog):
    """Test that empty files (no datasets) are skipped with a warning."""
    with pytest.raises(ValueError, match="corresponds to no data"):
        load_dataset("hdf5", data_files=[empty_hdf5_file], split="train")

    # Check that warning was logged
    assert any(
        record.levelname == "WARNING" and "contains no data, skipping" in record.message for record in caplog.records
    )


def test_hdf5_feature_inference(hdf5_file_with_arrays):
    """Test automatic feature inference from HDF5 datasets."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_arrays], split="train")

    # Check that features were inferred
    assert dataset.features is not None

    # Check specific feature types
    features = dataset.features
    # (n_rows, 3, 4) -> Array2D with shape (3, 4)
    assert isinstance(features["matrix_2d"], Array2D)
    assert features["matrix_2d"].shape == (3, 4)
    # (n_rows, 2, 3, 4) -> Array3D with shape (2, 3, 4)
    assert isinstance(features["tensor_3d"], Array3D)
    assert features["tensor_3d"].shape == (2, 3, 4)
    # (n_rows, 2, 3, 4, 5) -> Array4D with shape (2, 3, 4, 5)
    assert isinstance(features["tensor_4d"], Array4D)
    assert features["tensor_4d"].shape == (2, 3, 4, 5)
    # (n_rows, 10) -> List of length 10
    assert isinstance(features["vector_1d"], List)
    assert features["vector_1d"].length == 10


def test_hdf5_vlen_feature_inference(hdf5_file_with_vlen_arrays):
    """Test automatic feature inference from variable-length HDF5 datasets."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_vlen_arrays], split="train")

    # Check that features were inferred
    assert dataset.features is not None

    # Check specific feature types for variable-length arrays
    features = dataset.features
    # Variable-length arrays should become List features by default (for small datasets)
    assert isinstance(features["vlen_ints"], List)
    assert isinstance(features["mixed_data"], List)

    # Check that the inner feature types are correct
    assert isinstance(features["vlen_ints"].feature, Value)
    assert features["vlen_ints"].feature.dtype == "int32"
    assert isinstance(features["mixed_data"].feature, Value)
    assert features["mixed_data"].feature.dtype == "int32"


def test_hdf5_variable_string_feature_inference(hdf5_file_with_variable_length_strings):
    """Test automatic feature inference from variable-length string datasets."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_variable_length_strings], split="train")

    # Check that features were inferred
    assert dataset.features is not None

    # Check specific feature types for variable-length strings
    features = dataset.features
    # Variable-length strings should become Value("string") features
    assert isinstance(features["var_strings"], Value)
    assert isinstance(features["var_bytes"], Value)

    # Check that the feature types are correct
    assert features["var_strings"].dtype == "string"
    assert features["var_bytes"].dtype == "string"


def test_hdf5_invalid_features(hdf5_file_with_arrays):
    """Test that invalid features raise an error."""
    features = Features({"fakefeature": Value("int32")})
    with pytest.raises(ValueError):
        load_dataset("hdf5", data_files=[hdf5_file_with_arrays], split="train", features=features)

    # try with one valid and one invalid feature
    features = Features({"matrix_2d": Array2D(shape=(3, 4), dtype="float32"), "fakefeature": Value("int32")})
    with pytest.raises(DatasetGenerationError):
        load_dataset("hdf5", data_files=[hdf5_file_with_arrays], split="train", features=features)


def test_hdf5_no_data_files_error():
    """Test that missing data_files raises an error."""
    config = HDF5Config(name="test", data_files=None)
    hdf5 = HDF5()
    hdf5.config = config

    with pytest.raises(ValueError, match="At least one data file must be specified"):
        hdf5._split_generators(None)


def test_hdf5_complex_numbers(hdf5_file_with_complex_data):
    """Test HDF5 loading with complex number datasets."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_complex_data], split="train")

    # Check that complex numbers are represented as nested Features
    expected_columns = {
        "complex_64",
        "complex_128",
        "complex_array",
    }
    assert set(dataset.column_names) == expected_columns

    # Check complex_64 data
    complex_64_data = dataset["complex_64"]
    assert len(complex_64_data) == 4
    assert complex_64_data[0] == {"real": 1.0, "imag": 2.0}
    assert complex_64_data[1] == {"real": 3.0, "imag": 4.0}
    assert complex_64_data[2] == {"real": 5.0, "imag": 6.0}
    assert complex_64_data[3] == {"real": 7.0, "imag": 8.0}
    assert np.asarray(dataset.data["complex_64"].flatten()[0]).dtype == np.float32
    assert np.asarray(dataset.data["complex_64"].flatten()[1]).dtype == np.float32
    assert np.asarray(dataset.data["complex_128"].flatten()[0]).dtype == np.float64
    assert np.asarray(dataset.data["complex_128"].flatten()[1]).dtype == np.float64


def test_hdf5_compound_types(hdf5_file_with_compound_data):
    """Test HDF5 loading with compound/structured datasets."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_compound_data], split="train")

    # Check that compound types are represented as nested structures
    expected_columns = {
        "simple_compound",
        "complex_compound",
        "nested_compound",
    }
    assert set(dataset.column_names) == expected_columns

    # Check simple compound data
    simple_compound_data = dataset["simple_compound"]
    assert len(simple_compound_data) == 3
    assert simple_compound_data[0] == {"x": 1, "y": 2.5}
    assert simple_compound_data[1] == {"x": 3, "y": 4.5}
    assert simple_compound_data[2] == {"x": 5, "y": 6.5}


def test_hdf5_feature_inference_complex(hdf5_file_with_complex_data):
    """Test automatic feature inference for complex datasets."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_complex_data], split="train")

    # Check that features were inferred correctly
    assert dataset.features is not None
    features = dataset.features

    # Check complex number features
    assert "complex_64" in features
    # Complex features are represented as dict, not Features object
    assert isinstance(features["complex_64"], dict)
    assert features["complex_64"]["real"] == Value("float32")
    assert features["complex_64"]["imag"] == Value("float32")


def test_hdf5_feature_inference_compound(hdf5_file_with_compound_data):
    """Test automatic feature inference for compound datasets."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_compound_data], split="train")

    # Check that features were inferred correctly
    assert dataset.features is not None
    features = dataset.features

    # Check compound type features
    assert "simple_compound" in features
    # Compound features are represented as dict, not Features object
    assert isinstance(features["simple_compound"], dict)
    assert features["simple_compound"]["x"] == Value("int32")
    assert features["simple_compound"]["y"] == Value("float64")


def test_hdf5_mixed_data_types(hdf5_file_with_mixed_data_types):
    """Test HDF5 loading with mixed data types in the same file."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_mixed_data_types], split="train")

    # Check all expected columns are present
    expected_columns = {
        "regular_int",
        "regular_float",
        "complex_data",
        "compound_data",
    }
    assert set(dataset.column_names) == expected_columns

    # Check data types
    assert dataset["regular_int"] == [0, 1, 2]
    assert len(dataset["complex_data"]) == 3
    assert len(dataset["compound_data"]) == 3


def test_hdf5_mismatched_lengths_with_column_filtering(hdf5_file_with_mismatched_lengths):
    """Test that mismatched dataset lengths are ignored when the mismatched dataset is excluded via columns config."""
    # Test 1: Include only the first dataset
    features = Features({"data1": Value("int32")})
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_mismatched_lengths], split="train", features=features)

    # Should work without error since we're only including the first dataset
    expected_columns = {"data1"}
    assert set(dataset.column_names) == expected_columns
    assert "data2" not in dataset.column_names

    # Check the data
    data1_values = dataset["data1"]
    assert data1_values == [0, 1, 2, 3, 4]

    # Test 2: Include multiple compatible datasets (all with 5 rows)
    features = Features(
        {
            "data1": Value("int32"),
            "data3": Array2D(shape=(3, 4), dtype="float32"),
            "data4": Value("float64"),
            "data5": Value("bool"),
            "data6": Value("string"),
        }
    )
    dataset2 = load_dataset("hdf5", data_files=[hdf5_file_with_mismatched_lengths], split="train", features=features)

    # Should work without error since we're excluding the mismatched dataset
    expected_columns2 = {"data1", "data3", "data4", "data5", "data6"}
    assert set(dataset2.column_names) == expected_columns2
    assert "data2" not in dataset2.column_names

    # Check data types and values
    assert dataset2["data1"] == [0, 1, 2, 3, 4]  # int32
    assert len(dataset2["data3"]) == 5  # Array2D
    assert len(dataset2["data3"][0]) == 3  # 3 rows in each 2D array
    assert len(dataset2["data3"][0][0]) == 4  # 4 columns in each 2D array
    np.testing.assert_allclose(dataset2["data4"], [0.0, 0.1, 0.2, 0.3, 0.4], rtol=1e-6)  # float64
    assert dataset2["data5"] == [True, False, True, False, True]  # boolean
    assert dataset2["data6"] == [
        "short",
        "medium length",
        "very long string",
        "tiny",
        "another string",
    ]  # vlen string


def test_hdf5_compound_with_complex_arrays(hdf5_file_with_compound_complex_arrays):
    """Test HDF5 loading with compound datasets containing complex arrays."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_compound_complex_arrays], split="train")

    # Check that compound types with complex arrays are represented as nested structures
    expected_columns = {"compound_with_complex"}
    assert set(dataset.column_names) == expected_columns

    # Check compound data with complex arrays
    compound_data = dataset["compound_with_complex"]
    assert len(compound_data) == 3

    # Check first row
    first_row = compound_data[0]
    assert first_row["position"]["x"] == 1
    assert first_row["position"]["y"] == 2

    # Check complex field (should be represented as real/imag structure)
    assert first_row["complex_field"]["real"] == 1.0
    assert first_row["complex_field"]["imag"] == 2.0

    # Check complex array (should be represented as nested real/imag structures)
    complex_array = first_row["complex_array"]
    assert len(complex_array["real"]) == 2  # 2 rows
    assert len(complex_array["real"][0]) == 3  # 3 columns

    # Check first element of complex array
    assert complex_array["real"][0][0] == 1.0
    assert complex_array["imag"][0][0] == 2.0

    # Check nested complex field
    assert first_row["nested_complex"]["real"] == 1.5
    assert first_row["nested_complex"]["imag"] == 2.5


def test_hdf5_feature_inference_compound_complex_arrays(hdf5_file_with_compound_complex_arrays):
    """Test automatic feature inference for compound datasets with complex arrays."""
    dataset = load_dataset("hdf5", data_files=[hdf5_file_with_compound_complex_arrays], split="train")

    # Check that features were inferred correctly
    assert dataset.features is not None
    features = dataset.features

    # Check compound type features with complex arrays
    assert "compound_with_complex" in features

    # Check nested structure
    compound_features = features["compound_with_complex"]
    assert "position" in compound_features
    assert "complex_field" in compound_features
    assert "complex_array" in compound_features
    assert "nested_complex" in compound_features

    # Check position field (nested compound)
    assert compound_features["position"]["x"] == Value("int32")
    assert compound_features["position"]["y"] == Value("int32")

    # Check complex field (should be real/imag structure)
    assert compound_features["complex_field"]["real"] == Value("float32")
    assert compound_features["complex_field"]["imag"] == Value("float32")

    # Check complex array (should be nested real/imag structures)
    assert compound_features["complex_array"]["real"] == Array2D(shape=(2, 3), dtype="float32")
    assert compound_features["complex_array"]["imag"] == Array2D(shape=(2, 3), dtype="float32")

    # Check nested complex field
    assert compound_features["nested_complex"]["real"] == Value("float32")
    assert compound_features["nested_complex"]["imag"] == Value("float32")
