# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
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
"""Tests for tensorflow_datasets.core.example_serializer."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_datasets import testing
from tensorflow_datasets.core import example_serializer
from tensorflow_datasets.core.features import feature as feature_lib
from tensorflow_datasets.core.utils import py_utils


class ExampleSerializerTest(testing.SubTestCase):

  def assertRaggedFieldEqual(self, dict1, dict2):
    self.assertIsInstance(dict1, dict)
    self.assertIsInstance(dict2, dict)
    self.assertEqual(set(dict1.keys()), set(dict2.keys()))
    for k, (field1, field2) in py_utils.zip_dict(dict1, dict2):
      with self._subTest(k):
        # Compare the example_data
        self.assertAllEqual(field1[0], field2[0])
        # Compare the tensor_info
        self.assertEqual(field1[1], field2[1])

  def test_ragged_dict_to_tf_example(self):
    example_data = {
        'input': [[1, 2, 3], [], [4, 5]],
    }
    tensor_info = {
        'input': feature_lib.TensorInfo(
            shape=(None, None,),
            dtype=tf.int64,
            sequence_rank=2,
        ),
    }
    ex_proto = example_serializer._dict_to_tf_example(example_data, tensor_info)
    feature = ex_proto.features.feature
    self.assertEqual(
        [1, 2, 3, 4, 5],
        list(feature['input/ragged_flat_values'].int64_list.value),
    )
    self.assertEqual(
        [3, 0, 2],
        list(feature['input/ragged_row_lengths_0'].int64_list.value),
    )

  def test_ragged_dict_to_tf_example_empty(self):
    example_data = {
        'input': [],
    }
    tensor_info = {
        'input': feature_lib.TensorInfo(
            shape=(None, None,),
            dtype=tf.int64,
            sequence_rank=2,
        ),
    }
    ex_proto = example_serializer._dict_to_tf_example(example_data, tensor_info)
    feature = ex_proto.features.feature
    self.assertEqual(
        [], list(feature['input/ragged_flat_values'].int64_list.value),
    )
    self.assertEqual(
        [], list(feature['input/ragged_row_lengths_0'].int64_list.value),
    )

  def test_add_ragged_fields(self):
    # Nested `Sequence(Sequence(tf.int64))`
    example_data = [
        [1, 2, 3],
        [],
        [4, 5],
    ]
    tensor_info = feature_lib.TensorInfo(
        shape=(None, None,), dtype=tf.int64, sequence_rank=2)
    out = example_serializer._add_ragged_fields(example_data, tensor_info)
    self.assertRaggedFieldEqual(out, {
        'ragged_flat_values': (
            np.array([1, 2, 3, 4, 5]),
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
        'ragged_row_lengths_0': (
            [3, 0, 2],
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
    })

  def test_add_ragged_fields_np(self):
    # List of np.array.
    example_data = [
        np.array([1, 2, 3], dtype=np.int64),
        np.array([], dtype=np.int64),
        np.array([4, 5], dtype=np.int64),
    ]
    tensor_info = feature_lib.TensorInfo(
        shape=(None, None,), dtype=tf.int64, sequence_rank=2)
    out = example_serializer._add_ragged_fields(example_data, tensor_info)
    self.assertRaggedFieldEqual(out, {
        'ragged_flat_values': (
            np.array([1, 2, 3, 4, 5]),
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
        'ragged_row_lengths_0': (
            [3, 0, 2],
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
    })

  def test_add_ragged_fields_empty_np(self):
    # List of np.array.
    example_data = [
        np.array([], dtype=np.int64),
        np.array([], dtype=np.int64),
    ]
    tensor_info = feature_lib.TensorInfo(
        shape=(None, None,), dtype=tf.int64, sequence_rank=2)
    out = example_serializer._add_ragged_fields(example_data, tensor_info)
    self.assertRaggedFieldEqual(out, {
        'ragged_flat_values': (
            np.zeros(shape=(0,), dtype=np.int64),
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
        'ragged_row_lengths_0': (
            [0, 0],
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
    })

  def test_add_ragged_fields_empty(self):
    # List of empty values
    example_data = [
        [],
        [],
        []
    ]
    tensor_info = feature_lib.TensorInfo(
        shape=(None, None,), dtype=tf.int64, sequence_rank=2)
    out = example_serializer._add_ragged_fields(example_data, tensor_info)
    self.assertRaggedFieldEqual(out, {
        'ragged_flat_values': (
            np.zeros(shape=(0,), dtype=np.int64),
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
        'ragged_row_lengths_0': (
            [0, 0, 0],
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
    })

  def test_add_ragged_fields_all_empty(self):
    # Empty list
    example_data = []
    tensor_info = feature_lib.TensorInfo(
        shape=(None, None,), dtype=tf.int64, sequence_rank=2)
    out = example_serializer._add_ragged_fields(example_data, tensor_info)
    self.assertRaggedFieldEqual(out, {
        'ragged_flat_values': (
            np.zeros(shape=(0,), dtype=np.int64),
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
        'ragged_row_lengths_0': (
            np.zeros(shape=(0,), dtype=np.int64),
            feature_lib.TensorInfo(shape=(None,), dtype=tf.int64),
        ),
    })

  def test_add_ragged_fields_single_level_sequence(self):
    # Single level sequence
    example_data = [
        [1, 2],
        [2, 3],
        [4, 5],
    ]
    tensor_info = feature_lib.TensorInfo(
        shape=(None, 2,), dtype=tf.int64, sequence_rank=1)
    out = example_serializer._add_ragged_fields(example_data, tensor_info)
    self.assertAllEqual(out[0], [
        [1, 2],
        [2, 3],
        [4, 5],
    ])
    self.assertEqual(out[1], tensor_info)


if __name__ == '__main__':
  testing.test_main()
