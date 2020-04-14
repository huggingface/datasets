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
"""Tests for para_crawl dataset module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow_datasets.testing as tfds_test
from tensorflow_datasets.translate import para_crawl


class ParacrawlTest(tfds_test.DatasetBuilderTestCase):

  DATASET_CLASS = para_crawl.ParaCrawl
  BUILDER_CONFIG_NAMES_TO_TEST = ["enhu_plain_text"]
  SPLITS = {
      "train": 5,
  }
  DL_EXTRACT_RESULT = {"data_file": "en-hu.bicleaner07.txt"}


if __name__ == "__main__":
  tfds_test.test_main()
