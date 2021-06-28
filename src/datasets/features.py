# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the TensorFlow Datasets Authors.
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

# Lint as: python3
""" This class handle features definition in datasets and some utilities to display table type."""
import copy
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass, field, fields
from typing import Any, ClassVar, Dict, List, Optional
from typing import Sequence as Sequence_
from typing import Tuple, Union

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.types
from pandas.api.extensions import ExtensionArray as PandasExtensionArray
from pandas.api.extensions import ExtensionDtype as PandasExtensionDtype
from pyarrow.lib import TimestampType
from pyarrow.types import is_boolean, is_primitive

from . import config, utils
from .utils.logging import get_logger


logger = get_logger(__name__)


def _arrow_to_datasets_dtype(arrow_type: pa.DataType) -> str:
    """
    _arrow_to_datasets_dtype takes a pyarrow.DataType and converts it to a datasets string dtype.
    In effect, `dt == string_to_arrow(_arrow_to_datasets_dtype(dt))`
    """

    if pyarrow.types.is_null(arrow_type):
        return "null"
    elif pyarrow.types.is_boolean(arrow_type):
        return "bool"
    elif pyarrow.types.is_int8(arrow_type):
        return "int8"
    elif pyarrow.types.is_int16(arrow_type):
        return "int16"
    elif pyarrow.types.is_int32(arrow_type):
        return "int32"
    elif pyarrow.types.is_int64(arrow_type):
        return "int64"
    elif pyarrow.types.is_uint8(arrow_type):
        return "uint8"
    elif pyarrow.types.is_uint16(arrow_type):
        return "uint16"
    elif pyarrow.types.is_uint32(arrow_type):
        return "uint32"
    elif pyarrow.types.is_uint64(arrow_type):
        return "uint64"
    elif pyarrow.types.is_float16(arrow_type):
        return "float16"  # pyarrow dtype is "halffloat"
    elif pyarrow.types.is_float32(arrow_type):
        return "float32"  # pyarrow dtype is "float"
    elif pyarrow.types.is_float64(arrow_type):
        return "float64"  # pyarrow dtype is "double"
    elif pyarrow.types.is_timestamp(arrow_type):
        assert isinstance(arrow_type, TimestampType)
        if arrow_type.tz is None:
            return f"timestamp[{arrow_type.unit}]"
        elif arrow_type.tz:
            return f"timestamp[{arrow_type.unit}, tz={arrow_type.tz}]"
        else:
            raise ValueError(f"Unexpected timestamp object {arrow_type}.")
    elif pyarrow.types.is_binary(arrow_type):
        return "binary"
    elif pyarrow.types.is_large_binary(arrow_type):
        return "large_binary"
    elif pyarrow.types.is_string(arrow_type):
        return "string"
    elif pyarrow.types.is_large_string(arrow_type):
        return "large_string"
    else:
        raise ValueError(f"Arrow type {arrow_type} does not have a datasets dtype equivalent.")


def string_to_arrow(datasets_dtype: str) -> pa.DataType:
    """
    string_to_arrow takes a datasets string dtype and converts it to a pyarrow.DataType.

    In effect, `dt == string_to_arrow(_arrow_to_datasets_dtype(dt))`

    This is necessary because the datasets.Value() primitive type is constructed using a string dtype

    Value(dtype=str)

    But Features.type (via `get_nested_type()` expects to resolve Features into a pyarrow Schema,
        which means that each Value() must be able to resolve into a corresponding pyarrow.DataType, which is the
        purpose of this function.
    """
    timestamp_regex = re.compile(r"^timestamp\[(.*)\]$")
    timestamp_matches = timestamp_regex.search(datasets_dtype)
    if timestamp_matches:
        """
        Example timestamp dtypes:

        timestamp[us]
        timestamp[us, tz=America/New_York]
        """
        timestamp_internals = timestamp_matches.group(1)
        internals_regex = re.compile(r"^(s|ms|us|ns),\s*tz=([a-zA-Z0-9/_+:]*)$")
        internals_matches = internals_regex.search(timestamp_internals)
        if timestamp_internals in ["s", "ms", "us", "ns"]:
            return pa.timestamp(timestamp_internals)
        elif internals_matches:
            return pa.timestamp(internals_matches.group(1), internals_matches.group(2))
        else:
            raise ValueError(
                f"{datasets_dtype} is not a validly formatted string representation of a pyarrow timestamp."
                f"Examples include timestamp[us] or timestamp[us, tz=America/New_York]"
                f"See: https://arrow.apache.org/docs/python/generated/pyarrow.timestamp.html#pyarrow.timestamp"
            )
    elif datasets_dtype not in pa.__dict__:
        if str(datasets_dtype + "_") not in pa.__dict__:
            raise ValueError(
                f"Neither {datasets_dtype} nor {datasets_dtype + '_'} seems to be a pyarrow data type. "
                f"Please make sure to use a correct data type, see: "
                f"https://arrow.apache.org/docs/python/api/datatypes.html#factory-functions"
            )
        arrow_data_factory_function_name = str(datasets_dtype + "_")
    else:
        arrow_data_factory_function_name = datasets_dtype

    return pa.__dict__[arrow_data_factory_function_name]()


def _cast_to_python_objects(obj: Any) -> Tuple[Any, bool]:
    """
    Cast numpy/pytorch/tensorflow/pandas objects to python lists.
    It works recursively.

    To avoid iterating over possibly long lists, it first checks if the first element that is not None has to be casted.
    If the first element needs to be casted, then all the elements of the list will be casted, otherwise they'll stay the same.
    This trick allows to cast objects that contain tokenizers outputs without iterating over every single token for example.

    Args:
        obj: the object (nested struct) to cast

    Returns:
        casted_obj: the casted object
        has_changed (bool): True if the object has been changed, False if it is identical
    """

    if config.TF_AVAILABLE and "tensorflow" in sys.modules:
        import tensorflow as tf

    if config.TORCH_AVAILABLE and "torch" in sys.modules:
        import torch

    if config.JAX_AVAILABLE and "jax" in sys.modules:
        import jax.numpy as jnp

    if isinstance(obj, np.ndarray):
        return obj.tolist(), True
    elif config.TORCH_AVAILABLE and "torch" in sys.modules and isinstance(obj, torch.Tensor):
        return obj.detach().cpu().numpy().tolist(), True
    elif config.TF_AVAILABLE and "tensorflow" in sys.modules and isinstance(obj, tf.Tensor):
        return obj.numpy().tolist(), True
    elif config.JAX_AVAILABLE and "jax" in sys.modules and isinstance(obj, jnp.ndarray):
        return obj.tolist(), True
    elif isinstance(obj, pd.Series):
        return obj.values.tolist(), True
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict("list"), True
    elif isinstance(obj, dict):
        output = {}
        has_changed = False
        for k, v in obj.items():
            casted_v, has_changed_v = _cast_to_python_objects(v)
            has_changed |= has_changed_v
            output[k] = casted_v
        return output if has_changed else obj, has_changed
    elif isinstance(obj, (list, tuple)):
        if len(obj) > 0:
            for first_elmt in obj:
                if first_elmt is not None:
                    break
            casted_first_elmt, has_changed_first_elmt = _cast_to_python_objects(first_elmt)
            if has_changed_first_elmt:
                return [_cast_to_python_objects(elmt)[0] for elmt in obj], True
            else:
                if isinstance(obj, list):
                    return obj, False
                else:
                    return list(obj), True
        else:
            return obj if isinstance(obj, list) else [], isinstance(obj, tuple)
    else:
        return obj, False


def cast_to_python_objects(obj: Any) -> Any:
    """
    Cast numpy/pytorch/tensorflow/pandas objects to python lists.
    It works recursively.

    To avoid iterating over possibly long lists, it first checks if the first element that is not None has to be casted.
    If the first element needs to be casted, then all the elements of the list will be casted, otherwise they'll stay the same.
    This trick allows to cast objects that contain tokenizers outputs without iterating over every single token for example.

    Args:
        obj: the object (nested struct) to cast

    Returns:
        casted_obj: the casted object
    """
    return _cast_to_python_objects(obj)[0]


@dataclass
class Value:
    """
    The Value dtypes are as follows:

    null
    bool
    int8
    int16
    int32
    int64
    uint8
    uint16
    uint32
    uint64
    float16
    float32 (alias float)
    float64 (alias double)
    timestamp[(s|ms|us|ns)]
    timestamp[(s|ms|us|ns), tz=(tzstring)]
    binary
    large_binary
    string
    large_string
    """

    dtype: str
    id: Optional[str] = None
    # Automatically constructed
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Value", init=False, repr=False)

    def __post_init__(self):
        if self.dtype == "double":  # fix inferred type
            self.dtype = "float64"
        if self.dtype == "float":  # fix inferred type
            self.dtype = "float32"
        self.pa_type = string_to_arrow(self.dtype)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value):
        if pa.types.is_boolean(self.pa_type):
            return bool(value)
        elif pa.types.is_integer(self.pa_type):
            return int(value)
        elif pa.types.is_floating(self.pa_type):
            return float(value)
        else:
            return value


class _ArrayXD:
    def __post_init__(self):
        self.shape = tuple(self.shape)

    def __call__(self):
        pa_type = globals()[self.__class__.__name__ + "ExtensionType"](self.shape, self.dtype)
        return pa_type

    def encode_example(self, value):
        if isinstance(value, np.ndarray):
            value = value.tolist()
        return value


@dataclass
class Array2D(_ArrayXD):
    shape: tuple
    dtype: str
    id: Optional[str] = None
    # Automatically constructed
    _type: str = field(default="Array2D", init=False, repr=False)


@dataclass
class Array3D(_ArrayXD):
    shape: tuple
    dtype: str
    id: Optional[str] = None
    # Automatically constructed
    _type: str = field(default="Array3D", init=False, repr=False)


@dataclass
class Array4D(_ArrayXD):
    shape: tuple
    dtype: str
    id: Optional[str] = None
    # Automatically constructed
    _type: str = field(default="Array4D", init=False, repr=False)


@dataclass
class Array5D(_ArrayXD):
    shape: tuple
    dtype: str
    id: Optional[str] = None
    # Automatically constructed
    _type: str = field(default="Array5D", init=False, repr=False)


class _ArrayXDExtensionType(pa.PyExtensionType):
    ndims: Optional[int] = None

    def __init__(self, shape: tuple, dtype: str):
        assert (
            self.ndims is not None and self.ndims > 1
        ), "You must instantiate an array type with a value for dim that is > 1"
        assert len(shape) == self.ndims, "shape={} and ndims={} dom't match".format(shape, self.ndims)
        self.shape = tuple(shape)
        self.value_type = dtype
        self.storage_dtype = self._generate_dtype(self.value_type)
        pa.PyExtensionType.__init__(self, self.storage_dtype)

    def __reduce__(self):
        return self.__class__, (
            self.shape,
            self.value_type,
        )

    def __arrow_ext_class__(self):
        return ArrayExtensionArray

    def _generate_dtype(self, dtype):
        dtype = string_to_arrow(dtype)
        for d in reversed(self.shape):
            dtype = pa.list_(dtype)
            # Don't specify the size of the list, since fixed length list arrays have issues
            # being validated after slicing in pyarrow 0.17.1
        return dtype

    def to_pandas_dtype(self):
        return PandasArrayExtensionDtype(self.value_type)


class Array2DExtensionType(_ArrayXDExtensionType):
    ndims = 2


class Array3DExtensionType(_ArrayXDExtensionType):
    ndims = 3


class Array4DExtensionType(_ArrayXDExtensionType):
    ndims = 4


class Array5DExtensionType(_ArrayXDExtensionType):
    ndims = 5


def _is_zero_copy_only(pa_type: pa.DataType) -> bool:
    """
    When converting a pyarrow array to a numpy array, we must know whether this could be done in zero-copy or not.
    This function returns the value of the ``zero_copy_only`` parameter to pass to ``.to_numpy()``, given the type of the pyarrow array.

    # zero copy is available for all primitive types except booleans
    # primitive types are types for which the physical representation in arrow and in numpy
    # https://github.com/wesm/arrow/blob/c07b9b48cf3e0bbbab493992a492ae47e5b04cad/python/pyarrow/types.pxi#L821
    # see https://arrow.apache.org/docs/python/generated/pyarrow.Array.html#pyarrow.Array.to_numpy
    # and https://issues.apache.org/jira/browse/ARROW-2871?jql=text%20~%20%22boolean%20to_numpy%22
    """
    return is_primitive(pa_type) and not is_boolean(pa_type)


class ArrayExtensionArray(pa.ExtensionArray):
    def __array__(self):
        zero_copy_only = _is_zero_copy_only(self.storage.type)
        return self.to_numpy(zero_copy_only=zero_copy_only)

    def __getitem__(self, i):
        return self.storage[i]

    def to_numpy(self, zero_copy_only=True):
        storage: pa.ListArray = self.storage
        size = 1
        for i in range(self.type.ndims):
            size *= self.type.shape[i]
            storage = storage.flatten()
        numpy_arr = storage.to_numpy(zero_copy_only=zero_copy_only)
        numpy_arr = numpy_arr.reshape(len(self), *self.type.shape)
        return numpy_arr

    def to_pylist(self):
        zero_copy_only = _is_zero_copy_only(self.storage.type)
        return self.to_numpy(zero_copy_only=zero_copy_only).tolist()


class PandasArrayExtensionDtype(PandasExtensionDtype):
    _metadata = "value_type"

    def __init__(self, value_type: Union["PandasArrayExtensionDtype", np.dtype]):
        self._value_type = value_type

    def __from_arrow__(self, array):
        zero_copy_only = _is_zero_copy_only(array.type)
        if isinstance(array, pa.ChunkedArray):
            numpy_arr = np.vstack([chunk.to_numpy(zero_copy_only=zero_copy_only) for chunk in array.chunks])
        else:
            numpy_arr = array.to_numpy(zero_copy_only=zero_copy_only)
        return PandasArrayExtensionArray(numpy_arr)

    @classmethod
    def construct_array_type(cls):
        return PandasArrayExtensionArray

    @property
    def type(self) -> type:
        return np.ndarray

    @property
    def kind(self) -> str:
        return "O"

    @property
    def name(self) -> str:
        return f"array[{self.value_type}]"

    @property
    def value_type(self) -> np.dtype:
        return self._value_type


class PandasArrayExtensionArray(PandasExtensionArray):
    def __init__(self, data: np.ndarray, copy: bool = False):
        self._data = data if not copy else np.array(data)
        self._dtype = PandasArrayExtensionDtype(data.dtype)

    def __array__(self, dtype=None):
        """
        Convert to NumPy Array.
        Note that Pandas expects a 1D array when dtype is set to object.
        But for other dtypes, the returned shape is the same as the one of ``data``.

        More info about pandas 1D requirement for PandasExtensionArray here:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray

        """
        if dtype == object:
            out = np.empty(len(self._data), dtype=object)
            for i in range(len(self._data)):
                out[i] = self._data[i]
            return out
        if dtype is None:
            return self._data
        else:
            return self._data.astype(dtype)

    def copy(self, deep: bool = False) -> "PandasArrayExtensionArray":
        return PandasArrayExtensionArray(self._data, copy=True)

    @classmethod
    def _from_sequence(
        cls, scalars, dtype: Optional[PandasArrayExtensionDtype] = None, copy: bool = False
    ) -> "PandasArrayExtensionArray":
        data = np.array(scalars, dtype=dtype if dtype is None else dtype.value_type, copy=copy)
        return cls(data, copy=copy)

    @classmethod
    def _concat_same_type(cls, to_concat: Sequence_["PandasArrayExtensionArray"]) -> "PandasArrayExtensionArray":
        data = np.vstack([va._data for va in to_concat])
        return cls(data, copy=False)

    @property
    def dtype(self) -> PandasArrayExtensionDtype:
        return self._dtype

    @property
    def nbytes(self) -> int:
        return self._data.nbytes

    def isna(self) -> np.ndarray:
        return np.array([pd.isna(arr).any() for arr in self._data])

    def __setitem__(self, key: Union[int, slice, np.ndarray], value: Any) -> None:
        raise NotImplementedError()

    def __getitem__(self, item: Union[int, slice, np.ndarray]) -> Union[np.ndarray, "PandasArrayExtensionArray"]:
        if isinstance(item, int):
            return self._data[item]
        return PandasArrayExtensionArray(self._data[item], copy=False)

    def take(
        self, indices: Sequence_[int], allow_fill: bool = False, fill_value: bool = None
    ) -> "PandasArrayExtensionArray":
        indices: np.ndarray = np.asarray(indices, dtype="int")
        if allow_fill:
            fill_value = (
                self.dtype.na_value if fill_value is None else np.asarray(fill_value, dtype=self.dtype.value_type)
            )
            mask = indices == -1
            if (indices < -1).any():
                raise ValueError("Invalid value in `indices`, must be all >= -1 for `allow_fill` is True")
            elif len(self) > 0:
                pass
            elif not np.all(mask):
                raise IndexError("Invalid take for empty PandasArrayExtensionArray, must be all -1.")
            else:
                data = np.array([fill_value] * len(indices), dtype=self.dtype.value_type)
                return PandasArrayExtensionArray(data, copy=False)
        took = self._data.take(indices, axis=0)
        if allow_fill and mask.any():
            took[mask] = [fill_value] * np.sum(mask)
        return PandasArrayExtensionArray(took, copy=False)

    def __len__(self) -> int:
        return len(self._data)

    def __eq__(self, other) -> np.ndarray:
        if not isinstance(other, PandasArrayExtensionArray):
            raise NotImplementedError("Invalid type to compare to: {}".format(type(other)))
        return (self._data == other._data).all()


def pandas_types_mapper(dtype):
    if isinstance(dtype, _ArrayXDExtensionType):
        return PandasArrayExtensionDtype(dtype.value_type)


@dataclass
class ClassLabel:
    """Handle integer class labels. Here for compatiblity with tfds.

    There are 3 ways to define a ClassLabel, which correspond to the 3
    arguments:

     * `num_classes`: create 0 to (num_classes-1) labels
     * `names`: a list of label strings
     * `names_file`: a file containing the list of labels.

    Note: On python2, the strings are encoded as utf-8.

    Args:
        num_classes: `int`, number of classes. All labels must be < num_classes.
        names: `list<str>`, string names for the integer classes. The
            order in which the names are provided is kept.
        names_file: `str`, path to a file with names for the integer
            classes, one per line.
    """

    num_classes: int = None
    names: List[str] = None
    names_file: Optional[str] = None
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "int64"
    pa_type: ClassVar[Any] = pa.int64()
    _str2int: ClassVar[Dict[str, int]] = None
    _int2str: ClassVar[Dict[int, int]] = None
    _type: str = field(default="ClassLabel", init=False, repr=False)

    def __post_init__(self):
        if self.names_file is not None and self.names is not None:
            raise ValueError("Please provide either names or names_file but not both.")
        # Set self.names
        if self.names is None:
            if self.names_file is not None:
                self.names = self._load_names_from_file(self.names_file)
            elif self.num_classes is not None:
                self.names = [str(i) for i in range(self.num_classes)]
            else:
                raise ValueError("Please provide either num_classes, names or names_file.")
        # Set self.num_classes
        if self.num_classes is None:
            self.num_classes = len(self.names)
        elif self.num_classes != len(self.names):
            raise ValueError(
                "ClassLabel number of names do not match the defined num_classes. "
                "Got {} names VS {} num_classes".format(len(self.names), self.num_classes)
            )
        # Prepare mappings
        self._int2str = [str(name) for name in self.names]
        self._str2int = {name: i for i, name in enumerate(self._int2str)}
        if len(self._int2str) != len(self._str2int):
            raise ValueError("Some label names are duplicated. Each label name should be unique.")

    def __call__(self):
        return self.pa_type

    def str2int(self, values: Union[str, Iterable]):
        """Conversion class name string => integer."""
        assert isinstance(values, str) or isinstance(
            values, Iterable
        ), f"Values {values} should be a string or an Iterable (list, numpy array, pytorch, tensorflow tensors)"
        return_list = True
        if isinstance(values, str):
            values = [values]
            return_list = False

        output = []
        for value in values:
            if self._str2int:
                # strip key if not in dict
                if value not in self._str2int:
                    value = str(value).strip()
                output.append(self._str2int[str(value)])
            else:
                # No names provided, try to integerize
                failed_parse = False
                try:
                    output.append(int(value))
                except ValueError:
                    failed_parse = True
                if failed_parse or not 0 <= value < self.num_classes:
                    raise ValueError("Invalid string class label %s" % value)
        return output if return_list else output[0]

    def int2str(self, values: Union[int, Iterable]):
        """Conversion integer => class name string."""
        assert isinstance(values, int) or isinstance(
            values, Iterable
        ), f"Values {values} should be an integer or an Iterable (list, numpy array, pytorch, tensorflow tensors)"
        return_list = True
        if isinstance(values, int):
            values = [values]
            return_list = False

        for v in values:
            if not 0 <= v < self.num_classes:
                raise ValueError("Invalid integer class label %d" % v)

        if self._int2str:
            output = [self._int2str[int(v)] for v in values]
        else:
            # No names provided, return str(values)
            output = [str(v) for v in values]
        return output if return_list else output[0]

    def encode_example(self, example_data):
        if self.num_classes is None:
            raise ValueError(
                "Trying to use ClassLabel feature with undefined number of class. "
                "Please set ClassLabel.names or num_classes."
            )

        # If a string is given, convert to associated integer
        if isinstance(example_data, str):
            example_data = self.str2int(example_data)

        # Allowing -1 to mean no label.
        if not -1 <= example_data < self.num_classes:
            raise ValueError(
                "Class label %d greater than configured num_classes %d" % (example_data, self.num_classes)
            )
        return example_data

    @staticmethod
    def _load_names_from_file(names_filepath):
        with open(names_filepath, "r", encoding="utf-8") as f:
            return [name.strip() for name in f.read().split("\n") if name.strip()]  # Filter empty names


@dataclass
class Translation:
    """`FeatureConnector` for translations with fixed languages per example.
    Here for compatiblity with tfds.

    Input: The Translate feature accepts a dictionary for each example mapping
        string language codes to string translations.

    Output: A dictionary mapping string language codes to translations as `Text`
        features.

    Example::

        # At construction time:

        datasets.features.Translation(languages=['en', 'fr', 'de'])

        # During data generation:

        yield {
                'en': 'the cat',
                'fr': 'le chat',
                'de': 'die katze'
        }
    """

    languages: List[str]
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Translation", init=False, repr=False)

    def __call__(self):
        return pa.struct({lang: pa.string() for lang in sorted(self.languages)})


@dataclass
class TranslationVariableLanguages:
    """`FeatureConnector` for translations with variable languages per example.
    Here for compatiblity with tfds.

    Input: The TranslationVariableLanguages feature accepts a dictionary for each
        example mapping string language codes to one or more string translations.
        The languages present may vary from example to example.

    Output:
        language: variable-length 1D tf.Tensor of tf.string language codes, sorted
            in ascending order.
        translation: variable-length 1D tf.Tensor of tf.string plain text
            translations, sorted to align with language codes.

    Example::

        # At construction time:

        datasets.features.Translation(languages=['en', 'fr', 'de'])

        # During data generation:

        yield {
                'en': 'the cat',
                'fr': ['le chat', 'la chatte,']
                'de': 'die katze'
        }

        # Tensor returned :

        {
                'language': ['en', 'de', 'fr', 'fr'],
                'translation': ['the cat', 'die katze', 'la chatte', 'le chat'],
        }
    """

    languages: Optional[List] = None
    num_languages: Optional[int] = None
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="TranslationVariableLanguages", init=False, repr=False)

    def __post_init__(self):
        self.languages = list(sorted(list(set(self.languages)))) if self.languages else None
        self.num_languages = len(self.languages) if self.languages else None

    def __call__(self):
        return pa.struct({"language": pa.list_(pa.string()), "translation": pa.list_(pa.string())})

    def encode_example(self, translation_dict):
        lang_set = set(self.languages)
        if self.languages and set(translation_dict) - lang_set:
            raise ValueError(
                "Some languages in example ({0}) are not in valid set ({1}).".format(
                    ", ".join(sorted(set(translation_dict) - lang_set)), ", ".join(lang_set)
                )
            )

        # Convert dictionary into tuples, splitting out cases where there are
        # multiple translations for a single language.
        translation_tuples = []
        for lang, text in translation_dict.items():
            if isinstance(text, str):
                translation_tuples.append((lang, text))
            else:
                translation_tuples.extend([(lang, el) for el in text])

        # Ensure translations are in ascending order by language code.
        languages, translations = zip(*sorted(translation_tuples))

        return {"language": languages, "translation": translations}


@dataclass
class Sequence:
    """Construct a list of feature from a single type or a dict of types.
    Mostly here for compatiblity with tfds.
    """

    feature: Any
    length: int = -1
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "list"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Sequence", init=False, repr=False)


FeatureType = Union[
    dict,
    list,
    tuple,
    Value,
    ClassLabel,
    Translation,
    TranslationVariableLanguages,
    Sequence,
    Array2D,
    Array3D,
    Array4D,
    Array5D,
]


def get_nested_type(schema: FeatureType) -> pa.DataType:
    """
    get_nested_type() converts a datasets.FeatureType into a pyarrow.DataType, and acts as the inverse of
        generate_from_arrow_type().

    It performs double-duty as the implementation of Features.type and handles the conversion of
        datasets.Feature->pa.struct
    """
    # Nested structures: we allow dict, list/tuples, sequences
    if isinstance(schema, Features):
        return pa.struct(
            {key: get_nested_type(schema[key]) for key in schema}
        )  # Features is subclass of dict, and dict order is deterministic since Python 3.6
    elif isinstance(schema, dict):
        return pa.struct(
            {key: get_nested_type(schema[key]) for key in schema}
        )  # however don't sort on struct types since the order matters
    elif isinstance(schema, (list, tuple)):
        assert len(schema) == 1, "We defining list feature, you should just provide one example of the inner type"
        value_type = get_nested_type(schema[0])
        return pa.list_(value_type)
    elif isinstance(schema, Sequence):
        value_type = get_nested_type(schema.feature)
        # We allow to reverse list of dict => dict of list for compatibility with tfds
        if isinstance(value_type, pa.StructType):
            return pa.struct({f.name: pa.list_(f.type, schema.length) for f in value_type})
        return pa.list_(value_type, schema.length)

    # Other objects are callable which returns their data type (ClassLabel, Array2D, Translation, Arrow datatype creation methods)
    return schema()


def encode_nested_example(schema, obj):
    """Encode a nested example.
    This is used since some features (in particular ClassLabel) have some logic during encoding.
    """
    # Nested structures: we allow dict, list/tuples, sequences
    if isinstance(schema, dict):
        return {
            k: encode_nested_example(sub_schema, sub_obj) for k, (sub_schema, sub_obj) in utils.zip_dict(schema, obj)
        }
    elif isinstance(schema, (list, tuple)):
        sub_schema = schema[0]
        return [encode_nested_example(sub_schema, o) for o in obj]
    elif isinstance(schema, Sequence):
        # We allow to reverse list of dict => dict of list for compatiblity with tfds
        if isinstance(schema.feature, dict):
            # dict of list to fill
            list_dict = {}
            if isinstance(obj, (list, tuple)):
                # obj is a list of dict
                for k, dict_tuples in utils.zip_dict(schema.feature, *obj):
                    list_dict[k] = [encode_nested_example(dict_tuples[0], o) for o in dict_tuples[1:]]
                return list_dict
            else:
                # obj is a single dict
                for k, (sub_schema, sub_objs) in utils.zip_dict(schema.feature, obj):
                    list_dict[k] = [encode_nested_example(sub_schema, o) for o in sub_objs]
                return list_dict
        # schema.feature is not a dict
        if isinstance(obj, str):  # don't interpret a string as a list
            raise ValueError("Got a string but expected a list instead: '{}'".format(obj))
        return [encode_nested_example(schema.feature, o) for o in obj]
    # Object with special encoding:
    # ClassLabel will convert from string to int, TranslationVariableLanguages does some checks
    elif isinstance(schema, (ClassLabel, TranslationVariableLanguages, Value, _ArrayXD)):
        return schema.encode_example(obj)
    # Other object should be directly convertible to a native Arrow type (like Translation and Translation)
    return obj


def generate_from_dict(obj: Any):
    """Regenerate the nested feature object from a deserialized dict.
    We use the '_type' fields to get the dataclass name to load.

    generate_from_dict is the recursive helper for Features.from_dict, and allows for a convenient constructor syntax
    to define features from deserialized JSON dictionaries. This function is used in particular when deserializing
    a :class:`DatasetInfo` that was dumped to a JSON object. This acts as an analogue to
    :meth:`Features.from_arrow_schema` and handles the recursive field-by-field instantiation, but doesn't require any
    mapping to/from pyarrow, except for the fact that it takes advantage of the mapping of pyarrow primitive dtypes
    that :class:`Value` automatically performs.
    """
    # Nested structures: we allow dict, list/tuples, sequences
    if isinstance(obj, list):
        return [generate_from_dict(value) for value in obj]
    # Otherwise we have a dict or a dataclass
    if "_type" not in obj or isinstance(obj["_type"], dict):
        return {key: generate_from_dict(value) for key, value in obj.items()}
    class_type = globals()[obj.pop("_type")]

    if class_type == Sequence:
        return Sequence(feature=generate_from_dict(obj["feature"]), length=obj["length"])

    field_names = set(f.name for f in fields(class_type))
    return class_type(**{k: v for k, v in obj.items() if k in field_names})


def generate_from_arrow_type(pa_type: pa.DataType) -> FeatureType:
    """
    generate_from_arrow_type accepts an arrow DataType and returns a datasets FeatureType to be used as the type for
        a single field.

    This is the high-level arrow->datasets type conversion and is inverted by get_nested_type().

    This operates at the individual *field* level, whereas Features.from_arrow_schema() operates at the
        full schema level and holds the methods that represent the bijection from Features<->pyarrow.Schema
    """
    if isinstance(pa_type, pa.StructType):
        return {field.name: generate_from_arrow_type(field.type) for field in pa_type}
    elif isinstance(pa_type, pa.FixedSizeListType):
        return Sequence(feature=generate_from_arrow_type(pa_type.value_type), length=pa_type.list_size)
    elif isinstance(pa_type, pa.ListType):
        feature = generate_from_arrow_type(pa_type.value_type)
        if isinstance(feature, (dict, tuple, list)):
            return [feature]
        return Sequence(feature=feature)
    elif isinstance(pa_type, _ArrayXDExtensionType):
        array_feature = [None, None, Array2D, Array3D, Array4D, Array5D][pa_type.ndims]
        return array_feature(shape=pa_type.shape, dtype=pa_type.value_type)
    elif isinstance(pa_type, pa.DictionaryType):
        raise NotImplementedError  # TODO(thom) this will need access to the dictionary as well (for labels). I.e. to the py_table
    elif isinstance(pa_type, pa.DataType):
        return Value(dtype=_arrow_to_datasets_dtype(pa_type))
    else:
        raise ValueError(f"Cannot convert {pa_type} to a Feature type.")


class Features(dict):
    @property
    def type(self):
        """
        Features field types.

        Returns:
            :obj:`pyarrow.DataType`
        """
        return get_nested_type(self)

    @classmethod
    def from_arrow_schema(cls, pa_schema: pa.Schema) -> "Features":
        """
        Construct Features from Arrow Schema.

        Args:
            pa_schema (:obj:`pyarrow.Schema`): Arrow Schema.

        Returns:
            :class:`Features`
        """
        obj = {field.name: generate_from_arrow_type(field.type) for field in pa_schema}
        return cls(**obj)

    @classmethod
    def from_dict(cls, dic) -> "Features":
        """
        Construct Features from dict.

        Regenerate the nested feature object from a deserialized dict.
        We use the '_type' key to infer the dataclass name of the feature FieldType.

        It allows for a convenient constructor syntax
        to define features from deserialized JSON dictionaries. This function is used in particular when deserializing
        a :class:`DatasetInfo` that was dumped to a JSON object. This acts as an analogue to
        :meth:`Features.from_arrow_schema` and handles the recursive field-by-field instantiation, but doesn't require
        any mapping to/from pyarrow, except for the fact that it takes advantage of the mapping of pyarrow primitive
        dtypes that :class:`Value` automatically performs.

        Args:
            dic (:obj:`dict[str, Any]`): Python dictionary.

        Returns:
            :class:`Features`

        Examples:
            >>> Features.from_dict({'_type': {'dtype': 'string', 'id': None, '_type': 'Value'}})
            {'_type': Value(dtype='string', id=None)}
        """
        obj = generate_from_dict(dic)
        return cls(**obj)

    def encode_example(self, example):
        """
        Encode example into a format for Arrow.

        Args:
            example (:obj:`dict[str, Any]`): Data in a Dataset row.

        Returns:
            :obj:`dict[str, Any]`
        """
        example = cast_to_python_objects(example)
        return encode_nested_example(self, example)

    def encode_batch(self, batch):
        """
        Encode batch into a format for Arrow.

        Args:
            batch (:obj:`dict[str, list[Any]]`): Data in a Dataset batch.

        Returns:
            :obj:`dict[str, list[Any]]`
        """
        encoded_batch = {}
        if set(batch) != set(self):
            raise ValueError("Column mismatch between batch {} and features {}".format(set(batch), set(self)))
        for key, column in batch.items():
            column = cast_to_python_objects(column)
            encoded_batch[key] = [encode_nested_example(self[key], obj) for obj in column]
        return encoded_batch

    def copy(self) -> "Features":
        """
        Make a deep copy of Features.

        Returns:
            :class:`Features`
        """
        return copy.deepcopy(self)

    def reorder_fields_as(self, other: "Features") -> "Features":
        """
        Reorder Features fields to match the field order of other Features.

        The order of the fields is important since it matters for the underlying arrow data.
        Re-ordering the fields allows to make the underlying arrow data type match.

        Args:
            other (:class:`Features`): The other Features to align with.

        Returns:
            :class:`Features`

        Examples:

            >>> from datasets import Features, Sequence, Value
            >>> # let's say we have to features with a different order of nested fields (for a and b for example)
            >>> f1 = Features({"root": Sequence({"a": Value("string"), "b": Value("string")})})
            >>> f2 = Features({"root": {"b": Sequence(Value("string")), "a": Sequence(Value("string"))}})
            >>> assert f1.type != f2.type
            >>> # re-ordering keeps the base structure (here Sequence is defined at the root level), but make the fields order match
            >>> f1.reorder_fields_as(f2)
            {'root': Sequence(feature={'b': Value(dtype='string', id=None), 'a': Value(dtype='string', id=None)}, length=-1, id=None)}
            >>> assert f1.reorder_fields_as(f2).type == f2.type
        """

        def recursive_reorder(source, target, stack=""):
            stack_position = " at " + stack[1:] if stack else ""
            if isinstance(target, Sequence):
                target = target.feature
                if isinstance(target, dict):
                    target = {k: [v] for k, v in target.items()}
                else:
                    target = [target]
            if isinstance(source, Sequence):
                source, id_, length = source.feature, source.id, source.length
                if isinstance(source, dict):
                    source = {k: [v] for k, v in source.items()}
                    reordered = recursive_reorder(source, target, stack)
                    return Sequence({k: v[0] for k, v in reordered.items()}, id=id_, length=length)
                else:
                    source = [source]
                    reordered = recursive_reorder(source, target, stack)
                    return Sequence(reordered[0], id=id_, length=length)
            elif isinstance(source, dict):
                if not isinstance(target, dict):
                    raise ValueError(f"Type mismatch: between {source} and {target}" + stack_position)
                if sorted(source) != sorted(target):
                    raise ValueError(f"Keys mismatch: between {source} and {target}" + stack_position)
                return {key: recursive_reorder(source[key], target[key], stack + f".{key}") for key in target}
            elif isinstance(source, list):
                if not isinstance(target, list):
                    raise ValueError(f"Type mismatch: between {source} and {target}" + stack_position)
                if len(source) != len(target):
                    raise ValueError(f"Length mismatch: between {source} and {target}" + stack_position)
                return [recursive_reorder(source[i], target[i], stack + f".<list>") for i in range(len(target))]
            else:
                return source

        return Features(recursive_reorder(self, other))
