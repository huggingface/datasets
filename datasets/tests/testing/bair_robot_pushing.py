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
"""Tool for preparing test example of BAIR dataset.

mkdir test/
mkdir train/

./bair_robot_pushing  --output_file=train/traj_1792_to_2047.tfrecords
./bair_robot_pushing  --output_file=test/traj_0_to_255.tfrecords
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
import numpy as np
import tensorflow.compat.v2 as tf

FLAGS = flags.FLAGS

flags.DEFINE_string("output_file", None, "Path to the output file.")


def main(argv):
  if len(argv) > 1:
    raise tf.app.UsageError("Too many command-line arguments.")

  writer = tf.io.TFRecordWriter(FLAGS.output_file)

  feature = {}

  for frame in range(30):
    feature["%d/action" % frame] = tf.train.Feature(
        float_list=tf.train.FloatList(value=np.random.uniform(size=(4))))
    feature["%d/endeffector_pos" % frame] = tf.train.Feature(
        float_list=tf.train.FloatList(value=np.random.uniform(size=(3))))
    feature["%d/image_aux1/encoded" % frame] = tf.train.Feature(
        bytes_list=tf.train.BytesList(value=["\x00\xff\x00" * 64 * 64]))
    feature["%d/image_main/encoded" % frame] = tf.train.Feature(
        bytes_list=tf.train.BytesList(value=["\x00\x00\xff" * 64 * 64]))
  example = tf.train.Example(features=tf.train.Features(feature=feature))
  writer.write(example.SerializeToString())
  writer.close()


if __name__ == "__main__":
  app.run(main)
