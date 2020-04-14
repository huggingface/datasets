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
"""Test utilities."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import contextlib
import functools
import os
import subprocess
import tempfile

from absl.testing import absltest

import dill
import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_datasets.core import builder
from tensorflow_datasets.core import dataset_info
from tensorflow_datasets.core import dataset_utils
from tensorflow_datasets.core import features
from tensorflow_datasets.core import file_format_adapter
from tensorflow_datasets.core import splits
from tensorflow_datasets.core import utils
from tensorflow_datasets.testing import test_case


@contextlib.contextmanager
def tmp_dir(dirname=None):
  """Context manager for a temporary directory."""
  tmp = make_tmp_dir(dirname)
  yield tmp
  rm_tmp_dir(tmp)


def make_tmp_dir(dirname=None):
  """Make a temporary directory."""
  if dirname and not tf.io.gfile.exists(dirname):
    tf.io.gfile.makedirs(dirname)
  return tempfile.mkdtemp(dir=dirname)


def rm_tmp_dir(dirname):
  """Rm temporary directory."""
  tf.io.gfile.rmtree(dirname)


def remake_dir(d):
  """Possibly deletes and recreates directory."""
  if tf.io.gfile.exists(d):
    tf.io.gfile.rmtree(d)
  tf.io.gfile.makedirs(d)


def fake_examples_dir():
  return os.path.join(os.path.dirname(__file__), "test_data", "fake_examples")


class FeatureExpectationItem(object):
  """Test item of a FeatureExpectation."""

  def __init__(
      self,
      value,
      expected=None,
      expected_serialized=None,
      decoders=None,
      dtype=None,
      shape=None,
      raise_cls=None,
      raise_msg=None):
    self.value = value
    self.expected = expected
    self.expected_serialized = expected_serialized
    self.decoders = decoders
    self.dtype = dtype
    self.shape = shape
    if not decoders and (dtype is not None or shape is not None):
      raise ValueError("dtype and shape should only be set with transform")
    self.raise_cls = raise_cls
    self.raise_msg = raise_msg


class SubTestCase(test_case.TestCase):
  """Adds subTest() context manager to the TestCase if supported.

  Note: To use this feature, make sure you call super() in setUpClass to
  initialize the sub stack.
  """

  @classmethod
  def setUpClass(cls):
    super(SubTestCase, cls).setUpClass()
    cls._sub_test_stack = []

  @contextlib.contextmanager
  def _subTest(self, test_str):
    sub_test_not_implemented = True
    if sub_test_not_implemented:
      yield
    else:
      self._sub_test_stack.append(test_str)
      sub_test_str = "/".join(self._sub_test_stack)
      with self.subTest(sub_test_str):
        yield
      self._sub_test_stack.pop()

  def assertAllEqualNested(self, d1, d2):
    """Same as assertAllEqual but compatible with nested dict."""
    if isinstance(d1, dict):
      # assertAllEqual do not works well with dictionaries so assert
      # on each individual elements instead
      zipped_examples = utils.zip_nested(d1, d2, dict_only=True)
      utils.map_nested(
          lambda x: self.assertAllEqual(x[0], x[1]),
          zipped_examples,
          dict_only=True,
      )
    else:
      self.assertAllEqual(d1, d2)


def run_in_graph_and_eager_modes(func=None,
                                 config=None,
                                 use_gpu=True):
  """Execute the decorated test in both graph mode and eager mode.

  This function returns a decorator intended to be applied to test methods in
  a `test_case.TestCase` class. Doing so will cause the contents of the test
  method to be executed twice - once in graph mode, and once with eager
  execution enabled. This allows unittests to confirm the equivalence between
  eager and graph execution.

  NOTE: This decorator can only be used when executing eagerly in the
  outer scope.

  For example, consider the following unittest:

  ```python
  tf.enable_v2_behavior()

  class SomeTest(testing.TestCase):

    @testing.run_in_graph_and_eager_modes
    def test_foo(self):
      x = tf.constant([1, 2])
      y = tf.constant([3, 4])
      z = tf.add(x, y)
      self.assertAllEqual([4, 6], self.evaluate(z))

  if __name__ == "__main__":
    testing.test_main()
  ```

  This test validates that `tf.add()` has the same behavior when computed with
  eager execution enabled as it does when constructing a TensorFlow graph and
  executing the `z` tensor with a session.

  Args:
    func: function to be annotated. If `func` is None, this method returns a
      decorator the can be applied to a function. If `func` is not None this
      returns the decorator applied to `func`.
    config: An optional config_pb2.ConfigProto to use to configure the session
      when executing graphs.
    use_gpu: If True, attempt to run as many operations as possible on GPU.

  Returns:
    Returns a decorator that will run the decorated test method twice:
    once by constructing and executing a graph in a session and once with
    eager execution enabled.
  """

  def decorator(f):
    """Decorator for a method."""
    def decorated(self, *args, **kwargs):
      """Run the decorated test method."""
      if not tf.executing_eagerly():
        raise ValueError("Must be executing eagerly when using the "
                         "run_in_graph_and_eager_modes decorator.")

      # Run eager block
      f(self, *args, **kwargs)
      self.tearDown()

      # Run in graph mode block
      with tf.Graph().as_default():
        self.setUp()
        with self.test_session(use_gpu=use_gpu, config=config):
          f(self, *args, **kwargs)

    return decorated

  if func is not None:
    return decorator(func)

  return decorator


class RaggedConstant(object):
  """Container of tf.ragged.constant values.

  This simple wrapper forward the arguments to delay the RaggedTensor
  construction after `@run_in_graph_and_eager_modes` has been called.
  This is required to avoid incompabilities between Graph/eager.
  """

  def __init__(self, *args, **kwargs):
    self._args = args
    self._kwargs = dict(kwargs)

  def build(self):
    return tf.ragged.constant(*self._args, **self._kwargs)


class FeatureExpectationsTestCase(SubTestCase):
  """Tests FeatureExpectations with full encode-decode."""

  @run_in_graph_and_eager_modes()
  def assertFeature(self, feature, shape, dtype, tests, serialized_info=None):
    """Test the given feature against the predicates."""

    # Check the shape/dtype
    with self._subTest("shape"):
      self.assertEqual(feature.shape, shape)
    with self._subTest("dtype"):
      self.assertEqual(feature.dtype, dtype)

    # Check the serialized features
    if serialized_info is not None:
      with self._subTest("serialized_info"):
        self.assertEqual(
            serialized_info,
            feature.get_serialized_info(),
        )

    # Create the feature dict
    fdict = features.FeaturesDict({"inner": feature})
    fdict._set_top_level()  # pylint: disable=protected-access

    for i, test in enumerate(tests):
      with self._subTest(str(i)):
        self.assertFeatureTest(
            fdict=fdict,
            test=test,
            feature=feature,
            shape=shape,
            dtype=dtype,
        )

  def assertFeatureTest(self, fdict, test, feature, shape, dtype):
    """Test that encode=>decoding of a value works correctly."""
    # test feature.encode_example can be pickled and unpickled for beam.
    dill.loads(dill.dumps(feature.encode_example))

    input_value = {"inner": test.value}

    if test.raise_cls is not None:
      with self._subTest("raise"):
        if not test.raise_msg:
          raise ValueError(
              "test.raise_msg should be set with {} for test {}".format(
                  test.raise_cls, type(feature)))
        with self.assertRaisesWithPredicateMatch(
            test.raise_cls, test.raise_msg):
          features_encode_decode(fdict, input_value, decoders=test.decoders)
    else:
      # Test the serialization only
      if test.expected_serialized is not None:
        with self._subTest("out_serialize"):
          self.assertEqual(
              test.expected_serialized,
              feature.encode_example(test.value),
          )

      # Test serialization + decoding from disk
      with self._subTest("out"):
        out_tensor, out_numpy = features_encode_decode(
            fdict,
            input_value,
            decoders={"inner": test.decoders},
        )
        out_tensor = out_tensor["inner"]
        out_numpy = out_numpy["inner"]

        # Assert the returned type match the expected one
        with self._subTest("dtype"):
          out_dtypes = utils.map_nested(lambda s: s.dtype, out_tensor)
          self.assertEqual(out_dtypes, test.dtype or feature.dtype)
        with self._subTest("shape"):
          # For shape, because (None, 3) match with (5, 3), we use
          # tf.TensorShape.assert_is_compatible_with on each of the elements
          expected_shape = feature.shape if test.shape is None else test.shape
          out_shapes = utils.zip_nested(out_tensor, expected_shape)
          utils.map_nested(
              lambda x: x[0].shape.assert_is_compatible_with(x[1]),
              out_shapes
          )

        # Assert value
        with self._subTest("out_value"):
          # Eventually construct the tf.RaggedTensor
          expected = utils.map_nested(
              lambda t: t.build() if isinstance(t, RaggedConstant) else t,
              test.expected)
          self.assertAllEqualNested(out_numpy, expected)


def features_encode_decode(features_dict, example, decoders):
  """Runs the full pipeline: encode > write > tmp files > read > decode."""
  # Encode example
  encoded_example = features_dict.encode_example(example)

  with tmp_dir() as tmp_dir_:
    tmp_filename = os.path.join(tmp_dir_, "tmp.tfrecord")

    # Read/write the file
    file_adapter = file_format_adapter.TFRecordExampleAdapter(
        features_dict.get_serialized_info())
    file_adapter.write_from_generator(
        generator=[encoded_example],
        output_files=[tmp_filename],
    )
    ds = file_adapter.dataset_from_filename(tmp_filename)

    # Decode the example
    decode_fn = functools.partial(
        features_dict.decode_example,
        decoders=decoders,
    )
    ds = ds.map(decode_fn)

    if tf.executing_eagerly():
      out_tensor = next(iter(ds))
    else:
      out_tensor = tf.compat.v1.data.make_one_shot_iterator(ds).get_next()
    out_numpy = dataset_utils.as_numpy(out_tensor)
    return out_tensor, out_numpy


class DummyDatasetSharedGenerator(builder.GeneratorBasedBuilder):
  """Test DatasetBuilder."""

  VERSION = utils.Version("1.0.0")
  SUPPORTED_VERSIONS = [
      "2.0.0",
      "0.0.9",
      "0.0.8",
      utils.Version("0.0.7", tfds_version_to_prepare="v1.0.0"),
  ]

  def _info(self):
    return dataset_info.DatasetInfo(
        builder=self,
        features=features.FeaturesDict({"x": tf.int64}),
        supervised_keys=("x", "x"),
    )

  def _split_generators(self, dl_manager):
    # Split the 30 examples from the generator into 2 train shards and 1 test
    # shard.
    del dl_manager
    return [
        splits.SplitGenerator(
            name=splits.Split.TRAIN,
            gen_kwargs={"range_": range(20)}),
        splits.SplitGenerator(
            name=splits.Split.TEST,
            gen_kwargs={"range_": range(20, 30)}),
    ]

  def _generate_examples(self, range_):
    for i in range_:
      yield i, {"x": i}


class DummyMnist(builder.GeneratorBasedBuilder):
  """Test DatasetBuilder."""

  VERSION = utils.Version("1.0.0")

  def _info(self):
    return dataset_info.DatasetInfo(
        builder=self,
        features=features.FeaturesDict({
            "image": features.Image(shape=(28, 28, 1)),
            "label": features.ClassLabel(num_classes=10),
        }),
        description="Mnist description.",
    )

  def _split_generators(self, dl_manager):
    return [
        splits.SplitGenerator(
            name=splits.Split.TRAIN,
            gen_kwargs=dict()),
        splits.SplitGenerator(
            name=splits.Split.TEST,
            gen_kwargs=dict()),
    ]

  def _generate_examples(self):
    for i in range(20):
      yield i, {
          "image": np.ones((28, 28, 1), dtype=np.uint8),
          "label": i % 10,
      }


def test_main():
  """Entrypoint for tests."""
  tf.enable_v2_behavior()
  tf.test.main()


@contextlib.contextmanager
def mock_kaggle_api(filenames=None, err_msg=None):
  """Mock out the kaggle CLI.

  Args:
    filenames: `list<str>`, names of the competition files.
    err_msg: `str`, if provided, the kaggle CLI will raise a CalledProcessError
      and this will be the command output.

  Yields:
    None, context will have kaggle CLI mocked out.
  """

  def make_mock_files_call(filenames, err_msg):
    """Mock subprocess.check_output for files call."""

    def check_output(command_args):
      assert command_args[2] == "files"
      if err_msg:
        raise subprocess.CalledProcessError(1, command_args,
                                            tf.compat.as_bytes(err_msg))
      return tf.compat.as_bytes(
          "\n".join(["name,size,creationDate"] +
                    ["%s,34MB,None\n" % fname for fname in filenames]))

    return check_output

  def make_mock_download_call():
    """Mock subprocess.check_output for download call."""

    def check_output(command_args):
      assert command_args[2] == "download"
      fname = command_args[command_args.index("--file") + 1]
      out_dir = command_args[command_args.index("--path") + 1]
      fpath = os.path.join(out_dir, fname)
      with tf.io.gfile.GFile(fpath, "w") as f:
        f.write(fname)
      return tf.compat.as_bytes("Downloading %s to %s" % (fname, fpath))

    return check_output

  def make_mock_check_output(filenames, err_msg):
    """Mock subprocess.check_output for both calls."""

    files_call = make_mock_files_call(filenames, err_msg)
    dl_call = make_mock_download_call()

    def check_output(command_args):
      if command_args[2] == "files":
        return files_call(command_args)
      else:
        assert command_args[2] == "download"
        return dl_call(command_args)

    return check_output

  with absltest.mock.patch("subprocess.check_output",
                           make_mock_check_output(filenames, err_msg)):
    yield


class DummySerializer(object):
  """To mock example_serializer.ExampleSerializer."""

  def __init__(self, specs):
    del specs

  def serialize_example(self, example):
    return bytes(example)


class DummyParser(object):
  """To mock example_parser.ExampleParser."""

  def __init__(self, specs):
    del specs

  def parse_example(self, ex):
    return ex

