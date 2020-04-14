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
"""Tests for tensorflow_datasets.core._sharded_files."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_datasets import testing
from tensorflow_datasets.core import _sharded_files


class GetReadInstructionsTest(testing.TestCase):

  def test_read_all_even_sharding(self):
    # Even sharding
    res = _sharded_files.get_read_instructions(
        0, 12, ["f1", "f2", "f3"], [4, 4, 4])
    self.assertEqual(res, [
        {"filename": "f1", "skip": 0, "take": -1},
        {"filename": "f2", "skip": 0, "take": -1},
        {"filename": "f3", "skip": 0, "take": -1},
    ])

  def test_read_all_empty_shard(self):
    res = _sharded_files.get_read_instructions(
        0, 12, ["f1", "f2", "f3", "f4"], [4, 4, 0, 4])
    self.assertEqual(res, [
        {"filename": "f1", "skip": 0, "take": -1},
        {"filename": "f2", "skip": 0, "take": -1},
        {"filename": "f4", "skip": 0, "take": -1},
    ])

  def test_from1_to10(self):
    res = _sharded_files.get_read_instructions(
        1, 10, ["f1", "f2", "f3", "f4"], [4, 4, 0, 4])
    self.assertEqual(res, [
        {"filename": "f1", "skip": 1, "take": -1},
        {"filename": "f2", "skip": 0, "take": -1},
        {"filename": "f4", "skip": 0, "take": 2},
    ])

  def test_nothing_to_read(self):
    res = _sharded_files.get_read_instructions(
        0, 0, ["f1", "f2", "f3", "f4"], [0, 3, 0, 2])
    self.assertEqual(res, [])
    res = _sharded_files.get_read_instructions(
        4, 4, ["f1", "f2", "f3", "f4"], [0, 3, 0, 2])
    self.assertEqual(res, [])
    res = _sharded_files.get_read_instructions(
        5, 5, ["f1", "f2", "f3", "f4"], [0, 3, 0, 2])
    self.assertEqual(res, [])


if __name__ == "__main__":
  testing.test_main()
