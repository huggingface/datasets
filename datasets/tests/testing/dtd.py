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
r"""Generate DTD like files, smaller and with random data.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import random

from absl import app
from absl import flags

import tensorflow.compat.v2 as tf
from tensorflow_datasets.core.utils import py_utils
import tensorflow_datasets.public_api as tfds
from tensorflow_datasets.testing import fake_data_utils

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory")
FLAGS = flags.FLAGS


def _output_dir():
  return os.path.join(FLAGS.tfds_dir, "testing", "test_data", "fake_examples",
                      "dtd")


def _makedir_if_not_exists(dirname):
  if not tf.io.gfile.exists(dirname):
    tf.io.gfile.makedirs(dirname)


def _generate_data(split_name, num_examples):
  """Generate test data."""
  names_file = tfds.core.get_tfds_path(
      os.path.join("image", "dtd_key_attributes.txt"))
  label_names = tfds.features.ClassLabel(names_file=names_file).names

  # Generate images.
  generated_filenames = []
  for n in range(num_examples):
    label = random.choice(label_names)
    fname = "%s/%s_%04d.jpg" % (label, label, n)
    tmp_file_path = fake_data_utils.get_random_jpeg()
    dst_file_path = os.path.join(_output_dir(), "dtd", "images", fname)
    generated_filenames.append(fname)

    _makedir_if_not_exists(os.path.dirname(dst_file_path))
    tf.io.gfile.copy(tmp_file_path, dst_file_path, overwrite=True)

  split_path = os.path.join(_output_dir(), "dtd", "labels", split_name + ".txt")
  _makedir_if_not_exists(os.path.dirname(split_path))
  with tf.io.gfile.GFile(split_path, "w") as split_file:
    for fname in generated_filenames:
      split_file.write("%s\n" % fname)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  _generate_data("test1", 3)
  _generate_data("train1", 2)
  _generate_data("val1", 1)


if __name__ == "__main__":
  app.run(main)
