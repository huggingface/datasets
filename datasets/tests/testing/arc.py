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
r"""Generate ARC-like files, smaller and with random data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os

from absl import app
from absl import flags
import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import test_utils

flags.DEFINE_string(
    name="tfds_dir",
    default=py_utils.tfds_dir(),
    help="Path to tensorflow_datasets directory")
FLAGS = flags.FLAGS

_COMMIT = "0123456789abcdef0123456789abcdef01234567"  # fake commit
_EXTRACT_SUBDIR = "fchollet-ARC-{}".format(_COMMIT[:7])
NUM_TASKS = {"training": 10, "evaluation": 5}


def examples_dir():
  return os.path.join(FLAGS.tfds_dir, "testing", "test_data", "fake_examples",
                      "arc", _EXTRACT_SUBDIR, "data")


def arc_dir(name):
  return os.path.join(examples_dir(), name)


def make_grid_data():
  size = np.random.randint(30, size=2) + 1
  grid = np.random.randint(10, size=size[0] * size[1]).reshape(size)
  return grid.tolist()


def make_pair():
  return {
      "input": make_grid_data(),
      "output": make_grid_data(),
  }


def make_task():
  num_train_pairs = np.random.randint(3) + 2  # 2 to 4
  num_test_pairs = np.random.randint(2) + 1  # 1 or 2
  return {
      "train": [make_pair() for _ in range(num_train_pairs)],
      "test": [make_pair() for _ in range(num_test_pairs)],
  }


def write_task(output_dir, task_id, task):
  path = os.path.join(output_dir, "{}.json".format(task_id))
  with tf.io.gfile.GFile(path, "w") as f:
    json.dump(task, f)


def main(_):
  task_index = np.random.randint(2**31)
  for subset in ["training", "evaluation"]:
    output_dir = arc_dir(subset)
    test_utils.remake_dir(output_dir)
    num_tasks = NUM_TASKS[subset]
    for _ in range(num_tasks):
      task_index += 1
      task_id = "{:08x}".format(task_index)
      task = make_task()
      write_task(output_dir, task_id, task)


if __name__ == "__main__":
  app.run(main)
