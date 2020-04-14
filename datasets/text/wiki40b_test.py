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

"""Tests for wiki40b dataset module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from tensorflow_datasets import testing
from tensorflow_datasets.text import wiki40b

_EXAMPLE_DIR = os.path.join(
    os.path.normpath(os.path.dirname(__file__) + "/../"),
    "testing",
    "test_data",
    "fake_examples",
    "wiki40b",
)


class Wiki40bTest(testing.DatasetBuilderTestCase):

  @classmethod
  def setUpClass(cls):
    super(Wiki40bTest, cls).setUpClass()
    wiki40b._DATA_DIRECTORY = _EXAMPLE_DIR

  DATASET_CLASS = wiki40b.Wiki40b
  BUILDER_CONFIG_NAMES_TO_TEST = ["Wiki40B.en"]

  SPLITS = {
      "train": 3,
      "validation": 2,
      "test": 1,
  }


if __name__ == "__main__":
  testing.test_main()
