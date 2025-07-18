import itertools
from dataclasses import dataclass
from typing import Dict, List, Optional

import h5py
import numpy as np
import pyarrow as pa

import datasets
from datasets.features.features import LargeList, Sequence, _ArrayXD
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)

EXTENSIONS = [".h5", ".hdf5"]


@dataclass
class HDF5Config(datasets.BuilderConfig):
    """BuilderConfig for HDF5."""

    batch_size: Optional[int] = None
    columns: Optional[List[str]] = None
    features: Optional[datasets.Features] = None

    def __post_init__(self):
        super().__post_init__()


class HDF5(datasets.ArrowBasedBuilder):
    """ArrowBasedBuilder that converts HDF5 files to Arrow tables using the HF extension types."""

    BUILDER_CONFIG_CLASS = HDF5Config

    def _info(self):
        if (
            self.config.columns is not None
            and self.config.features is not None
            and set(self.config.columns) != set(self.config.features)
        ):
            raise ValueError(
                "The columns and features argument must contain the same columns, but got ",
                f"{self.config.columns} and {self.config.features}",
            )
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        data_files = dl_manager.download_and_extract(self.config.data_files)
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]

            files = [dl_manager.iter_files(file) for file in files]
            # Infer features from first file
            if self.info.features is None:
                for first_file in itertools.chain.from_iterable(files):
                    with h5py.File(first_file, "r") as h5:
                        dataset_map = _traverse_datasets(h5)
                        features_dict = {}
                        for path, dset in dataset_map.items():
                            feat = _infer_feature_from_dataset(dset)
                            features_dict[path] = feat
                        self.info.features = datasets.Features(features_dict)
                    break
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        if self.config.columns is not None and set(self.config.columns) != set(self.info.features):
            self.info.features = datasets.Features(
                {col: feat for col, feat in self.info.features.items() if col in self.config.columns}
            )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            has_zero_dims = any(has_zero_dimensions(feature) for feature in self.info.features.values())
            if not has_zero_dims:
                pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_tables(self, files):
        batch_size_cfg = self.config.batch_size
        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            with h5py.File(file, "r") as h5:
                dataset_map = _traverse_datasets(h5)
                if not dataset_map:
                    logger.warning(f"File '{file}' contains no datasets, skipping…")
                    continue
                first_dset = next(iter(dataset_map.values()))
                num_rows = first_dset.shape[0]
                # Sanity-check lengths
                for path, dset in dataset_map.items():
                    if dset.shape[0] != num_rows:
                        raise ValueError(
                            f"Dataset '{path}' length {dset.shape[0]} differs from {num_rows} in file '{file}'"
                        )
                effective_batch = batch_size_cfg or self._writer_batch_size or num_rows
                for start in range(0, num_rows, effective_batch):
                    end = min(start + effective_batch, num_rows)
                    batch_dict = {}
                    for path, dset in dataset_map.items():
                        if self.config.columns is not None and path not in self.config.columns:
                            continue
                        arr = dset[start:end]
                        pa_arr = datasets.features.features.numpy_to_pyarrow_listarray(arr)
                        batch_dict[path] = pa_arr
                    pa_table = pa.Table.from_pydict(batch_dict)
                    yield f"{file_idx}_{start}", self._cast_table(pa_table)


def _traverse_datasets(h5_obj, prefix: str = "") -> Dict[str, h5py.Dataset]:
    mapping: Dict[str, h5py.Dataset] = {}
    for key in h5_obj:
        item = h5_obj[key]
        sub_path = f"{prefix}{key}"
        if isinstance(item, h5py.Dataset):
            mapping[sub_path] = item
        elif isinstance(item, h5py.Group):
            mapping.update(_traverse_datasets(item, prefix=f"{sub_path}/"))
    return mapping


_DTYPE_TO_DATASETS: Dict[np.dtype, str] = {  # FIXME: necessary/check if util exists?
    np.dtype("bool").newbyteorder("="): "bool",
    np.dtype("int8").newbyteorder("="): "int8",
    np.dtype("int16").newbyteorder("="): "int16",
    np.dtype("int32").newbyteorder("="): "int32",
    np.dtype("int64").newbyteorder("="): "int64",
    np.dtype("uint8").newbyteorder("="): "uint8",
    np.dtype("uint16").newbyteorder("="): "uint16",
    np.dtype("uint32").newbyteorder("="): "uint32",
    np.dtype("uint64").newbyteorder("="): "uint64",
    np.dtype("float16").newbyteorder("="): "float16",
    np.dtype("float32").newbyteorder("="): "float32",
    np.dtype("float64").newbyteorder("="): "float64",
    # np.dtype("complex64").newbyteorder("="): "complex64",
    # np.dtype("complex128").newbyteorder("="): "complex128",
}


def _dtype_to_dataset_dtype(dtype: np.dtype) -> str:
    """Map NumPy dtype to datasets.Value dtype string, falls back to "binary" for unknown or unsupported dtypes."""

    # FIXME: endian fix necessary/correct?
    base_dtype = dtype.newbyteorder("=")
    if base_dtype in _DTYPE_TO_DATASETS:
        return _DTYPE_TO_DATASETS[base_dtype]

    if base_dtype.kind in {"S", "a"}:
        return "binary"

    # FIXME: seems h5 converts unicode back to bytes?
    if base_dtype.kind == "U":
        return "binary"

    if base_dtype.kind == "O":
        return "binary"

    # FIXME: support varlen?

    return "binary"


def _infer_feature_from_dataset(dset: h5py.Dataset):
    """Infer a ``datasets.Features`` entry for one HDF5 dataset."""

    import datasets as hfd

    dtype_str = _dtype_to_dataset_dtype(dset.dtype)
    value_shape = dset.shape[1:]

    # Reject ragged datasets (variable-length or None dims)
    if dset.dtype.kind == "O" or any(s is None for s in value_shape):
        raise ValueError(f"Ragged dataset {dset.name} with shape {value_shape} and dtype {dset.dtype} not supported")

    if dset.dtype.kind not in {"b", "i", "u", "f", "S", "a"}:
        raise ValueError(f"Unsupported dtype {dset.dtype} for dataset {dset.name}")

    rank = len(value_shape)
    if 2 <= rank <= 5:
        from datasets.features import Array2D, Array3D, Array4D, Array5D

        array_cls = [None, None, Array2D, Array3D, Array4D, Array5D][rank]
        return array_cls(shape=value_shape, dtype=dtype_str)

    # Fallback to nested Sequence
    def _build_feature(shape: tuple[int, ...]):
        if len(shape) == 0:
            return hfd.Value(dtype_str)
        return hfd.Sequence(length=shape[0], feature=_build_feature(shape[1:]))

    return _build_feature(value_shape)


def has_zero_dimensions(feature: _ArrayXD | Sequence | LargeList):
    if isinstance(feature, _ArrayXD):
        return any(dim == 0 for dim in feature.shape)
    elif isinstance(feature, (Sequence, LargeList)):
        return feature.length == 0 or has_zero_dimensions(feature.feature)
    else:
        return False
