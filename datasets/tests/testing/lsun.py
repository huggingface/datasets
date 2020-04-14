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
"""Tool for putting given images into a single lmdb database.

This is the format that's used by LSUN dataset (it also
uses webP encoded images inside).

To generate the example dataset:

python lsun.py --input_files=test_data/lsun_examples/1.webp,
                             test_data/lsun_examples/2.webp,
                             test_data/lsun_examples/3.webp
               --output_file=/tmp/lsun/train


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
import lmdb
import tensorflow.compat.v2 as tf

FLAGS = flags.FLAGS

flags.DEFINE_string("input_files", None,
                    "Comma separated list of files to put into the database.")
flags.DEFINE_string("output_file", None, "Path to the output file.")


def main(argv):
  if len(argv) > 1:
    raise tf.app.UsageError("Too many command-line arguments.")

  db = lmdb.open(FLAGS.output_file)
  with db.begin(write=True) as txn:
    for index, path in enumerate(FLAGS.input_files.split(",")):
      data = tf.io.gfile.GFile(path, "rb").read()
      txn.put(str(index), data)


if __name__ == "__main__":
  app.run(main)
