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
"""NEWSROOM Dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os

import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """
@article{Grusky_2018,
   title={Newsroom: A Dataset of 1.3 Million Summaries with Diverse Extractive Strategies},
   url={http://dx.doi.org/10.18653/v1/n18-1065},
   DOI={10.18653/v1/n18-1065},
   journal={Proceedings of the 2018 Conference of the North American Chapter of
          the Association for Computational Linguistics: Human Language
          Technologies, Volume 1 (Long Papers)},
   publisher={Association for Computational Linguistics},
   author={Grusky, Max and Naaman, Mor and Artzi, Yoav},
   year={2018}
}

"""

_DESCRIPTION = """
NEWSROOM is a large dataset for training and evaluating summarization systems.
It contains 1.3 million articles and summaries written by authors and
editors in the newsrooms of 38 major publications.

Dataset features includes:
  - text: Input news text.
  - summary: Summary for the news.
And additional features:
  - title: news title.
  - url: url of the news.
  - date: date of the article.
  - density: extractive density.
  - coverage: extractive coverage.
  - compression: compression ratio.
  - density_bin: low, medium, high.
  - coverage_bin: extractive, abstractive.
  - compression_bin: low, medium, high.

This dataset can be downloaded upon requests. Unzip all the contents
"train.jsonl, dev.josnl, test.jsonl" to the tfds folder.

"""

_DOCUMENT = "text"
_SUMMARY = "summary"
_ADDITIONAL_TEXT_FEATURES = [
    "title", "url", "date", "density_bin", "coverage_bin", "compression_bin"
]
_ADDITIONAL_FLOAT_FEATURES = [
    "density",
    "coverage",
    "compression",
]


class Newsroom(tfds.core.GeneratorBasedBuilder):
  """NEWSROOM Dataset."""

  VERSION = tfds.core.Version("1.0.0")
  MANUAL_DOWNLOAD_INSTRUCTIONS = """\
  You should download the dataset from https://summari.es/download/
  The webpage requires registration.
  After downloading, please put dev.jsonl, test.jsonl and train.jsonl
  files in the manual_dir.
  """

  def _info(self):
    features = {
        k: tfds.features.Text()
        for k in [_DOCUMENT, _SUMMARY] + _ADDITIONAL_TEXT_FEATURES
    }
    features.update({
        k: tfds.features.Tensor(shape=[], dtype=tf.float32)
        for k in _ADDITIONAL_FLOAT_FEATURES
    })
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict(features),
        supervised_keys=(_DOCUMENT, _SUMMARY),
        homepage="https://summari.es",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={
                "input_file": os.path.join(dl_manager.manual_dir, "train.jsonl")
            },
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={
                "input_file": os.path.join(dl_manager.manual_dir, "dev.jsonl")
            },
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={
                "input_file": os.path.join(dl_manager.manual_dir, "test.jsonl")
            },
        ),
    ]

  def _generate_examples(self, input_file=None):
    """Yields examples."""
    with tf.io.gfile.GFile(input_file) as f:
      for i, line in enumerate(f):
        d = json.loads(line)
        # fields are "url", "archive", "title", "date", "text",
        #  "compression_bin", "density_bin", "summary", "density",
        #  "compression', "coverage", "coverage_bin",
        yield i, {
            k: d[k] for k in [_DOCUMENT, _SUMMARY] + _ADDITIONAL_TEXT_FEATURES +
            _ADDITIONAL_FLOAT_FEATURES
        }
