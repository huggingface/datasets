from dataclasses import dataclass
from typing import Optional

import numpy as np
import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.features.features import Array2D, Array3D, Array4D, Array5D, Features, List, Value, _arrow_to_datasets_dtype
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
    - Pass the path(s) to a Zarr root metadata file via `data_files`:
      - Zarr v2 (consolidated): `.zmetadata`
      - Zarr v3: `zarr.json`
    - Nested groups are not yet supported (only arrays at the selected group root).
    """

    batch_size: Optional[int] = None
    features: Optional[datasets.Features] = None
    group: Optional[str] = None
    consolidated: bool = True


class Zarr(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = ZarrConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        data_files = dl_manager.download(self.config.data_files)
        storage_options = dl_manager.download_config.storage_options or {}

        splits = []
        for split_name, metadata_files in data_files.items():
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={"metadata_files": metadata_files, "storage_options": storage_options},
                )
            )
        return splits

    def _generate_shards(self, metadata_files, storage_options):
        yield from metadata_files

    def _generate_tables(self, metadata_files, storage_options):
        zarr = _require_zarr()

        batch_size_cfg = self.config.batch_size
        group_path = self.config.group

        for store_idx, metadata_file in enumerate(metadata_files):
            metadata_file = str(metadata_file)
            is_v2_consolidated = metadata_file.endswith("/.zmetadata") or metadata_file.endswith("\\.zmetadata")
            is_v3_root = metadata_file.endswith("/zarr.json") or metadata_file.endswith("\\zarr.json")
            if not (is_v2_consolidated or is_v3_root):
                raise ValueError(
                    "Zarr packaged module expects a Zarr root metadata file. Supported values:\n"
                    "- Zarr v2 consolidated: `.zmetadata`\n"
                    "- Zarr v3: `zarr.json`\n"
                    f"Got: {metadata_file}"
                )

            store_root = xdirname(metadata_file)
            mapper = _get_fsspec_mapper(store_root, storage_options)

            if is_v2_consolidated and self.config.consolidated:
                zgroup = zarr.open_consolidated(store=mapper, mode="r")
            else:
                zgroup = zarr.open_group(store=mapper, mode="r")

            if group_path:
                zgroup = zgroup[group_path]

            arrays = _get_root_arrays(zgroup)
            if not arrays:
                raise ValueError(f"No arrays found in Zarr group at '{store_root}'")

            if self.info.features is None:
                self.info.features = _infer_features_from_zarr_arrays(arrays)

            num_rows = _check_array_lengths(arrays, self.info.features)
            effective_batch = batch_size_cfg or self._writer_batch_size or num_rows

            for batch_idx, start in enumerate(range(0, num_rows, effective_batch)):
                end = min(start + effective_batch, num_rows)
                pa_table = _load_batch(arrays, self.info.features, start, end)
                yield Key(store_idx, batch_idx), cast_table_to_features(pa_table, self.info.features)


ZarrDatasetBuilder = Zarr


def _require_zarr():
    try:
        import zarr  # type: ignore
    except Exception as e:  # pragma: no cover
        raise ImportError(
            "Using the packaged module `zarr` requires the optional dependency `zarr`.\n"
            "Install it with: `pip install \"datasets[zarr]\"` (or `pip install zarr`)"
        ) from e
    return zarr


def _get_fsspec_mapper(store_root: str, storage_options: dict):
    import fsspec

    protocol = store_root.split("://", 1)[0] if "://" in store_root else "file"
    per_protocol = storage_options.get(protocol, {}) if isinstance(storage_options, dict) else {}
    return fsspec.get_mapper(store_root, **(per_protocol or {}))


def _get_root_arrays(zgroup) -> dict[str, "zarr.Array"]:
    out = {}
    for name in zgroup.array_keys():
        out[name] = zgroup[name]
    return out


def _np_to_hf_value(dtype: np.dtype) -> Value:
    if dtype.kind in {"O", "U", "S"}:
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
    first = next(iter(arrays))
    num_rows = arrays[first].shape[0]
    for name, arr in arrays.items():
        if name not in features:
            continue
        if arr.shape[0] != num_rows:
            raise ValueError(f"Array '{name}' has length {arr.shape[0]} but expected {num_rows}")
    return num_rows


def _load_batch(arrays: dict[str, "zarr.Array"], features: Features, start: int, end: int) -> pa.Table:
    batch = {}
    for name, arr in arrays.items():
        if name not in features:
            continue
        np_batch = arr[start:end]
        if np.dtype(arr.dtype).kind in {"O", "U", "S"}:
            batch[name] = pa.array([x.decode("utf-8") if isinstance(x, (bytes, bytearray)) else str(x) for x in np_batch])
        else:
            batch[name] = datasets.features.features.numpy_to_pyarrow_listarray(np_batch)
    return pa.Table.from_pydict(batch)

