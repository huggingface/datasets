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
"""Tests for tensorflow_datasets.core.features.top_level_feature."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core import features as features_lib
from tensorflow_datasets.core.features import top_level_feature


class FeaturesManagerTest(testing.TestCase):

  def test_sequence_rank(self):

    self.assertEqual(1, top_level_feature._get_sequence_rank({
        'a': features_lib.TensorInfo(
            shape=(None, 3), dtype=tf.int32, sequence_rank=1),
        'b': features_lib.TensorInfo(
            shape=(None,), dtype=tf.int32, sequence_rank=1),
    }))

    with self.assertRaisesWithPredicateMatch(
        NotImplementedError, 'mixing sequence and context'):
      top_level_feature._get_sequence_rank({
          'a': features_lib.TensorInfo(
              shape=(), dtype=tf.int32),
          'b': features_lib.TensorInfo(
              shape=(None,), dtype=tf.int32, sequence_rank=1),
      })

  def test_flatten_nested(self):

    f = features_lib.FeaturesDict({
        'a': tf.int32,
        'b': {
            'c': {
                'd': tf.int32,
                'e': tf.int32,
            },
        },
        'f': features_lib.Sequence({
            'g': features_lib.Sequence(tf.int32),
            'h': tf.int32,
        }),
    })

    flat1 = f._flatten({
        'a': 'a',
        'b': {
            'c': {
                'd': {'d': 123},
            },
        },
        'f': {
            'g': 'g',
        },
    })
    self.assertEqual(flat1, [
        'a',
        {'d': 123},
        None,  # 'e'
        'g',
        None,  # h
    ])
    self.assertEqual(f._nest(flat1), {
        'a': 'a',
        'b': {
            'c': {
                'd': {'d': 123},
                'e': None,
            },
        },
        'f': {
            'g': 'g',
            'h': None,
        },
    })

    f = features_lib.FeaturesDict({
        'a': tf.int32,
        'b': {
            'c': tf.int32,
        },
    })
    with self.assertRaisesWithPredicateMatch(ValueError, 'received a non dict'):
      f._flatten({'b': 123})

    with self.assertRaisesWithPredicateMatch(
        ValueError, 'Unrecognized keys: [\'d\']'):
      f._flatten({'b': {'c': 123, 'd': 123}})

    with self.assertRaisesWithPredicateMatch(
        ValueError, 'Expected length 2 does not match input length 3'):
      f._nest([None, None, None])

  def test_top_level(self):

    f = features_lib.FeaturesDict({
        'a': tf.int32,
        'b': {
            'c': tf.int32,
        },
    })
    f._set_top_level()

    # Only top level can be decoded
    f.decode_example({
        'a': 1,
        'b': {
            'c': 2,
        },
    })

    with self.assertRaisesWithPredicateMatch(
        AssertionError, 'decoded when defined as top-level'):
      f['b'].decode_example({'c': 1})


if __name__ == '__main__':
  testing.test_main()
