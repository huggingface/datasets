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
"""Fake Data Generator for Malaria Dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from absl import app
from absl import flags

import tensorflow.compat.v2 as tf
from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import fake_data_utils

flags.DEFINE_string('tfds_dir', py_utils.tfds_dir(),
                    'Path to tensorflow_datasets directory')

FLAGS = flags.FLAGS


def _output_dir():
  return os.path.join(FLAGS.tfds_dir, 'testing', 'test_data', 'fake_examples',
                      'malaria', 'cell_images')


def create_folder(fname):
  images_dir = os.path.join(_output_dir(), fname)
  if not tf.io.gfile.exists(images_dir):
    tf.io.gfile.makedirs(images_dir)
  for i in range(2):
    image_name = 'C189P150ThinF_IMG_20151203_141809_cell_{:03d}.png'.format(i)
    tf.io.gfile.copy(
        fake_data_utils.get_random_png(300, 300),
        os.path.join(images_dir, image_name),
        overwrite=True)


def main(argv):
  del argv
  create_folder('Parasitized')
  create_folder('Uninfected')


if __name__ == '__main__':
  app.run(main)
