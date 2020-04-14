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
r"""Generate Shapes3d-like files, smaller and with random data.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from absl import app
from absl import flags
import h5py
import numpy as np

from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import test_utils

NUM_IMAGES = 5
FACTOR_VALUES = [[0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                 [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                 [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                 [
                     0.75, 0.82142857, 0.89285714, 0.96428571, 1.03571429,
                     1.10714286, 1.17857143, 1.25
                 ], [0., 1., 2., 3.],
                 [
                     -30., -25.71428571, -21.42857143, -17.14285714,
                     -12.85714286, -8.57142857, -4.28571429, 0., 4.28571429,
                     8.57142857, 12.85714286, 17.14285714, 21.42857143,
                     25.71428571, 30.
                 ]]
OUTPUT_NAME = "3dshapes.h5"

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory")
FLAGS = flags.FLAGS


def _create_fake_samples():
  """Creates a fake set of samples.

  Returns:
    Tuple with fake images and fake latent values.
  """
  rs = np.random.RandomState(0)
  images = rs.randint(256, size=(NUM_IMAGES, 64, 64, 3)).astype("uint8")
  values = []
  for factor_values in FACTOR_VALUES:
    values.append(rs.choice(factor_values, size=(NUM_IMAGES)))

  return images, np.transpose(values)


def _generate():
  """Generates a fake data set and writes it to the fake_examples directory."""
  output_dir = os.path.join(FLAGS.tfds_dir, "testing", "test_data",
                            "fake_examples", "shapes3d")
  test_utils.remake_dir(output_dir)

  images, values = _create_fake_samples()

  with h5py.File(os.path.join(output_dir, OUTPUT_NAME), "w") as f:
    img_dataset = f.create_dataset("images", images.shape, "|u1")
    img_dataset.write_direct(images)
    values_dataset = f.create_dataset("labels", values.shape, "<f8")
    values_dataset.write_direct(np.ascontiguousarray(values))


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  _generate()


if __name__ == "__main__":
  app.run(main)
