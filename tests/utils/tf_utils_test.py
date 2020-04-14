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
"""Tests for tensorflow_datasets.core.utils.tf_utils."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core.utils import tf_utils

tf.enable_v2_behavior()


class TfUtilsTest(testing.TestCase):

  @testing.run_in_graph_and_eager_modes()
  def test_graph_runner(self):
    graph_runner = tf_utils.TFGraphRunner()

    output = graph_runner.run(tf.nn.relu, [1, 1, -1, -1, 1])
    self.assertAllEqual(output, [1, 1, 0, 0, 1])

    output = graph_runner.run(tf.nn.relu, [-1, -1, -1, 1, 1])
    self.assertAllEqual(output, [0, 0, 0, 1, 1])

    # Cache should have been re-used, so should only contains one GraphRun
    # Ideally there should be two separate @tf.eager.run_test_in_graph() and
    # @tf.eager.run_test_in_eager() to avoid logic on the test. But haven't
    # found it.
    if not tf.executing_eagerly():
      self.assertEqual(len(graph_runner._graph_run_cache), 1)
    else:
      self.assertEqual(len(graph_runner._graph_run_cache), 0)

    # Different signature (different shape), so new GraphRun created
    output = graph_runner.run(tf.nn.relu, [-1, 1, 1])
    self.assertAllEqual(output, [0, 1, 1])
    if not tf.executing_eagerly():
      self.assertEqual(len(graph_runner._graph_run_cache), 2)
    else:
      self.assertEqual(len(graph_runner._graph_run_cache), 0)


if __name__ == '__main__':
  testing.test_main()
