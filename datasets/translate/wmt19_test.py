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
"""Tests for WMT translate dataset module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_datasets import testing
from tensorflow_datasets.translate import wmt19


class TranslateDeEnWmt19Test(testing.DatasetBuilderTestCase):
  DATASET_CLASS = wmt19.Wmt19Translate
  BUILDER_CONFIG_NAMES_TO_TEST = ["de-en"]
  OVERLAPPING_SPLITS = ["validation"]

  DL_EXTRACT_RESULT = {
      "europarl_v9": ["sentences.de-en.tsv"],
      "paracrawl_v3": ["sentences.de-en.tmx"],
      "commoncrawl": ["commoncrawl"],
      "newscommentary_v14": ["sentences.de-en.tsv"],
      "wikititles_v1": ["sentences.de-en.tsv"],
      "rapid_2019": ["rapid_2019"],
      "newstest2018": ["validation"],
  }

  SPLITS = {
      "train": 12,
      "validation": 2,
  }


class TranslateCsEnWmt19Test(testing.DatasetBuilderTestCase):
  DATASET_CLASS = wmt19.Wmt19Translate
  BUILDER_CONFIG_NAMES_TO_TEST = ["cs-en"]
  OVERLAPPING_SPLITS = ["validation"]

  DL_EXTRACT_RESULT = {
      "czeng17_filter": ["czeng"],
      "europarl_v9": ["sentences.cs-en.tsv"],
      "paracrawl_v3": ["sentences.cs-en.tmx"],
      "commoncrawl": ["commoncrawl"],
      "newscommentary_v14": ["sentences.cs-en.tsv"],
      "wikititles_v1": ["sentences.cs-en.tsv"],
      "newstest2018": ["validation"],
  }

  SPLITS = {
      "train": 13,
      "validation": 2,
  }

if __name__ == "__main__":
  testing.test_main()
