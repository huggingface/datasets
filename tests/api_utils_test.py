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
"""Tests for tensorflow_datasets.core.api_utils."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from tensorflow_datasets import testing
from tensorflow_datasets.core import api_utils


class ApiUtilsTest(testing.TestCase):

  def test_disallow_positional_args(self):

    @api_utils.disallow_positional_args
    def fn(a, b, c=api_utils.REQUIRED_ARG, d=4):
      return (a, b, c, d)

    self.assertEqual(["a", "b", "c", "d"], api_utils.getargspec(fn).args)
    self.assertEqual((1, 2, 3, 4), fn(a=1, b=2, c=3))
    predicate = "use keyword"
    with self.assertRaisesWithPredicateMatch(ValueError, predicate):
      fn(1, 2, 3)
    with self.assertRaisesWithPredicateMatch(ValueError, predicate):
      fn(1, b=2, c=3)
    with self.assertRaisesWithPredicateMatch(ValueError, "is required"):
      fn(a=1, b=2)

  def test_disallow_positional_args_with_exceptions(self):

    @api_utils.disallow_positional_args(allowed=["a"])
    def fn(a, b, c=api_utils.REQUIRED_ARG, d=4):
      return (a, b, c, d)

    self.assertEqual(["a", "b", "c", "d"], api_utils.getargspec(fn).args)
    self.assertEqual((1, 2, 3, 4), fn(a=1, b=2, c=3))
    predicate = "use keyword"
    with self.assertRaisesWithPredicateMatch(ValueError, predicate):
      fn(1, 2, 3)
    self.assertEqual((1, 2, 3, 4), fn(1, b=2, c=3))

  def test_disallow_positional_args_method(self):

    class A(object):

      def __init__(self):
        self.e = 5

      @api_utils.disallow_positional_args
      def fn(self, a, b, c=api_utils.REQUIRED_ARG, d=4):
        return (a, b, c, d, self.e)

    obj = A()
    fn = obj.fn

    self.assertEqual((1, 2, 3, 4, 5), fn(a=1, b=2, c=3))
    predicate = "use keyword"
    with self.assertRaisesWithPredicateMatch(ValueError, predicate):
      fn(1, 2, 3)
    with self.assertRaisesWithPredicateMatch(ValueError, predicate):
      fn(1, b=2, c=3)
    with self.assertRaisesWithPredicateMatch(ValueError, "is required"):
      fn(a=1, b=2)


if __name__ == "__main__":
  testing.test_main()
