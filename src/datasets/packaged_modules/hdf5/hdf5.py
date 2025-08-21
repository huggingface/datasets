import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Optional
from typing import List as ListT

import numpy as np
import pyarrow as pa

import datasets
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
from datasets.table import table_cast


if TYPE_CHECKING:
    import h5py

logger = datasets.utils.logging.get_logger(__name__)

EXTENSIONS = [".h5", ".hdf5"]


@dataclass
class HDF5Config(datasets.BuilderConfig):
    """BuilderConfig for HDF5."""

    batch_size: Optional[int] = None
    columns: Optional[ListT[str]] = None
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
        import h5py

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
                        self.info.features = _recursive_infer_features(h5)
                    break
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        if self.config.columns is not None and set(self.config.columns) != set(self.info.features):
            self.info.features = datasets.Features(
                {col: feat for col, feat in self.info.features.items() if col in self.config.columns}
            )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_tables(self, files):
        import h5py

        batch_size_cfg = self.config.batch_size
        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            try:
                with h5py.File(file, "r") as h5:
                    if self.info.features is None:
                        self.info.features = _recursive_infer_features(h5)
                    num_rows = _check_dataset_lengths(h5, self.info.features)
                    if num_rows is None:
                        logger.warning(f"File {file} contains no data, skipping...")
                        continue
                    effective_batch = batch_size_cfg or self._writer_batch_size or num_rows
                    for start in range(0, num_rows, effective_batch):
                        end = min(start + effective_batch, num_rows)
                        pa_table = _recursive_load_data(h5, self.info.features, start, end)
                        yield f"{file_idx}_{start}", self._cast_table(pa_table)
            except ValueError as e:
                logger.error(f"Failed to read file '{file}' with error {type(e)}: {e}")
                raise


# ┌───────────┐
# │  Complex  │
# └───────────┘


def _is_complex_dtype(dtype: np.dtype) -> bool:
    """Check if dtype is a complex number type."""
    return dtype.kind == "c"


def _create_complex_features(dset: "h5py.Dataset") -> Dict[str, Features]:
    """Create Features for complex data with real and imaginary parts `real` and `imag`.

    NOTE: Always uses float64 for the real and imaginary parts.
    """
    logger.info(
        f"Complex dataset '{dset.name}' (dtype: {dset.dtype}) represented as nested structure with 'real' and 'imag' fields"
    )
    
    dset_shape = dset.shape[1:]
    rank = len(dset_shape)

    if rank == 0:
        return Features({"real": Value("float64"), "imag": Value("float64")})
    elif rank == 1:
        return Features({
            "real": List(Value("float64"), length=dset_shape[0]),
            "imag": List(Value("float64"), length=dset_shape[0])
        })
    elif rank <= 5:
        array_feature = _sized_arrayxd(rank)
        return Features({
            "real": array_feature(shape=dset_shape, dtype="float64"),
            "imag": array_feature(shape=dset_shape, dtype="float64")
        })
    else:
        raise TypeError(f"Complex Array{rank}D not supported. Maximum 5 dimensions allowed.")


def _convert_complex_to_nested(arr: np.ndarray) -> Dict[str, pa.Array]:
    """Convert complex to Features with real and imaginary parts `real` and `imag`."""
    if arr.size > 1:
        data = {
            "real": datasets.features.features.numpy_to_pyarrow_listarray(arr.real),
            "imag": datasets.features.features.numpy_to_pyarrow_listarray(arr.imag)
        }
    else:
        data = {"real": float(arr.item().real), "imag": float(arr.item().imag)}

    return pa.StructArray.from_arrays(data.values(), names=data.keys())


# ┌────────────┐
# │  Compound  │
# └────────────┘


def _is_compound_dtype(dtype: np.dtype) -> bool:
    """Check if dtype is a compound/structured type."""
    return dtype.names is not None


class _MockDataset:
    def __init__(self, dtype, name):
        self.dtype = dtype
        self.name = name


def _create_compound_features(dset: "h5py.Dataset") -> Dict[str, Features]:
    """Create nested features for compound data with field names as keys."""
    field_names = list(dset.dtype.names)
    logger.info(
        f"Compound dataset '{dset.name}' (dtype: {dset.dtype}) represented as nested Features with fields: {field_names}"
    )

    nested_features_dict = {}
    for field_name in field_names:
        field_dtype = dset.dtype[field_name]

        if _is_complex_dtype(field_dtype):
            nested_features_dict[field_name] = Features(
                {
                    "real": Value("float64"),
                    "imag": Value("float64"),
                }
            )
        elif _is_compound_dtype(field_dtype):
            mock_dset = _MockDataset(field_dtype, f"subfield {field_name} of {dset.name}")
            nested_features_dict[field_name] = _create_compound_features(mock_dset)
        else:
            nested_features_dict[field_name] = _np_to_pa_to_hf_value(field_dtype)

    return Features(nested_features_dict)


def _convert_compound_to_nested(arr: np.ndarray, dset: "h5py.Dataset") -> Dict[str, pa.Array]:
    """Convert compound array to nested structure with field names as keys."""
    def _convert_compound_recursive(compound_arr, compound_dtype):
        """Recursively convert compound array to nested structure."""
        nested_data = []
        for row in compound_arr:
            row_dict = {}
            for field_name in compound_dtype.names:
                field_dtype = compound_dtype[field_name]
                field_data = row[field_name]

                if _is_complex_dtype(field_dtype):
                    row_dict[field_name] = {"real": float(field_data.real), "imag": float(field_data.imag)}
                elif _is_compound_dtype(field_dtype):
                    row_dict[field_name] = _convert_compound_recursive([field_data], field_dtype)[0]
                else:
                    row_dict[field_name] = field_data.item() if field_data.size == 1 else field_data.tolist()
            nested_data.append(row_dict)
        return nested_data
    return pa.array(_convert_compound_recursive(arr, dset.dtype))


# ┌───────────────────────────┐
# │  Variable-Length Strings  │
# └───────────────────────────┘


def _is_vlen_string_dtype(dtype: np.dtype) -> bool:
    """Check if dtype is a variable-length string type."""
    if hasattr(dtype, "metadata") and dtype.metadata and "vlen" in dtype.metadata:
        vlen_dtype = dtype.metadata["vlen"]
        return vlen_dtype in (str, bytes)
    return False


def _is_vlen_not_string_dtype(dtype: np.dtype) -> bool:
    if hasattr(dtype, "metadata") and dtype.metadata and "vlen" in dtype.metadata:
        vlen_dtype = dtype.metadata["vlen"]
        return vlen_dtype not in (str, bytes)
    return False


def _convert_vlen_string_to_array(arr: np.ndarray) -> pa.Array:
    list_of_items = []
    for item in arr:
        if isinstance(item, bytes):
            logger.info("Assuming variable-length bytes are utf-8 encoded strings")
            list_of_items.append(item.decode("utf-8"))
        elif isinstance(item, str):
            list_of_items.append(item)
        else:
            raise ValueError(f"Unsupported variable-length string type: {type(item)}")
    return pa.array(list_of_items)


# ┌───────────┐
# │  Generic  │
# └───────────┘


def _recursive_infer_features(h5_obj) -> Features:
    import h5py

    features_dict = {}
    for path, dset in h5_obj.items():
        if isinstance(dset, h5py.Group):
            features_dict[path] = _recursive_infer_features(dset)
        elif isinstance(dset, h5py.Dataset):
            features_dict[path] = _infer_feature(dset)
    return Features(features_dict)

def _infer_feature(dset: "h5py.Dataset"):
    if _is_complex_dtype(dset.dtype):
        return _create_complex_features(dset)
    elif _is_compound_dtype(dset.dtype):
        return _create_compound_features(dset)
    elif _is_vlen_string_dtype(dset.dtype):
        return Value("string")
    elif _is_vlen_not_string_dtype(dset.dtype):
        vlen_dtype = dset.dtype.metadata["vlen"]
        inner_feature = _np_to_pa_to_hf_value(vlen_dtype)
        return List(inner_feature)

    value_feature = _np_to_pa_to_hf_value(dset.dtype)
    dtype_str = value_feature.dtype

    dset_shape = dset.shape[1:]
    if any(dim == 0 for dim in dset_shape):
        logger.warning(
            f"HDF5 to Arrow: Found a dataset named '{dset.name}' with shape {dset_shape} and dtype {dtype_str} that has a dimension with size 0. Shape information will be lost in the conversion to List({value_feature})."
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


def _load_array(dset: "h5py.Dataset", path: str, start: int, end: int) -> Dict[str, any]:
    arr = dset[start:end]

    if _is_vlen_string_dtype(dset.dtype):
        logger.debug(
            f"Converting variable-length string data for '{path}' (shape: {arr.shape})"
        )
        return _convert_vlen_string_to_array(arr)
    elif _is_vlen_not_string_dtype(dset.dtype):
        return datasets.features.features.numpy_to_pyarrow_listarray(arr)
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

def _recursive_load_data(h5_obj, features: Features, start: int, end: int):
    import h5py

    batch_dict = {}
    for path, dset in h5_obj.items():
        if path not in features:
            print(f"skipping {path} not in features: {features}")
            continue
        else:
            print(f"checked {path} in features: {features}")
        if isinstance(dset, h5py.Group):
            batch_dict[path] = _recursive_load_data(dset, features[path], start, end)
        elif isinstance(dset, h5py.Dataset):
            batch_dict[path] = _load_array(dset, path, start, end)

    if isinstance(h5_obj, h5py.File):
        return pa.Table.from_pydict(batch_dict)
    else:
        return pa.StructArray.from_arrays(batch_dict.values(), names=batch_dict.keys())


# ┌─────────────┐
# │  Utilities  │
# └─────────────┘

def _has_zero_dimensions(feature):
    if isinstance(feature, _ArrayXD):
        return any(dim == 0 for dim in feature.shape)
    elif isinstance(feature, List):  # also gets regular List
        return feature.length == 0 or _has_zero_dimensions(feature.feature)
    elif isinstance(feature, LargeList):
        return _has_zero_dimensions(feature.feature)
    else:
        return False


def _sized_arrayxd(rank: int):
    return {2: Array2D, 3: Array3D, 4: Array4D, 5: Array5D}[rank]


def _np_to_pa_to_hf_value(numpy_dtype: np.dtype) -> Value:
    return Value(dtype=_arrow_to_datasets_dtype(pa.from_numpy_dtype(numpy_dtype)))

def _first_nongroup_dataset(h5_obj, features: Features, prefix="") -> str:
    import h5py
    
    for path, dset in h5_obj.items():
        if path not in features:
            continue
        if isinstance(dset, h5py.Group):
            return _first_nongroup_dataset(dset, features[path], prefix=f"{path}/")
        elif isinstance(dset, h5py.Dataset):
            return f"{prefix}{path}"

def _check_dataset_lengths(h5_obj, features: Features) -> int:
    import h5py

    first_path = _first_nongroup_dataset(h5_obj, features)
    if first_path is None:
        return None

    num_rows = h5_obj[first_path].shape[0]
    for path, dset in h5_obj.items():
        if path not in features:
            continue
        if isinstance(dset, h5py.Dataset):
            if dset.shape[0] != num_rows:
                raise ValueError(f"Dataset '{path}' has length {dset.shape[0]} but expected {num_rows}")
    return num_rows