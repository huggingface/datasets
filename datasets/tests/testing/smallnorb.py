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
r"""Generate Smallnorb-like files, smaller and with random data.

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

NUM_IMAGES = 5
FACTOR_VALUES = [
    list(range(10)),
    list(range(9)),
    list(range(0, 36, 2)),
    list(range(6)),
]
TRAINING_OUTPUT_NAME = "smallnorb-5x46789x9x18x6x2x96x96-training"
TESTING_OUTPUT_NAME = "smallnorb-5x01235x9x18x6x2x96x96-testing"

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory.")
FLAGS = flags.FLAGS


def write_binary_matrix(filename, array):
  """Writes array as a binary formatted matrix to the file.

  The file format is described on the data set page:
  https://cs.nyu.edu/~ylclab/data/norb-v1.0-small/

  Args:
    filename: String with path to the file.
    array: Numpy array that should be written to the file.
  """
  with tf.io.gfile.GFile(filename, "wb") as f:

    # All data is stored in little-endian byte order.
    int32_dtype = np.dtype("int32").newbyteorder("<")

    # The first 4 bytes specify the data type.
    if array.dtype.str == "<i4":
      # Magic code for little-endian int32.
      f.write(np.asarray(507333716, dtype=int32_dtype).tobytes())
    elif array.dtype.str == "|u1":
      # Magic code for uint8.
      f.write(np.asarray(507333717, dtype=int32_dtype).tobytes())
    else:
      raise ValueError("Array data type %r not supported." % array.dtype.str)

    # Next, we specify the number of dimensions of the array to be stored as a
    # 32 bit integer.
    f.write(np.asarray(array.ndim, int32_dtype).tobytes())

    # The shape of the array is saved as 32-bit integers. If there are less than
    # 3 dimensions, the shape is padded with ones.
    shape = list(array.shape) + [1] * max(0, 3 - array.ndim)
    f.write(np.asarray(shape, int32_dtype).tobytes())

    # Finally, the data is written as a C-contiguous matrix. There is no need to
    # check for the byte order as we checked for this when writing the magic
    # code.
    f.write(np.ascontiguousarray(array).tobytes())


def _create_chunk(prefix, random_state):
  """Creates fake dat, cat, and info files with the given prefix."""
  # Create the images.
  image_shape = (NUM_IMAGES, 2, 96, 96)  # Data file contains pairs of images.
  images = random_state.randint(256, size=image_shape).astype("uint8")
  write_binary_matrix("%s-dat.mat" % prefix, images)

  # Create the class label file.
  class_labels = random_state.choice(range(5), size=(NUM_IMAGES))
  write_binary_matrix("%s-cat.mat" % prefix, class_labels.astype("int32"))

  # Create the auxiliary info file that contains additional labels.
  info = []
  for values in FACTOR_VALUES:
    info.append(random_state.choice(values, size=(NUM_IMAGES)))
  write_binary_matrix("%s-info.mat" % prefix, np.array(info).T.astype("int32"))


def _generate():
  """Generates a fake data set and writes it to the fake_examples directory."""
  output_dir = os.path.join(FLAGS.tfds_dir, "testing", "test_data",
                            "fake_examples", "smallnorb")
  test_utils.remake_dir(output_dir)
  random_state = np.random.RandomState(0)
  _create_chunk(os.path.join(output_dir, TRAINING_OUTPUT_NAME), random_state)
  _create_chunk(os.path.join(output_dir, TESTING_OUTPUT_NAME), random_state)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  _generate()


if __name__ == "__main__":
  app.run(main)
