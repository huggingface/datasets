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
# -*- coding: utf-8 -*-
"""Tests for WMT translate dataset module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import six
from tensorflow_datasets import testing
import tensorflow_datasets.public_api as tfds
from tensorflow_datasets.translate import wmt


class TranslateWmtCustomConfigTest(testing.DatasetBuilderTestCase):

  @classmethod
  def setUpClass(cls):
    super(TranslateWmtCustomConfigTest, cls).setUpClass()

    config = wmt.WmtConfig(
        name="small",
        language_pair=("cs", "en"),
        description="Example of custom config",
        subsets={
            "train": ["paracrawl_v3"],
            "validation": ["newstest2009", "newstest2010"],
        },
        version=tfds.core.Version("1.0.0"),
    )
    wmt.WmtTranslate.BUILDER_CONFIGS = [config]

  @classmethod
  def tearDownClass(cls):
    super(TranslateWmtCustomConfigTest, cls).tearDownClass()
    wmt.WmtTranslate.BUILDER_CONFIGS.pop()

  DATASET_CLASS = wmt.WmtTranslate
  # OVERLAPPING_SPLITS = ["validation"]

  DL_EXTRACT_RESULT = {
      "czeng17_filter": ["czeng"],
      "europarl_v9": ["sentences.cs-en.tsv"],
      "paracrawl_v3": ["sentences.cs-en.tmx"],
      "commoncrawl": ["commoncrawl"],
      "newscommentary_v14": ["sentences.cs-en.tsv"],
      "wikititles_v1": ["sentences.cs-en.tsv"],
      "newssyscomb2009": ["validation"],
      "newstest2008": ["validation"],
      "newstest2009": ["validation"],
      "newstest2010": ["validation"],
      "newstest2011": ["validation"],
      "newstest2012": ["validation"],
      "newstest2013": ["validation"],
      "newstest2014": ["validation"],
      "newstest2015": ["validation"],
      "newstest2016": ["validation"],
      "newstest2017": ["validation"],
      "newstest2018": ["validation"],
  }

  SPLITS = {
      "train": 2,
      "validation": 4,
  }

  # Wmt itself do not define checksums. Checksums are contained in individual
  # `wmt16.txt`, `wmt17.txt`,... files.
  SKIP_CHECKSUMS = True

  def test_gzip_reading(self):
    results = [
        x for _, x in wmt._parse_parallel_sentences(
            os.path.join(self.example_dir, "first.cs.gz"),
            os.path.join(self.example_dir, "second.en.txt"))
    ]
    self.assertEqual(results[1]["cs"], "zmizel")
    if six.PY3:
      self.assertEqual(results[0]["cs"], "běžím")
    else:
      self.assertTrue(results[0]["cs"] == u"běžím")  # pylint: disable=g-generic-assert


if __name__ == "__main__":
  testing.test_main()
