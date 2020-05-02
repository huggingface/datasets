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
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Union

import pyarrow as pa

from . import utils


logger = logging.getLogger(__name__)


def get_nested_type(schema):
    # Nested structures: we allow dict, list/tuples, sequences
    if isinstance(schema, dict):
        return pa.struct({key: get_nested_type(value) for key, value in schema.items()})
    elif isinstance(schema, (list, tuple)):
        assert len(schema) == 1, "We defining list feature, you should just provide one example of the inner type"
        inner_type = get_nested_type(schema[0])
        return pa.list_(inner_type)
    elif isinstance(schema, Sequence):
        inner_type = get_nested_type(schema.feature)
        # We allow to reverse list of dict => dict of list for compatiblity with tfds
        if isinstance(inner_type, pa.StructType):
            return pa.struct(dict((f.name, pa.list_(f.type, intlist_size=schema.length)) for f in inner_type))
        return pa.list_(inner_type, intlist_size=schema.length)

    # Other objects are callable which returns their data type (ClassLabel, Tensor, Translation, Arrow datatype creation methods)
    return schema()


def encode_nested_example(schema, obj):
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
            return dict(
                (k, [encode_nested_example(sub_schema, o) for o in sub_obj])
                for k, (sub_schema, sub_obj) in utils.zip_dict(schema, obj)
            )
        return [encode_nested_example(schema.feature, o) for o in obj]

    # Object with special encoding:
    # ClassLabel will convert from string to int, TranslationVariableLanguages does some checks
    elif isinstance(schema, (ClassLabel, TranslationVariableLanguages)):
        return schema.encode_example(obj)

    # Other object should be directly convertible to a native Arrow type (like Translation and Translation)
    return obj


@dataclass
class Tensor:
    """ Construct a 0D or 1D Tensor feature.
        If 0D, the Tensor is an dtype element, if 1D it will be a fixed length list or dtype elements.
        Mostly here for compatiblity with tfds.
    """

    shape: Union[Tuple[int], List[int]]
    dtype: pa.DataType

    def __post_init__(self):
        assert len(self.shape) < 2, "Tensor can only take 0 or 1 dimensional shapes ."
        if len(self.shape) == 1:
            self.dtype = pa.list_(self.dtype(), intlist_size=self.shape[0])
        else:
            self.dtype = self.dtype()

    def __call__(self):
        return self.dtype


class ClassLabel(object):
    """ Handle integer class labels.
        Here for compatiblity with tfds.
    """

    def __init__(self, num_classes=None, names=None, names_file=None):
        """Constructs a ClassLabel.

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
        self._num_classes = None
        self._str2int = None
        self._int2str = None

        # The label is explicitly set as undefined (no label defined)
        if not sum(bool(a) for a in (num_classes, names, names_file)):
            return

        if sum(bool(a) for a in (num_classes, names, names_file)) != 1:
            raise ValueError("Only a single argument of ClassLabel() should be provided.")

        if num_classes:
            self._num_classes = num_classes
        else:
            self.names = names or self._load_names_from_file(names_file)

    def __call__(self):
        return pa.int64()

    @property
    def num_classes(self):
        return self._num_classes

    @property
    def names(self):
        if not self._int2str:
            return [str(i) for i in range(self._num_classes)]
        return list(self._int2str)

    @names.setter
    def names(self, new_names):
        int2str = [str(name) for name in new_names]
        # Names can only be defined once
        if self._int2str is not None and self._int2str != int2str:
            raise ValueError(
                "Trying to overwrite already defined ClassLabel names. Previous: {} "
                ", new: {}".format(self._int2str, int2str)
            )

        # Set-up [new] names
        self._int2str = int2str
        self._str2int = {name: i for i, name in enumerate(self._int2str)}
        if len(self._int2str) != len(self._str2int):
            raise ValueError("Some label names are duplicated. Each label name should be unique.")

        # If num_classes has been defined, ensure that num_classes and names match
        num_classes = len(self._str2int)
        if self._num_classes is None:
            self._num_classes = num_classes
        elif self._num_classes != num_classes:
            raise ValueError(
                "ClassLabel number of names do not match the defined num_classes. "
                "Got {} names VS {} num_classes".format(num_classes, self._num_classes)
            )

    def str2int(self, str_value):
        """Conversion class name string => integer."""
        str_value = str(str_value)
        if self._str2int:
            return self._str2int[str_value]

        # No names provided, try to integerize
        failed_parse = False
        try:
            int_value = int(str_value)
        except ValueError:
            failed_parse = True
        if failed_parse or not 0 <= int_value < self._num_classes:
            raise ValueError("Invalid string class label %s" % str_value)
        return int_value

    def int2str(self, int_value):
        """Conversion integer => class name string."""
        if self._int2str:
            # Maybe should support batched np array/eager tensors, to allow things
            # like
            # out_ids = model(inputs)
            # labels = cifar10.info.features['label'].int2str(out_ids)
            return self._int2str[int_value]

        # No names provided, return str(int)
        if not 0 <= int_value < self._num_classes:
            raise ValueError("Invalid integer class label %d" % int_value)
        return str(int_value)

    def encode_example(self, example_data):
        if self._num_classes is None:
            raise ValueError(
                "Trying to use ClassLabel feature with undefined number of class. "
                "Please set ClassLabel.names or num_classes."
            )

        # If a string is given, convert to associated integer
        if isinstance(example_data, str):
            example_data = self.str2int(example_data)

        # Allowing -1 to mean no label.
        if not -1 <= example_data < self._num_classes:
            raise ValueError(
                "Class label %d greater than configured num_classes %d" % (example_data, self._num_classes)
            )
        return example_data

    def save_metadata(self, data_dir, feature_name=None):
        """See base class for details."""
        # Save names if defined
        if self._str2int is not None:
            names_filepath = self._get_names_filepath(data_dir, feature_name)
            self._write_names_to_file(names_filepath, self.names)

    def load_metadata(self, data_dir, feature_name=None):
        """See base class for details."""
        # Restore names if defined
        names_filepath = self._get_names_filepath(data_dir, feature_name)
        if os.path.exists(names_filepath):
            self.names = self._load_names_from_file(names_filepath)

    def _additional_repr_info(self):
        return {"num_classes": self.num_classes}

    @staticmethod
    def _get_names_filepath(data_dir, feature_name):
        return os.path.join(data_dir, "{}.labels.txt".format(feature_name))

    @staticmethod
    def _load_names_from_file(names_filepath):
        with open(names_filepath, "r") as f:
            return [name.strip() for name in f.read().split("\n") if name.strip()]  # Filter empty names

    @staticmethod
    def _write_names_to_file(names_filepath, names):
        with open(names_filepath, "w") as f:
            f.write("\n".join(names) + "\n")


@dataclass
class Sequence:
    """ Construct a list of feature from a single type or a dict of types.
        Mostly here for compatiblity with tfds.
    """

    feature: Any
    length: int = -1


class Translation(object):
    """`FeatureConnector` for translations with fixed languages per example.
        Here for compatiblity with tfds.

    Input: The Translate feature accepts a dictionary for each example mapping
        string language codes to string translations.

    Output: A dictionary mapping string language codes to translations as `Text`
        features.

    Example:
    At construction time:

    ```
    nlp.features.Translation(languages=['en', 'fr', 'de'])
    ```

    During data generation:

    ```
    yield {
            'en': 'the cat',
            'fr': 'le chat',
            'de': 'die katze'
    }
    ```

    Tensor returned by `.as_dataset()`:

    ```
    {
            'en': 'the cat',
            'fr': 'le chat',
            'de': 'die katze',
    }
    ```
    """

    def __init__(self, languages):
        """Constructs a Translation FeatureConnector.

        Args:
            languages: `list<string>` Full list of languages codes.
        """
        self._languages = languages

    @property
    def languages(self):
        """ List of languages. """
        return self._languages

    def __call__(self):
        return pa.struct({lang: pa.string() for lang in self._languages})


class TranslationVariableLanguages(object):
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

    Example (fixed language list):
    At construction time:

    ```
    nlp.features.Translation(languages=['en', 'fr', 'de'])
    ```

    During data generation:

    ```
    yield {
            'en': 'the cat',
            'fr': ['le chat', 'la chatte,']
            'de': 'die katze'
    }
    ```

    Tensor returned :

    ```
    {
            'language': ['en', 'de', 'fr', 'fr'],
            'translation': ['the cat', 'die katze', 'la chatte', 'le chat'],
    }
    ```
    """

    def __init__(self, languages=None):
        """Constructs a Translation FeatureConnector.

        Args:
            languages: `list<string>` (optional), full list of language codes if known
                in advance.
        """
        self._languages = set(languages) if languages else None

    def __call__(self):
        return pa.struct({"language": pa.list_(pa.string()), "translation": pa.list_(pa.string())})

    @property
    def num_languages(self):
        """Number of languages or None, if not specified in advance."""
        return len(self._languages) if self._languages else None

    @property
    def languages(self):
        """List of languages or None, if not specified in advance."""
        return sorted(list(self._languages)) if self._languages else None

    def encode_example(self, translation_dict):
        if self.languages and set(translation_dict) - self._languages:
            raise ValueError(
                "Some languages in example ({0}) are not in valid set ({1}).".format(
                    ", ".join(sorted(set(translation_dict) - self._languages)), ", ".join(self.languages)
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


class Features(object):
    def __init__(self, schema: Dict[str, Any]):
        self._schema = schema
        self._type = get_nested_type(schema)

    @property
    def type(self):
        return self._type

    def encode_example(self, example):
        return encode_nested_example(self._schema, example)
