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
"""ParaCrawl (Bitextor) parallel open-source machine translation benchmark."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import tensorflow.compat.v2 as tf
from tensorflow_datasets.core import utils
import tensorflow_datasets.public_api as tfds

_DESCRIPTION = "Web-Scale Parallel Corpora for Official European Languages."

_BENCHMARK_URL = "https://paracrawl.eu/releases.html"

_CITATION = """\
@misc {paracrawl,
    title  = "ParaCrawl",
    year   = "2018",
    url    = "http://paracrawl.eu/download.html."
}
"""

_BASE_DATA_URL_FORMAT_STR = ("https://s3.amazonaws.com/web-language-models/"
                             "paracrawl/release4/en-{target_lang}.bicleaner07."
                             "txt.gz")


@utils.memoize()
def _target_languages():
  """Create the sorted dictionary of language codes, and language names.

  Returns:
    The sorted dictionary as an instance of `collections.OrderedDict`.
  """
  langs = {
      "bg": "Bulgarian",
      "cs": "Czech",
      "da": "Danish",
      "de": "German",
      "el": "Greek",
      "es": "Spanish",
      "et": "Estonian",
      "fi": "Finnish",
      "fr": "French",
      "ga": "Irish",
      "hr": "Croatian",
      "hu": "Hungarian",
      "it": "Italian",
      "lt": "Lithuanian",
      "lv": "Latvian",
      "mt": "Maltese",
      "nl": "Dutch",
      "pl": "Polish",
      "pt": "Portuguese",
      "ro": "Romanian",
      "sk": "Slovak",
      "sl": "Slovenian",
      "sv": "Swedish",
  }
  return collections.OrderedDict(sorted(langs.items()))


class ParaCrawlConfig(tfds.core.BuilderConfig):
  """BuilderConfig for ParaCrawl."""

  @tfds.core.disallow_positional_args
  def __init__(self, text_encoder_config=None, target_language=None, **kwargs):
    """BuilderConfig for ParaCrawl.

    Args:
      text_encoder_config: `tfds.features.text.TextEncoderConfig`, configuration
        for the `tfds.features.text.TextEncoder` used for the features feature.
      target_language: Target language that will be used to translate to from
        English which is always the source language. It has to contain 2-letter
        coded strings. For example: "se", "hu".
      **kwargs: Keyword arguments forwarded to super.
    """
    # Validate the target language.
    if target_language not in _target_languages():
      raise ValueError("Invalid target language: %s " % target_language)

    # Initialize the base class.
    encoder_name = (
        text_encoder_config.name if text_encoder_config else "plain_text")
    name = "en%s_%s" % (target_language, encoder_name)

    description = ("Translation dataset from English to %s, uses encoder %s."
                  ) % (target_language, encoder_name)
    super(ParaCrawlConfig, self).__init__(
        name=name, description=description, **kwargs)

    # Store the attributes.
    self.text_encoder_config = (
        text_encoder_config or tfds.features.text.TextEncoderConfig())
    self.target_language = target_language
    self.data_url = _BASE_DATA_URL_FORMAT_STR.format(
        target_lang=target_language)


class ParaCrawl(tfds.core.GeneratorBasedBuilder):
  """ParaCrawl machine translation dataset."""

  # Version history:
  # 1.0.0: S3 (new shuffling, sharding and slicing mechanism).
  # 0.1.0: Initial version.
  BUILDER_CONFIGS = [
      # The version below does not refer to the version of the released
      # database. It only indicates the version of the TFDS integration.
      ParaCrawlConfig(  # pylint: disable=g-complex-comprehension
          target_language=target_language,
          version=tfds.core.Version("1.0.0"),
      )
      for target_language in _target_languages()
  ]

  def _info(self):
    target_language = self.builder_config.target_language
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.Translation(
            languages=("en", target_language),
            encoder_config=self.builder_config.text_encoder_config),
        supervised_keys=("en", target_language),
        homepage=_BENCHMARK_URL,
        citation=_CITATION)

  def _vocab_text_gen(self, files, language):
    for _, ex in self._generate_examples(**files):
      yield ex[language]

  def _split_generators(self, dl_manager):
    # Download the data file.
    data_file = dl_manager.download_and_extract(
        {"data_file": self.builder_config.data_url})

    # Return the single split of the data.
    return [
        tfds.core.SplitGenerator(name=tfds.Split.TRAIN, gen_kwargs=data_file)
    ]

  def _generate_examples(self, data_file):
    """This function returns the examples in the raw (text) form."""
    target_language = self.builder_config.target_language

    with tf.io.gfile.GFile(data_file) as f:
      for idx, line in enumerate(f):
        line_parts = line.strip().split("\t")
        if len(line_parts) != 2:
          msg = ("Wrong data format in line {}. The line '{}' does "
                 "not have exactly one delimiter.").format(idx, line)
          raise ValueError(msg)
        source, target = line_parts[0].strip(), line_parts[1].strip()
        yield idx, {"en": source, target_language: target}
