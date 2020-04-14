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
"""Tests for Kaggle API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import subprocess

import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core.download import kaggle


class KaggleTest(testing.TestCase):

  def test_competition_download(self):
    filenames = ["a", "b"]
    with testing.mock_kaggle_api(filenames):
      downloader = kaggle.KaggleCompetitionDownloader("digit-recognizer")
      self.assertEqual(downloader.competition_files, ["a", "b"])
      with testing.tmp_dir() as tmp_dir:
        for fname in downloader.competition_files:
          out_path = downloader.download_file(fname, tmp_dir)
          self.assertEqual(out_path, os.path.join(tmp_dir, fname))
          with tf.io.gfile.GFile(out_path) as f:
            self.assertEqual(fname, f.read())

  def test_competition_download_404(self):
    with testing.mock_kaggle_api(err_msg="404 - Not found"):
      with self.assertLogs(
          "spelled the competition name correctly", level="error"):
        downloader = kaggle.KaggleCompetitionDownloader("digit-recognizer")
        with self.assertRaises(subprocess.CalledProcessError):
          _ = downloader.competition_files

  def test_competition_download_error(self):
    with testing.mock_kaggle_api(err_msg="Some error"):
      with self.assertLogs("install the kaggle API", level="error"):
        downloader = kaggle.KaggleCompetitionDownloader("digit-recognizer")
        with self.assertRaises(subprocess.CalledProcessError):
          _ = downloader.competition_files

  def test_kaggle_type(self):
    downloader = kaggle.KaggleCompetitionDownloader("digit-recognizer")
    self.assertEqual(downloader._kaggle_type.download_cmd, "competitions")

    downloader = kaggle.KaggleCompetitionDownloader("author/dataset")
    self.assertEqual(downloader._kaggle_type.download_cmd, "datasets")


if __name__ == "__main__":
  testing.test_main()
