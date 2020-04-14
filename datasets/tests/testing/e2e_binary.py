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
r"""Binary exercising critical workflow of tensorflow datasets.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
import tensorflow.compat.v2 as tf
import tensorflow_datasets as tfds

tf.enable_v2_behavior()


def main(argv):
  del argv
  mnist, info = tfds.load('mnist', with_info=True)
  print(mnist, info)
  mnist_train = tfds.load('mnist', split='train')
  print(mnist_train)
  mnist_subsplit = tfds.Split.TRAIN.subsplit(tfds.percent[:10])
  mnist_train2 = tfds.load('mnist', split=mnist_subsplit)
  print(mnist_train2)
  for i, unused_row in enumerate(mnist_train2):
    if i > 10:
      break
    print(i)
  builder = tfds.builder('cifar10')
  dataset = builder.as_dataset(split='train')
  print(dataset)
  cifar10_np = tfds.as_numpy(dataset)
  print(cifar10_np)


if __name__ == '__main__':
  app.run(main)
