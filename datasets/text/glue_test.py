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
"""Tests for the GLUE data set.

We have an individual test for each config so that we can use sharding to
prevent the test from timing out.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_datasets import testing
from tensorflow_datasets.text import glue


class GlueColaTest(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["cola"]
  DATASET_CLASS = glue.Glue
  SPLITS = {
      "train": 3,
      "validation": 2,
      "test": 1,
  }


class GlueSst2Test(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["sst2"]
  DATASET_CLASS = glue.Glue
  SPLITS = {
      "train": 3,
      "validation": 2,
      "test": 1,
  }


class GlueQqpTest(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["qqp"]
  DATASET_CLASS = glue.Glue
  SPLITS = {
      "train": 3,
      "validation": 2,
      "test": 1,
  }


class GlueStsbTest(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["stsb"]
  DATASET_CLASS = glue.Glue
  SPLITS = {
      "train": 3,
      "validation": 2,
      "test": 1,
  }


class GlueMnliTest(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["mnli"]
  DATASET_CLASS = glue.Glue
  SPLITS = {
      "train": 3,
      "validation_matched": 2,
      "validation_mismatched": 2,
      "test_matched": 1,
      "test_mismatched": 1,
  }


class GlueQnliTest(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["qnli"]
  DATASET_CLASS = glue.Glue
  SPLITS = {
      "train": 3,
      "validation": 2,
      "test": 1,
  }


class GlueRteTest(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["rte"]
  DATASET_CLASS = glue.Glue
  SPLITS = {
      "train": 3,
      "validation": 2,
      "test": 1,
  }


class GlueWnliTest(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["wnli"]
  DATASET_CLASS = glue.Glue
  SPLITS = {
      "train": 3,
      "validation": 2,
      "test": 1,
  }


class GlueMrpcTest(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["mrpc"]
  DATASET_CLASS = glue.Glue
  DL_EXTRACT_RESULT = {
      "train": "MRPC/msr_paraphrase_train.txt",
      "test": "MRPC/msr_paraphrase_test.txt",
      "dev_ids": "MRPC/mrpc_dev_ids.tsv",
  }
  SPLITS = {
      "train": 10,
      "validation": 8,
      "test": 15,
  }


class GlueAxTest(testing.DatasetBuilderTestCase):
  BUILDER_CONFIG_NAMES_TO_TEST = ["ax"]
  DATASET_CLASS = glue.Glue
  DL_EXTRACT_RESULT = "AX/ax.tsv"
  SPLITS = {
      "test": 3,
  }


if __name__ == "__main__":
  testing.test_main()
