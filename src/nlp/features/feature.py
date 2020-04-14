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
"""Feature connector.

FeatureConnector is a way of abstracting what data is returned by the
datasets builders from how they are encoded/decoded from file.

# Use FeatureConnector in `GeneratorBasedBuilder`

1) In the _build_info() function, define the features as you would like them
to be returned by the pa.data.Dataset() object.

Ex:

    ```
    features=features.FeaturesDict({
            'input': features.Image(),
            'target': features.Text(encoder=SubWordEncoder()),
            'extra_data': {
                    'label_id': pa.int64,
                    'language': pa.string,
            }
    })
    ```

The pa.data.Dataset will return each examples as a dict:

    ```
    {
            'input': pa.Tensor(shape=(batch, height, width, channel), pa.uint8),
            'target': pa.Tensor(shape=(batch, sequence_length), pa.int64),
            'extra_data': {
                    'label_id': pa.Tensor(shape=(batch,), pa.int64),
                    'language': pa.Tensor(shape=(batch,), pa.string),
            }
    }
    ```

2) In the generator function, yield the examples to match what you have defined
in the spec. The values will automatically be encoded.

    ```
    yield {
            'input': np_image,
            'target': 'This is some text',
            'extra_data': {
                    'label_id': 43,
                    'language': 'en',
            }
    }
    ```

# Create your own FeatureConnector

To create your own feature connector, you need to inherit from FeatureConnector
and implement the abstract methods.

1. If your connector only contains one value, then the get_type,
     get_tensor_info, encode_example, and decode_example can directly process
     single value, without wrapping it in a dict.

2. If your connector is a container of multiple sub-connectors, the easiest
     way is to inherit from features.FeaturesDict and use the super() methods to
     automatically encode/decode the sub-connectors.

This file contains the following FeatureConnector:
 * FeatureConnector: The abstract base class defining the interface
 * FeaturesDict: Container of FeatureConnector
 * Tensor: Simple tensor value with static or dynamic shape

"""

import abc
import collections

import numpy as np

import pyarrow as pa


class TensorInfo(object):
    """Structure containing info on the `pa.Tensor` shape/dtype."""

    def __init__(self, shape, dtype, default_value=None, sequence_rank=None):
        """Constructor.

        Args:
            shape: `tuple[int]`, shape of the tensor
            dtype: Tensor dtype
            default_value: Used for retrocompatibility with previous files if a new
                field is added to provide a default value when reading the file.
            sequence_rank: `int`, Number of `nlp.features.Sequence` dimension.
        """
        self.shape = shape
        self.dtype = dtype
        self.default_value = default_value
        self.sequence_rank = sequence_rank or 0

    @classmethod
    def copy_from(cls, tensor_info):
        """Copy constructor."""
        return cls(
                shape=tensor_info.shape,
                dtype=tensor_info.dtype,
                default_value=tensor_info.default_value,
                sequence_rank=tensor_info.sequence_rank,
        )

    def __eq__(self, other):
        """Equality."""
        return (
                self.shape == other.shape and
                self.dtype == other.dtype and
                self.default_value == other.default_value
        )

    def __repr__(self):
        return '{}(shape={}, dtype={})'.format(
                type(self).__name__,
                self.shape,
                repr(self.dtype),
        )


class FeatureConnector(metaclass=abc.ABCMeta):
    """Abstract base class for feature types.

    This class provides an interface between the way the information is stored
    on disk, and the way it is presented to the user.

    Here is a diagram on how FeatureConnector methods fit into the data
    generation/reading:

    ```
    generator => encode_example() => tf_example => decode_example() => data dict
    ```

    The connector can either get raw or dictionary values as input, depending on
    the connector type.

    """

    @property
    def shape(self):
        """Return the shape (or dict of shape) of this FeatureConnector."""
        raise NotImplementedError

    @property
    def dtype(self):
        """Return the dtype (or dict of dtype) of this FeatureConnector."""
        return self.get_type()
        # return utils.map_nested(lambda t: t.dtype, self.get_type())

    # @abc.abstractmethod
    def get_type(self):
        """Return the shape/dtype of features after encoding (for the adapter).

        The `FileAdapter` then use those information to write data on disk.

        This function indicates how this feature is encoded on file internally.
        The DatasetBuilder are written on disk as pa.train.Example proto.

        Ex:

        ```
        return {
                'image': nlp.features.TensorInfo(shape=(None,), dtype=pa.uint8),
                'height': nlp.features.TensorInfo(shape=(), dtype=pa.int32),
                'width': nlp.features.TensorInfo(shape=(), dtype=pa.int32),
        }
        ```

        FeatureConnector which are not containers should return the feature proto
        directly:

        ```
        return nlp.features.TensorInfo(shape=(64, 64), pa.uint8)
        ```

        If not defined, the retuned values are automatically deduced from the
        `get_tensor_info` function.

        Returns:
            features: Either a dict of feature proto object, or a feature proto object

        """
        raise NotImplementedError

    @abc.abstractmethod
    def encode_example(self, example_data):
        """Encode the feature dict into tf-example compatible input.

        The input example_data can be anything that the user passed at data
        generation. For example:

        For features:

        ```
        features={
                'image': nlp.features.Image(),
                'custom_feature': nlp.features.CustomFeature(),
        }
        ```

        At data generation (in `_generate_examples`), if the user yields:

        ```
        yield {
                'image': 'path/to/img.png',
                'custom_feature': [123, 'str', lambda x: x+1]
        }
        ```

        Then:

         * `nlp.features.Image.encode_example` will get `'path/to/img.png'` as
             input
         * `nlp.features.CustomFeature.encode_example` will get `[123, 'str',
             lambda x: x+1] as input

        Args:
            example_data: Value or dictionary of values to convert into tf-example
                compatible data.

        Returns:
            tfexample_data: Data or dictionary of data to write as tf-example. Data
                can be a list or numpy array.
                Note that numpy arrays are flattened so it's the feature connector
                responsibility to reshape them in `decode_example()`.
                Note that pa.train.Example only supports int64, float32 and string so
                the data returned here should be integer, float or string. User type
                can be restored in `decode_example()`.
        """
        raise NotImplementedError

    def decode_example(self, tfexample_data):
        """Decode the feature dict to TF compatible input.

        Note: If eager is not enabled, this function will be executed as a
        tensorflow graph (in `pa.data.Dataset.map(features.decode_example)`).

        Args:
            tfexample_data: Data or dictionary of data, as read by the tf-example
                reader. It correspond to the `pa.Tensor()` (or dict of `pa.Tensor()`)
                extracted from the `pa.train.Example`, matching the info defined in
                `get_type()`.

        Returns:
            tensor_data: Tensor or dictionary of tensor, output of the pa.data.Dataset
                object
        """
        return tfexample_data

    def decode_batch_example(self, tfexample_data):
        """Decode multiple features batched in a single pa.Tensor.

        This function is used to decode features wrapped in
        `nlp.features.Sequence()`.
        By default, this function apply `decode_example` on each individual
        elements using `pa.map_fn`. However, for optimization, features can
        overwrite this method to apply a custom batch decoding.

        Args:
            tfexample_data: Same `pa.Tensor` inputs as `decode_example`, but with
                and additional first dimension for the sequence length.

        Returns:
            tensor_data: Tensor or dictionary of tensor, output of the pa.data.Dataset
                object
        """
        # Note: This all works fine in Eager mode (without pa.function) because
        # pa.data pipelines are always executed in Graph mode.

        # Apply the decoding to each of the individual distributed features.
        return tf.map_fn(
                self.decode_example,
                tfexample_data,
                dtype=self.dtype,
                parallel_iterations=10,
                back_prop=False,
                name='sequence_decode',
        )


    def decode_ragged_example(self, tfexample_data):
        """Decode nested features from a pa.RaggedTensor.

        This function is used to decode features wrapped in nested
        `nlp.features.Sequence()`.
        By default, this function apply `decode_batch_example` on the flat values
        of the ragged tensor. For optimization, features can
        overwrite this method to apply a custom batch decoding.

        Args:
            tfexample_data: `pa.RaggedTensor` inputs containing the nested encoded
                examples.

        Returns:
            tensor_data: The decoded `pa.RaggedTensor` or dictionary of tensor,
                output of the pa.data.Dataset object
        """
        return tf.ragged.map_flat_values(self.decode_batch_example, tfexample_data)

    def _flatten(self, x):
        """Flatten the input dict into a list of values.

        For instance, the following feature:
        ```
        feature = FeatureDict({
                'a': w,
                'b': x,
                'c': {
                        'd': y,
                        'e': z,
                },
        })
        ```

        Applied to the following `dict`:
        ```
        feature._flatten({
                'b': X,
                'c': {
                        'd': Y,
                },
        })
        ```

        Will produce the following flattened output:
        ```
        [
                None,
                X,
                Y,
                None,
        ]
        ```

        Args:
            x: A nested `dict` like structure matching the structure of the
            `FeatureConnector`. Note that some elements may be missing.

        Returns:
            `list`: The flattened list of element of `x`. Order is guaranteed to be
            deterministic. Missing elements will be filled with `None`.
        """
        return [x]

    def _nest(self, list_x):
        """Pack the list into a nested dict.

        This is the reverse function of flatten.

        For instance, the following feature:
        ```
        feature = FeatureDict({
                'a': w,
                'b': x,
                'c': {
                        'd': y,
                        'e': z,
                },
        })
        ```

        Applied to the following `dict`:
        ```
        feature._nest([
                None,
                X,
                Y,
                None,
        ])
        ```

        Will produce the following flattened output:
        ```
        {
                'a': None,
                'b': X,
                'c': {
                        'd': Y,
                        'e': None,
                },
        }
        ```

        Args:
            list_x: List of values matching the flattened `FeatureConnector`
                structure. Missing values should be filled with None.

        Returns:
            nested_x: nested `dict` matching the flattened `FeatureConnector`
                structure.
        """
        assert len(list_x) == 1
        return list_x[0]

    def _additional_repr_info(self):
        """Override to return additional info to go into __repr__."""
        return {}

    def __repr__(self):
        """Display the feature dictionary."""
        tensor_info = self.get_type()
        return str(tensor_info)
        # if not isinstance(tensor_info, TensorInfo):
        #     return '{}({})'.format(type(self).__name__, tensor_info)

        # # Ensure ordering of keys by adding them one-by-one
        # repr_info = collections.OrderedDict()
        # repr_info['shape'] = tensor_info.shape
        # repr_info['dtype'] = repr(tensor_info.dtype)
        # additional_info = self._additional_repr_info()
        # for k, v in additional_info.items():
        #     repr_info[k] = v

        # info_str = ', '.join(['%s=%s' % (k, v) for k, v in repr_info.items()])
        # return '{}({})'.format(
        #         type(self).__name__,
        #         info_str,
        # )

    def save_metadata(self, data_dir, feature_name):
        """Save the feature metadata on disk.

        This function is called after the data has been generated (by
        `_download_and_prepare`) to save the feature connector info with the
        generated dataset.

        Some dataset/features dynamically compute info during
        `_download_and_prepare`. For instance:

         * Labels are loaded from the downloaded data
         * Vocabulary is created from the downloaded data
         * ImageLabelFolder compute the image dtypes/shape from the manual_dir

        After the info have been added to the feature, this function allow to
        save those additional info to be restored the next time the data is loaded.

        By default, this function do not save anything, but sub-classes can
        overwrite the function.

        Args:
            data_dir: `str`, path to the dataset folder to which save the info (ex:
                `~/datasets/cifar10/1.2.0/`)
            feature_name: `str`, the name of the feature (from the FeaturesDict key)
        """
        pass

    def load_metadata(self, data_dir, feature_name):
        """Restore the feature metadata from disk.

        If a dataset is re-loaded and generated files exists on disk, this function
        will restore the feature metadata from the saved file.

        Args:
            data_dir: `str`, path to the dataset folder to which save the info (ex:
                `~/datasets/cifar10/1.2.0/`)
            feature_name: `str`, the name of the feature (from the FeaturesDict key)
        """
        pass


class Tensor(FeatureConnector):
    """`FeatureConnector` for generic data of arbitrary shape and type.
        We are deprecating 'shape'
    """

    def __init__(self, shape, dtype):
        """Construct a Tensor feature."""
        assert len(shape) < 2, "Tensor can only take 0 or 1 dimensional shapes ."
        self._shape = tuple(shape)
        if len(shape) == 1:
            self._dtype = pa.list_(dtype())
        else:
            self._dtype = dtype()

    def get_type(self) -> pa.DataType:
        """See base class for details."""
        return self._dtype

    def decode_batch_example(self, example_data):
        """See base class for details."""
        # Overwrite the `pa.map_fn`, decoding is a no-op
        return self.decode_example(example_data)

    def decode_ragged_example(self, example_data):
        """See base class for details."""
        # Overwrite the `pa.map_fn`, decoding is a no-op
        return self.decode_example(example_data)

    def encode_example(self, example_data):
        """See base class for details."""
        # np_dtype = np.dtype(self.dtype.to_pandas_dtype())
        # if not isinstance(example_data, np.ndarray):
        #     example_data = np.array(example_data, dtype=np_dtype)
        # # Ensure the shape and dtype match
        # if example_data.dtype != np_dtype:
        #     raise ValueError('Dtype {} do not match {}'.format(
        #             example_data.dtype, np_dtype))
        # utils.assert_shape_match(example_data.shape, self._shape)
        return example_data
