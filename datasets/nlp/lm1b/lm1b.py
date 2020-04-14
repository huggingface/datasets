# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""The Language Model 1 Billion dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import logging
import nlp

_CITATION = """\
@article{DBLP:journals/corr/ChelbaMSGBK13,
  author    = {Ciprian Chelba and
               Tomas Mikolov and
               Mike Schuster and
               Qi Ge and
               Thorsten Brants and
               Phillipp Koehn},
  title     = {One Billion Word Benchmark for Measuring Progress in Statistical Language
               Modeling},
  journal   = {CoRR},
  volume    = {abs/1312.3005},
  year      = {2013},
  url       = {http://arxiv.org/abs/1312.3005},
  archivePrefix = {arXiv},
  eprint    = {1312.3005},
  timestamp = {Mon, 13 Aug 2018 16:46:16 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/ChelbaMSGBK13},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
A benchmark corpus to be used for measuring progress in statistical language \
modeling. This has almost one billion words in the training data.
"""

_DOWNLOAD_URL = ("http://www.statmt.org/lm-benchmark/"
                 "1-billion-word-language-modeling-benchmark-r13output.tar.gz")
_TOP_LEVEL_DIR = "1-billion-word-language-modeling-benchmark-r13output"
_TRAIN_FILE_FORMAT = os.path.join(_TOP_LEVEL_DIR,
                                  "training-monolingual.tokenized.shuffled",
                                  "news.en-*")
_HELDOUT_FILE_FORMAT = os.path.join(_TOP_LEVEL_DIR,
                                    "heldout-monolingual.tokenized.shuffled",
                                    "news.en.heldout-*")


class Lm1bConfig(nlp.BuilderConfig):
  """BuilderConfig for Lm1b."""

  def __init__(self, text_encoder_config=None, **kwargs):
    """BuilderConfig for Lm1b.

    Args:
      text_encoder_config: `nlp.features.text.TextEncoderConfig`, configuration
        for the `nlp.features.text.TextEncoder` used for the Lm1b `"text"`
        feature.
      **kwargs: keyword arguments forwarded to super.
    """
    super(Lm1bConfig, self).__init__(
        version=nlp.Version(
            "1.0.0",
            "New split API (https://tensorflow.org/datasets/splits)"),
        **kwargs)
    self.text_encoder_config = (
        text_encoder_config or nlp.features.text.TextEncoderConfig())


def _train_data_filenames(tmp_dir):
  return nlp.io.gfile.glob(os.path.join(tmp_dir, _TRAIN_FILE_FORMAT))


def _test_data_filenames(tmp_dir):
  return nlp.io.gfile.glob(os.path.join(tmp_dir, _HELDOUT_FILE_FORMAT))


class Lm1b(nlp.GeneratorBasedBuilder):
  """1 Billion Word Language Model Benchmark dataset."""
  BUILDER_CONFIGS = [
      Lm1bConfig(
          name="plain_text",
          description="Plain text",
      ),
      Lm1bConfig(
          name="bytes",
          description=("Uses byte-level text encoding with "
                       "`nlp.features.text.ByteTextEncoder`"),
          text_encoder_config=nlp.features.text.TextEncoderConfig(
              encoder=nlp.features.text.ByteTextEncoder()),
      ),
      Lm1bConfig(
          name="subwords8k",
          description=("Uses `nlp.features.text.SubwordTextEncoder` with 8k "
                       "vocab size"),
          text_encoder_config=nlp.features.text.TextEncoderConfig(
              encoder_cls=nlp.features.text.SubwordTextEncoder,
              vocab_size=2**13),
      ),
      Lm1bConfig(
          name="subwords32k",
          description=("Uses `nlp.features.text.SubwordTextEncoder` with "
                       "32k vocab size"),
          text_encoder_config=nlp.features.text.TextEncoderConfig(
              encoder_cls=nlp.features.text.SubwordTextEncoder,
              vocab_size=2**15),
      ),
  ]

  def _info(self):
    return nlp.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=nlp.features.FeaturesDict({
            "text":
                nlp.features.Text(
                    encoder_config=self.builder_config.text_encoder_config),
        }),
        supervised_keys=("text", "text"),
        homepage="http://www.statmt.org/lm-benchmark/",
        citation=_CITATION,
    )

  def _vocab_text_gen(self, training_files):
    for _, ex in self._generate_examples(training_files):
      yield ex["text"]

  def _split_generators(self, dl_manager):
    lm1b_path = dl_manager.download_and_extract(_DOWNLOAD_URL)

    train_files = _train_data_filenames(lm1b_path)
    test_files = _test_data_filenames(lm1b_path)

    # Generate vocabulary from training data if SubwordTextEncoder configured
    self.info.features["text"].maybe_build_from_corpus(
        self._vocab_text_gen(train_files))

    return [
        nlp.SplitGenerator(
            name=nlp.Split.TRAIN,
            gen_kwargs={"files": train_files}),
        nlp.SplitGenerator(
            name=nlp.Split.TEST,
            gen_kwargs={"files": test_files}),
    ]

  def _generate_examples(self, files):
    for filepath in files:
      logging.info("generating examples from = %s", filepath)
      with open(filepath) as f:

        for idx, line in enumerate(f):
          yield "%s_%d" % (os.path.basename(filepath), idx), {
              "text": line.strip(),
          }
