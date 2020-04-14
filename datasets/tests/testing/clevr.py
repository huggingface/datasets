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

import json
import os

from absl import app
from absl import flags

import tensorflow.compat.v2 as tf

from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import fake_data_utils


flags.DEFINE_string('tfds_dir', py_utils.tfds_dir(),
                    'Path to tensorflow_datasets directory')
FLAGS = flags.FLAGS

_IMAGE_NUMBERS = {'train': 5, 'val': 5, 'test': 5}
_NUM_OBJECTS = 7


def _output_dir():
  return os.path.join(FLAGS.tfds_dir, 'testing', 'test_data',
                      'fake_examples', 'clevr', 'CLEVR_v1.0')


def _generate_data(split):
  """Generate images archive."""

  # Generate images
  images_dir = os.path.join(_output_dir(), 'images', split)
  if not tf.io.gfile.exists(images_dir):
    tf.io.gfile.makedirs(images_dir)
  for i in range(_IMAGE_NUMBERS[split]):
    image_name = 'CLEVR_{}_{:06d}.png'.format(split, i)
    tf.io.gfile.copy(fake_data_utils.get_random_png(),
                     os.path.join(images_dir, image_name),
                     overwrite=True)

  if split in ['train', 'val']:
    # Generate annotations
    scenes_dir = os.path.join(_output_dir(), 'scenes')
    if not tf.io.gfile.exists(scenes_dir):
      tf.io.gfile.makedirs(scenes_dir)

    annotations = {'scenes': [{'objects':
                                   [{'color': 'red',
                                     'shape': 'sphere',
                                     'size': 'small',
                                     'material': 'rubber',
                                     '3d_coords': [0.0, 0.0, 0.0],
                                     'pixel_coords': [0.0, 0.0, 0.0],
                                     'rotation': 0.0}] * _NUM_OBJECTS
                              }] * _IMAGE_NUMBERS[split]
                  }

    annotations_file = os.path.join(scenes_dir,
                                    'CLEVR_{}_scenes.json'.format(split))
    with tf.io.gfile.GFile(annotations_file, 'w') as f:
      json.dump(annotations, f)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')
  for split in ['train', 'val', 'test']:
    _generate_data(split)


if __name__ == '__main__':
  app.run(main)
