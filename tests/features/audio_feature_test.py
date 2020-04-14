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
"""Tests for tensorflow_datasets.core.features.audio_feature."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import array
import tempfile

import numpy as np
import pydub
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core import features

tf.enable_v2_behavior()


class AudioFeatureTest(testing.FeatureExpectationsTestCase):

  def create_np_audio(self):
    return np.random.randint(-2**10, 2**10, size=(10,), dtype=np.int64)

  def test_numpy_array(self):
    np_audio = self.create_np_audio()

    self.assertFeature(
        feature=features.Audio(),
        shape=(None,),
        dtype=tf.int64,
        tests=[
            testing.FeatureExpectationItem(
                value=np_audio,
                expected=np_audio,
            ),
        ],
    )

  def write_wave_file(self, np_audio, path):
    audio = pydub.AudioSegment.empty().set_sample_width(2)
    # See documentation for _spawn usage:
    # https://github.com/jiaaro/pydub/blob/master/API.markdown#audiosegmentget_array_of_samples
    audio = audio._spawn(array.array(audio.array_type, np_audio))
    audio.export(path, format="wav")

  def test_wav_file(self):

    np_audio = self.create_np_audio()
    _, tmp_file = tempfile.mkstemp()
    self.write_wave_file(np_audio, tmp_file)

    self.assertFeature(
        feature=features.Audio(file_format="wav"),
        shape=(None,),
        dtype=tf.int64,
        tests=[
            testing.FeatureExpectationItem(
                value=tmp_file,
                expected=np_audio,
            ),
        ],
    )

  def test_file_object(self):
    np_audio = self.create_np_audio()
    _, tmp_file = tempfile.mkstemp()
    self.write_wave_file(np_audio, tmp_file)

    class GFileWithSeekOnRead(tf.io.gfile.GFile):
      """Wrapper around GFile which is reusable across multiple read() calls.

      This is needed because assertFeature reuses the same
      FeatureExpectationItem several times.
      """

      def read(self, *args, **kwargs):
        data_read = super(GFileWithSeekOnRead, self).read(*args, **kwargs)
        self.seek(0)
        return data_read

    with GFileWithSeekOnRead(tmp_file, "rb") as file_obj:
      self.assertFeature(
          feature=features.Audio(file_format="wav"),
          shape=(None,),
          dtype=tf.int64,
          tests=[
              testing.FeatureExpectationItem(
                  value=file_obj,
                  expected=np_audio,
              ),
          ],
      )


if __name__ == "__main__":
  testing.test_main()
