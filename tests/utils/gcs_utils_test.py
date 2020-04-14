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
"""GCS utils test."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow_datasets as tfds
from tensorflow_datasets import testing
from tensorflow_datasets.core.utils import gcs_utils


class GcsUtilsTest(testing.TestCase):

  def is_dataset_accessible(self):
    # Re-enable GCS access. TestCase disables it.
    with self.gcs_access():
      self.assertTrue(gcs_utils.is_dataset_on_gcs("mnist/1.0.0"))

  def test_mnist(self):
    with self.gcs_access():
      mnist = tfds.image.MNIST(data_dir="gs://tfds-data/datasets")
      example = next(tfds.as_numpy(mnist.as_dataset(split="train").take(1)))
    _ = example["image"], example["label"]


if __name__ == "__main__":
  testing.test_main()
