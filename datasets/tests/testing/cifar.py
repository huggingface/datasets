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
r"""Generate cifar10/cifar100 like files, smaller and with random data.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from absl import app
from absl import flags
import numpy as np

import tensorflow_datasets as tfds
from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import test_utils

NUMBER_IMAGES_PER_BATCH = 2
HEIGHT, WIDTH = (32, 32)
NUMBER_BATCHES = 5
NUMBER_LABELS = 10
NUMBER_FINE_LABELS = 100
NUMBER_COARSE_LABELS = 20

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory")
FLAGS = flags.FLAGS


def cifar10_output_dir():
  return os.path.join(FLAGS.tfds_dir, "testing", "test_data", "fake_examples",
                      "cifar10", "cifar-10-batches-bin")


def cifar100_output_dir():
  return os.path.join(FLAGS.tfds_dir, "testing", "test_data", "fake_examples",
                      "cifar100", "cifar-100-binary")


def dump(output_dir, fname, images, labels):
  path = os.path.join(output_dir, fname)
  print("Writing %s..." % path)
  with open(path, "wb") as out_file:
    for image, labels in zip(images, labels):
      out_file.write(labels.tobytes())
      out_file.write(image.tobytes())


def generate_cifar100_batch(fname, num_examples):
  images = np.random.randint(
      256, size=(num_examples, HEIGHT * WIDTH * 3), dtype=np.uint8)
  fine_labels = np.random.randint(
      NUMBER_FINE_LABELS, size=(num_examples), dtype=np.uint8)
  coarse_labels = np.random.randint(
      NUMBER_COARSE_LABELS, size=(num_examples), dtype=np.uint8)
  labels = np.vstack((coarse_labels, fine_labels)).T
  dump(cifar100_output_dir(), fname, images, labels)


def generate_cifar10_batch(batch_name):
  images = np.random.randint(
      256, size=(NUMBER_IMAGES_PER_BATCH, HEIGHT * WIDTH * 3), dtype=np.uint8)
  labels = np.random.randint(
      NUMBER_LABELS, size=(NUMBER_IMAGES_PER_BATCH), dtype=np.uint8)
  dump(cifar10_output_dir(), batch_name, images, labels)


def _generate_cifar100_data():
  """Generates .bin and label .txt files for cifar100."""
  output_dir = cifar100_output_dir()
  test_utils.remake_dir(output_dir)
  generate_cifar100_batch("train.bin", 10)
  generate_cifar100_batch("test.bin", 2)
  fine_names = tfds.builder("cifar100").info.features["label"].names
  coarse_names = tfds.builder("cifar100").info.features["coarse_label"].names
  with open(os.path.join(output_dir, "fine_label_names.txt"), "w") as f:
    f.write("\n".join(fine_names))
  with open(os.path.join(output_dir, "coarse_label_names.txt"), "w") as f:
    f.write("\n".join(coarse_names))


def _generate_cifar10_data():
  output_dir = cifar10_output_dir()
  test_utils.remake_dir(output_dir)
  for batch_number in range(1, NUMBER_BATCHES + 1):
    generate_cifar10_batch("data_batch_%s.bin" % batch_number)
  generate_cifar10_batch("test_batch.bin")
  label_names = tfds.builder("cifar10").info.features["label"].names
  print(label_names)
  with open(os.path.join(output_dir, "batches.meta.txt"), "w") as f:
    f.write("\n".join(label_names))


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  _generate_cifar10_data()
  _generate_cifar100_data()


if __name__ == "__main__":
  app.run(main)
