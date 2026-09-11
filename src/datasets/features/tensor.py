# Copyright 2026 The HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""NumPy tensors backed by Arrow tensor extensions."""

import base64
import json
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pyarrow as pa
from pandas.api.extensions import ExtensionDtype


def _normalize_shape(shape, allow_unknown_dims=False):
    if not isinstance(shape, (tuple, list, np.ndarray)):
        raise ValueError(f"Invalid Tensor shape: {shape!r}")
    if any(
        not (dim is None and allow_unknown_dims)
        and (isinstance(dim, (bool, np.bool_)) or not isinstance(dim, (int, np.integer)) or not 0 <= dim <= 2**31 - 1)
        for dim in shape
    ):
        raise ValueError(f"Invalid Tensor shape: {shape!r}; dimensions must be nonnegative integers")
    return tuple(int(dim) if dim is not None else None for dim in shape)


class VariableShapeTensorType(pa.ExtensionType):
    """Python representation of the variable tensor layout.

    Data is flattened in C order. Absent permutation and dimension names mean
    identity order and unnamed dimensions. uniform_shape constrains the
    rank and any known dimensions.

    The canonical storage is struct<data: list<value_type>,
    shape: fixed_size_list<int32>[ndim]>. Arrow 25 provides the C++ reader but
    no Python constructor, so this class implements its Python representation.
    """

    def __init__(self, value_type, uniform_shape=None, *, ndim=None, permutation=None, dim_names=None):
        self.value_type = value_type
        self.uniform_shape = (
            _normalize_shape(uniform_shape, allow_unknown_dims=True) if uniform_shape is not None else None
        )
        if ndim is None and self.uniform_shape is not None:
            ndim = len(self.uniform_shape)
        if isinstance(ndim, (bool, np.bool_)) or not isinstance(ndim, (int, np.integer)) or not 0 <= ndim <= 2**31 - 1:
            raise ValueError("Tensor ndim must be a nonnegative integer; provide a shape with None entries or ndim=")
        self.ndim = int(ndim)
        self.permutation = permutation
        self.dim_names = dim_names
        if self.uniform_shape is not None and len(self.uniform_shape) != self.ndim:
            raise ValueError("Tensor uniform_shape must match the storage rank")
        shape_type = pa.list_(pa.int32(), self.ndim)
        storage_type = pa.struct([("data", pa.list_(value_type)), ("shape", shape_type)])
        super().__init__(storage_type, "arrow.variable_shape_tensor")

    def __arrow_ext_serialize__(self):
        metadata = {}
        if self.permutation is not None:
            metadata["permutation"] = self.permutation
        if self.dim_names is not None:
            metadata["dim_names"] = self.dim_names
        if self.uniform_shape is not None:
            metadata["uniform_shape"] = self.uniform_shape
        return json.dumps(metadata, separators=(",", ":")).encode()

    @classmethod
    def __arrow_ext_deserialize__(cls, storage_type, serialized):
        metadata = json.loads(serialized)
        if not isinstance(storage_type, pa.StructType) or storage_type.names != ["data", "shape"]:
            raise ValueError(f"Unsupported Tensor storage type: {storage_type}")
        data_type = storage_type.field("data").type
        shape_type = storage_type.field("shape").type
        if not pa.types.is_list(data_type) or not (
            pa.types.is_fixed_size_list(shape_type) and shape_type.value_type == pa.int32()
        ):
            raise ValueError(f"Unsupported Tensor storage type: {storage_type}")
        return cls(
            data_type.value_type,
            metadata.get("uniform_shape"),
            ndim=shape_type.list_size,
            permutation=metadata.get("permutation"),
            dim_names=metadata.get("dim_names"),
        )

    def __eq__(self, other):
        if not is_tensor_type(other) or other.extension_name != self.extension_name:
            return NotImplemented
        other = normalize_tensor_type(other)
        # Arrow delegates schema and array type equality to this method.
        # Storage alone only describes value_type and rank.
        return self.storage_type == other.storage_type and json.loads(self.__arrow_ext_serialize__()) == json.loads(
            other.__arrow_ext_serialize__()
        )

    def __ne__(self, other):
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    def __reduce__(self):
        return self.__arrow_ext_deserialize__, (self.storage_type, self.__arrow_ext_serialize__())


# Arrow 25 registers the C++ canonical type even without exposing a Python
# constructor. Register the Python representation of the same canonical layout.
try:
    pa.register_extension_type(VariableShapeTensorType(pa.float32(), ndim=1))
except pa.ArrowKeyError:
    pa.unregister_extension_type("arrow.variable_shape_tensor")
    pa.register_extension_type(VariableShapeTensorType(pa.float32(), ndim=1))


def is_tensor_type(arrow_type):
    return isinstance(arrow_type, pa.BaseExtensionType) and arrow_type.extension_name in (
        "arrow.fixed_shape_tensor",
        "arrow.variable_shape_tensor",
    )


def normalize_tensor_type(arrow_type):
    """Recover parameters even for a C++ type read before Datasets was imported."""
    if isinstance(arrow_type, (pa.FixedShapeTensorType, VariableShapeTensorType)):
        return arrow_type
    if is_tensor_type(arrow_type):
        # BaseExtensionType has no Python metadata accessor in Arrow 25.
        # IPC preserves the canonical serialized metadata; read it through the
        # registered deserializer to recover all parameters, including layout.
        schema = pa.schema([("tensor", arrow_type)])
        restored = pa.ipc.read_schema(pa.BufferReader(schema.serialize())).field("tensor").type
        if isinstance(restored, (pa.FixedShapeTensorType, VariableShapeTensorType)):
            return restored
    raise ValueError(f"Unsupported Tensor extension type: {arrow_type}")


def contains_tensor_type(arrow_type):
    """Whether an Arrow field contains tensors at any nesting depth."""
    if is_tensor_type(arrow_type):
        return True
    if pa.types.is_struct(arrow_type):
        return any(contains_tensor_type(field.type) for field in arrow_type)
    if pa.types.is_list(arrow_type) or pa.types.is_large_list(arrow_type) or pa.types.is_fixed_size_list(arrow_type):
        return contains_tensor_type(arrow_type.value_type)
    return False


@dataclass
class Tensor:
    """An array with a fixed number of dimensions and optionally variable sizes.

    Args:
        shape (optional tuple of optional int):
            Size of each dimension. None dimensions may vary between rows.
            If omitted, ndim must specify the number of dimensions.
        dtype (str, defaults to "float32"):
            NumPy boolean, integer, or floating-point dtype. Values are converted
            to this dtype; invalid values and lossy integer conversions raise
            ValueError.
        ndim (optional int):
            Number of dimensions, required when shape is omitted. If both are
            provided, ndim must equal len(shape). All rows have this rank.

    Examples:
        >>> from datasets import Dataset, Features, Tensor
        >>> features = Features({"x": Tensor(shape=(None, None, 3), dtype="uint8")})
        >>> dataset = Dataset.from_dict({"x": [[[[0, 1, 2]]]]}, features=features)
        >>> dataset[0]["x"].shape
        (1, 1, 3)
    """

    shape: Optional[tuple[Optional[int], ...]] = None
    dtype: str = "float32"
    ndim: Optional[int] = None
    _type: str = field(default="Tensor", init=False, repr=False)

    def __post_init__(self):
        if self.ndim is not None and (
            isinstance(self.ndim, (bool, np.bool_))
            or not isinstance(self.ndim, (int, np.integer))
            or not 0 <= self.ndim <= 2**31 - 1
        ):
            raise ValueError("Tensor ndim must be a nonnegative integer")
        if self.shape is None:
            if self.ndim is None:
                raise ValueError(
                    "Tensor requires a shape with None entries for dynamic dimensions or an explicit ndim="
                )
            self.shape = (None,) * self.ndim
        else:
            self.shape = _normalize_shape(self.shape, allow_unknown_dims=True)
            if self.ndim is not None and self.ndim != len(self.shape):
                raise ValueError(f"Tensor ndim={self.ndim} does not match shape {self.shape}")
        self.ndim = len(self.shape)
        try:
            dtype = np.dtype(self.dtype)
            if dtype.kind not in "biuf" or not dtype.isnative:
                raise ValueError
            pa.from_numpy_dtype(dtype)
        except (TypeError, ValueError, pa.ArrowNotImplementedError) as e:
            raise ValueError(
                f"Invalid Tensor dtype: {self.dtype!r}; expected a boolean, integer or floating dtype"
            ) from e
        self.dtype = dtype.name

    def __call__(self):
        value_type = pa.from_numpy_dtype(np.dtype(self.dtype))
        if all(dim is not None for dim in self.shape):
            return pa.fixed_shape_tensor(value_type, self.shape)
        return VariableShapeTensorType(
            value_type, self.shape if any(dim is not None for dim in self.shape) else None, ndim=self.ndim
        )

    def _validate_shape(self, shape):
        if len(shape) != self.ndim or any(
            expected is not None and actual != expected for actual, expected in zip(shape, self.shape)
        ):
            raise ValueError(f"Tensor shape {tuple(shape)} does not match expected shape {self.shape}")

    def encode_example(self, value):
        from .features import cast_to_python_objects

        if value is None:
            return None
        value = cast_to_python_objects(value, optimize_list_casting=False)
        try:
            raw_data = value["data"] if isinstance(value, dict) else value
            python_integers = np.dtype(self.dtype).kind in "iu" and not isinstance(raw_data, np.ndarray)
            array = np.asarray(raw_data, dtype=object if python_integers else None)
            if python_integers:
                # NumPy infers float64 for Python integers mixing small values
                # and values above int64's maximum. Validate before conversion
                # so these inputs cannot silently lose uint64 precision.
                bounds = np.iinfo(self.dtype)
                integers = []
                for item in array.flat:
                    if not isinstance(item, (bool, int, float, np.bool_, np.integer, np.floating)):
                        raise ValueError("expected numeric or boolean values")
                    integer = int(item)
                    if integer != item or not bounds.min <= integer <= bounds.max:
                        raise ValueError(f"value {item!r} cannot be represented as {self.dtype}")
                    integers.append(integer)
                array = np.asarray(integers, dtype=self.dtype).reshape(array.shape)
            if isinstance(value, dict):
                shape = _normalize_shape(value["shape"])
                self._validate_shape(shape)
                array = array.reshape(shape)
            if array.dtype.kind not in "biuf":
                raise ValueError("expected numeric or boolean values")
            self._validate_shape(array.shape)
            if self.dtype == "bool" and not np.all((array == 0) | (array == 1)):
                raise ValueError("values must be exactly 0 or 1 to be represented as bool")
            target_type = pa.from_numpy_dtype(np.dtype(self.dtype))
            if np.dtype(self.dtype).kind in "iu":
                # Arrow's safe cast rejects fractional values and integer overflow.
                data = pa.array(array.reshape(-1)).cast(target_type).to_numpy(zero_copy_only=False)
            else:
                with np.errstate(over="raise", invalid="raise"):
                    data = array.astype(self.dtype).reshape(-1)
        except (KeyError, TypeError, ValueError, OverflowError, FloatingPointError, pa.ArrowException) as e:
            raise ValueError(f"Cannot encode Tensor with dtype {self.dtype} and shape {self.shape}: {e}") from e
        if isinstance(self(), pa.FixedShapeTensorType):
            # Preserve rank until the writer builds Arrow storage. A flat user
            # value must never be mistaken for an already encoded fixed tensor.
            return data.reshape(array.shape)
        return {"data": data, "shape": list(array.shape)}

    def decode_example(self, value, token_per_repo_id=None):
        if value is None:
            return None
        try:
            if isinstance(value, dict):
                shape = _normalize_shape(value["shape"])
                data = value["data"]
            else:
                data = np.asarray(value, dtype=self.dtype)
                # Fixed tensor storage is flattened; decoded arrays already
                # carry their shape. Variable storage always includes a shape.
                shape = self.shape if isinstance(self(), pa.FixedShapeTensorType) and data.ndim == 1 else data.shape
            self._validate_shape(shape)
            return tensor_to_backend(np.asarray(data, dtype=self.dtype).reshape(shape))
        except (KeyError, TypeError, ValueError, OverflowError) as e:
            raise ValueError(f"Cannot decode Tensor with dtype {self.dtype} and shape {self.shape}: {e}") from e

    def cast_storage(self, storage):
        from .features import generate_from_arrow_type

        arrow_type = self()
        if isinstance(storage, pa.ExtensionArray):
            if normalize_tensor_type(storage.type) == arrow_type:
                # Native and Python implementations can have identical canonical
                # parameters while Arrow refuses a direct extension-to-extension
                # cast. Rewrap the storage without copying its buffers.
                return arrow_type.wrap_array(storage.storage)
            source = generate_from_arrow_type(storage.type)
            values = [source.decode_example(value) for value in storage.to_pylist()]
        else:
            values = storage.to_pylist()
            if (
                isinstance(arrow_type, pa.FixedShapeTensorType)
                and (pa.types.is_list(storage.type) or pa.types.is_fixed_size_list(storage.type))
                and not pa.types.is_nested(storage.type.value_type)
            ):
                # Reshape storage without converting dtype before validation.
                values = [
                    np.asarray(value, dtype=storage.type.value_type.to_pandas_dtype()).reshape(self.shape)
                    if value is not None
                    else None
                    for value in values
                ]
        values = [encode_tensor_storage(self, value) for value in values]
        return pa.array(values, type=arrow_type)

    def embed_storage(
        self, storage: pa.ExtensionArray, token_per_repo_id=None, local_files: bool = True, remote_files: bool = True
    ) -> pa.ExtensionArray:
        """Return the tensor extension unchanged; all tensor data is already embedded."""
        return storage


class TensorPandasDtype(ExtensionDtype):
    """Use the existing pandas array container after restoring tensor shapes."""

    type = np.ndarray
    kind = "O"
    name = "tensor"

    def __from_arrow__(self, array):
        from .features import PandasArrayExtensionArray, generate_from_arrow_type

        feature = generate_from_arrow_type(array.type)
        # Restore only Tensor leaves here. The pandas feature decoder uses
        # the original metadata to decode siblings, including Json(decode=False).
        values = [_map_nested_tensor(feature, value, Tensor.decode_example) for value in array.to_pylist()]
        if (
            values
            and isinstance(values[0], np.ndarray)
            and values[0].ndim > 0
            and all(isinstance(value, np.ndarray) and value.shape == values[0].shape for value in values)
        ):
            data = np.stack(values)
        else:
            data = np.empty(len(values), dtype=object)
            data[:] = values
        return PandasArrayExtensionArray(data)


def _tensor_parquet_type(arrow_type):
    """Storage fallback for Arrow's Parquet reader bug with null fixed-size lists."""
    if is_tensor_type(arrow_type):
        arrow_type = normalize_tensor_type(arrow_type)
    if isinstance(arrow_type, pa.FixedShapeTensorType):
        return pa.list_(arrow_type.storage_type.value_field)
    if isinstance(arrow_type, VariableShapeTensorType):
        return pa.struct(
            [
                arrow_type.storage_type.field("data"),
                arrow_type.storage_type.field("shape").with_type(pa.list_(pa.int32())),
            ]
        )
    if pa.types.is_struct(arrow_type):
        return pa.struct([field.with_type(_tensor_parquet_type(field.type)) for field in arrow_type])
    if pa.types.is_list(arrow_type):
        return pa.list_(arrow_type.value_field.with_type(_tensor_parquet_type(arrow_type.value_type)))
    if pa.types.is_large_list(arrow_type):
        return pa.large_list(arrow_type.value_field.with_type(_tensor_parquet_type(arrow_type.value_type)))
    if pa.types.is_fixed_size_list(arrow_type):
        value_type = _tensor_parquet_type(arrow_type.value_type)
        if value_type != arrow_type.value_type:
            return pa.list_(arrow_type.value_field.with_type(value_type))
    return arrow_type


def _requires_tensor_parquet_storage(array, parent_nulls=False):
    if isinstance(array, pa.ChunkedArray):
        return any(_requires_tensor_parquet_storage(chunk, parent_nulls) for chunk in array.chunks)
    has_nulls = parent_nulls or array.null_count > 0
    if is_tensor_type(array.type):
        return has_nulls or (
            isinstance(array.type, pa.FixedShapeTensorType) and array.type.storage_type.list_size == 0
        )
    if pa.types.is_struct(array.type):
        return any(_requires_tensor_parquet_storage(array.field(field.name), has_nulls) for field in array.type)
    if pa.types.is_list(array.type) or pa.types.is_large_list(array.type) or pa.types.is_fixed_size_list(array.type):
        return _requires_tensor_parquet_storage(array.values, has_nulls)
    return False


def tensor_to_parquet_schema(schema, table=None):
    # Preserve canonical extensions whenever the complete table proves safe.
    # Streaming writers cannot rule out nulls in future batches, so use storage.
    fields = [
        field.with_type(_tensor_parquet_type(field.type))
        if table is None or _requires_tensor_parquet_storage(table[field.name])
        else field
        for field in schema
    ]
    if all(field.type == original.type for field, original in zip(fields, schema)):
        return schema
    # Keep the canonical schema separately: applying it as ARROW:schema would
    # trigger Arrow 25's fixed-size-list reader bug. Plain Arrow can read both
    # the storage table and this serialized schema without importing Datasets.
    metadata = {
        **(schema.metadata or {}),
        b"huggingface:tensor_schema": base64.b64encode(schema.serialize().to_pybytes()),
    }
    return pa.schema(fields, metadata=metadata)


def tensor_from_parquet_schema(schema):
    metadata = schema.metadata or {}
    if b"huggingface:tensor_schema" not in metadata:
        return schema
    canonical_schema = pa.ipc.read_schema(
        pa.BufferReader(base64.b64decode(metadata[b"huggingface:tensor_schema"], validate=True))
    )
    canonical_fields = {field.name: field for field in canonical_schema}
    # Respect projections and schema changes made by other Arrow consumers.
    fields = [
        canonical_fields[field.name]
        if field.name in canonical_fields and field.type == _tensor_parquet_type(canonical_fields[field.name].type)
        else field
        for field in schema
    ]
    return pa.schema(
        fields, metadata={key: value for key, value in metadata.items() if key != b"huggingface:tensor_schema"}
    )


def tensor_to_parquet_table(table, schema=None):
    from ..table import array_cast

    if schema is None:
        schema = tensor_to_parquet_schema(table.schema, table)
    if schema == table.schema:
        return table
    arrays = [
        column if field.type == column.type else array_cast(column, field.type)
        for field, column in zip(schema, table.columns)
    ]
    return pa.Table.from_arrays(arrays, schema=schema)


def contains_tensor(feature):
    from .features import LargeList, List

    if isinstance(feature, Tensor):
        return True
    if isinstance(feature, dict):
        return any(contains_tensor(subfeature) for subfeature in feature.values())
    if isinstance(feature, (list, tuple)):
        return any(contains_tensor(subfeature) for subfeature in feature)
    if isinstance(feature, (LargeList, List)):
        return contains_tensor(feature.feature)
    return False


def _map_nested_tensor(feature, value, function):
    """Apply a conversion only to Tensor leaves, preserving sibling fields."""
    from .features import LargeList, List

    if value is None:
        return None
    if isinstance(feature, Tensor):
        return function(feature, value)
    if isinstance(feature, dict):
        return {key: _map_nested_tensor(feature.get(key), item, function) for key, item in value.items()}
    if isinstance(feature, (List, LargeList)):
        return [_map_nested_tensor(feature.feature, item, function) for item in value]
    if isinstance(feature, (list, tuple)):
        return [_map_nested_tensor(feature[0], item, function) for item in value]
    return value


def encode_tensor_storage(feature, value):
    """Normalize Tensor leaves before Arrow infers nested list ranks."""

    def encode(feature, value):
        encoded = feature.encode_example(value)
        return encoded.reshape(-1) if isinstance(feature(), pa.FixedShapeTensorType) else encoded

    return _map_nested_tensor(feature, value, encode)


def tensor_to_backend(value, backend="numpy", **kwargs):
    """Convert a decoded Tensor without applying a formatter's default dtype.

    Pandas and Polars keep NumPy arrays in their object columns. Native backends
    infer the same dtype from NumPy. JAX requires x64 mode for 64-bit values;
    reject unsupported conversions instead of silently truncating them.
    Explicit formatter dtype arguments still override the feature dtype.
    """
    if backend == "numpy":
        return np.asarray(value, **kwargs)
    if backend == "torch":
        import torch

        if value.dtype == np.uint64 and not hasattr(torch, "uint64"):
            raise ValueError("Tensor dtype uint64 requires a PyTorch version with native uint64 support")
        return torch.tensor(value, **kwargs)
    if backend == "tensorflow":
        import tensorflow as tf

        return tf.convert_to_tensor(value, **kwargs)
    if backend == "jax":
        import jax
        import jax.numpy as jnp

        dtype = kwargs.get("dtype", value.dtype)
        if np.dtype(dtype).itemsize == 8 and np.dtype(dtype).kind in "iuf" and not jax.config.jax_enable_x64:
            raise ValueError(f"Tensor dtype {np.dtype(dtype).name} requires jax_enable_x64=True")
        with jax.default_device(kwargs.pop("device", None)):
            return jnp.asarray(value, **{"dtype": value.dtype, **kwargs})
    raise ValueError(f"Unsupported Tensor backend: {backend}")
