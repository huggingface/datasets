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
"""FeatureDict: Main feature connector container.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pyarrow as pa

from .. import utils
from .feature import Tensor, FeatureConnector
from .top_level_feature import TopLevelFeature


class FeaturesDict(TopLevelFeature):
    """Composite `FeatureConnector`; each feature in `dict` has its own connector.

    The encode/decode method of the spec feature will recursively encode/decode
    every sub-connector given on the constructor.
    Other features can inherit from this class and call super() in order to get
    nested container.

    Example:

    For DatasetInfo:

    ```
    features = nlp.features.FeaturesDict({
            'input': nlp.features.Image(),
            'output': pa.int32,
    })
    ```

    At generation time:

    ```
    for image, label in generate_examples:
        yield {
                'input': image,
                'output': label
        }
    ```

    At pa.data.Dataset() time:

    ```
    for example in nlp.load(...):
        tf_input = example['input']
        tf_output = example['output']
    ```

    For nested features, the FeaturesDict will internally flatten the keys for the
    features and the conversion to pa.train.Example. Indeed, the pa.train.Example
    proto do not support nested feature, while pa.data.Dataset does.
    But internal transformation should be invisible to the user.

    Example:

    ```
    nlp.features.FeaturesDict({
            'input': pa.int32,
            'target': {
                    'height': pa.int32,
                    'width': pa.int32,
            },
    })
    ```

    Will internally store the data as:

    ```
    {
            'input': pa.io.FixedLenFeature(shape=(), dtype=pa.int32),
            'target/height': pa.io.FixedLenFeature(shape=(), dtype=pa.int32),
            'target/width': pa.io.FixedLenFeature(shape=(), dtype=pa.int32),
    }
    ```

    """

    def __init__(self, feature_dict):
        """Initialize the features.

        Args:
            feature_dict (dict): Dictionary containing the feature connectors of a
                example. The keys should correspond to the data dict as returned by
                pa.data.Dataset(). Types (pa.int32,...) and dicts will automatically
                be converted into FeatureConnector.

        Raises:
            ValueError: If one of the given features is not recognized
        """
        super(FeaturesDict, self).__init__()
        self._feature_dict = {k: to_feature(v) for k, v in feature_dict.items()}

    # Dict functions.
    # In Python 3, should inherit from collections.abc.Mapping().

    def keys(self):
        return self._feature_dict.keys()

    def items(self):
        return self._feature_dict.items()

    def values(self):
        return self._feature_dict.values()

    def __contains__(self, k):
        return k in self._feature_dict

    def __getitem__(self, key):
        """Return the feature associated with the key."""
        return self._feature_dict[key]

    def __len__(self):
        return len(self._feature_dict)

    def __iter__(self):
        return iter(self._feature_dict)

    # Feature functions

    def get_type(self) -> pa.DataType:
        """See base class for details."""
        return  pa.struct({
                feature_key: feature.get_type()
                for feature_key, feature in self._feature_dict.items()
        })

    def encode_example(self, example_dict):
        """See base class for details."""
        return {
                k: feature.encode_example(example_value)
                for k, (feature, example_value)
                in utils.zip_dict(self._feature_dict, example_dict)
        }

    def _flatten(self, x):
        """See base class for details."""
        if x and not isinstance(x, (dict, FeaturesDict)):
            raise ValueError(
                    'Error while flattening dict: FeaturesDict received a non dict item: '
                    '{}'.format(x))

        cache = {'counter': 0}  # Could use nonlocal in Python
        def _get(k):
            if x and k in x:
                cache['counter'] += 1
                return x[k]
            return None

        out = []
        for k, f in sorted(self.items()):
            out.extend(f._flatten(_get(k)))  # pylint: disable=protected-access

        if x and cache['counter'] != len(x):
            raise ValueError(
                    'Error while flattening dict: Not all dict items have been consumed, '
                    'this means that the provided dict structure does not match the '
                    '`FeatureDict`. Please check for typos in the key names. '
                    'Available keys: {}. Unrecognized keys: {}'.format(
                            list(self.keys()), list(set(x.keys()) - set(self.keys())))
            )
        return out

    def _nest(self, list_x):
        """See base class for details."""
        curr_pos = 0
        out = {}
        for k, f in sorted(self.items()):
            offset = len(f._flatten(None))  # pylint: disable=protected-access
            out[k] = f._nest(list_x[curr_pos:curr_pos+offset])  # pylint: disable=protected-access
            curr_pos += offset
        if curr_pos != len(list_x):
            raise ValueError(
                    'Error while nesting: Expected length {} does not match input '
                    'length {} of {}'.format(curr_pos, len(list_x), list_x))
        return out

    def save_metadata(self, data_dir, feature_name=None):
        """See base class for details."""
        # Recursively save all child features
        for feature_key, feature in self._feature_dict.items():
            feature_key = feature_key.replace('/', '.')
            if feature_name:
                feature_key = '-'.join((feature_name, feature_key))
            feature.save_metadata(data_dir, feature_name=feature_key)

    def load_metadata(self, data_dir, feature_name=None):
        """See base class for details."""
        # Recursively load all child features
        for feature_key, feature in self._feature_dict.items():
            feature_key = feature_key.replace('/', '.')
            if feature_name:
                feature_key = '-'.join((feature_name, feature_key))
            feature.load_metadata(data_dir, feature_name=feature_key)


class Sequence(TopLevelFeature):
    """Composite `FeatureConnector` for a `dict` where each value is a list.

    `Sequence` correspond to sequence of `nlp.features.FeatureConnector`. At
    generation time, a list for each of the sequence element is given. The output
    of `pa.data.Dataset` will batch all the elements of the sequence together.

    If the length of the sequence is static and known in advance, it should be
    specified in the constructor using the `length` param.

    Note that `Sequence` does not support features which are of type
    `pa.io.FixedLenSequenceFeature`.

    Example:
    At construction time:

    ```
    nlp.features.Sequence(nlp.features.Image(), length=NB_FRAME)
    ```

    or:

    ```
    nlp.features.Sequence({
            'frame': nlp.features.Image(shape=(64, 64, 3))
            'action': nlp.features.ClassLabel(['up', 'down', 'left', 'right'])
    }, length=NB_FRAME)
    ```

    During data generation:

    ```
    yield {
            'frame': np.ones(shape=(NB_FRAME, 64, 64, 3)),
            'action': ['left', 'left', 'up', ...],
    }
    ```

    Tensor returned by `.as_dataset()`:

    ```
    {
            'frame': pa.Tensor(shape=(NB_FRAME, 64, 64, 3), dtype=pa.uint8),
            'action': pa.Tensor(shape=(NB_FRAME,), dtype=pa.int64),
    }
    ```

    At generation time, you can specify a list of features dict, a dict of list
    values or a stacked numpy array. The lists will automatically be distributed
    into their corresponding `FeatureConnector`.

    """

    def __init__(self, feature, length=None, **kwargs):
        """Construct a sequence.

        Args:
            feature: `dict`, the features to wrap
            length: `int`, length of the sequence if static and known in advance
            **kwargs: `dict`, constructor kwargs of `nlp.features.FeaturesDict`
        """
        # Convert {} => FeaturesDict, pa.int32 => pa.int32()
        self._feature = to_feature(feature)
        self._length = length
        super(Sequence, self).__init__(**kwargs)

    @property
    def feature(self):
        """The inner feature."""
        return self._feature

    def get_type(self):
        """See base class for details."""
        # Add the additional length dimension to every serialized features
        inner_type = self._feature.get_type()
        if isinstance(inner_type, pa.StructType):
            return pa.struct(dict((f.name, pa.list_(f.type)) for f in inner_type))
        return pa.list_(inner_type)

    def encode_example(self, example_dict):
        # Convert nested dict[list] into list[nested dict]
        sequence_elements = _transpose_dict_list(example_dict)

        # If length is static, ensure that the given length match
        if self._length is not None and len(sequence_elements) != self._length:
            raise ValueError(
                    'Input sequence length do not match the defined one. Got {} != '
                    '{}'.format(len(sequence_elements), self._length)
            )

        # Empty sequences return empty arrays
        if not sequence_elements:
            def _build_empty_np(serialized_info):
                return []
                # return np.empty(
                #         shape=tuple(s if s else 0 for s in serialized_info.shape),
                #         dtype=serialized_info.dtype.as_numpy_dtype,
                # )

            return utils.map_nested(_build_empty_np, self.get_serialized_info())

        # Encode each individual elements
        sequence_elements = [
                self.feature.encode_example(sequence_elem)
                for sequence_elem in sequence_elements
        ]

        # Then convert back list[nested dict] => nested dict[list]
        def _stack_nested(sequence_elements):
            """Recursivelly stack the tensors from the same dict field."""
            if isinstance(sequence_elements[0], dict):
                return {
                        # Stack along the first dimension
                        k: _stack_nested(sub_sequence)
                        for k, sub_sequence in utils.zip_dict(*sequence_elements)
                }
            # Note: As each field can be a nested ragged list, we don't check here
            # that all elements from the list have matching dtype/shape.
            # Checking is done in `example_serializer` when elements
            # are converted to numpy array and stacked togethers.
            return list(sequence_elements)

        return _stack_nested(sequence_elements)

    def _flatten(self, x):
        """See base class for details."""
        if isinstance(x, Sequence):
            return self.feature._flatten(x.feature)  # pylint: disable=protected-access
        return self.feature._flatten(x)  # pylint: disable=protected-access

    def _nest(self, list_x):
        """See base class for details."""
        return self.feature._nest(list_x)  # pylint: disable=protected-access

    def save_metadata(self, *args, **kwargs):
        """See base class for details."""
        self._feature.save_metadata(*args, **kwargs)

    def load_metadata(self, *args, **kwargs):
        """See base class for details."""
        self._feature.load_metadata(*args, **kwargs)

    def __getitem__(self, key):
        """Convenience method to access the underlying features."""
        return self._feature[key]

    def __getattr__(self, key):
        """Allow to access the underlying attributes directly."""
        return getattr(self._feature, key)

    # The __getattr__ method triggers an infinite recursion loop when loading a
    # pickled instance. So we override that name in the instance dict, and remove
    # it when unplickling.
    def __getstate__(self):
        state = self.__dict__.copy()
        state['__getattr__'] = 0
        return state

    def __setstate__(self, state):
        del state['__getattr__']
        self.__dict__.update(state)


def _np_to_list(elem):
    """Returns list from list, tuple or ndarray."""
    if isinstance(elem, list):
        return elem
    elif isinstance(elem, tuple):
        return list(elem)
    elif isinstance(elem, np.ndarray):
        return list(elem)
    else:
        raise ValueError(
                'Input elements of a sequence should be either a numpy array, a '
                'python list or tuple. Got {}'.format(type(elem)))


def _transpose_dict_list(dict_list):
    """Transpose a nested dict[list] into a list[nested dict]."""
    # 1. Unstack numpy arrays into list
    dict_list = utils.map_nested(_np_to_list, dict_list, dict_only=True)

    # 2. Extract the sequence length (and ensure the length is constant for all
    # elements)
    length = {'value': None}  # dict because `nonlocal` is Python3 only
    def update_length(elem):
        if length['value'] is None:
            length['value'] = len(elem)
        elif length['value'] != len(elem):
            raise ValueError(
                    'The length of all elements of one sequence should be the same. '
                    'Got {} != {}'.format(length['value'], len(elem)))
        return elem
    utils.map_nested(update_length, dict_list, dict_only=True)

    # 3. Extract each individual elements
    return [
            utils.map_nested(lambda elem: elem[i], dict_list, dict_only=True)   # pylint: disable=cell-var-from-loop
            for i in range(length['value'])
    ]


def to_feature(value):
    """Convert the given value to Feature if necessary."""
    if isinstance(value, FeatureConnector):
        return value
    elif isinstance(value, dict):
        return FeaturesDict(value)
    return Tensor(shape=(), dtype=value)
