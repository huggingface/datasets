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
"""Tool for preparing test example of Starcraft dataset.


./starcraft  --resolution=64 --output_file=test.tfrecords
./starcraft  --resolution=64 --output_file=train_0.tfrecords
./starcraft  --resolution=64 --output_file=train_1.tfrecords
./starcraft  --resolution=64 --output_file=valid.tfrecords
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
import numpy as np
import png
import six
import tensorflow.compat.v2 as tf

FLAGS = flags.FLAGS

flags.DEFINE_integer("resolution", 64, "Resolution of the video.")
flags.DEFINE_string("output_file", None, "Path to the output file.")


def main(argv):
  if len(argv) > 1:
    raise tf.app.UsageError("Too many command-line arguments.")

  writer = tf.io.TFRecordWriter(FLAGS.output_file)

  feature_list = {}
  frame_list = []
  for _ in range(20):
    # generate 20 frames.
    png_image = six.StringIO()
    png.from_array(
        np.random.randint(
            low=0,
            high=255,
            size=(FLAGS.resolution, FLAGS.resolution, 3),
            dtype=np.uint8), "RGB").save(png_image)
    frame_list.append(
        tf.train.Feature(
            bytes_list=tf.train.BytesList(value=[png_image.getvalue()])))
    png_image.close()

  feature_list["rgb_screen"] = tf.train.FeatureList(feature=frame_list)

  context_feature = {}
  context_feature["game_duration_loops"] = tf.train.Feature(
      int64_list=tf.train.Int64List(value=[20]))
  context_feature["game_duration_seconds"] = tf.train.Feature(
      float_list=tf.train.FloatList(value=[20.0]))
  context_feature["n_steps"] = tf.train.Feature(
      int64_list=tf.train.Int64List(value=[20]))
  context_feature["screen_size"] = tf.train.Feature(
      int64_list=tf.train.Int64List(value=[FLAGS.resolution, FLAGS.resolution]))

  example = tf.train.SequenceExample(
      feature_lists=tf.train.FeatureLists(feature_list=feature_list),
      context=tf.train.Features(feature=context_feature))
  writer.write(example.SerializeToString())
  writer.close()


if __name__ == "__main__":
  app.run(main)
