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
"""Tests for tensorflow_datasets.core.features.video_feature."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os.path
import numpy as np
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core import features

tf.enable_v2_behavior()


class VideoFeatureTest(testing.FeatureExpectationsTestCase):

  @property
  def _test_data_path(self):
    return os.path.join(os.path.dirname(__file__), '../../testing/test_data')

  def test_video_numpy(self):
    np_video = np.random.randint(256, size=(128, 64, 64, 3), dtype=np.uint8)

    self.assertFeature(
        feature=features.Video(shape=(None, 64, 64, 3)),
        shape=(None, 64, 64, 3),
        dtype=tf.uint8,
        tests=[
            testing.FeatureExpectationItem(
                value=np_video,
                expected=np_video,
            ),
        ],
    )

  def test_video_concatenated_frames(self):
    video_shape = (None, 400, 640, 3)
    lsun_examples_path = os.path.join(self._test_data_path, 'lsun_examples')
    frames_paths = [os.path.join(lsun_examples_path, '{}.jpg'.format(i))
                    for i in (1, 2, 3, 4)]
    frames = []
    for frame_path in frames_paths:
      with tf.io.gfile.GFile(frame_path, 'rb') as frame_fp:
        frames.append(tf.image.decode_jpeg(frame_fp.read(), channels=3))
    video = tf.stack(frames)

    self.assertFeature(
        feature=features.Video(shape=video_shape),
        shape=video_shape,
        dtype=tf.uint8,
        tests=[
            # Numpy array
            testing.FeatureExpectationItem(
                value=frames_paths,
                expected=video,
            ),
        ],
    )

  def test_video_ffmpeg(self):
    video_path = os.path.join(self._test_data_path, 'video.mkv')
    video_json_path = os.path.join(self._test_data_path, 'video.json')
    with tf.io.gfile.GFile(video_json_path) as fp:
      video_array = np.asarray(json.load(fp))

    self.assertFeature(
        feature=features.Video(shape=(5, 4, 2, 3)),
        shape=(5, 4, 2, 3),
        dtype=tf.uint8,
        tests=[
            testing.FeatureExpectationItem(
                value=video_path,
                expected=video_array,
            ),
        ],
    )

    self.assertFeature(
        feature=features.Video(shape=(5, 4, 2, 3)),
        shape=(5, 4, 2, 3),
        dtype=tf.uint8,
        tests=[
            testing.FeatureExpectationItem(
                value=video_path,
                expected=video_array,
            ),
        ],
    )

    class GFileWithSeekOnRead(tf.io.gfile.GFile):

      def read(self, *args, **kwargs):
        data_read = super(GFileWithSeekOnRead, self).read(*args, **kwargs)
        self.seek(0)
        return data_read

    with GFileWithSeekOnRead(video_path, 'rb') as video_fp:
      self.assertFeature(
          feature=features.Video(shape=(5, 4, 2, 3)),
          shape=(5, 4, 2, 3),
          dtype=tf.uint8,
          tests=[
              testing.FeatureExpectationItem(
                  value=video_fp,
                  expected=video_array,
              ),
          ],
      )


if __name__ == '__main__':
  testing.test_main()
