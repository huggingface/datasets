import gzip
from pathlib import Path

import numpy as np
import pytest

from datasets import Array2D, DownloadManager, Features, Value, load_dataset, load_dataset_builder
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.zarr.zarr import (
    ZarrConfig,
    _maybe_decode_gzip_metadata,
    _np_to_hf_value,
    _to_python_string_or_none,
)


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


def _get_store_probe_file(store_root: str) -> str:
    for metadata_name in [".zgroup", "zarr.json", ".zmetadata"]:
        metadata_path = Path(store_root) / metadata_name
        if metadata_path.exists():
            return str(metadata_path)
    raise AssertionError(f"Expected a Zarr metadata file in {store_root}")


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


@pytest.fixture
def zarr_root_metadata_file_mixed_axis0_lengths(tmp_path) -> str:
    zarr = pytest.importorskip("zarr")

    store_dir = tmp_path / "mixed.zarr"
    root = zarr.open_group(store=str(store_dir), mode="w")
    _create_array_compat(root, "basin", np.arange(3, dtype=np.int32), chunks=(3,))
    _create_array_compat(root, "time", np.arange(5, dtype=np.int64), chunks=(2,))
    _create_array_compat(
        root,
        "precipitation_rate",
        np.random.randn(5, 3).astype(np.float32),
        chunks=(2, 3),
    )

    zarr_json = store_dir / "zarr.json"
    if zarr_json.exists():
        return str(zarr_json)

    zmetadata = store_dir / ".zmetadata"
    if not zmetadata.exists():
        _maybe_consolidate_v2_metadata(zarr, store_dir)
    assert zmetadata.exists()
    return str(zmetadata)


@pytest.fixture
def zarr_root_metadata_file_coord_heavy(tmp_path) -> str:
    zarr = pytest.importorskip("zarr")

    store_dir = tmp_path / "coord_heavy.zarr"
    root = zarr.open_group(store=str(store_dir), mode="w")
    _create_array_compat(root, "basin", np.arange(3, dtype=np.int32), chunks=(3,))
    _create_array_compat(root, "basin_lat", np.arange(3, dtype=np.float32), chunks=(3,))
    _create_array_compat(root, "basin_lon", np.arange(3, dtype=np.float32), chunks=(3,))
    _create_array_compat(root, "time", np.arange(5, dtype=np.int64), chunks=(2,))
    _create_array_compat(
        root,
        "precipitation_rate",
        np.random.randn(5, 3).astype(np.float32),
        chunks=(2, 3),
    )

    zarr_json = store_dir / "zarr.json"
    if zarr_json.exists():
        return str(zarr_json)

    zmetadata = store_dir / ".zmetadata"
    if not zmetadata.exists():
        _maybe_consolidate_v2_metadata(zarr, store_dir)
    assert zmetadata.exists()
    return str(zmetadata)


@pytest.fixture
def zarr_v2_non_consolidated_store_root(tmp_path) -> str:
    zarr = pytest.importorskip("zarr")

    store_dir = tmp_path / "v2_non_consolidated.zarr"
    try:
        root = zarr.open_group(store=str(store_dir), mode="w", zarr_format=2)
    except TypeError:
        root = zarr.open_group(store=str(store_dir), mode="w")

    if (store_dir / "zarr.json").exists():
        pytest.skip("This zarr version/environment doesn't support creating v2 stores for this test")

    _create_array_compat(root, "int32", np.arange(5, dtype=np.int32), chunks=(2,))
    _create_array_compat(root, "float32", np.arange(5, dtype=np.float32), chunks=(2,))
    assert (store_dir / ".zgroup").exists()
    assert not (store_dir / ".zmetadata").exists()
    return str(store_dir)


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
    probe_file = _get_store_probe_file(store_root)
    ds = load_dataset("zarr", data_files=[probe_file], split="train")
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
    assert ds.num_shards == 3


def test_zarr_count_examples(zarr_root_metadata_file):
    builder = load_dataset_builder("zarr", data_files=[zarr_root_metadata_file])
    assert builder.count_examples(DownloadManager()) == {"train": 5}


def test_zarr_count_examples_from_store_root_directory(zarr_root_metadata_file):
    store_root = str(Path(zarr_root_metadata_file).parent)
    probe_file = _get_store_probe_file(store_root)
    builder = load_dataset_builder("zarr", data_files=[probe_file])
    assert builder.count_examples(DownloadManager()) == {"train": 5}


def test_zarr_count_examples_with_custom_sharding(zarr_root_metadata_file):
    builder = load_dataset_builder("zarr", data_files=[zarr_root_metadata_file], rows_per_shard=4)
    assert builder.count_examples(DownloadManager()) == {"train": 5}


def test_zarr_streaming_rows_per_shard(zarr_root_metadata_file):
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file], split="train", streaming=True, rows_per_shard=4)
    assert ds.num_shards == 2
    assert [example["int32"] for example in ds] == [0, 1, 2, 3, 4]


def test_zarr_streaming_target_num_shards(zarr_root_metadata_file):
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file], split="train", streaming=True, target_num_shards=2)
    assert ds.num_shards == 2
    assert [example["int32"] for example in ds] == [0, 1, 2, 3, 4]


def test_zarr_raises_when_rows_and_target_shards_are_set_together(zarr_root_metadata_file):
    with pytest.raises(ValueError, match="Only one of rows_per_shard or target_num_shards"):
        _ = load_dataset(
            "zarr",
            data_files=[zarr_root_metadata_file],
            split="train",
            rows_per_shard=2,
            target_num_shards=2,
        )


def test_zarr_loading_with_mixed_axis0_lengths(zarr_root_metadata_file_mixed_axis0_lengths):
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file_mixed_axis0_lengths], split="train")
    assert set(ds.column_names) == {"time", "precipitation_rate"}
    assert len(ds) == 5


def test_zarr_loading_prefers_nd_arrays_for_row_dimension(zarr_root_metadata_file_coord_heavy):
    ds = load_dataset("zarr", data_files=[zarr_root_metadata_file_coord_heavy], split="train")
    assert set(ds.column_names) == {"time", "precipitation_rate"}
    assert len(ds) == 5


def test_zarr_loading_from_v2_non_consolidated_store_root(zarr_v2_non_consolidated_store_root):
    probe_file = str(Path(zarr_v2_non_consolidated_store_root) / ".zgroup")
    ds = load_dataset("zarr", data_files=[probe_file], split="train", consolidated=False)
    assert set(ds.column_names) == {"int32", "float32"}
    assert ds["int32"] == [0, 1, 2, 3, 4]


def test_zarr_count_examples_from_v2_non_consolidated_store_root(zarr_v2_non_consolidated_store_root):
    probe_file = str(Path(zarr_v2_non_consolidated_store_root) / ".zgroup")
    builder = load_dataset_builder("zarr", data_files=[probe_file], consolidated=False)
    assert builder.count_examples(DownloadManager()) == {"train": 5}


def test_maybe_decode_gzip_metadata_decodes_only_metadata_keys():
    decoded = b'{"zarr_format": 2}'
    encoded = gzip.compress(decoded)
    assert _maybe_decode_gzip_metadata(".zmetadata", encoded) == decoded
    assert _maybe_decode_gzip_metadata("0.0", encoded) == encoded


def test_np_to_hf_value_supports_numpy_string_dtype():
    if not hasattr(np, "dtypes") or not hasattr(np.dtypes, "StringDType"):
        pytest.skip("This numpy version doesn't expose StringDType")
    value = _np_to_hf_value(np.dtype(np.dtypes.StringDType()))
    assert value.dtype == "string"


def test_to_python_string_or_none_preserves_missing_values():
    assert _to_python_string_or_none(None) is None
    assert _to_python_string_or_none(float("nan")) is None
    assert _to_python_string_or_none(np.float64("nan")) is None
    assert _to_python_string_or_none(b"abc") == "abc"
    assert _to_python_string_or_none(np.bytes_(b"def")) == "def"
    assert _to_python_string_or_none(np.str_("ghi")) == "ghi"
