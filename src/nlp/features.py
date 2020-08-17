# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
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
import logging
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, Sequence, Union

import numpy as np
import pandas as pd
import pyarrow as pa
from pandas.api.extensions import ExtensionArray as PandasExtensionArray
from pandas.api.extensions import ExtensionDtype as PandasExtensionDtype

from . import utils
from .utils.file_utils import _tf_available, _torch_available


logger = logging.getLogger(__name__)


if _torch_available:
    import torch

if _tf_available:
    import tensorflow as tf


def string_to_arrow(type_str: str) -> pa.DataType:
    if type_str not in pa.__dict__:
        if str(type_str + "_") not in pa.__dict__:
            raise ValueError(
                f"Neither {type_str} nor {type_str + '_'} seems to be a pyarrow data type. "
                f"Please make sure to use a correct data type, see: "
                f"https://arrow.apache.org/docs/python/api/datatypes.html#factory-functions"
            )
        arrow_data_type_str = str(type_str + "_")
    else:
        arrow_data_type_str = type_str

    return pa.__dict__[arrow_data_type_str]()


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
    if isinstance(obj, np.ndarray):
        return obj.tolist(), True
    elif _torch_available and isinstance(obj, torch.Tensor):
        return obj.detach().cpu().numpy().tolist(), True
    elif _tf_available and isinstance(obj, tf.Tensor):
        return obj.numpy().tolist(), True
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
    """ Encapsulate an Arrow datatype for easy serialization.
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


@dataclass
class Array2D:
    dtype: str
    id: Optional[str] = None
    # Automatically constructed
    _type: str = field(default="Array2D", init=False, repr=False)

    def __call__(self):
        return Array2DExtensionType(self.dtype)

    def encode_example(self, value):
        if isinstance(value, np.ndarray):
            value = value[np.newaxis, ...]
            value = value.tolist()
        elif isinstance(value, list):
            value = [value]
        encoded = pa.ExtensionArray.from_storage(self(), pa.array(value, self().storage_type_name))
        return encoded


# 2D main class and helper classes
class Array2DExtensionType(pa.PyExtensionType):

    dims: int = 2

    def __init__(self, dtype: str):
        self.inner_type = dtype
        self.storage_type_name = Array2DExtensionType._generate_dtype(self.inner_type, self.dims)
        pa.PyExtensionType.__init__(self, self.storage_type_name)

    def __reduce__(self):
        return Array2DExtensionType, (self.inner_type,)

    def __arrow_ext_class__(self):
        return Array2DExtensionArray

    @staticmethod
    def _generate_dtype(dtype, ndims=2):
        dtype = string_to_arrow(dtype)
        for i in range(ndims):
            if i == 0:
                dtype = pa.list_(dtype, -1)
            else:
                dtype = pa.list_(dtype)
        return dtype

    @staticmethod
    def _generate_flatten(storage, ndims=2):
        for i in range(ndims):
            storage = storage.flatten()
        return storage.to_numpy()

    @property
    def _get_arrow_ext_name(self):
        return Array2DExtensionArray._get_class().__name__


class Array2DExtensionArray(pa.ExtensionArray):

    dims: int = 2

    def __repr__(self):
        return f"{Array2DExtensionArray._get_class().__name__}:" f"{self._construct_shape(self.storage)}"

    def __array__(self):
        return self.to_numpy()

    def __iter__(self):
        for i in range(self.storage.offsets[-1].as_py()):
            yield self.to_numpy()[i].tolist()

    @staticmethod
    def _construct_shape(storage, ndims=2):
        shape = []
        prev_channels = 1
        for i in range(ndims):
            if i == 0:
                pass
            else:
                storage = storage.flatten()
            cur_channels = storage.offsets[-1].as_py() // prev_channels
            shape.append(cur_channels)
            prev_channels = cur_channels
        return tuple(shape)

    @classmethod
    def _get_class(cls):
        return cls

    @property
    def shape(self):
        return Array2DExtensionArray._construct_shape(self.storage)

    def to_numpy(self):
        numpy_arr = Array2DExtensionType._generate_flatten(self.storage, self.dims)
        numpy_arr = numpy_arr.reshape(len(self), *Array2DExtensionArray._construct_shape(self.storage))
        return numpy_arr

    def to_pylist(self):
        return self.to_numpy().tolist()


class PandasArrayExtensionDtype(PandasExtensionDtype):
    _metadata = "subtype"

    def __init__(self, subtype: Union["PandasArrayExtensionDtype", np.dtype]):
        self._subtype = subtype

    def __from_arrow__(self, array):
        if isinstance(array, pa.ChunkedArray):
            numpy_arr = np.vstack([chunk.to_numpy() for chunk in array.chunks])
        else:
            numpy_arr = array.to_numpy()
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
        return f"array[{self.subtype}]"

    @property
    def subtype(self) -> np.dtype:
        return self._subtype


class PandasArrayExtensionArray(PandasExtensionArray):
    def __init__(self, data: np.ndarray, copy: bool = False):
        self._data = data if not copy else np.array(data)
        self._dtype = PandasArrayExtensionDtype(data.dtype)

    def copy(self, deep: bool = False) -> "PandasArrayExtensionArray":
        return PandasArrayExtensionArray(self._data, copy=True)

    @classmethod
    def _from_sequence(
        cls, scalars, dtype: Optional[PandasArrayExtensionDtype] = None, copy: bool = False
    ) -> "PandasArrayExtensionArray":
        data = np.array(scalars, dtype=dtype if dtype is None else dtype.subtype, copy=copy)
        return PandasArrayExtensionArray(data, dtype=dtype, copy=copy)

    @classmethod
    def _concat_same_type(cls, to_concat: Sequence["PandasArrayExtensionArray"]) -> "PandasArrayExtensionArray":
        data = np.vstack([va._data for va in to_concat])
        return cls(data, copy=False)

    @property
    def dtype(self) -> PandasArrayExtensionDtype:
        return self._dtype

    @property
    def nbytes(self) -> int:
        return self._data.nbytes

    def isna(self) -> np.ndarray:
        if np.issubdtype(self.dtype.subtype, np.floating):
            return np.array(np.isnan(arr).any() for arr in self._data)
        return np.array((arr < 0).any() for arr in self._data)

    def __setitem__(self, key: Union[int, slice, np.ndarray], value: Any) -> None:
        raise NotImplementedError()

    def __getitem__(self, item: Union[int, slice, np.ndarray]) -> Union[np.ndarray, "PandasArrayExtensionArray"]:
        if isinstance(item, int):
            return self._data[item]
        return PandasArrayExtensionArray(self._data[item, :], copy=False)

    def take(
        self, indices: Sequence[int], allow_fill: bool = False, fill_value: bool = None
    ) -> "PandasArrayExtensionArray":
        indices = np.asarray(indices, dtype="int")
        if allow_fill:
            fill_value = (
                self.dtype.na_value if fill_value is None else np.asarray(fill_value, dtype=self.dtype.subtype)
            )
            mask = indices == -1
            if (indices < -1).any():
                raise ValueError("Invalid value in `indices`, must be all >= -1 for `allow_fill` is True")
            elif len(self) > 0:
                pass
            elif not np.all(mask):
                raise IndexError("Invalid take for empty PandasArrayExtensionArray, must be all -1.")
            else:
                data = np.array([fill_value] * len(indices), dtype=self.dtype.subtype)
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
    if isinstance(dtype, Array2DExtensionType):
        return PandasArrayExtensionDtype(dtype.inner_type)


@dataclass
class ClassLabel:
    """ Handle integer class labels. Here for compatiblity with tfds.

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
    names_file: str = None
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "int64"
    pa_type: ClassVar[Any] = pa.int64()
    _str2int: ClassVar[Dict[str, int]] = None
    _int2str: ClassVar[Dict[int, int]] = None
    _type: str = field(default="ClassLabel", init=False, repr=False)

    def __post_init__(self):
        # The label is explicitly set as undefined (no label defined)
        if not sum(bool(a) for a in (self.num_classes, self.names, self.names_file)):
            return

        # if sum(bool(a) for a in (self.num_classes, self.names, self.names_file)) != 1:
        #     raise ValueError("Only a single argument of ClassLabel() should be provided.")

        if self.num_classes is None:
            if self.names is None:
                self.names = self._load_names_from_file(self.names_file)
        else:
            if self.names is None:
                self.names = [str(i) for i in range(self.num_classes)]
            elif len(self.names) != self.num_classes:
                raise ValueError(
                    "ClassLabel number of names do not match the defined num_classes. "
                    "Got {} names VS {} num_classes".format(len(self.names), self.num_classes)
                )

        # Prepare mappings
        self._int2str = [str(name) for name in self.names]
        self._str2int = {name: i for i, name in enumerate(self._int2str)}
        if len(self._int2str) != len(self._str2int):
            raise ValueError("Some label names are duplicated. Each label name should be unique.")

        # If num_classes has been defined, ensure that num_classes and names match
        num_classes = len(self._str2int)
        if self.num_classes is None:
            self.num_classes = num_classes
        elif self.num_classes != num_classes:
            raise ValueError(
                "ClassLabel number of names do not match the defined num_classes. "
                "Got {} names VS {} num_classes".format(num_classes, self.num_classes)
            )

    def __call__(self):
        return self.pa_type

    def str2int(self, values: Union[str, Iterable]):
        """Conversion class name string => integer."""
        assert isinstance(values, str) or isinstance(values, Iterable), (
            f"Values {values} should be a string " f"or an Iterable (list, numpy array, pytorch, tensorflow tensors"
        )
        return_list = True
        if isinstance(values, str):
            values = [values]
            return_list = False

        output = []
        for value in values:
            if self._str2int:
                # strip key if not in dict
                if value not in self._str2int:
                    value = value.strip()
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
        assert isinstance(values, int) or isinstance(values, Iterable), (
            f"Values {values} should be an integer " f"or an Iterable (list, numpy array, pytorch, tensorflow tensors"
        )
        return_list = True
        if isinstance(values, int):
            values = [values]
            return_list = False

        if any(not 0 <= v < self.num_classes for v in values):
            raise ValueError("Invalid integer class label %d" % values)

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
        with open(names_filepath, "r") as f:
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

        nlp.features.Translation(languages=['en', 'fr', 'de'])

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

        nlp.features.Translation(languages=['en', 'fr', 'de'])

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

    languages: List = None
    num_languages: int = None
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
    """ Construct a list of feature from a single type or a dict of types.
        Mostly here for compatiblity with tfds.
    """

    feature: Any
    length: int = -1
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "list"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Sequence", init=False, repr=False)


FeatureType = Union[dict, list, tuple, Value, ClassLabel, Translation, TranslationVariableLanguages, Sequence, Array2D]


def get_nested_type(schema: FeatureType) -> pa.DataType:
    """ Convert our Feature nested object in an Apache Arrow type """
    # Nested structures: we allow dict, list/tuples, sequences
    if isinstance(schema, dict):
        return pa.struct(
            {key: get_nested_type(schema[key]) for key in sorted(schema)}
        )  # sort to make the type deterministic
    elif isinstance(schema, (list, tuple)):
        assert len(schema) == 1, "We defining list feature, you should just provide one example of the inner type"
        inner_type = get_nested_type(schema[0])
        return pa.list_(inner_type)
    elif isinstance(schema, Sequence):
        inner_type = get_nested_type(schema.feature)
        # We allow to reverse list of dict => dict of list for compatiblity with tfds
        if isinstance(inner_type, pa.StructType):
            return pa.struct(dict(sorted((f.name, pa.list_(f.type, schema.length)) for f in inner_type)))
        return pa.list_(inner_type, schema.length)

    # Other objects are callable which returns their data type (ClassLabel, Tensor, Translation, Arrow datatype creation methods)
    return schema()


def encode_nested_example(schema, obj):
    """ Encode a nested example.
        This is used since some features (in particular ClassLabel) have some logic during encoding.
    """
    # Nested structures: we allow dict, list/tuples, sequences
    if isinstance(schema, dict):
        return dict(
            (k, encode_nested_example(sub_schema, sub_obj)) for k, (sub_schema, sub_obj) in utils.zip_dict(schema, obj)
        )
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
    elif isinstance(schema, (ClassLabel, TranslationVariableLanguages, Value, Array2D)):
        return schema.encode_example(obj)
    # Other object should be directly convertible to a native Arrow type (like Translation and Translation)
    return obj


def generate_from_dict(obj: Any):
    """ Regenerate the nested feature object from a serialized dict.
        We use the '_type' fields to get the dataclass name to load.
    """
    # Nested structures: we allow dict, list/tuples, sequences
    if isinstance(obj, list):
        return [generate_from_dict(value) for value in obj]
    # Otherwise we have a dict or a dataclass
    if "_type" not in obj:
        return {key: generate_from_dict(value) for key, value in obj.items()}
    class_type = globals()[obj.pop("_type")]

    if class_type == Sequence:
        return Sequence(feature=generate_from_dict(obj["feature"]), length=obj["length"])
    return class_type(**obj)


def generate_from_arrow_type(pa_type: pa.DataType):
    if isinstance(pa_type, pa.StructType):
        return {field.name: generate_from_arrow_type(field.type) for field in pa_type}
    elif isinstance(pa_type, pa.FixedSizeListType):
        return Sequence(feature=generate_from_arrow_type(pa_type.value_type), length=pa_type.list_size)
    elif isinstance(pa_type, pa.ListType):
        feature = generate_from_arrow_type(pa_type.value_type)
        if isinstance(feature, (dict, tuple, list)):
            return [feature]
        return Sequence(feature=feature)
    elif isinstance(pa_type, Array2DExtensionType):
        return Array2D(dtype=pa_type.inner_type)
    elif isinstance(pa_type, pa.DictionaryType):
        raise NotImplementedError  # TODO(thom) this will need access to the dictionary as well (for labels). I.e. to the py_table
    elif isinstance(pa_type, pa.DataType):
        return Value(dtype=str(pa_type))
    else:
        raise ValueError(f"Cannot convert {pa_type} to a Feature type.")


class Features(dict):
    @property
    def type(self):
        return get_nested_type(self)

    @classmethod
    def from_arrow_schema(cls, pa_schema: pa.Schema) -> "Features":
        obj = {field.name: generate_from_arrow_type(field.type) for field in pa_schema}
        return cls(**obj)

    @classmethod
    def from_dict(cls, dic) -> "Features":
        obj = generate_from_dict(dic)
        return cls(**obj)

    def encode_example(self, example):
        example = cast_to_python_objects(example)
        return encode_nested_example(self, example)

    def encode_batch(self, batch):
        encoded_batch = {}
        if set(batch) != set(self):
            raise ValueError("Column mismatch between batch {} and features {}".format(set(batch), set(self)))
        for key, column in batch.items():
            encoded_batch[key] = [encode_nested_example(self[key], cast_to_python_objects(obj)) for obj in column]
        return encoded_batch

    def copy(self):
        return Features(super().copy())
