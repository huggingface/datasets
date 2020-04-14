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
"""Tests for tensorflow_datasets.testing.dataset_builder_testing."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.testing import dataset_builder_testing


class DatasetBuilderTesting(tf.test.TestCase):

  def test_checksum_string(self):
    def _make_hash():
      return dataset_builder_testing.checksum(
          tf.constant([b'foo', b'bar-obj']).numpy())

    # Ensure determinism by checking the hash is the same across examples
    # Could harcode value instead but hash is different between Py2 and 3.
    self.assertLen(set(_make_hash() for _ in range(5)), 1)


if __name__ == '__main__':
  testing.test_main()
