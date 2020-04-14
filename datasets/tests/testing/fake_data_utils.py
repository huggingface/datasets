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
"""Utility library to generate dataset-like files."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random
import tempfile

import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_datasets.core import utils

MIN_HEIGHT_WIDTH = 10
MAX_HEIGHT_WIDTH = 15
CHANNELS_NB = 3

_SAMPLE_RATE = 44100
_AUDIO_DURATION = 5


def get_random_picture(height=None, width=None, channels=CHANNELS_NB):
  """Returns random picture as np.ndarray (int)."""
  height = height or random.randrange(MIN_HEIGHT_WIDTH, MAX_HEIGHT_WIDTH)
  width = width or random.randrange(MIN_HEIGHT_WIDTH, MAX_HEIGHT_WIDTH)
  return np.random.randint(
      256, size=(height, width, channels), dtype=np.uint8)


def get_random_jpeg(height=None, width=None, channels=CHANNELS_NB):
  """Returns path to JPEG picture."""
  image = get_random_picture(height, width, channels)
  jpeg = tf.image.encode_jpeg(image)
  with utils.nogpu_session() as sess:
    res = sess.run(jpeg)
  fobj = tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.JPEG')
  fobj.write(res)
  fobj.close()
  return fobj.name


def get_random_png(height=None, width=None, channels=CHANNELS_NB):
  """Returns path to PNG picture."""
  # Big randomly generated pngs take large amounts of diskspace.
  # Instead, we resize a 4x4 random image to the png size.
  image = get_random_picture(4, 4, channels)
  image = tf.image.resize_nearest_neighbor(
      tf.expand_dims(image, 0), (height, width))[0]
  png = tf.image.encode_png(image)
  with utils.nogpu_session() as sess:
    res = sess.run(png)
  fobj = tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.PNG')
  fobj.write(res)
  fobj.close()
  return fobj.name


def get_random_audio(duration=_AUDIO_DURATION, sample=_SAMPLE_RATE):
  """Returns random audio as np.ndarray (float32)."""
  sample_number = np.arange(duration * sample)
  waveform = np.sin(
      2 * np.pi * sample_number * 440.0 / sample).astype(np.float32)
  waveform = waveform * 0.3
  return waveform


def get_random_wav_c1(
    channels=1, duration=_AUDIO_DURATION, sample=_SAMPLE_RATE):
  """Returns path to WAV audio having channels = 1."""
  audio = get_random_audio(duration, sample).reshape(-1, channels)
  wav = tf.audio.encode_wav(audio, sample)
  with utils.nogpu_session() as sess:
    res = sess.run(wav)
  with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.wav') as f:
    f.write(res)
  return f.name


def get_random_wav_c2(
    channels=2, duration=_AUDIO_DURATION, sample=_SAMPLE_RATE):
  """Returns path to WAV audio having channels = 2."""
  audio = get_random_audio(duration, sample).reshape(-1, channels)
  wav = tf.audio.encode_wav(audio, sample)
  with utils.nogpu_session() as sess:
    res = sess.run(wav)
  with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.wav') as f:
    f.write(res)
  return f.name
