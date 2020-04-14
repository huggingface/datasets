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
r"""Generate dsprites like files, smaller and with random data.

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
FACTOR_COUNTS = [1, 3, 6, 40, 32, 32]
FACTOR_VALUES = [
    [1.], [1., 2., 3.], [0.5, 0.6, 0.7, 0.8, 0.9, 1.],
    [
        0., 0.16110732, 0.32221463, 0.48332195, 0.64442926, 0.80553658,
        0.96664389, 1.12775121, 1.28885852, 1.44996584, 1.61107316, 1.77218047,
        1.93328779, 2.0943951, 2.25550242, 2.41660973, 2.57771705, 2.73882436,
        2.89993168, 3.061039, 3.22214631, 3.38325363, 3.54436094, 3.70546826,
        3.86657557, 4.02768289, 4.1887902, 4.34989752, 4.51100484, 4.67211215,
        4.83321947, 4.99432678, 5.1554341, 5.31654141, 5.47764873, 5.63875604,
        5.79986336, 5.96097068, 6.12207799, 6.28318531
    ],
    [
        0., 0.03225806, 0.06451613, 0.09677419, 0.12903226, 0.16129032,
        0.19354839, 0.22580645, 0.25806452, 0.29032258, 0.32258065, 0.35483871,
        0.38709677, 0.41935484, 0.4516129, 0.48387097, 0.51612903, 0.5483871,
        0.58064516, 0.61290323, 0.64516129, 0.67741935, 0.70967742, 0.74193548,
        0.77419355, 0.80645161, 0.83870968, 0.87096774, 0.90322581, 0.93548387,
        0.96774194, 1.
    ],
    [
        0., 0.03225806, 0.06451613, 0.09677419, 0.12903226, 0.16129032,
        0.19354839, 0.22580645, 0.25806452, 0.29032258, 0.32258065, 0.35483871,
        0.38709677, 0.41935484, 0.4516129, 0.48387097, 0.51612903, 0.5483871,
        0.58064516, 0.61290323, 0.64516129, 0.67741935, 0.70967742, 0.74193548,
        0.77419355, 0.80645161, 0.83870968, 0.87096774, 0.90322581, 0.93548387,
        0.96774194, 1.
    ]
]
OUTPUT_NAME = "dsprites_ndarray_co1sh3sc6or40x32y32_64x64.hdf5"

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory")
FLAGS = flags.FLAGS


def _create_fake_samples():
  """Creates a fake set of samples.

  Returns:
    Tuple with fake images, class labels and latent values.
  """
  rs = np.random.RandomState(0)
  images = rs.randint(256, size=(NUM_IMAGES, 64, 64)).astype("uint8")

  classes = []
  values = []
  for num_factors, factor_values in zip(FACTOR_COUNTS, FACTOR_VALUES):
    classes.append(rs.randint(num_factors, size=(NUM_IMAGES), dtype=np.int64))
    values.append(rs.choice(factor_values, size=(NUM_IMAGES)))

  return images, classes.T, values.T


def _generate():
  """Generates a fake data set and writes it to the fake_examples directory."""
  output_dir = os.path.join(FLAGS.tfds_dir, "testing", "test_data",
                            "fake_examples", "dsprites")
  test_utils.remake_dir(output_dir)

  images, classes, values = _create_fake_samples()

  with h5py.File(os.path.join(output_dir, OUTPUT_NAME), "w") as f:
    img_dataset = f.create_dataset("imgs", images.shape, "|u1")
    img_dataset.write_direct(images)

    classes_dataset = f.create_dataset("latents/classes", classes.shape, "<i8")
    classes_dataset.write_direct(np.ascontiguousarray(classes))

    values_dataset = f.create_dataset("latents/values", values.shape, "<f8")
    values_dataset.write_direct(np.ascontiguousarray(values))


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  _generate()


if __name__ == "__main__":
  app.run(main)
