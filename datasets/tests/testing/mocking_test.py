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
"""Tests for tensorflow_datasets.testing.mocking."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v2 as tf

from tensorflow_datasets.core import dataset_utils
from tensorflow_datasets.core import registered
from tensorflow_datasets.testing import mocking
from tensorflow_datasets.testing import test_case
from tensorflow_datasets.testing import test_utils

# Import for registration
from tensorflow_datasets.image import imagenet  # pylint: disable=unused-import,g-bad-import-order
from tensorflow_datasets.text import lm1b  # pylint: disable=unused-import,g-bad-import-order
from tensorflow_datasets.image import mnist  # pylint: disable=unused-import,g-bad-import-order

tf.enable_v2_behavior()


class MockingTest(test_case.TestCase):

  def test_mocking_imagenet(self):
    with mocking.mock_data():
      ds = registered.load('imagenet2012', split='train')
      for ex in ds.take(10):
        self.assertCountEqual(
            list(ex.keys()), ['file_name', 'image', 'label'])
        ex['image'].shape.assert_is_compatible_with((None, None, 3))

  def test_mocking_lm1b(self):
    with mocking.mock_data():
      ds = registered.load('lm1b/bytes', split='train')
      for ex in ds.take(10):
        self.assertEqual(ex['text'].dtype, tf.int64)
        ex['text'].shape.assert_is_compatible_with((None,))

  def test_custom_as_dataset(self):
    def _as_dataset(self, *args, **kwargs):  # pylint: disable=unused-argument
      return tf.data.Dataset.from_generator(
          lambda: ({  # pylint: disable=g-long-lambda
              'text': t,
          } for t in ['some sentence', 'some other sentence']),
          output_types=self.info.features.dtype,
          output_shapes=self.info.features.shape,
      )

    with mocking.mock_data(as_dataset_fn=_as_dataset):
      ds = registered.load('lm1b', split='train')
      out = [ex['text'] for ex in dataset_utils.as_numpy(ds)]
      self.assertEqual(out, [b'some sentence', b'some other sentence'])

  def test_max_values(self):
    with mocking.mock_data(num_examples=50):
      ds = registered.load('mnist', split='train')
      for ex in ds.take(50):
        self.assertLessEqual(tf.math.reduce_max(ex['label']).numpy(), 10)
      self.assertEqual(  # Test determinism
          [ex['label'].numpy() for ex in ds.take(5)],
          [1, 9, 2, 5, 3],
      )
      self.assertEqual(  # Iterating twice should yield the same samples
          [ex['label'].numpy() for ex in ds.take(5)],
          [1, 9, 2, 5, 3],
      )


if __name__ == '__main__':
  test_utils.test_main()
