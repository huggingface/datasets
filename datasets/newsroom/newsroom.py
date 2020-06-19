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
"""NEWSROOM Dataset."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


_CITATION = """
@inproceedings{N18-1065,
  author    = {Grusky, Max and Naaman, Mor and Artzi, Yoav},
  title     = {NEWSROOM: A Dataset of 1.3 Million Summaries
               with Diverse Extractive Strategies},
  booktitle = {Proceedings of the 2018 Conference of the
               North American Chapter of the Association for
               Computational Linguistics: Human Language Technologies},
  year      = {2018},
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
    "title",
    "url",
    "date",
    "density_bin",
    "coverage_bin",
    "compression_bin",
]
_ADDITIONAL_FLOAT_FEATURES = [
    "density",
    "coverage",
    "compression",
]


class Newsroom(nlp.GeneratorBasedBuilder):
    """NEWSROOM Dataset."""

    VERSION = nlp.Version("1.0.0")

    @property
    def manual_download_instructions(self):
        return """\
  You should download the dataset from http://lil.nlp.cornell.edu/newsroom/
  The webpage requires registration.
  To unzip the .tar file run `tar -zxvf complete.tar`. To unzip the .gz files
  run `gunzip train.json.gz` , ...
  After downloading, please put the files under the following names
  dev.jsonl, test.jsonl and train.jsonl in a dir of your choice,
  which will be used as a manual_dir, e.g. `~/.manual_dirs/newsroom`
  Newsroom can then be loaded via:
  `nlp.load_dataset("newsroom", data_dir="~/.manual_dirs/newsroom")`.
  """

    def _info(self):
        features = {k: nlp.Value("string") for k in [_DOCUMENT, _SUMMARY] + _ADDITIONAL_TEXT_FEATURES}
        features.update({k: nlp.Value("float32") for k in _ADDITIONAL_FLOAT_FEATURES})
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(features),
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage="http://lil.nlp.cornell.edu/newsroom/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `nlp.load_dataset('newsroom', data_dir=...)` that includes files unzipped from the reclor zip. Manual download instructions: {}".format(
                    data_dir, self.manual_download_instructions
                )
            )
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, gen_kwargs={"input_file": os.path.join(data_dir, "train.jsonl")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"input_file": os.path.join(data_dir, "dev.jsonl")},
            ),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"input_file": os.path.join(data_dir, "test.jsonl")},),
        ]

    def _generate_examples(self, input_file=None):
        """Yields examples."""
        with open(input_file) as f:
            for i, line in enumerate(f):
                d = json.loads(line)
                # fields are "url", "archive", "title", "date", "text",
                #  "compression_bin", "density_bin", "summary", "density",
                #  "compression', "coverage", "coverage_bin",
                yield i, {
                    k: d[k] for k in [_DOCUMENT, _SUMMARY] + _ADDITIONAL_TEXT_FEATURES + _ADDITIONAL_FLOAT_FEATURES
                }
