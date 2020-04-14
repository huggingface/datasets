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
"""Tests for tensorflow_datasets.core.test_utils."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v2 as tf

from tensorflow_datasets.testing import test_case
from tensorflow_datasets.testing import test_utils

tf.enable_v2_behavior()


class RunInGraphAndEagerTest(test_case.TestCase):

  def test_run_in_graph_and_eager_modes(self):
    l = []
    def inc(self, with_brackets):
      del self  # self argument is required by run_in_graph_and_eager_modes.
      mode = "eager" if tf.executing_eagerly() else "graph"
      with_brackets = "with_brackets" if with_brackets else "without_brackets"
      l.append((with_brackets, mode))

    f = test_utils.run_in_graph_and_eager_modes(inc)
    f(self, with_brackets=False)
    f = test_utils.run_in_graph_and_eager_modes()(inc)
    f(self, with_brackets=True)

    self.assertEqual(len(l), 4)
    self.assertEqual(set(l), {
        ("with_brackets", "graph"),
        ("with_brackets", "eager"),
        ("without_brackets", "graph"),
        ("without_brackets", "eager"),
    })

  def test_run_in_graph_and_eager_modes_setup_in_same_mode(self):
    modes = []
    mode_name = lambda: "eager" if tf.executing_eagerly() else "graph"

    class ExampleTest(test_case.TestCase):

      def runTest(self):
        pass

      def setUp(self):
        modes.append("setup_" + mode_name())

      @test_utils.run_in_graph_and_eager_modes
      def testBody(self):
        modes.append("run_" + mode_name())

    e = ExampleTest()
    e.setUp()
    e.testBody()

    self.assertEqual(modes[0:2], ["setup_eager", "run_eager"])
    self.assertEqual(modes[2:], ["setup_graph", "run_graph"])

if __name__ == "__main__":
  test_utils.test_main()
