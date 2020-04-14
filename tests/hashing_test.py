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
"""Tests for tensorflow_datasets.core.hashing."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_datasets import testing
from tensorflow_datasets.core import hashing


class HashingTest(testing.TestCase):

  def test_ints(self):
    hasher = hashing.Hasher(salt='')
    res = hasher.hash_key(0)
    self.assertEqual(res, 276215275525073243129443018166533317850)
    res = hasher.hash_key(123455678901234567890)
    self.assertEqual(res, 6876359009333865997613257802033240610)

  def test_ascii(self):
    hasher = hashing.Hasher(salt='')
    res = hasher.hash_key('foo')
    self.assertEqual(res, 229609063533823256041787889330700985560)


if __name__ == '__main__':
  testing.test_main()
