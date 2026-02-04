import numpy as np
import pytest

from datasets import Array2D, Features, Value, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.zarr.zarr import ZarrConfig


@pytest.fixture
def zarr_root_metadata_file(tmp_path):
    zarr = pytest.importorskip("zarr")

    store_dir = tmp_path / "basic.zarr"
    n_rows = 5

    root = zarr.open_group(store=str(store_dir), mode="w")
    root.create_array("int32", data=np.arange(n_rows, dtype=np.int32), chunks=(2,))
    root.create_array("float32", data=np.arange(n_rows, dtype=np.float32) / 10.0, chunks=(2,))
    root.create_array("matrix_2d", data=np.random.randn(n_rows, 3, 4).astype(np.float32), chunks=(2, 3, 4))

    zarr_json = store_dir / "zarr.json"
    assert zarr_json.exists()
    return str(zarr_json)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = ZarrConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = ZarrConfig(name="name", data_files=data_files)


def test_zarr_basic_loading(zarr_root_metadata_file):
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file], split="train")
    assert set(ds.column_names) == {"int32", "float32", "matrix_2d"}
    assert ds["int32"] == [0, 1, 2, 3, 4]


def test_zarr_loading_with_features_override(zarr_root_metadata_file):
    features = Features(
        {
            "int32": Value("int32"),
            "float32": Value("float32"),
            "matrix_2d": Array2D(shape=(3, 4), dtype="float32"),
        }
    )
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file], split="train", features=features)
    assert ds.features == features


def test_zarr_streaming(zarr_root_metadata_file):
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file], split="train", streaming=True)
    first = next(iter(ds))
    assert set(first.keys()) == {"int32", "float32", "matrix_2d"}

import numpy as np
import pytest

from datasets import Array2D, Features, Value, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.zarr.zarr import ZarrConfig


@pytest.fixture
def zarr_root_metadata_file(tmp_path):
    zarr = pytest.importorskip("zarr")

    store_dir = tmp_path / "basic.zarr"
    n_rows = 5

    root = zarr.open_group(store=str(store_dir), mode="w")
    root.create_array("int32", data=np.arange(n_rows, dtype=np.int32), chunks=(2,))
    root.create_array("float32", data=np.arange(n_rows, dtype=np.float32) / 10.0, chunks=(2,))
    root.create_array("matrix_2d", data=np.random.randn(n_rows, 3, 4).astype(np.float32), chunks=(2, 3, 4))

    # Zarr v3 root metadata file
    zarr_json = store_dir / "zarr.json"
    assert zarr_json.exists()
    return str(zarr_json)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = ZarrConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = ZarrConfig(name="name", data_files=data_files)


def test_zarr_basic_loading(zarr_root_metadata_file):
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file], split="train")
    assert set(ds.column_names) == {"int32", "float32", "matrix_2d"}
    assert ds["int32"] == [0, 1, 2, 3, 4]


def test_zarr_loading_with_features_override(zarr_root_metadata_file):
    features = Features(
        {
            "int32": Value("int32"),
            "float32": Value("float32"),
            "matrix_2d": Array2D(shape=(3, 4), dtype="float32"),
        }
    )
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file], split="train", features=features)
    assert ds.features == features


def test_zarr_streaming(zarr_root_metadata_file):
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file], split="train", streaming=True)
    first = next(iter(ds))
    assert set(first.keys()) == {"int32", "float32", "matrix_2d"}

