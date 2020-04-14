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
"""Tests for tensorflow_datasets.text.cnn_dailymail."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tempfile

from tensorflow_datasets import testing
import tensorflow_datasets.public_api as tfds
from tensorflow_datasets.summarization import cnn_dailymail

_STORY_FILE = b"""Some article.
This is some article text.

@highlight

highlight text

@highlight

Highlight two

@highlight

highlight Three
"""


class CnnDailymailTest(testing.DatasetBuilderTestCase):
  DATASET_CLASS = cnn_dailymail.CnnDailymail
  SPLITS = {'train': 3, 'validation': 2, 'test': 2}
  DL_EXTRACT_RESULT = {
      'cnn_stories': '',
      'dm_stories': '',
      'test_urls': 'all_test.txt',
      'train_urls': 'all_train.txt',
      'val_urls': 'all_val.txt'
  }

  def test_get_art_abs(self):
    with tempfile.NamedTemporaryFile(delete=True) as f:
      f.write(_STORY_FILE)
      f.flush()
      article, abstract = cnn_dailymail._get_art_abs(f.name,
                                                     tfds.core.Version('1.0.0'))
      self.assertEqual('Some article. This is some article text.', article)
      # This is a bit weird, but the original code at
      # https://github.com/abisee/cnn-dailymail/ adds space before period
      # for abstracts and we retain this behavior.
      self.assertEqual('highlight text . Highlight two . highlight Three .',
                       abstract)

      article, abstract = cnn_dailymail._get_art_abs(f.name,
                                                     tfds.core.Version('2.0.0'))
      self.assertEqual('highlight text .\nHighlight two .\nhighlight Three .',
                       abstract)


if __name__ == '__main__':
  testing.test_main()
