from pathlib import Path

import numpy as np
import pytest

from datasets import Array2D, DownloadManager, Features, Value, load_dataset, load_dataset_builder
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.zarr.zarr import ZarrConfig


def _maybe_consolidate_v2_metadata(zarr_module, store_dir) -> None:
    """
    Best-effort helper to write `.zmetadata` for Zarr v2 stores when possible.

    The location of `consolidate_metadata` can vary across Zarr versions.
    """

    try:
        consolidate = getattr(zarr_module, "consolidate_metadata", None)
        if consolidate is not None:
            consolidate(str(store_dir))
            return
    except Exception:
        pass
    try:
        from zarr.convenience import consolidate_metadata  # type: ignore

        consolidate_metadata(str(store_dir))
    except Exception:
        pass


def _create_array_compat(zarr_group, name: str, data: np.ndarray, chunks: tuple[int, ...]) -> None:
    create_array = getattr(zarr_group, "create_array", None)
    if create_array is not None:
        create_array(name, data=data, chunks=chunks)
    else:
        zarr_group.create_dataset(name, data=data, chunks=chunks)


@pytest.fixture
def zarr_root_metadata_file(tmp_path) -> str:
    zarr = pytest.importorskip("zarr")

    store_dir = tmp_path / "basic.zarr"
    n_rows = 5

    root = zarr.open_group(store=str(store_dir), mode="w")
    _create_array_compat(root, "int32", np.arange(n_rows, dtype=np.int32), chunks=(2,))
    _create_array_compat(root, "float32", np.arange(n_rows, dtype=np.float32) / 10.0, chunks=(2,))
    _create_array_compat(
        root,
        "matrix_2d",
        np.random.randn(n_rows, 3, 4).astype(np.float32),
        chunks=(2, 3, 4),
    )

    # Prefer Zarr v3 root metadata if present, else fall back to v2 consolidated metadata.
    zarr_json = store_dir / "zarr.json"
    if zarr_json.exists():
        return str(zarr_json)

    zmetadata = store_dir / ".zmetadata"
    if not zmetadata.exists():
        _maybe_consolidate_v2_metadata(zarr, store_dir)

    assert zmetadata.exists(), "Expected either Zarr v3 zarr.json or Zarr v2 .zmetadata to exist"
    return str(zmetadata)


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


def test_zarr_loading_from_store_root_directory(zarr_root_metadata_file):
    store_root = str(Path(zarr_root_metadata_file).parent)
    ds = load_dataset("zarr", data_files=[store_root], split="train")
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


def test_zarr_count_examples(zarr_root_metadata_file):
    builder = load_dataset_builder("zarr", data_files=[zarr_root_metadata_file])
    assert builder.count_examples(DownloadManager()) == {"train": 5}
