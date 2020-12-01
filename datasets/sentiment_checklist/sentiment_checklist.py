# coding=utf-8
# Copyright 2020 Marco Tulio Ribeiro
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
"""A CheckList suite for three-way sentiment analysis (negative, neutral, positive)."""

from __future__ import absolute_import, division, print_function

import csv
import json
import logging
import os

import nlp
from checklist.test_suite import TestSuite


_CITATION = """\
 @inproceedings{checklist:acl20},
 author = {Marco Tulio Ribeiro and Tongshuang Wu and Carlos Guestrin and Sameer Singh},
 title = {Beyond Accuracy: Behavioral Testing of NLP models with CheckList},
 booktitle = {Association for Computational Linguistics (ACL)},
 year = {2020}
"""

_DESCRIPTION = """\
A CheckList for three-way sentiment analysis (negative, neutral, positive).
Predictions: should be integers, where:
  - 0: negative
  - 1: neutral
  - 2: positive
Confidences: should be list(float) of length 3, with prediction probabilities
for negative, neutral and positive (respectively)

Test names for Table 1 in the paper:
['neutral words in context', 'Sentiment-laden words in context', 'change neutral words with BERT', 'add positive phrases', 'add negative phrases', 'add random urls and handles', 'typos', 'change locations', 'change names', 'used to, but now', 'simple negations: not negative', 'simple negations: not neutral is still neutral', 'simple negations: I thought x was negative, but it was not (should be neutral or positive)', 'Hard: Negation of positive with neutral stuff in the middle (should be negative)', 'my opinion is what matters', 'Q & A: yes', 'Q & A: no']

Use with nlp.checklist.CheckListSuite
"""

_URL = "https://github.com/marcotcr/checklist/raw/master/release_suites/sentiment_suite.tar.gz"
_SUITE_NAME = "sentiment_suite.pkl"


class SentimentCheckListConfig(nlp.BuilderConfig):
    """ BuilderConfig for NewDataset"""

    def __init__(self, url=_URL, suite_name=_SUITE_NAME, **kwargs):
        """

        Args:
            url: .tar.gz file url
            suite_name: name of the pickle file archived in url
            **kwargs: keyword arguments forwarded to super.
        """
        self.url = url
        self.suite_name = suite_name
        super(SentimentCheckListConfig, self).__init__(**kwargs)


class SentimentCheckList(nlp.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = nlp.Version("1.1.0")

    BUILDER_CONFIG_CLASS = SentimentCheckListConfig
    BUILDER_CONFIGS = [SentimentCheckListConfig(_URL, _SUITE_NAME, version=VERSION, name="sentiment_checklist_config")]

    test_dummy_data = False

    def _info(self):
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "tweet": nlp.Value("string"),
                    "test_name": nlp.Value("string"),
                    "test_case": nlp.Value("int32"),
                    "example_idx": nlp.Value("int32"),
                }
            ),
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/marcotcr/checklist",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_dir = dl_manager.download_and_extract(_URL)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                gen_kwargs={"filepath": os.path.join(dl_dir, self.config.suite_name), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        logging.info("generating examples from = %s", filepath)
        suite = TestSuite.from_file(filepath)
        example_to_dict_fn = lambda x: {"tweet": x}
        d = suite.to_dict(example_to_dict_fn)
        keys = list(d.keys())
        for i in range(len(d[keys[0]])):
            yield i, {k: d[k][i] for k in keys}
