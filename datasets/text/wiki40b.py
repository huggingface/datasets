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

"""Wiki40B: A clean Wikipedia dataset for 40+ languages."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import logging
import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """
"""

_DESCRIPTION = """
Clean-up text for 40+ Wikipedia languages editions of pages
correspond to entities. The datasets have train/dev/test splits per language.
The dataset is cleaned up by page filtering to remove disambiguation pages,
redirect pages, deleted pages, and non-entity pages. Each example contains the
wikidata id of the entity, and the full Wikipedia article after page processing
that removes non-content sections and structured objects.
"""

_LICENSE = """
This work is licensed under the Creative Commons Attribution-ShareAlike
3.0 Unported License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

_URL = "https://www.tensorflow.org/datasets/catalog/wiki40b"

_DATA_DIRECTORY = "/bigstore/tfds-data/downloads/wiki40b/tfrecord_prod"

WIKIPEDIA_LANGUAGES = [
    "en", "ar", "zh-cn", "zh-tw", "nl", "fr", "de", "it", "ja", "ko", "pl",
    "pt", "ru", "es", "th", "tr", "bg", "ca", "cs", "da", "el", "et", "fa",
    "fi", "he", "hi", "hr", "hu", "id", "lt", "lv", "ms", "no", "ro", "sk",
    "sl", "sr", "sv", "tl", "uk", "vi"]


class Wiki40bConfig(tfds.core.BuilderConfig):
  """BuilderConfig for Wiki40B."""

  @tfds.core.disallow_positional_args
  def __init__(self, language=None, **kwargs):
    """BuilderConfig for Wiki40B.

    Args:
      language: string, the language code for the Wiki40B dataset to use.
      **kwargs: keyword arguments forwarded to super.
    """
    super(Wiki40bConfig, self).__init__(
        name="Wiki40B.{0}".format(language),
        description="Wiki40B dataset for {0}.".format(language),
        **kwargs)
    self.language = language


_VERSION = tfds.core.Version("1.0.0")


class Wiki40b(tfds.core.BeamBasedBuilder):
  """Wiki40B: A Clean Wikipedia Dataset for Mutlilingual Language Modeling."""

  BUILDER_CONFIGS = [
      Wiki40bConfig(  # pylint:disable=g-complex-comprehension
          version=_VERSION,
          language=lang,
      ) for lang in WIKIPEDIA_LANGUAGES
  ]

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            "wikidata_id":
                tfds.features.Text(),
            "text":
                tfds.features.Text(),
        }),
        supervised_keys=None,
        homepage=_URL,
        citation=_CITATION,
        redistribution_info={"license": _LICENSE},
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""

    del dl_manager  # Unused

    lang = self._builder_config.language

    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={
                "filepaths": "%s/train/%s_examples-*" % (_DATA_DIRECTORY,
                                                         lang)},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={"filepaths": "%s/dev/%s_examples-*" % (_DATA_DIRECTORY,
                                                               lang)},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={"filepaths": "%s/test/%s_examples-*" % (_DATA_DIRECTORY,
                                                                lang)},
        ),
    ]

  def _build_pcollection(self, pipeline, filepaths):
    """Build PCollection of examples."""
    beam = tfds.core.lazy_imports.apache_beam
    logging.info("generating examples from = %s", filepaths)

    def _extract_content(example):
      """Extracts content from a TFExample."""
      wikidata_id = example.features.feature[
          "wikidata_id"].bytes_list.value[0].decode("utf-8")
      text = example.features.feature[
          "text"].bytes_list.value[0].decode("utf-8")

      yield wikidata_id, {"wikidata_id": wikidata_id,
                          "text": text,}

    return (
        pipeline
        | beam.io.ReadFromTFRecord(
            filepaths, coder=beam.coders.ProtoCoder(tf.train.Example))
        | beam.FlatMap(_extract_content))
