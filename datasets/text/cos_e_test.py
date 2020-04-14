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
"""Test for CoS-E dataset module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_datasets import testing
from tensorflow_datasets.text import cos_e


class CosETest(testing.DatasetBuilderTestCase):
  DATASET_CLASS = cos_e.CosE
  SPLITS = {
      "validation": 2,  # Number of fake validation examples
      "train": 2,  # Number of fake train examples
  }

  DL_EXTRACT_RESULT = {
      "dev": ["cos_e_dev.jsonl"],
      "train": ["cos_e_train.jsonl"],
      "cqa_dev": "cqa_dev.jsonl",
      "cqa_train": "cqa_train.jsonl",
      "cqa_test": "cqa_test.jsonl",
  }


if __name__ == "__main__":
  testing.test_main()
