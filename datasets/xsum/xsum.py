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
"""XSum dataset."""

from __future__ import absolute_import, division, print_function

import json
import logging
import os

import nlp


_CITATION = """
@article{Narayan2018DontGM,
  title={Don't Give Me the Details, Just the Summary! Topic-Aware Convolutional Neural Networks for Extreme Summarization},
  author={Shashi Narayan and Shay B. Cohen and Mirella Lapata},
  journal={ArXiv},
  year={2018},
  volume={abs/1808.08745}
}
"""

_DESCRIPTION = """
Extreme Summarization (XSum) Dataset.

There are two features:
  - document: Input news article.
  - summary: One sentence summary of the article.

"""


_URL = "https://s3.amazonaws.com/datasets.huggingface.co/summarization/xsum.tar.gz"

_DOCUMENT = "document"
_SUMMARY = "summary"


class Xsum(nlp.GeneratorBasedBuilder):
    """Extreme Summarization (XSum) Dataset."""

    # Version 1.1.0 removes web contents.
    VERSION = nlp.Version("1.1.0")
    SUPPORTED_VERSIONS = [nlp.Version("1.0.0", "Dataset without cleaning.")]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({_DOCUMENT: nlp.Value("string"), _SUMMARY: nlp.Value("string"),}),
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage="https://github.com/EdinburghNLP/XSum/tree/master/XSum-Dataset",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_path = dl_manager.download_and_extract(_URL)

        dl_path = os.path.join(dl_path, "xsum")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={
                    "source": os.path.join(dl_path, "train.source"),
                    "target": os.path.join(dl_path, "train.target"),
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                gen_kwargs={
                    "source": os.path.join(dl_path, "val.source"),
                    "target": os.path.join(dl_path, "val.target"),
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                gen_kwargs={
                    "source": os.path.join(dl_path, "test.source"),
                    "target": os.path.join(dl_path, "test.target"),
                },
            ),
        ]

    def _generate_examples(self, source, target):
        """Yields examples."""
        with open(source) as f1:
            source = f1.readlines()
        with open(target) as f2:
            target = f2.readlines()
        assert len(source) == len(target)
        for i in range(len(target)):
            yield i, {_DOCUMENT: source[i], _SUMMARY: target[i]}
