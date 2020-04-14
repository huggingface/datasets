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
"""Tests for tensorflow_datasets.core.file_format_adapter."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core import builder
from tensorflow_datasets.core import dataset_info
from tensorflow_datasets.core import dataset_utils
from tensorflow_datasets.core import example_serializer
from tensorflow_datasets.core import features
from tensorflow_datasets.core import file_format_adapter
from tensorflow_datasets.core import splits
from tensorflow_datasets.core import utils

tf.enable_v2_behavior()


class DummyTFRecordBuilder(builder.GeneratorBasedBuilder):

  VERSION = utils.Version("0.0.0", experiments={utils.Experiment.S3: False})

  def _split_generators(self, dl_manager):
    return [
        splits.SplitGenerator(
            name=splits.Split.TRAIN,
            num_shards=2,
            gen_kwargs={"range_": range(20)}),
        splits.SplitGenerator(
            name=splits.Split.VALIDATION,
            num_shards=1,
            gen_kwargs={"range_": range(20, 30)}),
        splits.SplitGenerator(
            name=splits.Split.TEST,
            num_shards=1,
            gen_kwargs={"range_": range(30, 40)}),
    ]

  def _generate_examples(self, range_):
    for i in range_:
      yield {
          "x": i,
          "y": np.array([-i]).astype(np.int64)[0],
          "z": tf.compat.as_text(str(i))
      }

  def _info(self):
    return dataset_info.DatasetInfo(
        builder=self,
        features=features.FeaturesDict({
            "x": tf.int64,
            "y": tf.int64,
            "z": tf.string,
        }),
    )


class FileFormatAdapterTest(testing.TestCase):

  def _test_generator_based_builder(self, builder_cls):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = builder_cls(data_dir=tmp_dir)
      builder.download_and_prepare()
      train_dataset = builder.as_dataset(split=splits.Split.TRAIN)
      valid_dataset = builder.as_dataset(split=splits.Split.VALIDATION)
      test_dataset = builder.as_dataset(split=splits.Split.TEST)

      self.assertIsInstance(train_dataset, tf.data.Dataset)

      def validate_dataset(dataset, min_val, max_val, test_range=False):
        els = []
        for el in dataset:
          x, y, z = el["x"].numpy(), el["y"].numpy(), el["z"].numpy()
          self.assertEqual(-x, y)
          self.assertEqual(x, int(z))
          self.assertGreaterEqual(x, min_val)
          self.assertLess(x, max_val)
          els.append(x)
        if test_range:
          self.assertCountEqual(list(range(min_val, max_val)), els)

      validate_dataset(train_dataset, 0, 30)
      validate_dataset(valid_dataset, 0, 30)
      validate_dataset(test_dataset, 30, 40, True)

  def test_tfrecords(self):
    self._test_generator_based_builder(DummyTFRecordBuilder)


class TFRecordUtilsTest(testing.SubTestCase):

  def test_dict_to_example(self):
    example = example_serializer._dict_to_tf_example({
        "a": 1,
        "a2": np.array(1),
        "b": ["foo", "bar"],
        "b2": np.array(["foo", "bar"]),
        "c": [2.0],
        "c2": np.array([2.0]),
        # Empty values supported when type is defined
        "d": np.array([], dtype=np.int32),
        # Support for byte strings
        "e": np.zeros(2, dtype=np.uint8).tobytes(),
        "e2": [np.zeros(2, dtype=np.uint8).tobytes()] * 2,
    })
    feature = example.features.feature
    self.assertEqual([1], list(feature["a"].int64_list.value))
    self.assertEqual([1], list(feature["a2"].int64_list.value))
    self.assertEqual([b"foo", b"bar"], list(feature["b"].bytes_list.value))
    self.assertEqual([b"foo", b"bar"], list(feature["b2"].bytes_list.value))
    self.assertEqual([2.0], list(feature["c"].float_list.value))
    self.assertEqual([2.0], list(feature["c2"].float_list.value))
    self.assertEqual([], list(feature["d"].int64_list.value))
    self.assertEqual([b"\x00\x00"], list(feature["e"].bytes_list.value))
    self.assertEqual([b"\x00\x00", b"\x00\x00"],
                     list(feature["e2"].bytes_list.value))

    with self.assertRaisesWithPredicateMatch(ValueError, "Received an empty"):
      # Raise error if an undefined empty value is given
      example_serializer._dict_to_tf_example({
          "empty": [],
      })

    with self.assertRaisesWithPredicateMatch(ValueError, "not support type"):
      # Raise error if an unsupported dtype is given
      example_serializer._dict_to_tf_example({
          "wrong_type": np.zeros(shape=(5,), dtype=np.complex64),
      })

  def test_features(self):

    default_dict = {
        "str": "some value",
        "int": 1,
        "bool": [True],
        "float": [[2.0, 3.0]],
    }

    self.assertFeature(
        specs={
            "str": features.TensorInfo(shape=(), dtype=tf.string),
            "int": features.TensorInfo(shape=(), dtype=tf.int32),
            "bool": features.TensorInfo(shape=(1,), dtype=tf.bool),
            "float": features.TensorInfo(shape=(1, 2), dtype=tf.float32),
        },
        serialized_info={
            "str": tf.io.FixedLenFeature(shape=(), dtype=tf.string),
            "int": tf.io.FixedLenFeature(shape=(), dtype=tf.int64),
            "bool": tf.io.FixedLenFeature(shape=(1,), dtype=tf.int64),
            "float": tf.io.FixedLenFeature(shape=(1, 2), dtype=tf.float32),
        },
        tests=[
            # Raw values
            testing.FeatureExpectationItem(
                value={
                    "str": "",
                    "int": 1,
                    "bool": [True],
                    "float": [[2.0, 3.0]],
                },
                expected={
                    "str": b"",
                    "int": 1,
                    "bool": [True],
                    "float": [[2.0, 3.0]],
                },
                expected_serialized={
                    "str": tf.train.Feature(
                        bytes_list=tf.train.BytesList(value=[b""])),
                    "int": tf.train.Feature(
                        int64_list=tf.train.Int64List(value=[1])),
                    "bool": tf.train.Feature(
                        int64_list=tf.train.Int64List(value=[1])),
                    "float": tf.train.Feature(
                        float_list=tf.train.FloatList(value=[2.0, 3.0])),
                },
            ),
            # Test numpy array
            testing.FeatureExpectationItem(
                value={
                    "str": np.zeros(2, dtype=np.uint8).tobytes(),
                    "int": np.array(1),
                    "bool": np.array([True]),
                    "float": np.array([[2.0, 3.0]]),
                },
                expected={
                    "str": b"\000\000",
                    "int": 1,
                    "bool": np.array([True]),
                    "float": np.array([[2.0, 3.0]], dtype=np.float32),
                },
                expected_serialized={
                    "str": tf.train.Feature(
                        bytes_list=tf.train.BytesList(value=[b"\000\000"])),
                    "int": tf.train.Feature(
                        int64_list=tf.train.Int64List(value=[1])),
                    "bool": tf.train.Feature(
                        int64_list=tf.train.Int64List(value=[1])),
                    "float": tf.train.Feature(
                        float_list=tf.train.FloatList(value=[2.0, 3.0])),
                },
            ),
            testing.FeatureExpectationItem(
                value=dict(default_dict, float=[[2.0], [3.0]]),  # Wrong shape
                raise_cls=ValueError,
                raise_msg="Shapes (2, 1) and (1, 2) are incompatible",
            ),
            testing.FeatureExpectationItem(
                value=dict(default_dict, bool=True),  # Wrong shape
                raise_cls=ValueError,
                raise_msg="Shapes () and (1,) must have the same rank",
            ),
            testing.FeatureExpectationItem(
                value=dict(default_dict, str=123),  # Wrong dtype
                raise_cls=ValueError,
                raise_msg="Could not convert to bytes",
            ),
        ],
    )

  def test_features_sequence(self):

    self.assertFeature(
        specs={
            "a": {
                "b": features.TensorInfo(shape=(None,), dtype=tf.string),
            },
            "a/c": features.TensorInfo(shape=(None, 2), dtype=tf.int32),
        },
        serialized_info={
            "a/b": tf.io.FixedLenSequenceFeature(
                shape=(), dtype=tf.string, allow_missing=True),
            "a/c": tf.io.FixedLenSequenceFeature(
                shape=(2,), dtype=tf.int64, allow_missing=True),
        },
        tests=[
            # Raw values
            testing.FeatureExpectationItem(
                value={
                    "a": {
                        "b": [],
                    },
                    "a/c": [[1, 2], [3, 4]],
                },
                expected={
                    "a": {
                        "b": [],
                    },
                    "a/c": [[1, 2], [3, 4]],
                },
                expected_serialized={
                    "a/b": tf.train.Feature(
                        bytes_list=tf.train.BytesList(value=[])),
                    "a/c": tf.train.Feature(
                        int64_list=tf.train.Int64List(value=[1, 2, 3, 4])),
                },
            ),
            testing.FeatureExpectationItem(
                value={
                    "a": {
                        "b": ["abc\n", "", "def  "],
                    },
                    "a/c": np.empty(shape=(0, 2), dtype=np.int32),
                },
                expected={
                    "a": {
                        "b": [b"abc\n", b"", b"def  "],
                    },
                    "a/c": np.empty(shape=(0, 2), dtype=np.int32),
                },
                expected_serialized={
                    "a/b": tf.train.Feature(
                        bytes_list=tf.train.BytesList(
                            value=[b"abc\n", b"", b"def  "])),
                    "a/c": tf.train.Feature(
                        int64_list=tf.train.Int64List(value=[])),
                },
            ),
        ],
    )

  def test_wrong_type(self):

    # Raise error if an unsupported dtype is given
    self.assertWrongSpecs(
        features.TensorInfo(shape=(), dtype=tf.complex64),
        raise_cls=NotImplementedError,
        raise_msg="not implemented for dtype",
    )

    # Raise error if an unsupported shape is given
    self.assertWrongSpecs(
        features.TensorInfo(shape=(3, None), dtype=tf.int32),
        raise_cls=NotImplementedError,
        raise_msg="unknown dimension not at the first position",
    )

  def assertWrongSpecs(self, specs, raise_cls, raise_msg):

    adapter = file_format_adapter.TFRecordExampleAdapter({"wrong_field": specs})
    # Raise error if an unsupported dtype is given
    with self.assertRaisesWithPredicateMatch(raise_cls, raise_msg):
      adapter._parser._build_feature_specs()

  @testing.run_in_graph_and_eager_modes()
  def assertFeature(self, specs, serialized_info, tests):
    """Test the TFRecordExampleAdapter encoding."""

    adapter = file_format_adapter.TFRecordExampleAdapter(specs)

    with self._subTest("serialized_info"):
      self.assertEqual(serialized_info, adapter._parser._build_feature_specs())

    for i, test in enumerate(tests):
      with self._subTest(str(i)):

        if test.raise_cls is not None:
          with self.assertRaisesWithPredicateMatch(
              test.raise_cls, test.raise_msg):
            adapter._serializer.serialize_example(test.value)
          continue
        serialized = adapter._serializer.serialize_example(test.value)

        if test.expected_serialized is not None:
          example_proto = tf.train.Example()
          example_proto.ParseFromString(serialized)
          expected_proto = tf.train.Example(
              features=tf.train.Features(feature=test.expected_serialized)
          )
          self.assertEqual(expected_proto, example_proto)

        example = _parse_example(serialized, adapter._parser.parse_example)

        with self._subTest("dtype"):
          out_dtypes = utils.map_nested(lambda s: s.dtype, example)
          expected_dtypes = utils.map_nested(lambda s: s.dtype, specs)
          self.assertEqual(out_dtypes, expected_dtypes)
        with self._subTest("shape"):
          # For shape, because (None, 3) match with (5, 3), we use
          # tf.TensorShape.assert_is_compatible_with on each of the elements
          utils.map_nested(
              lambda x: x[0].shape.assert_is_compatible_with(x[1].shape),
              utils.zip_nested(example, specs)
          )
        np_example = dataset_utils.as_numpy(example)
        self.assertAllEqualNested(np_example, test.expected)

  def test_default_value(self):

    # Encode example with the previous version
    file_adapter = file_format_adapter.TFRecordExampleAdapter({
        "image/encoded": features.TensorInfo(shape=(), dtype=tf.string),
    })
    serialized_example = file_adapter._serializer.serialize_example({
        "image/encoded": "hello world",
    })

    # Decode example with the new version
    file_adapter = file_format_adapter.TFRecordExampleAdapter({
        "image/encoded": features.TensorInfo(
            shape=(), dtype=tf.string, default_value=b"some string"),
        "image/height": features.TensorInfo(
            shape=(), dtype=tf.int64, default_value=-1),
        "image/width": features.TensorInfo(
            shape=(), dtype=tf.int64, default_value=-1),
    })

    # New fields should have the default values
    ds = tf.data.Dataset.from_tensors(serialized_example)
    ds = ds.map(file_adapter._parser.parse_example)
    example = next(iter(dataset_utils.as_numpy(ds)))
    self.assertEqual(example, {
        "image/encoded": b"hello world",
        "image/height": -1,
        "image/width": -1,
    })


def _parse_example(serialized, parse_function):
  """Decode the given feature."""
  ds = tf.data.Dataset.from_tensors(serialized)
  ds = ds.map(parse_function)

  if tf.executing_eagerly():
    return next(iter(ds))
  else:
    return tf.compat.v1.data.make_one_shot_iterator(ds).get_next()


if __name__ == "__main__":
  testing.test_main()
