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
"""

import abc

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
        return self.shape == other.shape and self.dtype == other.dtype and self.default_value == other.default_value

    def __repr__(self):
        return "{}(shape={}, dtype={})".format(type(self).__name__, self.shape, repr(self.dtype),)


class FeatureConnector(metaclass=abc.ABCMeta):

    @property
    def dtype(self):
        return self.get_type()
        # return utils.map_nested(lambda t: t.dtype, self.get_type())

    # @abc.abstractmethod
    def get_type(self):
        raise NotImplementedError

    @abc.abstractmethod
    def encode_example(self, example_data):

        raise NotImplementedError

    def decode_example(self, tfexample_data):
        return tfexample_data

    def _flatten(self, x):
        return [x]

    def _nest(self, list_x):
        assert len(list_x) == 1
        return list_x[0]

    def _additional_repr_info(self):
        """Override to return additional info to go into __repr__."""
        return {}

    def __repr__(self):
        """Display the feature dictionary."""
        tensor_info = self.get_type()
        return str(tensor_info)

    def save_metadata(self, data_dir, feature_name):
        pass

    def load_metadata(self, data_dir, feature_name):
        pass


class Tensor(FeatureConnector):
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
        return example_data
