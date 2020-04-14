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
"""Script to generate fake 'Lost and Found' data."""
import tensorflow.compat.v2 as tf

import tensorflow_datasets.testing.cityscapes as cityscapes

if __name__ == '__main__':
  example_dir = ('tensorflow_datasets/testing/test_data/fake_examples/'
                 'lost_and_found')
  base_path = example_dir + '/{}.zip'
  # generate image ids matching between zipfiles
  train_ids = list(cityscapes.generate_ids('01_Turmstr_17')) + list(
      cityscapes.generate_ids('02_Goethe_Str_6'))
  test_ids = list(cityscapes.generate_ids('03_Schlossallee_1'))
  splits = {'train': train_ids, 'test': test_ids}
  with tf.Graph().as_default():
    cityscapes.create_zipfile(
        base_path.format('leftImg8bit'),
        splits_with_ids=splits,
        suffixes=['leftImg8bit'])
    cityscapes.create_zipfile(
        base_path.format('gtCoarse'),
        splits_with_ids=splits,
        suffixes=[
            'gtCoarse_instanceIds', 'gtCoarse_labelIds', 'gtCoarse_color'
        ])
    cityscapes.create_zipfile(
        base_path.format('rightImg8bit'),
        splits_with_ids=splits,
        suffixes=['rightImg8bit'])
    cityscapes.create_zipfile(
        base_path.format('disparity'),
        splits_with_ids=splits,
        suffixes=['disparity'])
