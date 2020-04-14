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

import apache_beam as beam
import numpy as np
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core import builder
from tensorflow_datasets.core import dataset_info
from tensorflow_datasets.core import dataset_utils
from tensorflow_datasets.core import download
from tensorflow_datasets.core import features
from tensorflow_datasets.core import splits as splits_lib
from tensorflow_datasets.core import utils


tf.enable_v2_behavior()


class DummyBeamDataset(builder.BeamBasedBuilder):

  VERSION = utils.Version("1.0.0")

  def _info(self):
    return dataset_info.DatasetInfo(
        builder=self,
        features=features.FeaturesDict({
            "image": features.Image(shape=(16, 16, 1)),
            "label": features.ClassLabel(names=["dog", "cat"]),
            "id": tf.int32,
        }),
        supervised_keys=("x", "x"),
        metadata=dataset_info.BeamMetadataDict(),
    )

  def _split_generators(self, dl_manager):
    del dl_manager
    return [
        splits_lib.SplitGenerator(
            name=splits_lib.Split.TRAIN,
            gen_kwargs=dict(num_examples=1000),
        ),
        splits_lib.SplitGenerator(
            name=splits_lib.Split.TEST,
            gen_kwargs=dict(num_examples=725),
        ),
    ]

  def _compute_metadata(self, examples, num_examples):
    self.info.metadata["label_sum_%d" % num_examples] = (
        examples
        | beam.Map(lambda x: x[1]["label"])
        | beam.CombineGlobally(sum))
    self.info.metadata["id_mean_%d" % num_examples] = (
        examples
        | beam.Map(lambda x: x[1]["id"])
        | beam.CombineGlobally(beam.combiners.MeanCombineFn()))

  def _build_pcollection(self, pipeline, num_examples):
    """Generate examples as dicts."""
    examples = (
        pipeline
        | beam.Create(range(num_examples))
        | beam.Map(_gen_example)
    )
    self._compute_metadata(examples, num_examples)
    return examples


def _gen_example(x):
  return (x, {
      "image": (np.ones((16, 16, 1)) * x % 255).astype(np.uint8),
      "label": x % 2,
      "id": x,
  })


class CommonPipelineDummyBeamDataset(DummyBeamDataset):

  def _split_generators(self, dl_manager, pipeline):
    del dl_manager

    examples = (
        pipeline
        | beam.Create(range(1000))
        | beam.Map(_gen_example)
    )

    return [
        splits_lib.SplitGenerator(
            name=splits_lib.Split.TRAIN,
            gen_kwargs=dict(examples=examples, num_examples=1000),
        ),
        splits_lib.SplitGenerator(
            name=splits_lib.Split.TEST,
            gen_kwargs=dict(examples=examples, num_examples=725),
        ),
    ]

  def _build_pcollection(self, pipeline, examples, num_examples):
    """Generate examples as dicts."""
    del pipeline
    examples |= beam.Filter(lambda x: x[0] < num_examples)
    self._compute_metadata(examples, num_examples)
    return examples


class FaultyS3DummyBeamDataset(DummyBeamDataset):

  VERSION = utils.Version("1.0.0")


class BeamBasedBuilderTest(testing.TestCase):

  def test_download_prepare_raise(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = DummyBeamDataset(data_dir=tmp_dir)
      with self.assertRaisesWithPredicateMatch(ValueError, "no Beam Runner"):
        builder.download_and_prepare()

  def _assertBeamGeneration(self, dl_config, dataset_cls, dataset_name):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = dataset_cls(data_dir=tmp_dir)
      builder.download_and_prepare(download_config=dl_config)

      data_dir = os.path.join(tmp_dir, dataset_name, "1.0.0")
      self.assertEqual(data_dir, builder._data_dir)

      # Check number of shards
      self._assertShards(
          data_dir,
          pattern="%s-test.tfrecord-{:05}-of-{:05}" % dataset_name,
          # Liquid sharding is not guaranteed to always use the same number.
          num_shards=builder.info.splits["test"].num_shards,
      )
      self._assertShards(
          data_dir,
          pattern="%s-train.tfrecord-{:05}-of-{:05}" % dataset_name,
          num_shards=1,
      )

      datasets = dataset_utils.as_numpy(builder.as_dataset())

      def get_id(ex):
        return ex["id"]

      self._assertElemsAllEqual(
          sorted(list(datasets["test"]), key=get_id),
          sorted([_gen_example(i)[1] for i in range(725)], key=get_id),
      )
      self._assertElemsAllEqual(
          sorted(list(datasets["train"]), key=get_id),
          sorted([_gen_example(i)[1] for i in range(1000)], key=get_id),
      )

      self.assertDictEqual(
          builder.info.metadata,
          {
              "label_sum_1000": 500, "id_mean_1000": 499.5,
              "label_sum_725": 362, "id_mean_725": 362.0,
          }
      )

  def _assertShards(self, data_dir, pattern, num_shards):
    self.assertTrue(num_shards)
    shards_filenames = [
        pattern.format(i, num_shards) for i in range(num_shards)
    ]
    self.assertTrue(all(
        tf.io.gfile.exists(os.path.join(data_dir, f)) for f in shards_filenames
    ))

  def _assertElemsAllEqual(self, nested_lhs, nested_rhs):
    """assertAllEqual applied to a list of nested elements."""
    for dict_lhs, dict_rhs in zip(nested_lhs, nested_rhs):
      flat_lhs = tf.nest.flatten(dict_lhs)
      flat_rhs = tf.nest.flatten(dict_rhs)
      for lhs, rhs in zip(flat_lhs, flat_rhs):
        self.assertAllEqual(lhs, rhs)


  def _get_dl_config_if_need_to_run(self):
    return download.DownloadConfig(
        beam_options=beam.options.pipeline_options.PipelineOptions(),
    )

  def test_download_prepare(self):
    dl_config = self._get_dl_config_if_need_to_run()
    if not dl_config:
      return
    self._assertBeamGeneration(
        dl_config, DummyBeamDataset, "dummy_beam_dataset")
    self._assertBeamGeneration(
        dl_config, CommonPipelineDummyBeamDataset,
        "common_pipeline_dummy_beam_dataset")


if __name__ == "__main__":
  testing.test_main()
