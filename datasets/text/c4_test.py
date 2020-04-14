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
"""Tests for c4 dataset module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import six

from tensorflow_datasets import testing
from tensorflow_datasets.text import c4


class C4Test(testing.DatasetBuilderTestCase):
  DATASET_CLASS = c4.C4
  # 10k shards take make the test too slow.
  c4._DEFAULT_NUM_SHARDS = 1
  # GzipFile + GFile and TextIOWrapper are broken for py2.
  BUILDER_CONFIG_NAMES_TO_TEST = ["en"] if six.PY3 else []

  DL_EXTRACT_RESULT = {
      "wet_urls": ["wet_urls.txt"],
      "wet_files": ["cc_0.warc.wet.gz", "cc_1.warc.wet.gz"],
      "badwords": "badwords.txt",
  }
  SPLITS = {
      "train": 1,
      "validation": 1,
  }
  SKIP_CHECKSUMS = True  # TODO(tfds): Update checksums


class C4NoCleanTest(C4Test):
  # GzipFile + GFile and TextIOWrapper are broken for py2.
  BUILDER_CONFIG_NAMES_TO_TEST = ["en.noclean"] if six.PY3 else []
  SPLITS = {
      "train": 3,
      "validation": 1,
  }


if __name__ == "__main__":
  testing.test_main()
