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
r"""Generate open_images like files, smaller and with random data.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import random
import tarfile

from absl import app
from absl import flags

from tensorflow_datasets.core.features import ClassLabel
from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.object_detection import open_images
from tensorflow_datasets.testing import fake_data_utils

flags.DEFINE_string('tfds_dir', py_utils.tfds_dir(),
                    'Path to tensorflow_datasets directory')
FLAGS = flags.FLAGS


def _output_dir():
  return os.path.join(FLAGS.tfds_dir, 'testing', 'test_data', 'fake_examples',
                      'open_images_v4')


def _get_image_ids(images_number, prefix=None):
  """Returns the names (as string) of images."""
  if prefix:
    get_id = lambda: '%s%0.15X' % (prefix, random.getrandbits(56))
  else:
    get_id = lambda: '%0.16X' % random.getrandbits(64)
  return sorted([get_id().lower() for unused_i in range(images_number)])


def _write_tar(path, split_name, image_ids, prefix=None):
  """Writes tar file with images to given path.

  Args:
    path: sting, path to tar to be written.
    split_name: string. eg: 'train', 'validation', 'test'.
    image_ids: list of str, ids of the images to add to tar file.
    prefix: one of [0-9a-f], or None.
  """
  if prefix is not None:
    split_name = '%s_%s' % (split_name, prefix)
  with tarfile.open(path, mode='w') as tar:
    for i, image_id in enumerate(image_ids):
      fname = '%s/%s.jpg' % (split_name, image_id)
      # Note: Generate two large images with more than 300k pixels.
      kwargs = dict(height=600, width=600) if i < 2 else dict()
      tar.add(fake_data_utils.get_random_jpeg(**kwargs), arcname=fname)


def _write_image_level_labels(fname, image_ids, machine=False):
  """Writes CSV with 0-10 labels per image."""
  lines = ['ImageID,Source,LabelName,Condidence']
  all_class_label = ClassLabel(names_file=py_utils.get_tfds_path(
      os.path.join('object_detection', 'open_images_classes_all.txt')))
  trainable_class_label = ClassLabel(names_file=py_utils.get_tfds_path(
      os.path.join('object_detection', 'open_images_classes_trainable.txt')))
  for i, image_id in enumerate(image_ids):
    if i < 1:
      # Ensure that at least some image contains trainable classes.
      labels = random.sample(trainable_class_label.names, random.randint(0, 10))
    else:
      labels = random.sample(all_class_label.names, random.randint(0, 10))
    for label in labels:
      source = random.choice(open_images.IMAGE_LEVEL_SOURCES)
      confidence = random.choice((0, 1))
      if machine:
        confidence = '%.1f' % (random.randint(0, 10) / 10.)
      else:
        confidence = random.choice((0, 1))
      lines.append('%s,%s,%s,%s' % (image_id, source, label, confidence))
  path = os.path.join(_output_dir(), fname)
  with open(path, 'w') as csv_f:
    csv_f.write('\n'.join(lines))


def _write_bbox_labels(fname, image_ids):
  """Writes CSV with 0-10 labels per image."""
  lines = ['ImageID,Source,LabelName,Confidence,XMin,XMax,YMin,YMax,IsOccluded,'
           'IsTruncated,IsGroupOf,IsDepiction,IsInside']
  boxable_class_label = ClassLabel(names_file=py_utils.get_tfds_path(
      os.path.join('object_detection', 'open_images_classes_boxable.txt')))
  for image_id in image_ids:
    labels = random.sample(boxable_class_label.names, random.randint(0, 10))
    for label in labels:
      source = random.choice(open_images.BBOX_SOURCES)
      xmin = random.uniform(0, 1)
      xmax = random.uniform(xmin, 1)
      ymin = random.uniform(0, 1)
      ymax = random.uniform(ymin, 1)
      p1, p2, p3, p4, p5 = [random.randint(-1, 1) for unused_i in range(5)]
      lines.append('%s,%s,%s,1,%.6f,%.6f,%.6f,%.6f,%s,%s,%s,%s,%s' % (
          image_id, source, label, xmin, xmax, ymin, ymax, p1, p2, p3, p4, p5))
  path = os.path.join(_output_dir(), fname)
  with open(path, 'w') as csv_f:
    csv_f.write('\n'.join(lines))


def _generate_train_files():
  """Generate train files (archives and CSV files)."""
  all_image_ids = []
  for prefix in '0123456789abcdef':
    path = os.path.join(_output_dir(), 's3-tar_train_sha1_%s.tar' % prefix)
    image_ids = _get_image_ids(images_number=32, prefix=prefix)
    all_image_ids.extend(image_ids)
    _write_tar(path, 'train', image_ids, prefix)
  _write_image_level_labels('train-human-labels.csv', all_image_ids)
  _write_image_level_labels('train-machine-labels.csv', all_image_ids,
                            machine=True)
  _write_bbox_labels('train-annotations-bbox.csv', all_image_ids)


def _generate_test_files():
  """Generate test files (archive and CSV files)."""
  path = os.path.join(_output_dir(), 's3-tar_test_sha2.tar')
  image_ids = _get_image_ids(images_number=36)
  _write_tar(path, 'test', image_ids)
  _write_image_level_labels('test-human-labels.csv', image_ids)
  _write_image_level_labels('test-machine-labels.csv', image_ids, machine=True)
  _write_bbox_labels('test-annotations-bbox.csv', image_ids)


def _generate_validation_files():
  """Generate validation files (archive and CSV files)."""
  path = os.path.join(_output_dir(), 's3-tar_validation_sha3.tar')
  image_ids = _get_image_ids(images_number=12)
  _write_tar(path, 'test', image_ids)
  _write_image_level_labels('validation-human-labels.csv', image_ids)
  _write_image_level_labels('validation-machine-labels.csv', image_ids,
                            machine=True)
  _write_bbox_labels('validation-annotations-bbox.csv', image_ids)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')
  _generate_train_files()
  _generate_test_files()
  _generate_validation_files()


if __name__ == '__main__':
  app.run(main)
