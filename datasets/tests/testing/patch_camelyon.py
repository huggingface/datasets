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
r"""Create fake data for Camelyon Patch dataset.

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


flags.DEFINE_string('tfds_dir', py_utils.tfds_dir(),
                    'Path to tensorflow_datasets directory')
FLAGS = flags.FLAGS


def get_output_file_prefix(split):
  return os.path.join(FLAGS.tfds_dir, 'testing', 'test_data', 'fake_examples',
                      'patch_camelyon',
                      'camelyonpatch_level_2_split_%s' % split)


def write_to_h5_file(filepath, dataset_name, content):
  with h5py.File(filepath, 'w') as h5_f:
    h5_f.create_dataset(dataset_name, data=content)


def main(_):
  np.random.seed(0x12345)
  for split, num_examples in [('train', 5), ('test', 4), ('valid', 3)]:
    x = np.random.randint(
        low=0, high=256, size=(num_examples, 96, 96, 3), dtype=np.uint8)
    y = np.random.randint(
        low=0, high=2, size=(num_examples, 1, 1, 1), dtype=np.uint32)
    images_filepath = get_output_file_prefix(split) + '_x.h5'
    labels_filepath = get_output_file_prefix(split) + '_y.h5'
    write_to_h5_file(images_filepath, dataset_name='x', content=x)
    write_to_h5_file(labels_filepath, dataset_name='y', content=y)


if __name__ == '__main__':
  app.run(main)
