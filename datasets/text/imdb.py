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
"""IMDB movie reviews dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re

import tensorflow_datasets.public_api as tfds

_DESCRIPTION = """\
Large Movie Review Dataset.
This is a dataset for binary sentiment classification containing substantially \
more data than previous benchmark datasets. We provide a set of 25,000 highly \
polar movie reviews for training, and 25,000 for testing. There is additional \
unlabeled data for use as well.\
"""

_CITATION = """\
@InProceedings{maas-EtAl:2011:ACL-HLT2011,
  author    = {Maas, Andrew L.  and  Daly, Raymond E.  and  Pham, Peter T.  and  Huang, Dan  and  Ng, Andrew Y.  and  Potts, Christopher},
  title     = {Learning Word Vectors for Sentiment Analysis},
  booktitle = {Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies},
  month     = {June},
  year      = {2011},
  address   = {Portland, Oregon, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {142--150},
  url       = {http://www.aclweb.org/anthology/P11-1015}
}
"""

_DOWNLOAD_URL = "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"


class IMDBReviewsConfig(tfds.core.BuilderConfig):
  """BuilderConfig for IMDBReviews."""

  @tfds.core.disallow_positional_args
  def __init__(self, text_encoder_config=None, **kwargs):
    """BuilderConfig for IMDBReviews.

    Args:
      text_encoder_config: `tfds.features.text.TextEncoderConfig`, configuration
        for the `tfds.features.text.TextEncoder` used for the IMDB `"text"`
        feature.
      **kwargs: keyword arguments forwarded to super.
    """
    super(IMDBReviewsConfig, self).__init__(
        version=tfds.core.Version(
            "1.0.0",
            "New split API (https://tensorflow.org/datasets/splits)"),
        **kwargs)
    self.text_encoder_config = (
        text_encoder_config or tfds.features.text.TextEncoderConfig())


class IMDBReviews(tfds.core.GeneratorBasedBuilder):
  """IMDB movie reviews dataset."""
  BUILDER_CONFIGS = [
      IMDBReviewsConfig(
          name="plain_text",
          description="Plain text",
      ),
      IMDBReviewsConfig(
          name="bytes",
          description=("Uses byte-level text encoding with "
                       "`tfds.features.text.ByteTextEncoder`"),
          text_encoder_config=tfds.features.text.TextEncoderConfig(
              encoder=tfds.features.text.ByteTextEncoder()),
      ),
      IMDBReviewsConfig(
          name="subwords8k",
          description=("Uses `tfds.features.text.SubwordTextEncoder` with 8k "
                       "vocab size"),
          text_encoder_config=tfds.features.text.TextEncoderConfig(
              encoder_cls=tfds.features.text.SubwordTextEncoder,
              vocab_size=2**13),
      ),
      IMDBReviewsConfig(
          name="subwords32k",
          description=("Uses `tfds.features.text.SubwordTextEncoder` with "
                       "32k vocab size"),
          text_encoder_config=tfds.features.text.TextEncoderConfig(
              encoder_cls=tfds.features.text.SubwordTextEncoder,
              vocab_size=2**15),
      ),
  ]

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            "text": tfds.features.Text(
                encoder_config=self.builder_config.text_encoder_config),
            "label": tfds.features.ClassLabel(names=["neg", "pos"]),
        }),
        supervised_keys=("text", "label"),
        homepage="http://ai.stanford.edu/~amaas/data/sentiment/",
        citation=_CITATION,
    )

  def _vocab_text_gen(self, archive):
    for _, ex in self._generate_examples(
        archive, os.path.join("aclImdb", "train")):
      yield ex["text"]

  def _split_generators(self, dl_manager):
    arch_path = dl_manager.download(_DOWNLOAD_URL)
    archive = lambda: dl_manager.iter_archive(arch_path)

    # Generate vocabulary from training data if SubwordTextEncoder configured
    self.info.features["text"].maybe_build_from_corpus(
        self._vocab_text_gen(archive()))

    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={"archive": archive(),
                        "directory": os.path.join("aclImdb", "train")}),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={"archive": archive(),
                        "directory": os.path.join("aclImdb", "test")}),
        tfds.core.SplitGenerator(
            name=tfds.Split("unsupervised"),
            gen_kwargs={"archive": archive(),
                        "directory": os.path.join("aclImdb", "train"),
                        "labeled": False}),
    ]

  def _generate_examples(self, archive, directory, labeled=True):
    """Generate IMDB examples."""
    # For labeled examples, extract the label from the path.
    reg_path = "(?P<label>neg|pos)" if labeled else "unsup"
    reg = re.compile(
        os.path.join("^%s" % directory, reg_path, "").replace("\\", "\\\\"))
    for path, imdb_f in archive:
      res = reg.match(path)
      if not res:
        continue
      text = imdb_f.read().strip()
      label = res.groupdict()["label"] if labeled else -1
      yield path, {
          "text": text,
          "label": label,
      }
