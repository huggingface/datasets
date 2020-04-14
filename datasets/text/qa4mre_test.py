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
"""Tests for Qa4mre dataset module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_datasets import testing
from tensorflow_datasets.text import qa4mre


class Qa4mreMainTest(testing.DatasetBuilderTestCase):
  DATASET_CLASS = qa4mre.Qa4mre

  DL_EXTRACT_RESULT = {
      "2011.main.DE": "2011.main.DE.xml",
      "2011.main.EN": "2011.main.EN.xml",
      "2011.main.ES": "2011.main.ES.xml",
      "2011.main.IT": "2011.main.IT.xml",
      "2011.main.RO": "2011.main.RO.xml",
      "2012.main.AR": "2012.main.AR.xml",
      "2012.main.BG": "2012.main.BG.xml",
      "2012.main.DE": "2012.main.DE.xml",
      "2012.main.EN": "2012.main.EN.xml",
      "2012.main.ES": "2012.main.ES.xml",
      "2012.main.IT": "2012.main.IT.xml",
      "2012.main.RO": "2012.main.RO.xml",
      "2012.alzheimers.EN": "2012.alzheimers.EN.xml",
      "2013.main.AR": "2013.main.AR.xml",
      "2013.main.BG": "2013.main.BG.xml",
      "2013.main.EN": "2013.main.EN.xml",
      "2013.main.ES": "2013.main.ES.xml",
      "2013.main.RO": "2013.main.RO.xml",
      "2013.alzheimers.EN": "2013.alzheimers.EN.xml",
      "2013.entrance_exam.EN": "2013.entrance_exam.EN.xml"
  }

  SPLITS = {
      "train": 3,  # Number of fake train example
  }


if __name__ == "__main__":
  testing.test_main()
