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
"""Tests for tensorflow_datasets.core.visualization."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import mock

from tensorflow_datasets import testing
from tensorflow_datasets.core import visualization


class VisualizationTest(testing.TestCase):

  @mock.patch("matplotlib.pyplot.figure")
  def test_show_examples(self, mock_fig):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = testing.DummyMnist(data_dir=tmp_dir)
    builder.download_and_prepare()
    ds = builder.as_dataset(split="train")
    visualization.show_examples(builder.info, ds)


if __name__ == "__main__":
  testing.test_main()
