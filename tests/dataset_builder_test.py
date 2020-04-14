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
"""Tests for tensorflow_datasets.core.builder."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from absl.testing import absltest
import dill
import numpy as np
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core import builder
from tensorflow_datasets.core import dataset_info
from tensorflow_datasets.core import dataset_utils
from tensorflow_datasets.core import download
from tensorflow_datasets.core import features
from tensorflow_datasets.core import registered
from tensorflow_datasets.core import splits as splits_lib
from tensorflow_datasets.core import utils
from tensorflow_datasets.core.utils import read_config as read_config_lib

tf.enable_v2_behavior()

DummyDatasetSharedGenerator = testing.DummyDatasetSharedGenerator


class DummyBuilderConfig(builder.BuilderConfig):

  def __init__(self, increment=0, **kwargs):
    super(DummyBuilderConfig, self).__init__(**kwargs)
    self.increment = increment


class DummyDatasetWithConfigs(builder.GeneratorBasedBuilder):

  BUILDER_CONFIGS = [
      DummyBuilderConfig(
          name="plus1",
          version=utils.Version("0.0.1"),
          description="Add 1 to the records",
          increment=1),
      DummyBuilderConfig(
          name="plus2",
          version=utils.Version("0.0.2"),
          supported_versions=[utils.Version("0.0.1")],
          description="Add 2 to the records",
          increment=2),
  ]

  def _split_generators(self, dl_manager):
    del dl_manager
    return [
        splits_lib.SplitGenerator(
            name=splits_lib.Split.TRAIN,
            gen_kwargs={"range_": range(20)},
        ),
        splits_lib.SplitGenerator(
            name=splits_lib.Split.TEST,
            gen_kwargs={"range_": range(20, 30)},
        ),
    ]

  def _info(self):

    return dataset_info.DatasetInfo(
        builder=self,
        features=features.FeaturesDict({"x": tf.int64}),
        supervised_keys=("x", "x"),
    )

  def _generate_examples(self, range_):
    for i in range_:
      x = i
      if self.builder_config:
        x += self.builder_config.increment
      yield i, {"x": x}


class InvalidSplitDataset(DummyDatasetWithConfigs):

  def _split_generators(self, _):
    return [
        splits_lib.SplitGenerator(
            name="all",  # Error: ALL cannot be used as Split key
        )
    ]


class DatasetBuilderTest(testing.TestCase):

  @testing.run_in_graph_and_eager_modes()
  def test_load(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      dataset = registered.load(
          name="dummy_dataset_shared_generator",
          data_dir=tmp_dir,
          download=True,
          split=splits_lib.Split.TRAIN)
      data = list(dataset_utils.as_numpy(dataset))
      self.assertEqual(20, len(data))
      self.assertLess(data[0]["x"], 30)

  @testing.run_in_graph_and_eager_modes()
  def test_determinism(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      ds = registered.load(
          name="dummy_dataset_shared_generator",
          data_dir=tmp_dir,
          split=splits_lib.Split.TRAIN,
          shuffle_files=False)
      ds_values = list(dataset_utils.as_numpy(ds))

      # Ensure determinism. If this test fail, this mean that numpy random
      # module isn't always determinist (maybe between version, architecture,
      # ...), and so our datasets aren't guaranteed either.
      l = list(range(20))
      np.random.RandomState(42).shuffle(l)
      self.assertEqual(l, [
          0, 17, 15, 1, 8, 5, 11, 3, 18, 16, 13, 2, 9, 19, 4, 12, 7, 10, 14, 6
      ])

      # Ensure determinism. If this test fails, this mean the dataset are not
      # deterministically generated.
      self.assertEqual(
          [e["x"] for e in ds_values],
          [6, 16, 19, 12, 14, 18, 5, 13, 15, 4, 10, 17, 0, 8, 3, 1, 9, 7, 11,
           2],
      )

  @testing.run_in_graph_and_eager_modes()
  def test_load_from_gcs(self):
    from tensorflow_datasets.image import mnist  # pylint:disable=g-import-not-at-top
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      with absltest.mock.patch.object(
          mnist.MNIST, "_download_and_prepare",
          side_effect=NotImplementedError):
        # Make sure the dataset cannot be generated.
        with self.assertRaises(NotImplementedError):
          registered.load(
              name="mnist",
              data_dir=tmp_dir)
        # Enable GCS access so that dataset will be loaded from GCS.
        with self.gcs_access():
          _, info = registered.load(
              name="mnist",
              data_dir=tmp_dir,
              with_info=True)
      self.assertSetEqual(
          set(["dataset_info.json",
               "image.image.json",
               "mnist-test.tfrecord-00000-of-00001",
               "mnist-train.tfrecord-00000-of-00001",
              ]),
          set(tf.io.gfile.listdir(os.path.join(tmp_dir, "mnist/3.0.1"))))

      self.assertEqual(set(info.splits.keys()), set(["train", "test"]))

  @testing.run_in_graph_and_eager_modes()
  def test_multi_split(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      ds_train, ds_test = registered.load(
          name="dummy_dataset_shared_generator",
          data_dir=tmp_dir,
          split=["train", "test"],
          shuffle_files=False)

      data = list(dataset_utils.as_numpy(ds_train))
      self.assertEqual(20, len(data))

      data = list(dataset_utils.as_numpy(ds_test))
      self.assertEqual(10, len(data))

  def test_build_data_dir(self):
    # Test that the dataset loads the data_dir for the builder's version
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = DummyDatasetSharedGenerator(data_dir=tmp_dir)
      self.assertEqual(str(builder.info.version), "1.0.0")
      builder_data_dir = os.path.join(tmp_dir, builder.name)
      version_dir = os.path.join(builder_data_dir, "1.0.0")

      # The dataset folder contains multiple other versions
      tf.io.gfile.makedirs(os.path.join(builder_data_dir, "14.0.0.invalid"))
      tf.io.gfile.makedirs(os.path.join(builder_data_dir, "10.0.0"))
      tf.io.gfile.makedirs(os.path.join(builder_data_dir, "9.0.0"))
      tf.io.gfile.makedirs(os.path.join(builder_data_dir, "0.1.0"))

      # The builder's version dir is chosen
      self.assertEqual(builder._build_data_dir(), version_dir)

  def test_get_data_dir_with_config(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      config_name = "plus1"
      builder = DummyDatasetWithConfigs(config=config_name, data_dir=tmp_dir)

      builder_data_dir = os.path.join(tmp_dir, builder.name, config_name)
      version_data_dir = os.path.join(builder_data_dir, "0.0.1")

      tf.io.gfile.makedirs(version_data_dir)
      self.assertEqual(builder._build_data_dir(), version_data_dir)

  def test_config_construction(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      self.assertSetEqual(
          set(["plus1", "plus2"]),
          set(DummyDatasetWithConfigs.builder_configs.keys()))
      plus1_config = DummyDatasetWithConfigs.builder_configs["plus1"]
      builder = DummyDatasetWithConfigs(config="plus1", data_dir=tmp_dir)
      self.assertIs(plus1_config, builder.builder_config)
      builder = DummyDatasetWithConfigs(config=plus1_config, data_dir=tmp_dir)
      self.assertIs(plus1_config, builder.builder_config)
      self.assertIs(builder.builder_config,
                    DummyDatasetWithConfigs.BUILDER_CONFIGS[0])

  @testing.run_in_graph_and_eager_modes()
  def test_with_configs(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder1 = DummyDatasetWithConfigs(config="plus1", data_dir=tmp_dir)
      builder2 = DummyDatasetWithConfigs(config="plus2", data_dir=tmp_dir)
      # Test that builder.builder_config is the correct config
      self.assertIs(builder1.builder_config,
                    DummyDatasetWithConfigs.builder_configs["plus1"])
      self.assertIs(builder2.builder_config,
                    DummyDatasetWithConfigs.builder_configs["plus2"])
      builder1.download_and_prepare()
      builder2.download_and_prepare()
      data_dir1 = os.path.join(tmp_dir, builder1.name, "plus1", "0.0.1")
      data_dir2 = os.path.join(tmp_dir, builder2.name, "plus2", "0.0.2")
      # Test that subdirectories were created per config
      self.assertTrue(tf.io.gfile.exists(data_dir1))
      self.assertTrue(tf.io.gfile.exists(data_dir2))
      # 1 train shard, 1 test shard, plus metadata files
      self.assertGreater(len(tf.io.gfile.listdir(data_dir1)), 2)
      self.assertGreater(len(tf.io.gfile.listdir(data_dir2)), 2)

      # Test that the config was used and they didn't collide.
      splits_list = ["train", "test"]
      for builder, incr in [(builder1, 1), (builder2, 2)]:
        train_data, test_data = [   # pylint: disable=g-complex-comprehension
            [el["x"] for el in   # pylint: disable=g-complex-comprehension
             dataset_utils.as_numpy(builder.as_dataset(split=split))]
            for split in splits_list
        ]

        self.assertEqual(20, len(train_data))
        self.assertEqual(10, len(test_data))
        self.assertCountEqual(
            [incr + el for el in range(30)],
            train_data + test_data
        )

  def test_read_config(self):
    is_called = []
    def interleave_sort(lists):
      is_called.append(True)
      return lists

    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      read_config = read_config_lib.ReadConfig(
          experimental_interleave_sort_fn=interleave_sort,
      )
      read_config.options.experimental_stats.prefix = "tfds_prefix"
      ds = registered.load(
          name="dummy_dataset_shared_generator",
          data_dir=tmp_dir,
          split="train",
          read_config=read_config,
          shuffle_files=True,
      )

      # Check that the ReadConfig options are properly set
      self.assertEqual(ds.options().experimental_stats.prefix, "tfds_prefix")

      # The instruction function should have been called
      self.assertEqual(is_called, [True])

  def test_with_supported_version(self):
    DummyDatasetWithConfigs(config="plus1", version="0.0.1")

  def test_latest_experimental_version(self):
    builder1 = DummyDatasetSharedGenerator()
    self.assertEqual(str(builder1._version), "1.0.0")
    builder2 = DummyDatasetSharedGenerator(version="experimental_latest")
    self.assertEqual(str(builder2._version), "2.0.0")

  def test_with_unsupported_version(self):
    expected = "Dataset dummy_dataset_with_configs cannot be loaded at version"
    with self.assertRaisesWithPredicateMatch(AssertionError, expected):
      DummyDatasetWithConfigs(config="plus1", version="0.0.2")
    with self.assertRaisesWithPredicateMatch(AssertionError, expected):
      DummyDatasetWithConfigs(config="plus1", version="0.1.*")

  def test_previous_supported_version(self):
    default_builder = DummyDatasetSharedGenerator()
    self.assertEqual(str(default_builder.info.version), "1.0.0")
    older_builder = DummyDatasetSharedGenerator(version="0.0.*")
    self.assertEqual(str(older_builder.info.version), "0.0.9")

  def test_non_preparable_version(self, *unused_mocks):
    expected = (
        "The version of the dataset you are trying to use ("
        "dummy_dataset_shared_generator:0.0.7) can only be generated using TFDS"
        " code synced @ v1.0.0 or earlier. Either sync to that version of TFDS "
        "to first prepare the data or use another version of the dataset "
        "(available for `download_and_prepare`: 1.0.0, 2.0.0, 0.0.9, 0.0.8).")
    builder = DummyDatasetSharedGenerator(version="0.0.7")
    self.assertIsNotNone(builder)
    with self.assertRaisesWithPredicateMatch(AssertionError, expected):
      builder.download_and_prepare()

  def test_invalid_split_dataset(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      with self.assertRaisesWithPredicateMatch(
          ValueError, "`all` is a special"):
        # Raise error during .download_and_prepare()
        registered.load(
            name="invalid_split_dataset",
            data_dir=tmp_dir,
        )


class BuilderPickleTest(testing.TestCase):

  def test_load_dump(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = testing.DummyMnist(data_dir=tmp_dir)
    builder2 = dill.loads(dill.dumps(builder))
    self.assertEqual(builder.name, builder2.name)
    self.assertEqual(builder.version, builder2.version)


class BuilderRestoreGcsTest(testing.TestCase):

  def setUp(self):
    super(BuilderRestoreGcsTest, self).setUp()

    def load_mnist_dataset_info(self):
      mnist_info_path = os.path.join(
          utils.tfds_dir(),
          "testing/test_data/dataset_info/mnist/3.0.1",
      )
      mnist_info_path = os.path.normpath(mnist_info_path)
      self.read_from_directory(mnist_info_path)

    patcher = absltest.mock.patch.object(
        dataset_info.DatasetInfo,
        "initialize_from_bucket",
        new=load_mnist_dataset_info
    )
    patcher.start()
    self.patch_gcs = patcher
    self.addCleanup(patcher.stop)

    patcher = absltest.mock.patch.object(
        dataset_info.DatasetInfo, "compute_dynamic_properties",
    )
    self.compute_dynamic_property = patcher.start()
    self.addCleanup(patcher.stop)

  def test_stats_restored_from_gcs(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = testing.DummyMnist(data_dir=tmp_dir)
      self.assertEqual(builder.info.splits["train"].statistics.num_examples, 20)
      self.assertFalse(self.compute_dynamic_property.called)

      builder.download_and_prepare()

      # Statistics shouldn't have been recomputed
      self.assertEqual(builder.info.splits["train"].statistics.num_examples, 20)
      self.assertFalse(self.compute_dynamic_property.called)

  def test_stats_not_restored_gcs_overwritten(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      # If split are different that the one restored, stats should be recomputed
      builder = testing.DummyMnist(data_dir=tmp_dir)
      self.assertEqual(builder.info.splits["train"].statistics.num_examples, 20)
      self.assertFalse(self.compute_dynamic_property.called)

      dl_config = download.DownloadConfig(max_examples_per_split=5)
      builder.download_and_prepare(download_config=dl_config)

      # Statistics should have been recomputed (split different from the
      # restored ones)
      self.assertTrue(self.compute_dynamic_property.called)

  def test_gcs_not_exists(self):
    # By disabling the patch, and because DummyMnist is not on GCS, we can
    # simulate a new dataset starting from scratch
    self.patch_gcs.stop()
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = testing.DummyMnist(data_dir=tmp_dir)
      # No dataset_info restored, so stats are empty
      self.assertEqual(builder.info.splits.total_num_examples, 0)
      self.assertFalse(self.compute_dynamic_property.called)

      builder.download_and_prepare()

      # Statistics should have been recomputed
      self.assertTrue(self.compute_dynamic_property.called)
    self.patch_gcs.start()

  def test_skip_stats(self):
    # Test when stats do not exists yet and compute_stats='skip'

    # By disabling the patch, and because DummyMnist is not on GCS, we can
    # simulate a new dataset starting from scratch
    self.patch_gcs.stop()
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      # No dataset_info restored, so stats are empty
      builder = testing.DummyMnist(data_dir=tmp_dir)
      self.assertEqual(builder.info.splits, {})
      self.assertFalse(self.compute_dynamic_property.called)

      download_config = download.DownloadConfig(
          compute_stats=download.ComputeStatsMode.SKIP,
      )
      builder.download_and_prepare(download_config=download_config)

      # Statistics computation should have been skipped
      self.assertEqual(builder.info.splits["train"].statistics.num_examples, 0)
      self.assertFalse(self.compute_dynamic_property.called)
    self.patch_gcs.start()

  def test_force_stats(self):
    # Test when stats already exists but compute_stats='force'

    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      # No dataset_info restored, so stats are empty
      builder = testing.DummyMnist(data_dir=tmp_dir)
      self.assertEqual(builder.info.splits.total_num_examples, 40)
      self.assertFalse(self.compute_dynamic_property.called)

      download_config = download.DownloadConfig(
          compute_stats=download.ComputeStatsMode.FORCE,
      )
      builder.download_and_prepare(download_config=download_config)

      # Statistics computation should have been recomputed
      self.assertTrue(self.compute_dynamic_property.called)


class DatasetBuilderReadTest(testing.TestCase):

  @classmethod
  def setUpClass(cls):
    super(DatasetBuilderReadTest, cls).setUpClass()
    cls._tfds_tmp_dir = testing.make_tmp_dir()
    builder = DummyDatasetSharedGenerator(data_dir=cls._tfds_tmp_dir)
    builder.download_and_prepare()

  @classmethod
  def tearDownClass(cls):
    super(DatasetBuilderReadTest, cls).tearDownClass()
    testing.rm_tmp_dir(cls._tfds_tmp_dir)

  def setUp(self):
    super(DatasetBuilderReadTest, self).setUp()
    self.builder = DummyDatasetSharedGenerator(data_dir=self._tfds_tmp_dir)

  @testing.run_in_graph_and_eager_modes()
  def test_in_memory(self):
    train_data = dataset_utils.as_numpy(
        self.builder.as_dataset(split="train", in_memory=True))
    train_data = [el for el in train_data]
    self.assertEqual(20, len(train_data))

  def test_in_memory_with_device_ctx(self):
    # Smoke test to ensure that the inner as_numpy call does not fail when under
    # an explicit device context.
    # Only testing in graph mode. Eager mode would actually require job:foo to
    # exist in the cluster.
    with tf.Graph().as_default():
      # Testing it works even if a default Session is active
      with tf.compat.v1.Session() as _:
        with tf.device("/job:foo"):
          self.builder.as_dataset(split="train", in_memory=True)

  @testing.run_in_graph_and_eager_modes()
  def test_all_splits(self):
    splits = dataset_utils.as_numpy(
        self.builder.as_dataset(batch_size=-1))
    self.assertSetEqual(set(splits.keys()),
                        set([splits_lib.Split.TRAIN, splits_lib.Split.TEST]))

    # Test that enum and string both access same object
    self.assertIs(splits["train"], splits[splits_lib.Split.TRAIN])
    self.assertIs(splits["test"], splits[splits_lib.Split.TEST])

    train_data = splits[splits_lib.Split.TRAIN]["x"]
    test_data = splits[splits_lib.Split.TEST]["x"]
    self.assertEqual(20, len(train_data))
    self.assertEqual(10, len(test_data))
    self.assertEqual(sum(range(30)), int(train_data.sum() + test_data.sum()))

  @testing.run_in_graph_and_eager_modes()
  def test_with_batch_size(self):
    items = list(dataset_utils.as_numpy(self.builder.as_dataset(
        split="train+test", batch_size=10)))
    # 3 batches of 10
    self.assertEqual(3, len(items))
    x1, x2, x3 = items[0]["x"], items[1]["x"], items[2]["x"]
    self.assertEqual(10, x1.shape[0])
    self.assertEqual(10, x2.shape[0])
    self.assertEqual(10, x3.shape[0])
    self.assertEqual(sum(range(30)), int(x1.sum() + x2.sum() + x3.sum()))

    # By default batch_size is None and won't add a batch dimension
    ds = self.builder.as_dataset(split=splits_lib.Split.TRAIN)
    self.assertEqual(0, len(tf.compat.v1.data.get_output_shapes(ds)["x"]))
    # Setting batch_size=1 will add an extra batch dimension
    ds = self.builder.as_dataset(split=splits_lib.Split.TRAIN, batch_size=1)
    self.assertEqual(1, len(tf.compat.v1.data.get_output_shapes(ds)["x"]))
    # Setting batch_size=2 will add an extra batch dimension
    ds = self.builder.as_dataset(split=splits_lib.Split.TRAIN, batch_size=2)
    self.assertEqual(1, len(tf.compat.v1.data.get_output_shapes(ds)["x"]))

  @testing.run_in_graph_and_eager_modes()
  def test_supervised_keys(self):
    x, _ = dataset_utils.as_numpy(self.builder.as_dataset(
        split=splits_lib.Split.TRAIN, as_supervised=True, batch_size=-1))
    self.assertEqual(x.shape[0], 20)

  def test_is_dataset_v1(self):
    # For backward compatibility, ensure that the returned dataset object
    # has make_one_shot_iterator methods.
    with tf.Graph().as_default():
      ds = self.builder.as_dataset(split="train")
      ds.make_one_shot_iterator()
      ds.make_initializable_iterator()

  def test_autocache(self):
    # All the following should cache

    # Default should cache as dataset is small and has a single shard
    self.assertTrue(self.builder._should_cache_ds(
        split="train",
        shuffle_files=True,
        read_config=read_config_lib.ReadConfig(),
    ))

    # Multiple shards should cache when shuffling is disabled
    self.assertTrue(self.builder._should_cache_ds(
        split="train+test",
        shuffle_files=False,
        read_config=read_config_lib.ReadConfig(),
    ))

    # Multiple shards should cache when re-shuffling is disabled
    self.assertTrue(self.builder._should_cache_ds(
        split="train+test",
        shuffle_files=True,
        read_config=read_config_lib.ReadConfig(
            shuffle_reshuffle_each_iteration=False),
    ))

    # Sub-split API can cache if only a single shard is selected.
    self.assertTrue(self.builder._should_cache_ds(
        split="train+test[:0]",
        shuffle_files=True,
        read_config=read_config_lib.ReadConfig(),
    ))

    # All the following should NOT cache

    # Default should not cache if try_autocache is disabled
    self.assertFalse(self.builder._should_cache_ds(
        split="train",
        shuffle_files=True,
        read_config=read_config_lib.ReadConfig(try_autocache=False),
    ))

    # Multiple shards should not cache when shuffling is enabled
    self.assertFalse(self.builder._should_cache_ds(
        split="train+test",
        shuffle_files=True,
        read_config=read_config_lib.ReadConfig(),
    ))




class NestedSequenceBuilder(builder.GeneratorBasedBuilder):
  """Dataset containing nested sequences."""

  VERSION = utils.Version("0.0.1")

  def _info(self):
    return dataset_info.DatasetInfo(
        builder=self,
        features=features.FeaturesDict({
            "frames": features.Sequence({
                "coordinates": features.Sequence(
                    features.Tensor(shape=(2,), dtype=tf.int32)
                ),
            }),
        }),
    )

  def _split_generators(self, dl_manager):
    del dl_manager
    return [
        splits_lib.SplitGenerator(
            name=splits_lib.Split.TRAIN,
            gen_kwargs={},
        ),
    ]

  def _generate_examples(self):
    ex0 = [
        [[0, 1], [2, 3], [4, 5]],
        [],
        [[6, 7]]
    ]
    ex1 = []
    ex2 = [
        [[10, 11]],
        [[12, 13], [14, 15]],
    ]
    for i, ex in enumerate([ex0, ex1, ex2]):
      yield i, {"frames": {"coordinates": ex}}


class NestedSequenceBuilderTest(testing.TestCase):
  """Test of the NestedSequenceBuilder."""

  @testing.run_in_graph_and_eager_modes()
  def test_nested_sequence(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      ds_train, ds_info = registered.load(
          name="nested_sequence_builder",
          data_dir=tmp_dir,
          split="train",
          with_info=True,
          shuffle_files=False)
      ex0, ex1, ex2 = [
          ex["frames"]["coordinates"]
          for ex in dataset_utils.as_numpy(ds_train)
      ]
      self.assertAllEqual(ex0, tf.ragged.constant([
          [[0, 1], [2, 3], [4, 5]],
          [],
          [[6, 7]],
      ], inner_shape=(2,)))
      self.assertAllEqual(ex1, tf.ragged.constant([], ragged_rank=1))
      self.assertAllEqual(ex2, tf.ragged.constant([
          [[10, 11]],
          [[12, 13], [14, 15]],
      ], inner_shape=(2,)))

      self.assertEqual(
          ds_info.features.dtype,
          {"frames": {"coordinates": tf.int32}},
      )
      self.assertEqual(
          ds_info.features.shape,
          {"frames": {"coordinates": (None, None, 2)}},
      )
      nested_tensor_info = ds_info.features.get_tensor_info()
      self.assertEqual(
          nested_tensor_info["frames"]["coordinates"].sequence_rank,
          2,
      )


if __name__ == "__main__":
  testing.test_main()
