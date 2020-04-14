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
r"""Script to generate Caltech101 like files with random data for testing.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from absl import app
from absl import flags

import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_datasets.core import utils
from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.image import caltech
import tensorflow_datasets.public_api as tfds
from tensorflow_datasets.testing import fake_data_utils

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory")

FLAGS = flags.FLAGS

NUM_CLASSES = 3
IMAGES_PER_CLASS = 2
MIN_EDGE_LENGTH = 150
MAX_EDGE_LENGTH = 350


def _output_dir():
  """Returns output directory."""
  return os.path.join(FLAGS.tfds_dir, "testing", "test_data", "fake_examples",
                      "caltech101", "{}_ObjectCategories".format(NUM_CLASSES))


def _save_image(jpeg, label, image_idx):
  """Saves jpeg."""
  dirname = os.path.join(_output_dir(), label)
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  path = os.path.join(dirname, "image_{:04d}.jpg".format(image_idx))
  with open(path, "wb") as out_file:
    out_file.write(jpeg)


def _get_jpeg(height, width):
  """Returns jpeg picture."""
  image = fake_data_utils.get_random_picture(height, width)
  jpeg = tf.image.encode_jpeg(image)
  with utils.nogpu_session() as sess:
    res = sess.run(jpeg)
  return res


def _generate_images():
  """Generates training images."""
  names_file = tfds.core.get_tfds_path(caltech._LABELS_FNAME)  # pylint: disable=protected-access
  label_names = tfds.features.ClassLabel(
      names_file=names_file).names[:NUM_CLASSES]
  for label in label_names:
    for i in range(IMAGES_PER_CLASS):
      height = np.random.randint(low=MIN_EDGE_LENGTH, high=MAX_EDGE_LENGTH)
      width = np.random.randint(low=MIN_EDGE_LENGTH, high=MAX_EDGE_LENGTH)
      jpeg = _get_jpeg(height=height, width=width)
      _save_image(jpeg, label, i + 1)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  _generate_images()


if __name__ == "__main__":
  app.run(main)
