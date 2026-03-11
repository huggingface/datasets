import gzip
import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.features.features import (
    Array2D,
    Array3D,
    Array4D,
    Array5D,
    Features,
    List,
    Value,
    _arrow_to_datasets_dtype,
)
from datasets.table import cast_table_to_features
from datasets.utils.file_utils import xdirname


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class ZarrConfig(datasets.BuilderConfig):
    """
    BuilderConfig for Zarr.

    This packaged module turns a Zarr group into a 🤗 Datasets table, treating each array in the
    group as a column and the first dimension as the row dimension.

    Notes:
    - Pass either the Zarr store root directory (usually ending in `.zarr`) or the Zarr root metadata file(s)
      via `data_files`:
      - Store root directory: `.../store.zarr` (auto-detects metadata)
      - Zarr v2 (consolidated): `.zmetadata`
      - Zarr v3: `zarr.json`
    - Nested groups are not yet supported (only arrays at the selected group root).
    """

    batch_size: Optional[int] = None
    features: Optional[datasets.Features] = None
    group: Optional[str] = None
    consolidated: bool = True
    rows_per_shard: Optional[int] = None
    target_num_shards: Optional[int] = None

    def __post_init__(self):
        super().__post_init__()
        if self.rows_per_shard is not None and self.rows_per_shard <= 0:
            raise ValueError(f"rows_per_shard must be > 0, but got {self.rows_per_shard}")
        if self.target_num_shards is not None and self.target_num_shards <= 0:
            raise ValueError(f"target_num_shards must be > 0, but got {self.target_num_shards}")
        if self.rows_per_shard is not None and self.target_num_shards is not None:
            raise ValueError(
                f"Only one of rows_per_shard or target_num_shards can be set, but got {self.rows_per_shard} and {self.target_num_shards}"
            )


class Zarr(datasets.ArrowBasedBuilder, datasets.builder._CountableBuilderMixin):
    BUILDER_CONFIG_CLASS = ZarrConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        zarr = _require_zarr()
        data_files = self.config.data_files
        storage_options = dl_manager.download_config.storage_options or {}
        group_path = self.config.group

        splits = []
        for split_name, metadata_files in data_files.items():
            shards = []
            store_inputs = _resolve_split_store_inputs(metadata_files, storage_options=storage_options)
            for store_input, store_root, is_v2_consolidated in store_inputs:
                zgroup = _open_zarr_group(
                    zarr,
                    store_root=store_root,
                    is_v2_consolidated=is_v2_consolidated,
                    storage_options=storage_options,
                    consolidated=self.config.consolidated,
                    group_path=group_path,
                )
                arrays = _get_root_arrays(zgroup)
                if not arrays:
                    raise ValueError(f"No arrays found in Zarr group at '{store_root}'")

                if self.info.features is None:
                    primary_num_rows = _infer_primary_num_rows(arrays)
                    feature_arrays = _select_arrays_by_num_rows(arrays, primary_num_rows)
                    self.info.features = _infer_features_from_zarr_arrays(feature_arrays)
                else:
                    feature_arrays = _select_arrays_for_features(arrays, self.info.features)
                    if not feature_arrays:
                        raise ValueError(
                            f"None of the configured feature columns were found in Zarr group at '{store_root}'"
                        )

                num_rows = _check_array_lengths(arrays, self.info.features)
                row_ranges = _generate_row_ranges(
                    num_rows=num_rows,
                    arrays=feature_arrays,
                    rows_per_shard=self.config.rows_per_shard,
                    target_num_shards=self.config.target_num_shards,
                )

                for start, end in row_ranges:
                    shards.append(
                        {
                            "metadata_file": store_input,
                            "store_root": store_root,
                            "is_v2_consolidated": is_v2_consolidated,
                            "start": start,
                            "end": end,
                        }
                    )

            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={"shards": shards, "storage_options": storage_options},
                )
            )
        return splits

    def _generate_shards(self, shards, storage_options):
        for shard in shards:
            yield {"metadata_file": shard["metadata_file"], "row_start": shard["start"], "row_end": shard["end"]}

    def _generate_num_examples(self, shards, storage_options):
        for shard in shards:
            yield shard["end"] - shard["start"]

    def _generate_tables(self, shards, storage_options):
        zarr = _require_zarr()
        batch_size_cfg = self.config.batch_size
        group_path = self.config.group

        current_store_root = None
        current_is_v2_consolidated = None
        current_arrays = None

        for shard_idx, shard in enumerate(shards):
            store_root = shard["store_root"]
            is_v2_consolidated = shard["is_v2_consolidated"]
            start = shard["start"]
            end = shard["end"]

            if store_root != current_store_root or is_v2_consolidated != current_is_v2_consolidated:
                zgroup = _open_zarr_group(
                    zarr,
                    store_root=store_root,
                    is_v2_consolidated=is_v2_consolidated,
                    storage_options=storage_options,
                    consolidated=self.config.consolidated,
                    group_path=group_path,
                )
                current_arrays = _get_root_arrays(zgroup)
                if not current_arrays:
                    raise ValueError(f"No arrays found in Zarr group at '{store_root}'")

                if self.info.features is None:
                    self.info.features = _infer_features_from_zarr_arrays(current_arrays)
                _check_array_lengths(current_arrays, self.info.features)
                current_store_root = store_root
                current_is_v2_consolidated = is_v2_consolidated

            if end <= start:
                continue

            effective_batch = batch_size_cfg or self._writer_batch_size or (end - start)
            for batch_idx, batch_start in enumerate(range(start, end, effective_batch)):
                batch_end = min(batch_start + effective_batch, end)
                pa_table = _load_batch(current_arrays, self.info.features, batch_start, batch_end)
                yield Key(shard_idx, batch_idx), cast_table_to_features(pa_table, self.info.features)


ZarrDatasetBuilder = Zarr


def _require_zarr():
    try:
        import zarr  # type: ignore
    except Exception as e:  # pragma: no cover
        raise ImportError(
            "Using the packaged module `zarr` requires the optional dependency `zarr`.\n"
            'Install it with: `pip install "datasets[zarr]"` (or `pip install zarr`)'
        ) from e
    return zarr


def _get_fsspec_mapper(store_root: str, storage_options: dict):
    import fsspec

    protocol = store_root.split("://", 1)[0] if "://" in store_root else "file"
    per_protocol = storage_options.get(protocol, {}) if isinstance(storage_options, dict) else {}
    return fsspec.get_mapper(store_root, **(per_protocol or {}))


def _is_zarr_v3(zarr_module) -> bool:
    version = getattr(zarr_module, "__version__", "")
    major = version.split(".", 1)[0]
    return major.isdigit() and int(major) >= 3


def _get_zarr_store(zarr_module, store_root: str, storage_options: dict):
    mapper = _get_fsspec_mapper(store_root, storage_options)
    if not _is_zarr_v3(zarr_module):
        return mapper
    try:
        from zarr.storage._fsspec import FsspecStore
    except Exception:
        return mapper

    class _MetadataDecodingFsspecStore(FsspecStore):
        async def get(self, key, prototype, byte_range=None):
            value = await super().get(key, prototype, byte_range=byte_range)
            if value is None or byte_range is not None:
                return value
            if not _is_zarr_metadata_key(key):
                return value
            raw = value.to_bytes()
            decoded = _maybe_decode_gzip_metadata(key, raw)
            if decoded is raw:
                return value
            return prototype.buffer.from_bytes(decoded)

        async def get_partial_values(self, prototype, key_ranges):
            key_ranges = list(key_ranges)
            values = await super().get_partial_values(prototype, key_ranges)
            decoded_values = []
            for (key, byte_range), value in zip(key_ranges, values):
                if value is None or byte_range is not None:
                    decoded_values.append(value)
                    continue
                if not _is_zarr_metadata_key(key):
                    decoded_values.append(value)
                    continue
                raw = value.to_bytes()
                decoded = _maybe_decode_gzip_metadata(key, raw)
                if decoded is raw:
                    decoded_values.append(value)
                else:
                    decoded_values.append(prototype.buffer.from_bytes(decoded))
            return decoded_values

    return _MetadataDecodingFsspecStore.from_mapper(mapper, read_only=True)


def _maybe_decode_gzip_metadata(key, value):
    if not isinstance(value, (bytes, bytearray)) or len(value) < 2 or value[:2] != b"\x1f\x8b":
        return value
    if not _is_zarr_metadata_key(key):
        return value
    try:
        return gzip.decompress(value)
    except Exception:
        return value


def _is_zarr_metadata_key(key) -> bool:
    key = str(key)
    return (
        key.endswith(".zmetadata")
        or key.endswith(".zgroup")
        or key.endswith(".zattrs")
        or key.endswith(".zarray")
        or key.endswith("zarr.json")
    )


def _open_zarr_group(
    zarr_module,
    *,
    store_root: str,
    is_v2_consolidated: bool,
    storage_options: dict,
    consolidated: bool,
    group_path: Optional[str],
):
    store = _get_zarr_store(zarr_module, store_root, storage_options)
    if is_v2_consolidated and consolidated:
        zgroup = zarr_module.open_consolidated(store=store, mode="r")
    else:
        zgroup = zarr_module.open_group(store=store, mode="r")
    if group_path:
        zgroup = zgroup[group_path]
    return zgroup


def _extract_zarr_store_root(path: str) -> Optional[str]:
    match = re.match(r"^(.*\\.zarr)(?:$|[\\\\/].*)", str(path))
    if match:
        return match.group(1).rstrip("/\\")
    return None


def _resolve_split_store_inputs(metadata_files, *, storage_options: dict) -> list[tuple[str, str, bool]]:
    seen = set()
    store_inputs: list[tuple[str, str, bool]] = []
    for metadata_file in metadata_files:
        metadata_file = str(metadata_file)
        candidate = _extract_zarr_store_root(metadata_file) or metadata_file
        store_root, is_v2_consolidated, _ = _resolve_store_root_and_version(
            candidate, storage_options=storage_options
        )
        key = (store_root, is_v2_consolidated)
        if key in seen:
            continue
        seen.add(key)
        store_inputs.append((candidate, store_root, is_v2_consolidated))
    return store_inputs


def _resolve_store_root_and_version(path: str, *, storage_options: dict) -> tuple[str, bool, bool]:
    """
    Normalize the user input into a Zarr store root and detect whether it's a v2 consolidated store.

    Supported `path` values:
    - a Zarr root metadata file: `.../.zmetadata` (v2 consolidated) or `.../zarr.json` (v3)
    - a Zarr store root directory: `.../store.zarr` (auto-detect `zarr.json` / `.zmetadata` / `.zgroup`)
    """

    def _endswith_metadata(p: str, suffix: str) -> bool:
        return p.endswith("/" + suffix) or p.endswith("\\" + suffix)

    if _endswith_metadata(path, ".zmetadata"):
        return xdirname(path), True, False
    if _endswith_metadata(path, "zarr.json"):
        return xdirname(path), False, True

    protocol = path.split("://", 1)[0] if "://" in path else "file"
    per_protocol = storage_options.get(protocol, {}) if isinstance(storage_options, dict) else {}

    # Treat paths ending in ".zarr" as store roots, and also accept directories for convenience.
    is_store_root = path.rstrip("/\\").endswith(".zarr")

    from fsspec.core import url_to_fs

    fs, fs_path = url_to_fs(path, **(per_protocol or {}))
    try:
        if fs.isdir(fs_path):
            is_store_root = True
    except Exception:
        pass

    if not is_store_root:
        raise ValueError(
            "Zarr packaged module expects either a Zarr store root directory (usually ending in `.zarr`) or a Zarr "
            "root metadata file:\n"
            "- Zarr store root directory: `.../store.zarr`\n"
            "- Zarr v2 consolidated: `.../store.zarr/.zmetadata`\n"
            "- Zarr v3: `.../store.zarr/zarr.json`\n"
            f"Got: {path}"
        )

    store_root = path.rstrip("/\\")

    # Build candidate paths in the fs namespace.
    fs_root = fs_path.rstrip("/\\") if isinstance(fs_path, str) else fs_path
    cand_v3 = f"{fs_root}/zarr.json"
    cand_v2 = f"{fs_root}/.zmetadata"
    cand_v2_group = f"{fs_root}/.zgroup"

    try:
        if fs.exists(cand_v3):
            return store_root, False, True
        if fs.exists(cand_v2):
            return store_root, True, False
        if fs.exists(cand_v2_group):
            return store_root, False, False
    except Exception:
        pass

    raise ValueError(
        "Zarr store root directory does not contain expected metadata. Looked for:\n"
        f"- {store_root}/zarr.json\n"
        f"- {store_root}/.zmetadata\n"
        f"- {store_root}/.zgroup"
    )


def _infer_primary_num_rows(arrays: dict[str, "zarr.Array"]) -> int:
    n_dim_candidate_lengths = [arr.shape[0] for arr in arrays.values() if len(arr.shape) > 1]
    candidate_lengths = n_dim_candidate_lengths or [arr.shape[0] for arr in arrays.values() if len(arr.shape) > 0]
    if not candidate_lengths:
        raise ValueError("No arrays with at least one dimension were found to infer the row dimension")
    return max(candidate_lengths)


def _select_arrays_by_num_rows(arrays: dict[str, "zarr.Array"], num_rows: int) -> dict[str, "zarr.Array"]:
    return {name: arr for name, arr in arrays.items() if len(arr.shape) > 0 and arr.shape[0] == num_rows}


def _select_arrays_for_features(arrays: dict[str, "zarr.Array"], features: Features) -> dict[str, "zarr.Array"]:
    return {name: arr for name, arr in arrays.items() if name in features}


def _get_axis0_chunk_size(arrays: dict[str, "zarr.Array"]) -> Optional[int]:
    axis0_chunk_sizes = []
    for arr in arrays.values():
        chunks = getattr(arr, "chunks", None)
        if not chunks:
            continue
        axis0_chunk_size = chunks[0]
        if isinstance(axis0_chunk_size, int) and axis0_chunk_size > 0:
            axis0_chunk_sizes.append(axis0_chunk_size)
    if not axis0_chunk_sizes:
        return None
    counts = Counter(axis0_chunk_sizes)
    max_count = max(counts.values())
    return min(size for size, count in counts.items() if count == max_count)


def _generate_row_ranges(
    *,
    num_rows: int,
    arrays: dict[str, "zarr.Array"],
    rows_per_shard: Optional[int],
    target_num_shards: Optional[int],
) -> list[tuple[int, int]]:
    if num_rows == 0:
        return []

    chunk_size_axis0 = _get_axis0_chunk_size(arrays)
    if rows_per_shard is not None:
        shard_rows = rows_per_shard
    elif target_num_shards is not None:
        shard_rows = (num_rows + target_num_shards - 1) // target_num_shards
    elif chunk_size_axis0 is not None:
        shard_rows = chunk_size_axis0
    else:
        shard_rows = num_rows

    if chunk_size_axis0 is not None:
        shard_rows = max(shard_rows, chunk_size_axis0)
        if shard_rows % chunk_size_axis0:
            shard_rows += chunk_size_axis0 - (shard_rows % chunk_size_axis0)

    shard_rows = max(1, shard_rows)
    return [(start, min(start + shard_rows, num_rows)) for start in range(0, num_rows, shard_rows)]


def _get_root_arrays(zgroup) -> dict[str, "zarr.Array"]:
    out = {}
    for name in zgroup.array_keys():
        out[name] = zgroup[name]
    return out


def _np_to_hf_value(dtype: np.dtype) -> Value:
    if dtype.kind in {"O", "U", "S", "T"}:
        return Value("string")
    return Value(dtype=_arrow_to_datasets_dtype(pa.from_numpy_dtype(dtype)))


def _create_sized_feature_impl(shape_tail: tuple[int, ...], value_feature: Value):
    dtype_str = value_feature.dtype
    if any(dim == 0 for dim in shape_tail):
        logger.warning(
            f"Zarr to Arrow: Found an array with shape {shape_tail} and dtype {dtype_str} that has a dimension with size 0. "
            f"Shape information will be lost in the conversion to List({value_feature})."
        )
        return List(value_feature)

    rank = len(shape_tail)
    if rank == 0:
        return value_feature
    elif rank == 1:
        return List(value_feature, length=shape_tail[0])
    elif rank <= 5:
        return {2: Array2D, 3: Array3D, 4: Array4D, 5: Array5D}[rank](shape=shape_tail, dtype=dtype_str)
    else:
        raise TypeError(f"Array{rank}D not supported. Maximum 5 dimensions allowed.")


def _infer_features_from_zarr_arrays(arrays: dict[str, "zarr.Array"]) -> Features:
    features = {}
    for name, arr in arrays.items():
        value_feature = _np_to_hf_value(np.dtype(arr.dtype))
        features[name] = _create_sized_feature_impl(tuple(arr.shape[1:]), value_feature)
    return Features(features)


def _check_array_lengths(arrays: dict[str, "zarr.Array"], features: Features) -> int:
    missing_feature_arrays = [name for name in features if name not in arrays]
    if missing_feature_arrays:
        missing_display = ", ".join(sorted(missing_feature_arrays))
        raise ValueError(f"Missing arrays in Zarr group for configured features: {missing_display}")

    selected_arrays = [(name, arr) for name, arr in arrays.items() if name in features and len(arr.shape) > 0]
    if not selected_arrays:
        raise ValueError("No arrays with at least one dimension were found for the configured features")

    num_rows = selected_arrays[0][1].shape[0]
    for name, arr in selected_arrays:
        if arr.shape[0] != num_rows:
            raise ValueError(f"Array '{name}' has length {arr.shape[0]} but expected {num_rows}")
    return num_rows


def _load_batch(arrays: dict[str, "zarr.Array"], features: Features, start: int, end: int) -> pa.Table:
    batch = {}
    for name, arr in arrays.items():
        if name not in features:
            continue
        np_batch = arr[start:end]
        if np.dtype(arr.dtype).kind in {"O", "U", "S", "T"}:
            batch[name] = pa.array([_to_python_string_or_none(x) for x in np_batch], type=pa.string())
        else:
            batch[name] = datasets.features.features.numpy_to_pyarrow_listarray(np_batch)
    return pa.Table.from_pydict(batch)


def _to_python_string_or_none(value):
    if isinstance(value, np.generic):
        value = value.item()
    if value is None:
        return None
    if isinstance(value, float) and np.isnan(value):
        return None
    if isinstance(value, (bytes, bytearray)):
        return value.decode("utf-8")
    return str(value)
