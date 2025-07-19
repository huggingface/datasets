import itertools
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pyarrow as pa

import datasets
import h5py
from datasets.features.features import (
    Array2D,
    Array3D,
    Array4D,
    Array5D,
    LargeList,
    Sequence,
    Value,
    _ArrayXD,
    _arrow_to_datasets_dtype,
)
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
            has_zero_dims = any(_has_zero_dimensions(feature) for feature in self.info.features.values())
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
                        if _is_ragged_dataset(dset):
                            if _is_variable_length_string(dset):
                                pa_arr = _variable_length_string_to_pyarrow(arr, dset)
                            else:
                                pa_arr = _ragged_array_to_pyarrow_largelist(arr, dset)
                        else:
                            pa_arr = datasets.features.features.numpy_to_pyarrow_listarray(arr)  # NOTE: type=None
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


def _base_dtype(dtype):
    if hasattr(dtype, "metadata") and dtype.metadata and "vlen" in dtype.metadata:
        return dtype.metadata["vlen"]
    if hasattr(dtype, "subdtype") and dtype.subdtype is not None:
        return _base_dtype(dtype.subdtype[0])
    return dtype


def _ragged_array_to_pyarrow_largelist(arr: np.ndarray, dset: h5py.Dataset) -> pa.Array:
    if _is_variable_length_string(dset):
        list_of_strings = []
        for item in arr:
            if item is None:
                list_of_strings.append(None)
            else:
                if isinstance(item, bytes):
                    item = item.decode("utf-8")
                list_of_strings.append(item)
        return datasets.features.features.list_of_pa_arrays_to_pyarrow_listarray(
            [pa.array([item]) if item is not None else None for item in list_of_strings]
        )
    else:
        return _convert_nested_ragged_array_recursive(arr, dset.dtype)


def _convert_nested_ragged_array_recursive(arr: np.ndarray, dtype):
    if hasattr(dtype, "subdtype") and dtype.subdtype is not None:
        inner_dtype = dtype.subdtype[0]
        list_of_arrays = []
        for item in arr:
            if item is None:
                list_of_arrays.append(None)
            else:
                inner_array = _convert_nested_ragged_array_recursive(item, inner_dtype)
                list_of_arrays.append(inner_array)
        return datasets.features.features.list_of_pa_arrays_to_pyarrow_listarray(
            [pa.array(item) if item is not None else None for item in list_of_arrays]
        )
    else:
        list_of_arrays = []
        for item in arr:
            if item is None:
                list_of_arrays.append(None)
            else:
                if not isinstance(item, np.ndarray):
                    item = np.array(item, dtype=dtype)
                list_of_arrays.append(item)
        return datasets.features.features.list_of_pa_arrays_to_pyarrow_listarray(
            [pa.array(item) if item is not None else None for item in list_of_arrays]
        )


def _infer_feature_from_dataset(dset: h5py.Dataset):
    if _is_variable_length_string(dset):
        return Value("string")  # FIXME: large_string?

    if _is_ragged_dataset(dset):
        return _infer_nested_feature_recursive(dset.dtype, dset)

    value_feature = _np_to_pa_to_hf_value(dset.dtype)
    dtype_str = value_feature.dtype
    value_shape = dset.shape[1:]

    if dset.dtype.kind not in {"b", "i", "u", "f", "S", "a"}:
        raise TypeError(f"Unsupported dtype {dset.dtype} for dataset {dset.name}")

    rank = len(value_shape)
    if rank == 0:
        return value_feature
    elif rank == 1:
        return Sequence(value_feature, length=value_shape[0])
    elif 2 <= rank <= 5:
        return _sized_arrayxd(rank)(shape=value_shape, dtype=dtype_str)
    else:
        raise TypeError(f"Array{rank}D not supported. Only up to 5D arrays are supported.")


def _infer_nested_feature_recursive(dtype, dset: h5py.Dataset):
    if hasattr(dtype, "subdtype") and dtype.subdtype is not None:
        inner_dtype = dtype.subdtype[0]
        inner_feature = _infer_nested_feature_recursive(inner_dtype, dset)
        return Sequence(inner_feature)
    else:
        if hasattr(dtype, "kind") and dtype.kind == "O":
            if _is_variable_length_string(dset):
                base_dtype = np.dtype("S1")
            else:
                base_dtype = _base_dtype(dset.dtype)
            return Sequence(_np_to_pa_to_hf_value(base_dtype))
        else:
            return _np_to_pa_to_hf_value(dtype)


def _has_zero_dimensions(feature):
    if isinstance(feature, _ArrayXD):
        return any(dim == 0 for dim in feature.shape)
    elif isinstance(feature, (Sequence, LargeList)):
        return feature.length == 0 or _has_zero_dimensions(feature.feature)
    else:
        return False


def _sized_arrayxd(rank: int):
    return {2: Array2D, 3: Array3D, 4: Array4D, 5: Array5D}[rank]


def _np_to_pa_to_hf_value(numpy_dtype: np.dtype) -> Value:
    return Value(dtype=_arrow_to_datasets_dtype(pa.from_numpy_dtype(numpy_dtype)))


def _is_ragged_dataset(dset: h5py.Dataset) -> bool:
    return dset.dtype.kind == "O" and hasattr(dset.dtype, "subdtype")


def _is_variable_length_string(dset: h5py.Dataset) -> bool:
    if not _is_ragged_dataset(dset) or dset.shape[0] == 0:
        return False
    num_samples = min(3, dset.shape[0])
    for i in range(num_samples):
        try:
            if isinstance(dset[i], (str, bytes)):
                return True
        except (IndexError, TypeError):
            continue
    return False


def _variable_length_string_to_pyarrow(arr: np.ndarray, dset: h5py.Dataset) -> pa.Array:
    list_of_strings = []
    for item in arr:
        if isinstance(item, bytes):
            item = item.decode("utf-8")
        list_of_strings.append(item)
    return pa.array(list_of_strings)
