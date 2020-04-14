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
"""Tests for tensorflow_datasets.core.transform.image.image_transform."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core import decode as decode_lib
from tensorflow_datasets.core import features as features_lib
from tensorflow_datasets.core import utils

tf.enable_v2_behavior()

randint = np.random.randint


class BaseDecodeTest(testing.FeatureExpectationsTestCase):

  def test_image_custom_decode(self):

    # Do not uses random here because Jpeg compression has loss, so decoded
    # value isn't the same
    img_shaped = np.ones(shape=(30, 60, 3), dtype=np.uint8)
    x, y, w, h = 4, 7, 10, 13
    img_cropped = img_shaped[y:y + h, x:x + w, :]

    class DecodeCrop(decode_lib.Decoder):
      """Simple class on how to customize the decoding."""

      def decode_example(self, serialized_image):
        return tf.image.decode_and_crop_jpeg(
            serialized_image,
            [y, x, h, w],
            channels=self.feature.shape[-1],
        )

    @decode_lib.make_decoder()
    def decode_crop(serialized_image, feature):
      return tf.image.decode_and_crop_jpeg(
          serialized_image,
          [y, x, h, w],
          channels=feature.shape[-1],
      )

    image_path = utils.get_tfds_path('testing/test_data/test_image.jpg')
    with tf.io.gfile.GFile(image_path, 'rb') as f:
      serialized_img = f.read()

    self.assertFeature(
        # Image with statically defined shape
        feature=features_lib.Image(shape=(30, 60, 3), encoding_format='jpeg'),
        shape=(30, 60, 3),
        dtype=tf.uint8,
        tests=[
            testing.FeatureExpectationItem(
                value=img_shaped,
                expected=img_cropped,
                shape=(13, 10, 3),  # Shape is cropped
                decoders=DecodeCrop(),
            ),
            testing.FeatureExpectationItem(
                value=img_shaped,
                expected=img_cropped,
                shape=(13, 10, 3),  # Shape is cropped
                decoders=decode_crop(),  # pylint: disable=no-value-for-parameter
            ),
            testing.FeatureExpectationItem(
                value=image_path,
                expected=serialized_img,
                shape=(),
                dtype=tf.string,
                decoders=decode_lib.SkipDecoding(),
            ),
        ],
    )

  def test_video_custom_decode(self):

    image_path = utils.get_tfds_path('testing/test_data/test_image.jpg')
    with tf.io.gfile.GFile(image_path, 'rb') as f:
      serialized_img = f.read()

    self.assertFeature(
        # Image with statically defined shape
        feature=features_lib.Video(shape=(None, 30, 60, 3)),
        shape=(None, 30, 60, 3),
        dtype=tf.uint8,
        tests=[
            testing.FeatureExpectationItem(
                value=[image_path] * 15,  # 15 frames of video
                expected=[serialized_img] * 15,  # Non-decoded image
                shape=(15,),
                dtype=tf.string,  # Only string are decoded
                decoders=decode_lib.SkipDecoding(),
            ),
        ],
    )

    # Test with FeatureDict
    self.assertFeature(
        feature=features_lib.FeaturesDict({
            'image': features_lib.Image(
                shape=(30, 60, 3), encoding_format='jpeg'),
            'label': tf.int64,
        }),
        shape={
            'image': (30, 60, 3),
            'label': (),
        },
        dtype={
            'image': tf.uint8,
            'label': tf.int64,
        },
        tests=[
            testing.FeatureExpectationItem(
                decoders={
                    'image': decode_lib.SkipDecoding(),
                },
                value={
                    'image': image_path,
                    'label': 123,
                },
                expected={
                    'image': serialized_img,
                    'label': 123,
                },
                shape={
                    'image': (),
                    'label': (),
                },
                dtype={
                    'image': tf.string,
                    'label': tf.int64,
                },
            ),
        ],
    )


if __name__ == '__main__':
  testing.test_main()
