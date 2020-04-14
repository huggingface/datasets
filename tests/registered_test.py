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
"""Tests for tensorflow_datasets.core.registered."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import mock

from tensorflow_datasets import testing
from tensorflow_datasets.core import registered
from tensorflow_datasets.core import splits
from tensorflow_datasets.core.utils import py_utils


class EmptyDatasetBuilder(metaclass=registered.RegisteredDataset):

  def __init__(self, **kwargs):
    self.kwargs = kwargs
    self.download_called = False
    self.as_dataset_called = False

  def download_and_prepare(self, **kwargs):
    self.download_called = True
    self.download_kwargs = kwargs

  def as_dataset(self, **kwargs):
    self.as_dataset_called = True
    self.as_dataset_kwargs = kwargs
    return self


class UnregisteredBuilder(EmptyDatasetBuilder):

  @abc.abstractproperty
  def an_abstract_property(self):
    pass


class InDevelopmentDatasetBuilder(EmptyDatasetBuilder):

  IN_DEVELOPMENT = True


class RegisteredTest(testing.TestCase):

  def test_registered(self):
    name = "empty_dataset_builder"
    self.assertEqual(name, EmptyDatasetBuilder.name)
    self.assertIsInstance(registered.builder(name), EmptyDatasetBuilder)
    self.assertIn(name, registered.list_builders())

    nonexistent = "nonexistent_foobar_dataset"
    with self.assertRaisesWithPredicateMatch(ValueError, "not found"):
      registered.builder(nonexistent)
    # Prints registered datasets
    with self.assertRaisesWithPredicateMatch(ValueError, name):
      registered.builder(nonexistent)

  def test_abstract(self):
    name = "unregistered_builder"
    self.assertEqual(name, UnregisteredBuilder.name)
    self.assertNotIn(name, registered.list_builders())

    with self.assertRaisesWithPredicateMatch(ValueError, "an abstract class"):
      registered.builder(name)

  def test_in_development(self):
    name = "in_development_dataset_builder"
    self.assertEqual(name, InDevelopmentDatasetBuilder.name)
    self.assertNotIn(name, registered.list_builders())

    with self.assertRaisesWithPredicateMatch(
        ValueError,
        ("Dataset %s is under active development and is not available yet."
        ) % name):
      registered.builder(name)

  def test_builder_with_kwargs(self):
    name = "empty_dataset_builder"
    name_with_kwargs = name + "/k1=1,k2=1.,k3=foo,k4=True,k5=False"
    builder = registered.builder(name_with_kwargs, data_dir="bar")
    expectations = [("k1", 1), ("k2", 1.), ("k3", u"foo"), ("k4", True),
                    ("k5", False)]
    for k, v in expectations:
      self.assertEqual(type(builder.kwargs[k]), type(v))
      self.assertEqual(builder.kwargs[k], v)

  def test_builder_fullname(self):
    fullname = "empty_dataset_builder/conf1-attr:1.0.1/k1=1,k2=2"
    builder = registered.builder(fullname, data_dir="bar")
    expected = {"k1": 1, "k2": 2, "version": "1.0.1",
                "config": "conf1-attr", "data_dir": "bar"}
    self.assertEqual(expected, builder.kwargs)

  def test_load(self):
    name = "empty_dataset_builder/k1=1"
    data_dir = "foo"
    as_dataset_kwargs = dict(a=1, b=2)

    # EmptyDatasetBuilder returns self from as_dataset
    builder = registered.load(
        name=name, split=splits.Split.TEST, data_dir=data_dir,
        download=False, as_dataset_kwargs=as_dataset_kwargs)
    self.assertTrue(builder.as_dataset_called)
    self.assertFalse(builder.download_called)
    self.assertEqual(splits.Split.TEST,
                     builder.as_dataset_kwargs.pop("split"))
    self.assertEqual(None, builder.as_dataset_kwargs.pop("batch_size"))
    self.assertFalse(builder.as_dataset_kwargs.pop("as_supervised"))
    self.assertFalse(builder.as_dataset_kwargs.pop("decoders"))
    self.assertIsNone(builder.as_dataset_kwargs.pop("in_memory"))
    self.assertIsNone(builder.as_dataset_kwargs.pop("read_config"))
    self.assertFalse(builder.as_dataset_kwargs.pop("shuffle_files"))
    self.assertEqual(builder.as_dataset_kwargs, as_dataset_kwargs)
    self.assertEqual(dict(data_dir=data_dir, k1=1), builder.kwargs)

    builder = registered.load(
        name, split=splits.Split.TRAIN, data_dir=data_dir,
        download=True, as_dataset_kwargs=as_dataset_kwargs)
    self.assertTrue(builder.as_dataset_called)
    self.assertTrue(builder.download_called)

    # Tests for different batch_size
    # By default batch_size=None
    builder = registered.load(
        name=name, split=splits.Split.TEST, data_dir=data_dir)
    self.assertEqual(None, builder.as_dataset_kwargs.pop("batch_size"))
    # Setting batch_size=1
    builder = registered.load(
        name=name, split=splits.Split.TEST, data_dir=data_dir,
        batch_size=1)
    self.assertEqual(1, builder.as_dataset_kwargs.pop("batch_size"))

  def test_load_all_splits(self):
    name = "empty_dataset_builder"
    # EmptyDatasetBuilder returns self from as_dataset
    builder = registered.load(name=name, data_dir="foo")
    self.assertTrue(builder.as_dataset_called)
    self.assertEqual(None, builder.as_dataset_kwargs.pop("split"))

  def test_load_with_config(self):
    data_dir = "foo"
    name = "empty_dataset_builder/bar/k1=1"
    # EmptyDatasetBuilder returns self from as_dataset
    builder = registered.load(name=name, split=splits.Split.TEST,
                              data_dir=data_dir)
    expected = dict(data_dir=data_dir, k1=1, config="bar")
    self.assertEqual(expected, builder.kwargs)

    name = "empty_dataset_builder/bar"
    builder = registered.load(name=name, split=splits.Split.TEST,
                              data_dir=data_dir)
    self.assertEqual(dict(data_dir=data_dir, config="bar"),
                     builder.kwargs)

  def test_notebook_overwrite_dataset(self):
    """Redefining the same builder twice is possible on colab."""

    with mock.patch.object(py_utils, "is_notebook", lambda: True):
      name = "colab_builder"
      self.assertNotIn(name, registered.list_builders())

      class ColabBuilder(metaclass=registered.RegisteredDataset):
        pass

      self.assertIn(name, registered.list_builders())
      self.assertIsInstance(registered.builder(name), ColabBuilder)
      old_colab_class = ColabBuilder

      class ColabBuilder(metaclass=registered.RegisteredDataset):
        pass

      self.assertIsInstance(registered.builder(name), ColabBuilder)
      self.assertNotIsInstance(registered.builder(name), old_colab_class)

  def test_duplicate_dataset(self):
    """Redefining the same builder twice should raises error."""

    class DuplicateBuilder(metaclass=registered.RegisteredDataset):
      pass

    with self.assertRaisesWithPredicateMatch(ValueError, "already registered"):
      class DuplicateBuilder(metaclass=registered.RegisteredDataset):
        pass


if __name__ == "__main__":
  testing.test_main()
