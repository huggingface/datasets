from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

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
    LargeList,
    List,
    Value,
    _ArrayXD,
    _arrow_to_datasets_dtype,
)
from datasets.table import cast_table_to_features


if TYPE_CHECKING:
    import h5py

logger = datasets.utils.logging.get_logger(__name__)

EXTENSIONS = [".h5", ".hdf5"]


@dataclass
class HDF5Config(datasets.BuilderConfig):
    """BuilderConfig for HDF5."""

    batch_size: Optional[int] = None
    features: Optional[datasets.Features] = None


class HDF5(datasets.ArrowBasedBuilder):
    """ArrowBasedBuilder that converts HDF5 files to Arrow tables using the HF extension types."""

    BUILDER_CONFIG_CLASS = HDF5Config

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        import h5py

        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download(self.config.data_files)
        splits = []
        for split_name, files in data_files.items():
            # Infer features from first file
            if self.info.features is None:
                for first_file in files:
                    with open(first_file, "rb") as f:
                        with h5py.File(f, "r") as h5:
                            self.info.features = _recursive_infer_features(h5)
                    break
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _generate_shards(self, files):
        yield from files

    def _generate_tables(self, files):
        import h5py

        batch_size_cfg = self.config.batch_size
        for file_idx, file in enumerate(files):
            try:
                with open(file, "rb") as f:
                    with h5py.File(f, "r") as h5:
                        # Infer features and lengths from first file
                        if self.info.features is None:
                            self.info.features = _recursive_infer_features(h5)
                        num_rows = _check_dataset_lengths(h5, self.info.features)
                        if num_rows is None:
                            logger.warning(f"File {file} contains no data, skipping...")
                            continue
                        effective_batch = batch_size_cfg or self._writer_batch_size or num_rows
                        for batch_idx, start in enumerate(range(0, num_rows, effective_batch)):
                            end = min(start + effective_batch, num_rows)
                            pa_table = _recursive_load_arrays(h5, self.info.features, start, end)
                            if pa_table is None:
                                logger.warning(f"File {file} contains no data, skipping...")
                                continue
                            yield Key(file_idx, batch_idx), cast_table_to_features(pa_table, self.info.features)
            except ValueError as e:
                logger.error(f"Failed to read file '{file}' with error {type(e)}: {e}")
                raise


# ┌───────────┐
# │  Complex  │
# └───────────┘


def _is_complex_dtype(dtype: np.dtype) -> bool:
    if dtype.kind == "c":
        return True
    if dtype.subdtype is not None:
        return _is_complex_dtype(dtype.subdtype[0])
    return False


def _create_complex_features(dset) -> Features:
    if dset.dtype.subdtype is not None:
        dtype, data_shape = dset.dtype.subdtype
    else:
        data_shape = dset.shape[1:]
        dtype = dset.dtype

    if dtype == np.complex64:
        # two float32s
        value_type = Value("float32")
    elif dtype == np.complex128:
        # two float64s
        value_type = Value("float64")
    else:
        logger.warning(f"Found complex dtype {dtype} that is not supported. Converting to float64...")
        value_type = Value("float64")

    return Features(
        {
            "real": _create_sized_feature_impl(data_shape, value_type),
            "imag": _create_sized_feature_impl(data_shape, value_type),
        }
    )


def _convert_complex_to_nested(arr: np.ndarray) -> pa.StructArray:
    data = {
        "real": datasets.features.features.numpy_to_pyarrow_listarray(arr.real),
        "imag": datasets.features.features.numpy_to_pyarrow_listarray(arr.imag),
    }
    return pa.StructArray.from_arrays([data["real"], data["imag"]], names=["real", "imag"])


# ┌────────────┐
# │  Compound  │
# └────────────┘


def _is_compound_dtype(dtype: np.dtype) -> bool:
    return dtype.kind == "V"


@dataclass
class _CompoundGroup:
    dset: "h5py.Dataset"
    data: np.ndarray = None

    def items(self):
        for field_name in self.dset.dtype.names:
            field_dtype = self.dset.dtype[field_name]
            yield field_name, _CompoundField(self.data, field_name, field_dtype)


@dataclass
class _CompoundField:
    data: Optional[np.ndarray]
    name: str
    dtype: np.dtype
    shape: tuple[int, ...] = field(init=False)

    def __post_init__(self):
        self.shape = (len(self.data) if self.data is not None else 0,) + self.dtype.shape

    def __getitem__(self, key):
        return self.data[key][self.name]


def _create_compound_features(dset) -> Features:
    mock_group = _CompoundGroup(dset)
    return _recursive_infer_features(mock_group)


def _convert_compound_to_nested(arr, dset) -> pa.StructArray:
    mock_group = _CompoundGroup(dset, data=arr)
    features = _create_compound_features(dset)
    return _recursive_load_arrays(mock_group, features, 0, len(arr))


# ┌───────────────────┐
# │  Variable-Length  │
# └───────────────────┘


def _is_vlen_dtype(dtype: np.dtype) -> bool:
    if dtype.metadata and "vlen" in dtype.metadata:
        return True
    return False


def _create_vlen_features(dset) -> Features:
    vlen_dtype = dset.dtype.metadata["vlen"]
    if vlen_dtype in (str, bytes):
        return Value("string")
    inner_feature = _np_to_pa_to_hf_value(vlen_dtype)
    return List(inner_feature)


def _convert_vlen_to_array(arr: np.ndarray) -> pa.Array:
    return datasets.features.features.numpy_to_pyarrow_listarray(arr)


# ┌───────────┐
# │  Generic  │
# └───────────┘


def _recursive_infer_features(h5_obj) -> Features:
    features_dict = {}
    for path, dset in h5_obj.items():
        if _is_group(dset):
            features = _recursive_infer_features(dset)
            if features:
                features_dict[path] = features
        elif _is_dataset(dset):
            features = _infer_feature(dset)
            if features:
                features_dict[path] = features

    return Features(features_dict)


def _infer_feature(dset):
    if _is_complex_dtype(dset.dtype):
        return _create_complex_features(dset)
    elif _is_compound_dtype(dset.dtype) or dset.dtype.kind == "V":
        return _create_compound_features(dset)
    elif _is_vlen_dtype(dset.dtype):
        return _create_vlen_features(dset)
    return _create_sized_feature(dset)


def _load_array(dset, path: str, start: int, end: int) -> pa.Array:
    arr = dset[start:end]

    if _is_vlen_dtype(dset.dtype):
        return _convert_vlen_to_array(arr)
    elif _is_complex_dtype(dset.dtype):
        return _convert_complex_to_nested(arr)
    elif _is_compound_dtype(dset.dtype):
        return _convert_compound_to_nested(arr, dset)
    elif dset.dtype.kind == "O":
        raise ValueError(
            f"Object dtype dataset '{path}' is not supported. "
            f"For variable-length data, please use h5py.vlen_dtype() "
            f"when creating the HDF5 file. "
            f"See: https://docs.h5py.org/en/stable/special.html#variable-length-strings"
        )
    else:
        # If any non-batch dimension is zero, emit an unsized pa.list_
        # to avoid creating FixedSizeListArray with list_size=0.
        if any(dim == 0 for dim in dset.shape[1:]):
            inner_type = pa.from_numpy_dtype(dset.dtype)
            return pa.array([[] for _ in arr], type=pa.list_(inner_type))
        else:
            return datasets.features.features.numpy_to_pyarrow_listarray(arr)


def _recursive_load_arrays(h5_obj, features: Features, start: int, end: int):
    batch_dict = {}
    for path, dset in h5_obj.items():
        if path not in features:
            continue
        if _is_group(dset):
            arr = _recursive_load_arrays(dset, features[path], start, end)
        elif _is_dataset(dset):
            arr = _load_array(dset, path, start, end)
        else:
            raise ValueError(f"Unexpected type {type(dset)}")

        if arr is not None:
            batch_dict[path] = arr

    if _is_file(h5_obj):
        return pa.Table.from_pydict(batch_dict)

    if batch_dict:
        should_chunk, keys, values = False, [], []
        for k, v in batch_dict.items():
            if isinstance(v, pa.ChunkedArray):
                should_chunk = True
                v = v.combine_chunks()
            keys.append(k)
            values.append(v)

        sarr = pa.StructArray.from_arrays(values, names=keys)
        return pa.chunked_array(sarr) if should_chunk else sarr


# ┌─────────────┐
# │  Utilities  │
# └─────────────┘


def _create_sized_feature(dset):
    dset_shape = dset.shape[1:]
    value_feature = _np_to_pa_to_hf_value(dset.dtype)
    return _create_sized_feature_impl(dset_shape, value_feature)


def _create_sized_feature_impl(dset_shape, value_feature):
    dtype_str = value_feature.dtype
    if any(dim == 0 for dim in dset_shape):
        logger.warning(
            f"HDF5 to Arrow: Found a dataset with shape {dset_shape} and dtype {dtype_str} that has a dimension with size 0. Shape information will be lost in the conversion to List({value_feature})."
        )
        return List(value_feature)

    rank = len(dset_shape)
    if rank == 0:
        return value_feature
    elif rank == 1:
        return List(value_feature, length=dset_shape[0])
    elif rank <= 5:
        return _sized_arrayxd(rank)(shape=dset_shape, dtype=dtype_str)
    else:
        raise TypeError(f"Array{rank}D not supported. Maximum 5 dimensions allowed.")


def _sized_arrayxd(rank: int):
    return {2: Array2D, 3: Array3D, 4: Array4D, 5: Array5D}[rank]


def _np_to_pa_to_hf_value(numpy_dtype: np.dtype) -> Value:
    return Value(dtype=_arrow_to_datasets_dtype(pa.from_numpy_dtype(numpy_dtype)))


def _first_dataset(h5_obj, features: Features, prefix=""):
    for path, dset in h5_obj.items():
        if path not in features:
            continue
        if _is_group(dset):
            found = _first_dataset(dset, features[path], prefix=f"{prefix}{path}/")
            if found is not None:
                return found
        elif _is_dataset(dset):
            return f"{prefix}{path}"


def _check_dataset_lengths(h5_obj, features: Features) -> int:
    first_path = _first_dataset(h5_obj, features)
    if first_path is None:
        return None

    num_rows = h5_obj[first_path].shape[0]
    for path, dset in h5_obj.items():
        if path not in features:
            continue
        if _is_dataset(dset):
            if dset.shape[0] != num_rows:
                raise ValueError(f"Dataset '{path}' has length {dset.shape[0]} but expected {num_rows}")
    return num_rows


def _is_group(h5_obj) -> bool:
    import h5py

    return isinstance(h5_obj, h5py.Group) or isinstance(h5_obj, _CompoundGroup)


def _is_dataset(h5_obj) -> bool:
    import h5py

    return isinstance(h5_obj, h5py.Dataset) or isinstance(h5_obj, _CompoundField)


def _is_file(h5_obj) -> bool:
    import h5py

    return isinstance(h5_obj, h5py.File)


def _has_zero_dimensions(feature):
    if isinstance(feature, _ArrayXD):
        return any(dim == 0 for dim in feature.shape)
    elif isinstance(feature, List):
        return feature.length == 0 or _has_zero_dimensions(feature.feature)
    elif isinstance(feature, LargeList):
        return _has_zero_dimensions(feature.feature)
    else:
        return False
