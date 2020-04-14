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
"""Tests for tensorflow_datasets.core.dataset_info."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import tempfile
import numpy as np
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core import dataset_info
from tensorflow_datasets.core import features
from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.image import mnist

tf.enable_v2_behavior()

_TFDS_DIR = py_utils.tfds_dir()
_INFO_DIR = os.path.join(_TFDS_DIR, "testing", "test_data", "dataset_info",
                         "mnist", "3.0.1")
_INFO_DIR_UNLABELED = os.path.join(_TFDS_DIR, "testing", "test_data",
                                   "dataset_info", "mnist_unlabeled", "3.0.1")
_NON_EXISTENT_DIR = os.path.join(_TFDS_DIR, "non_existent_dir")


DummyDatasetSharedGenerator = testing.DummyDatasetSharedGenerator


class RandomShapedImageGenerator(DummyDatasetSharedGenerator):

  def _info(self):
    return dataset_info.DatasetInfo(
        builder=self,
        features=features.FeaturesDict({"im": features.Image()}),
        supervised_keys=("im", "im"),
        metadata=dataset_info.MetadataDict(),
    )

  def _generate_examples(self, range_):
    self.info.metadata["some_key"] = 123

    for i in range_:
      height = np.random.randint(5, high=10)
      width = np.random.randint(5, high=10)
      yield i, {
          "im":
              np.random.randint(
                  0, 255, size=(height, width, 3), dtype=np.uint8)
      }


class DatasetInfoTest(testing.TestCase):

  @classmethod
  def setUpClass(cls):
    super(DatasetInfoTest, cls).setUpClass()
    cls._tfds_tmp_dir = testing.make_tmp_dir()
    cls._builder = DummyDatasetSharedGenerator(data_dir=cls._tfds_tmp_dir)

  @classmethod
  def tearDownClass(cls):
    super(DatasetInfoTest, cls).tearDownClass()
    testing.rm_tmp_dir(cls._tfds_tmp_dir)

  def test_undefined_dir(self):
    with self.assertRaisesWithPredicateMatch(ValueError,
                                             "undefined dataset_info_dir"):
      info = dataset_info.DatasetInfo(builder=self._builder)
      info.read_from_directory(None)

  def test_non_existent_dir(self):
    info = dataset_info.DatasetInfo(builder=self._builder)
    with self.assertRaisesWithPredicateMatch(
        tf.errors.NotFoundError, "No such file or dir"):
      info.read_from_directory(_NON_EXISTENT_DIR)

  def test_reading(self):
    info = dataset_info.DatasetInfo(builder=self._builder)
    info.read_from_directory(_INFO_DIR)

    # Assert that we read the file and initialized DatasetInfo.
    self.assertTrue(info.initialized)
    self.assertEqual("dummy_dataset_shared_generator", info.name)
    self.assertEqual("dummy_dataset_shared_generator/1.0.0", info.full_name)

    # Test splits are initialized properly.
    split_dict = info.splits

    # Assert they are the correct number.
    self.assertTrue(len(split_dict), 2)

    # Assert on what they are
    self.assertIn("train", split_dict)
    self.assertIn("test", split_dict)

    # Assert that this is computed correctly.
    self.assertEqual(40, info.splits.total_num_examples)
    self.assertEqual(11594722, info.dataset_size)

    self.assertEqual("image", info.supervised_keys[0])
    self.assertEqual("label", info.supervised_keys[1])

  def test_reading_empty_properties(self):
    info = dataset_info.DatasetInfo(builder=self._builder)
    info.read_from_directory(_INFO_DIR_UNLABELED)

    # Assert supervised_keys has not been set
    self.assertEqual(None, info.supervised_keys)

  def test_writing(self):
    # First read in stuff.
    mnist_builder = mnist.MNIST(
        data_dir=tempfile.mkdtemp(dir=self.get_temp_dir()))

    info = dataset_info.DatasetInfo(
        builder=mnist_builder, features=mnist_builder.info.features)
    info.read_from_directory(_INFO_DIR)

    # Read the json file into a string.
    with tf.io.gfile.GFile(info._dataset_info_path(_INFO_DIR)) as f:
      existing_json = json.load(f)

    # Now write to a temp directory.
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      info.write_to_directory(tmp_dir)

      # Read the newly written json file into a string.
      with tf.io.gfile.GFile(info._dataset_info_path(tmp_dir)) as f:
        new_json = json.load(f)

      # Read the newly written LICENSE file into a string.
      with tf.io.gfile.GFile(info._license_path(tmp_dir)) as f:
        license_ = f.read()

    # Assert what was read and then written and read again is the same.
    self.assertEqual(existing_json, new_json)

    # Assert correct license was written.
    self.assertEqual(existing_json["redistributionInfo"]["license"], license_)

    self.assertEqual(repr(info), INFO_STR)

  def test_restore_after_modification(self):
    # Create a DatasetInfo
    info = dataset_info.DatasetInfo(
        builder=self._builder,
        description="A description",
        supervised_keys=("input", "output"),
        homepage="http://some-location",
        citation="some citation",
        redistribution_info={"license": "some license"}
    )
    info.download_size = 456
    info.as_proto.splits.add(name="train", num_bytes=512)
    info.as_proto.splits.add(name="validation", num_bytes=64)
    info.as_proto.schema.feature.add()
    info.as_proto.schema.feature.add()  # Add dynamic statistics
    info.download_checksums = {
        "url1": "some checksum",
        "url2": "some other checksum",
    }

    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      # Save it
      info.write_to_directory(tmp_dir)

      # If fields are not defined, then everything is restored from disk
      restored_info = dataset_info.DatasetInfo(builder=self._builder)
      restored_info.read_from_directory(tmp_dir)
      self.assertEqual(info.as_proto, restored_info.as_proto)

    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      # Save it
      info.write_to_directory(tmp_dir)

      # If fields are defined, then the code version is kept
      restored_info = dataset_info.DatasetInfo(
          builder=self._builder,
          supervised_keys=("input (new)", "output (new)"),
          homepage="http://some-location-new",
          citation="some citation (new)",
          redistribution_info={"license": "some license (new)"}
      )
      restored_info.download_size = 789
      restored_info.as_proto.splits.add(name="validation", num_bytes=288)
      restored_info.as_proto.schema.feature.add()
      restored_info.as_proto.schema.feature.add()
      restored_info.as_proto.schema.feature.add()
      restored_info.as_proto.schema.feature.add()  # Add dynamic statistics
      restored_info.download_checksums = {
          "url2": "some other checksum (new)",
          "url3": "some checksum (new)",
      }

      restored_info.read_from_directory(tmp_dir)

      # Even though restored_info has been restored, informations defined in
      # the code overwrite informations from the json file.
      self.assertEqual(restored_info.description, "A description")
      self.assertEqual(
          restored_info.supervised_keys, ("input (new)", "output (new)"))
      self.assertEqual(restored_info.homepage, "http://some-location-new")
      self.assertEqual(restored_info.citation, "some citation (new)")
      self.assertEqual(restored_info.redistribution_info.license,
                       "some license (new)")
      self.assertEqual(restored_info.download_size, 789)
      self.assertEqual(restored_info.dataset_size, 576)
      self.assertEqual(len(restored_info.as_proto.schema.feature), 4)
      self.assertEqual(restored_info.download_checksums, {
          "url2": "some other checksum (new)",
          "url3": "some checksum (new)",
      })

  def test_reading_from_gcs_bucket(self):
    # The base TestCase prevents GCS access, so we explicitly ask it to restore
    # access here.
    with self.gcs_access():
      mnist_builder = mnist.MNIST(
          data_dir=tempfile.mkdtemp(dir=self.get_temp_dir()))
      info = dataset_info.DatasetInfo(builder=mnist_builder)
      info = mnist_builder.info

      # A nominal check to see if we read it.
      self.assertTrue(info.initialized)
      self.assertEqual(10000, info.splits["test"].num_examples)

  def test_str_smoke(self):
    info = mnist.MNIST(data_dir="/tmp/some_dummy_dir").info
    _ = str(info)

  @testing.run_in_graph_and_eager_modes()
  def test_statistics_generation(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = DummyDatasetSharedGenerator(data_dir=tmp_dir)
      builder.download_and_prepare()

      # Overall
      self.assertEqual(30, builder.info.splits.total_num_examples)

      # Per split.
      test_split = builder.info.splits["test"].get_proto()
      train_split = builder.info.splits["train"].get_proto()
      self.assertEqual(10, test_split.statistics.num_examples)
      self.assertEqual(20, train_split.statistics.num_examples)

  @testing.run_in_graph_and_eager_modes()
  def test_statistics_generation_variable_sizes(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = RandomShapedImageGenerator(data_dir=tmp_dir)
      builder.download_and_prepare()

      # Get the expected type of the feature.
      schema_feature = builder.info.as_proto.schema.feature[0]
      self.assertEqual("im", schema_feature.name)

      self.assertEqual(-1, schema_feature.shape.dim[0].size)
      self.assertEqual(-1, schema_feature.shape.dim[1].size)
      self.assertEqual(3, schema_feature.shape.dim[2].size)

  def test_metadata(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = RandomShapedImageGenerator(data_dir=tmp_dir)
      builder.download_and_prepare()
      # Metadata should have been created
      self.assertEqual(builder.info.metadata, {"some_key": 123})

      # Metadata should have been restored
      builder2 = RandomShapedImageGenerator(data_dir=tmp_dir)
      self.assertEqual(builder2.info.metadata, {"some_key": 123})

  def test_updates_on_bucket_info(self):

    info = dataset_info.DatasetInfo(builder=self._builder,
                                    description="won't be updated")
    # No statistics in the above.
    self.assertEqual(0, info.splits.total_num_examples)
    self.assertEqual(0, len(info.as_proto.schema.feature))

    # Partial update will happen here.
    info.read_from_directory(_INFO_DIR)

    # Assert that description (things specified in the code) didn't change
    # but statistics are updated.
    self.assertEqual("won't be updated", info.description)

    # These are dynamically computed, so will be updated.
    self.assertEqual(40, info.splits.total_num_examples)
    self.assertEqual(2, len(info.as_proto.schema.feature))


INFO_STR = """tfds.core.DatasetInfo(
    name='mnist',
    version=3.0.1,
    description='The MNIST database of handwritten digits.',
    homepage='https://storage.googleapis.com/cvdf-datasets/mnist/',
    features=FeaturesDict({
        'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
    }),
    total_num_examples=40,
    splits={
        'test': 20,
        'train': 20,
    },
    supervised_keys=('image', 'label'),
    citation=\"\"\"@article{lecun2010mnist,
      title={MNIST handwritten digit database},
      author={LeCun, Yann and Cortes, Corinna and Burges, CJ},
      journal={ATT Labs [Online]. Available: http://yann. lecun. com/exdb/mnist},
      volume={2},
      year={2010}
    }\"\"\",
    redistribution_info=license: "test license",
)
"""


if __name__ == "__main__":
  testing.test_main()
