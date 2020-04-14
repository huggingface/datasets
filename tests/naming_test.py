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
"""Tests tensorflow_datasets.core.naming."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import parameterized
from tensorflow_datasets import testing
from tensorflow_datasets.core import naming
from tensorflow_datasets.core import splits


class NamingTest(parameterized.TestCase, testing.TestCase):

  @parameterized.parameters(
      ("HelloWorld", "hello_world"),
      ("FooBARBaz", "foo_bar_baz"),
      ("FooBar123", "foo_bar123"),
      ("FooBar123Baz", "foo_bar123_baz"),
      ("FooBar123baz", "foo_bar123baz"),
  )
  def test_camelcase_to_snakecase(self, camel, snake):
    self.assertEqual(snake, naming.camelcase_to_snakecase(camel))

  @parameterized.parameters(
      ("HelloWorld", "hello_world"),
      ("FooBar123", "foo_bar123"),
      ("FooBar123Baz", "foo_bar123_baz"),
      ("FooBar123baz", "foo_bar123baz"),
  )
  def test_snake_to_camelcase(self, camel, snake):
    self.assertEqual(naming.snake_to_camelcase(snake), camel)

  def test_sharded_filenames(self):
    prefix = "/tmp/foo"
    num_shards = 2
    expected = [
        "/tmp/foo-00000-of-00002",
        "/tmp/foo-00001-of-00002",
    ]
    self.assertEqual(expected, naming.sharded_filenames(prefix, num_shards))

  @parameterized.parameters(
      ("foo", "foo-train"),
      ("Foo", "foo-train"),
      ("FooBar", "foo_bar-train"),
  )
  def test_filename_prefix_for_split(self, prefix, expected):
    split = splits.Split.TRAIN
    self.assertEqual(expected, naming.filename_prefix_for_split(prefix, split))

  def test_filenames_for_dataset_split(self):
    self.assertEqual([
        "foo-train-00000-of-00002",
        "foo-train-00001-of-00002",
    ], naming.filenames_for_dataset_split(
        dataset_name="foo",
        split=splits.Split.TRAIN,
        num_shards=2))

  def test_filepaths_for_dataset_split(self):
    self.assertEqual([
        "/tmp/bar/foo-train-00000-of-00002",
        "/tmp/bar/foo-train-00001-of-00002",
    ],
                     naming.filepaths_for_dataset_split(
                         dataset_name="foo",
                         split=splits.Split.TRAIN,
                         num_shards=2,
                         data_dir="/tmp/bar/"))

  def test_filepaths_for_dataset_split_with_suffix(self):
    self.assertEqual([
        "/tmp/bar/foo-train.bar-00000-of-00002",
        "/tmp/bar/foo-train.bar-00001-of-00002",
    ],
                     naming.filepaths_for_dataset_split(
                         dataset_name="foo",
                         split=splits.Split.TRAIN,
                         num_shards=2,
                         data_dir="/tmp/bar/",
                         filetype_suffix="bar"))

  def test_filepattern_for_dataset_split(self):
    self.assertEqual("/tmp/bar/foo-test*",
                     naming.filepattern_for_dataset_split(
                         dataset_name="foo",
                         split=splits.Split.TEST,
                         data_dir="/tmp/bar/"))
    self.assertEqual("/tmp/bar/foo-test.bar*",
                     naming.filepattern_for_dataset_split(
                         dataset_name="foo",
                         split=splits.Split.TEST,
                         filetype_suffix="bar",
                         data_dir="/tmp/bar/"))


if __name__ == "__main__":
  testing.test_main()
