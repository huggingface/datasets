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
import tarfile
import tempfile

from absl import app
from absl import flags

from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.image import imagenet
import tensorflow_datasets.public_api as tfds
from tensorflow_datasets.testing import fake_data_utils

flags.DEFINE_string('tfds_dir', py_utils.tfds_dir(),
                    'Path to tensorflow_datasets directory')
FLAGS = flags.FLAGS

TRAIN_SYNSET_NUMBER = 10
TRAIN_IMAGES_PER_SYNSET = 10
VAL_IMAGES_NUMBER = 10


def _get_synset(synset_name):
  """Returns path to synset archive."""
  fobj = tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.tar')
  tar = tarfile.open(mode='w', fileobj=fobj)
  for i in range(1, TRAIN_IMAGES_PER_SYNSET+1):
    fname = '%s_%s.JPEG' % (synset_name, i)
    # There are a few PNG and CMYK images:
    if synset_name == 'n01440764' and i == 1:
      path = fake_data_utils.get_random_png()
    elif synset_name == 'n01440764' and i in [2, 3]:
      path = os.path.join(
          FLAGS.tfds_dir, 'testing', 'test_data', '6pixels_cmyk.jpeg')
    else:
      path = fake_data_utils.get_random_jpeg()
    tar.add(path, arcname=fname)
  fobj.close()
  return fobj.name


def _ilsvrc2012_output_dir():
  return os.path.join(FLAGS.tfds_dir, 'testing', 'test_data', 'fake_examples',
                      'imagenet2012')


def _generate_train_archive():
  """Generate train archive."""
  output_path = os.path.join(_ilsvrc2012_output_dir(),
                             'ILSVRC2012_img_train.tar')
  tar = tarfile.open(output_path, mode='w')
  names_file = tfds.core.get_tfds_path(imagenet._LABELS_FNAME)  # pylint: disable=protected-access
  label_names = tfds.features.ClassLabel(names_file=names_file).names
  for i in range(TRAIN_SYNSET_NUMBER):
    synset_name = label_names[i]
    synset = _get_synset(synset_name)
    tar.add(synset, arcname='%s.tar' % synset_name)
  tar.close()


def _generate_val_archive():
  """Generate val archive."""
  output_path = os.path.join(_ilsvrc2012_output_dir(),
                             'ILSVRC2012_img_val.tar')
  tar = tarfile.open(output_path, mode='w')
  for i in range(1, VAL_IMAGES_NUMBER+1):
    fname = 'ILSVRC2012_val_0000%03i.JPEG' % i
    jpeg = fake_data_utils.get_random_jpeg()
    tar.add(jpeg, arcname=fname)
  tar.close()


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')
  _generate_train_archive()
  _generate_val_archive()


if __name__ == '__main__':
  app.run(main)
