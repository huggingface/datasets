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
r"""Generate fake data for beans dataset.

"""

# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import os
import zipfile

from absl import app
from absl import flags

import tensorflow.compat.v2 as tf
from tensorflow_datasets.core import utils
from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import fake_data_utils

flags.DEFINE_string('tfds_dir', py_utils.tfds_dir(),
                    'Path to tensorflow_datasets directory')

FLAGS = flags.FLAGS


def _output_dir():
  return os.path.join(FLAGS.tfds_dir, 'testing', 'test_data', 'fake_examples',
                      'beans')


def _get_jpeg(height, width):
  """Returns jpeg picture."""
  image = fake_data_utils.get_random_picture(height, width)
  jpeg = tf.image.encode_jpeg(image)
  with utils.nogpu_session() as sess:
    res = sess.run(jpeg)
  return res


def create_zip(fname):
  out_path = os.path.join(_output_dir(), fname)
  jpeg = _get_jpeg(height=5, width=5)
  with zipfile.ZipFile(out_path, 'w') as myzip:
    myzip.writestr('angular_leaf_spot/0.jpg', jpeg)
    myzip.writestr('bean_rust/0.jpg', jpeg)
    myzip.writestr('healthy/0.jpg', jpeg)


def main(argv):
  del argv
  create_zip('beans_train.zip')
  create_zip('beans_validation.zip')
  create_zip('beans_test.zip')


if __name__ == '__main__':
  app.run(main)
