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
r"""Generate ilsvrc2012 like files, smaller and with random data.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tempfile

from absl import app
from absl import flags

import tensorflow.compat.v2 as tf

from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import fake_data_utils

flags.DEFINE_string('tfds_dir', py_utils.tfds_dir(),
                    'Path to tensorflow_datasets directory')
FLAGS = flags.FLAGS

_TRAIN_IMAGES_NUMBER = 5
_TEST_IMAGES_NUMBER = 5


def _output_dir():
  return os.path.join(FLAGS.tfds_dir, 'testing', 'test_data', 'fake_examples',
                      'oxford_iiit_pet')


def _generate_data():
  """Generate images archive."""

  # Generate images
  images_dir = os.path.join(_output_dir(), 'images')
  if not tf.io.gfile.exists(images_dir):
    tf.io.gfile.makedirs(images_dir)
  for i in range(_TRAIN_IMAGES_NUMBER + _TEST_IMAGES_NUMBER):
    image_name = 'image{:03d}.jpg'.format(i)
    tf.io.gfile.copy(fake_data_utils.get_random_jpeg(),
                     os.path.join(images_dir, image_name),
                     overwrite=True)

  # Generate annotations
  annotations_dir = os.path.join(_output_dir(), 'annotations')

  if not tf.io.gfile.exists(annotations_dir):
    tf.io.gfile.makedirs(annotations_dir)

  # Generate trimaps
  trimaps_dir = os.path.join(annotations_dir, 'trimaps')

  if not tf.io.gfile.exists(trimaps_dir):
    tf.io.gfile.makedirs(trimaps_dir)

  global_count = 0
  for filename, num_examples in [('trainval.txt', _TRAIN_IMAGES_NUMBER),
                                 ('test.txt', _TEST_IMAGES_NUMBER)]:
    fobj = tempfile.NamedTemporaryFile(delete=False, mode='w')
    with fobj:
      for i in range(num_examples):
        fobj.write('image{:03d} {} 0 0\n'.format(global_count, i % 37))
        global_count += 1
    tf.io.gfile.copy(fobj.name, os.path.join(annotations_dir, filename),
                     overwrite=True)

  # Create trimaps
  for i in range(_TRAIN_IMAGES_NUMBER + _TEST_IMAGES_NUMBER):
    trimap_name = 'image{:03d}.png'.format(i)
    tf.io.gfile.copy(fake_data_utils.get_random_png(channels=1),
                     os.path.join(trimaps_dir, trimap_name),
                     overwrite=True)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')
  _generate_data()


if __name__ == '__main__':
  app.run(main)
