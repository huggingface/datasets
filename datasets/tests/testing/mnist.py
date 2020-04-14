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
r"""Generate MNIST-like files, smaller and with random data.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from absl import app
from absl import flags
import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import test_utils

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory")
FLAGS = flags.FLAGS


def examples_dir():
  return os.path.join(FLAGS.tfds_dir, "testing", "test_data", "fake_examples")


def mnist_dir(name):
  return os.path.join(examples_dir(), name)


_TRAIN_DATA_FILENAME = "train-image"
_TRAIN_LABELS_FILENAME = "train-label"
_TEST_DATA_FILENAME = "test-image"
_TEST_LABELS_FILENAME = "test-label"


def make_images(num_images):
  return np.random.randint(256, size=(28 * 28 * num_images), dtype=np.uint8)


def make_labels(num_labels):
  return np.random.randint(10, size=(num_labels), dtype=np.uint8)


def write_image_file(filename, num_images):
  with tf.io.gfile.GFile(filename, "wb") as f:
    f.write(b"1" * 16)  # header
    f.write(make_images(num_images).tobytes())


def write_label_file(filename, num_labels):
  with tf.io.gfile.GFile(filename, "wb") as f:
    f.write(b"1" * 8)  # header
    f.write(make_labels(num_labels).tobytes())


def main(_):
  for mnist in ["mnist", "fashion_mnist", "kmnist", "emnist"]:
    output_dir = mnist_dir(mnist)
    test_utils.remake_dir(output_dir)
    write_image_file(os.path.join(output_dir, _TRAIN_DATA_FILENAME), 10)
    write_label_file(os.path.join(output_dir, _TRAIN_LABELS_FILENAME), 10)
    write_image_file(os.path.join(output_dir, _TEST_DATA_FILENAME), 2)
    write_label_file(os.path.join(output_dir, _TEST_LABELS_FILENAME), 2)


if __name__ == "__main__":
  app.run(main)
