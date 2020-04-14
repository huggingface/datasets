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
"""Tests for tensorflow_datasets.core.utils.image_utils."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import numpy as np
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core.utils import image_utils

# pylint: disable=bad-whitespace
SIX_PIXELS = [
    [[  0, 255,   0],
     [255,   0,   0],
     [255,   0, 255]],
    [[  0,   0, 255],
     [255, 255,   0],
     [126, 127, 128]]]

SIX_PIXELS_JPEG = [
    [[158, 161,  92],
     [ 76,  79,  10],
     [180,  57, 181]],
    [[ 33,  36,   0],
     [229, 232, 163],
     [201,  78, 202]]]
# pylint: enable=bad-whitespace


class ImageUtilsTest(testing.TestCase):

  def _get_image(self, name):
    path = os.path.join(self.test_data, name)
    with tf.io.gfile.GFile(path, 'rb') as img_f:
      return img_f.read()

  def test_decode_image(self):
    image = self._get_image('6pixels.png')
    np_image = image_utils.decode_image(image)
    np.testing.assert_array_equal(np_image, SIX_PIXELS)

  def test_png_to_jpeg(self):
    image = self._get_image('6pixels.png')
    jpeg = image_utils.png_to_jpeg(image)
    image_np_jpeg = image_utils.decode_image(jpeg)
    np.testing.assert_array_equal(image_np_jpeg, SIX_PIXELS_JPEG)

  def test_png_4chan_to_jpeg(self):
    image = self._get_image('6pixels_4chan.png')
    jpeg = image_utils.png_to_jpeg(image)
    image_np_jpeg = image_utils.decode_image(jpeg)
    np.testing.assert_array_equal(image_np_jpeg, SIX_PIXELS_JPEG)

  def test_jpeg_cmyk_to_rgb(self):
    image = self._get_image('6pixels_cmyk.jpeg')
    new_image = image_utils.jpeg_cmyk_to_rgb(image, quality=100)
    self.assertNotEqual(image, new_image)
    # Converting between color systems is not bijective, so high rtol.
    original_np_image = image_utils.decode_image(image)
    new_np_image = image_utils.decode_image(new_image)
    np.testing.assert_allclose(original_np_image, new_np_image, rtol=10)


if __name__ == '__main__':
  testing.test_main()
