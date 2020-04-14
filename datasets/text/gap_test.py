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
"""Test for GAP data set."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_datasets import testing
from tensorflow_datasets.text import gap


class GapTest(testing.DatasetBuilderTestCase):
  DATASET_CLASS = gap.Gap
  SPLITS = {
      "train": 5,  # Number of fake train examples
      "validation": 3,  # Number of fake validation examples
      "test": 3,  # Number of fake test examples
  }
  DL_EXTRACT_RESULT = {
      "train": "gap-development.tsv",
      "validation": "gap-validation.tsv",
      "test": "gap-test.tsv",
  }


if __name__ == "__main__":
  testing.test_main()
