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
r"""Script to generate imagenet resized like files for testing.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import zipfile

from absl import app
from absl import flags

import numpy as np
from tensorflow_datasets.core.utils import py_utils

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory")

FLAGS = flags.FLAGS


def _write_zipped(output_dir, data, tmp_name, zip_name):
  train_path = os.path.join(output_dir, tmp_name)
  with open(train_path, "w") as f:
    np.savez(f, **data)

  zip_path = os.path.join(output_dir, zip_name)
  with zipfile.ZipFile(zip_path, "w") as f:
    f.write(train_path)
  os.remove(train_path)


def _generate_data():
  """Generates training archives for both train and valiation."""
  output_dir = os.path.join(FLAGS.tfds_dir, "testing", "test_data",
                            "fake_examples", "imagenet_resized")

  train = {}
  train["data"] = np.zeros(shape=[3, 8, 8, 3], dtype=np.uint8)
  train["labels"] = np.zeros(shape=[3], dtype=np.int64)

  _write_zipped(output_dir, train, "Imagenet8_train.npz",
                "Imagenet8_train_npz.zip")

  valid = {}
  valid["data"] = np.ones(shape=[1, 8, 8, 3], dtype=np.uint8)
  valid["labels"] = np.ones(shape=[1], dtype=np.int64)

  _write_zipped(output_dir, valid, "Imagenet8_val.npz", "Imagenet8_val_npz.zip")


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  _generate_data()


if __name__ == "__main__":
  app.run(main)
