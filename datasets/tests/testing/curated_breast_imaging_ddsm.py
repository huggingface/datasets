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
r"""Generate CBIS-DDSM like files, smaller and with fake data.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import os

from absl import app
from absl import flags

import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_datasets.core.utils import py_utils
import tensorflow_datasets.public_api as tfds

flags.DEFINE_string('tfds_dir', py_utils.tfds_dir(),
                    'Path to tensorflow_datasets directory')
FLAGS = flags.FLAGS

MAMMOGRAPHY_HEIGHT = 100    # Note: Much smaller than original images.
MAMMOGRAPHY_WIDTH = 80
ABNORMALITY_SIZE_MIN = 10
ABNORMALITY_SIZE_MAX = 20
NUM_ABNORMALITIES_MAX = 5
BREAST_INTENSITY_MIN = 20
BREAST_INTENSITY_MAX = 200


def remake_dirs(path):
  if not tf.io.gfile.exists(path):
    tf.io.gfile.makedirs(path)


def write_png(filepath, img):
  cv2 = tfds.core.lazy_imports.cv2
  with tf.io.gfile.GFile(filepath, 'wb') as f:
    _, buf = cv2.imencode('.png', img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
    f.write(buf.tobytes())


def _yield_mammography_with_abnormalities():
  """Generate a fake mammography image containing a set of abnormalities."""
  mammography = np.zeros((MAMMOGRAPHY_HEIGHT, MAMMOGRAPHY_WIDTH),
                         dtype=np.uint8)
  # Draw a rectangle representing the breast region.
  breast_h = np.random.randint(
      int(MAMMOGRAPHY_HEIGHT * 0.7), int(MAMMOGRAPHY_HEIGHT * 0.9) + 1)
  breast_w = np.random.randint(
      int(MAMMOGRAPHY_WIDTH * 0.7), int(MAMMOGRAPHY_WIDTH * 0.9) + 1)
  breast_y = np.random.randint(0, MAMMOGRAPHY_HEIGHT - breast_h)
  breast_x = np.random.randint(0, MAMMOGRAPHY_WIDTH - breast_w)
  breast_intensity = np.random.randint(BREAST_INTENSITY_MIN,
                                       BREAST_INTENSITY_MAX + 1)
  mammography[
      breast_y:(breast_y + breast_h),
      breast_x:(breast_x + breast_w)] = breast_intensity

  abnormalities = []  # Note: pairs of (mask, crop).
  for _ in range(np.random.randint(1, NUM_ABNORMALITIES_MAX + 1)):
    abnorm_h = np.random.randint(ABNORMALITY_SIZE_MIN, ABNORMALITY_SIZE_MAX + 1)
    abnorm_w = np.random.randint(ABNORMALITY_SIZE_MIN, ABNORMALITY_SIZE_MAX + 1)
    abnorm_y = np.random.randint(0, breast_h - abnorm_h) + breast_y
    abnorm_x = np.random.randint(0, breast_w - abnorm_w) + breast_x
    abnorm_intensity = np.random.randint(int(BREAST_INTENSITY_MIN * 1.2), 256)
    while np.absolute(abnorm_intensity - breast_intensity) < 10:
      abnorm_intensity = np.random.randint(int(BREAST_INTENSITY_MIN * 1.2), 256)
    # Draw abnormality in the mammography.
    mammography[
        abnorm_y:(abnorm_y + abnorm_h),
        abnorm_x:(abnorm_x + abnorm_w)] = abnorm_intensity
    # Abnormality mask w.r.t the full mammography.
    abnorm_mask = np.zeros_like(mammography)
    abnorm_mask[
        abnorm_y:(abnorm_y + abnorm_h), abnorm_x:(abnorm_x + abnorm_w)] = 255
    # Abnormality crop.
    abnorm_crop = np.ones((abnorm_h, abnorm_w)) * abnorm_intensity
    abnormalities.append((abnorm_mask, abnorm_crop))

  return mammography, abnormalities


def _yield_csv_rows_base(output_dir, row_extra_info_gen_fn):
  """Yield rows for the CSV ground-truth files, also creates fake images."""
  mammography, abnormalities = _yield_mammography_with_abnormalities()
  patient_id = 'P_%05d' % np.random.randint(0, 1000)
  breast_density = np.random.randint(1, 5)
  left_or_right_breast = np.random.choice(['LEFT', 'RIGHT'])
  image_view = np.random.choice(['CC', 'MLO'])
  study_id = tuple(np.random.randint(0, 999999999+1, size=2))
  study_id = '1.3.6.1.4.1.9590.100.1.2.%010d.%010d' % study_id
  series_id = tuple(np.random.randint(0, 999999999+1, size=2))
  series_id = '1.3.6.1.4.1.9590.100.1.2.%010d.%010d' % series_id
  remake_dirs(os.path.join(output_dir, '%s/%s' % (study_id, series_id)))
  # Write mammography image.
  mammography_basename = '%s/%s/000000' % (study_id, series_id)
  write_png(
      os.path.join(output_dir, mammography_basename + '.png'), mammography)

  for abnormality_id, abnormality in enumerate(abnormalities, 1):
    # Write abnormality crop image.
    crop_basename = '%s/%s/%06d' % (study_id, series_id, abnormality_id * 2 - 1)
    write_png(
        os.path.join(output_dir, crop_basename + '.png'), abnormality[1])
    # Write abnormality mask image.
    mask_basename = '%s/%s/%06d' % (study_id, series_id, abnormality_id * 2)
    write_png(
        os.path.join(output_dir, mask_basename + '.png'), abnormality[0])
    row = {
        'patient_id': patient_id,
        'breast density': breast_density,
        'left or right breast': left_or_right_breast,
        'image view': image_view,
        'abnormality id': abnormality_id,
        'abnormality type': 'calcification',
        'assessment': np.random.randint(1, 5),
        'pathology': np.random.choice(
            ['BENIGN', 'BENIGN_WITHOUT_CALLBACK', 'MALIGNANT']),
        'subtlety': np.random.randint(1, 5),
        'image file path': mammography_basename + '.dcm',
        'cropped image file path': crop_basename + '.dcm',
        'ROI mask file path': mask_basename + '.dcm',
    }
    row.update(row_extra_info_gen_fn())
    yield row


def _yield_csv_rows_calc(output_dir, calc_types, calc_distributions):
  """Generate a row for the calcification abnormalities."""
  def _row_extra_info_gen_fn():
    return {
        'calc type': np.random.choice(calc_types),
        'calc distribution': np.random.choice(calc_distributions),
    }

  return _yield_csv_rows_base(output_dir, _row_extra_info_gen_fn)


def _yield_csv_rows_mass(output_dir, mass_shapes, mass_margins):
  """Generate a row for the mass abnormalities."""
  def _row_extra_info_gen_fn():
    return {
        'mass shape': np.random.choice(mass_shapes),
        'mass margins': np.random.choice(mass_margins),
    }

  return _yield_csv_rows_base(output_dir, _row_extra_info_gen_fn)


def _generate_csv(csv_filepath, row_yielder, number_of_mammograms):
  """Generate a csv file with `number_of_examples` mammograms."""
  with tf.io.gfile.GFile(os.path.join(csv_filepath), 'w') as f:
    writer = None
    for _ in range(number_of_mammograms):
      for row in row_yielder():
        if writer is None:
          writer = csv.DictWriter(f, row.keys())
          writer.writeheader()
        writer.writerow(row)


def _generate_data_calc(output_dir, number_of_mammograms):
  """Generate train/test CSV and images of calcification abnormalities."""
  calc_types = tfds.features.ClassLabel(
      names_file=tfds.core.get_tfds_path(
          os.path.join('image', 'cbis_ddsm_calc_types.txt'))).names
  calc_distributions = tfds.features.ClassLabel(
      names_file=tfds.core.get_tfds_path(
          os.path.join('image', 'cbis_ddsm_calc_distributions.txt'))).names
  _generate_csv(
      os.path.join(output_dir, 'calc_case_description_train_set.csv'),
      lambda: _yield_csv_rows_calc(output_dir, calc_types, calc_distributions),
      number_of_mammograms[0])
  _generate_csv(
      os.path.join(output_dir, 'calc_case_description_test_set.csv'),
      lambda: _yield_csv_rows_calc(output_dir, calc_types, calc_distributions),
      number_of_mammograms[1])


def _generate_data_mass(output_dir, number_of_mammograms):
  """Generate train/test CSV and images of mass abnormalities."""
  mass_shapes = tfds.features.ClassLabel(
      names_file=tfds.core.get_tfds_path(
          os.path.join('image', 'cbis_ddsm_mass_shapes.txt'))).names
  mass_margins = tfds.features.ClassLabel(
      names_file=tfds.core.get_tfds_path(
          os.path.join('image', 'cbis_ddsm_mass_margins.txt'))).names

  _generate_csv(
      os.path.join(output_dir, 'mass_case_description_train_set.csv'),
      lambda: _yield_csv_rows_mass(output_dir, mass_shapes, mass_margins),
      number_of_mammograms[0])
  _generate_csv(
      os.path.join(output_dir, 'mass_case_description_test_set.csv'),
      lambda: _yield_csv_rows_mass(output_dir, mass_shapes, mass_margins),
      number_of_mammograms[1])


def main(_):
  output_dir = os.path.join(FLAGS.tfds_dir, 'testing', 'test_data',
                            'fake_examples', 'curated_breast_imaging_ddsm')
  np.random.seed(0x12345)
  _generate_data_calc(output_dir, (3, 2))
  _generate_data_mass(output_dir, (3, 2))


if __name__ == '__main__':
  app.run(main)
