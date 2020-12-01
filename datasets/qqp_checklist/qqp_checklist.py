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
"""A CheckList suite for Quora Question Pair"""

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
A CheckList for Quora Question Pair.
Predictions: should be integers, where:
  - 0: non-duplicate
  - 1: duplicate
Confidences: should be list(float) of length 2, with prediction probabilities
for non-duplicate and duplicate(respectively)

Test names for Table 2 in the paper:
['Modifier: adj',  'How can I become more {synonym}?', 'Replace synonyms in real pairs', 'How can I become more X = How can I become less antonym(X)', 'add one typo', '(q, paraphrase(q))',  'Change same name in both questions',  'Change first and last name in one of the questions', 'Keep entitites, fill in with gibberish', 'Is person X != Did person use to be X',   'Is it {ok, dangerous, ...} to {smoke, rest, ...} after != before', "What was person's life before becoming X != What was person's life after becoming X", 'How can I become a X person != How can I become a person who is not X', 'How can I become a X person == How can I become a person who is not antonym(X)', 'Simple coref: he and she', 'Simple coref: his and her',  'Order does not matter for comparison', 'Order does not matter for symmetric relations', 'Order does matter for asymmetric relations',  'traditional SRL: active / passive swap with people', 'traditional SRL: wrong active / passive swap with people', 'Symmetry: f(a, b) = f(b, a)', 'Testing implications']

Use with nlp.checklist.CheckListSuite
"""

_URL = "https://github.com/marcotcr/checklist/raw/master/release_suites/qqp_suite.tar.gz"
_SUITE_NAME = "qqp_suite.pkl"


class QqpCheckListConfig(nlp.BuilderConfig):
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
        super(QqpCheckListConfig, self).__init__(**kwargs)


class QqpCheckList(nlp.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = nlp.Version("1.1.0")

    BUILDER_CONFIG_CLASS = QqpCheckListConfig
    BUILDER_CONFIGS = [QqpCheckListConfig(_URL, _SUITE_NAME, version=VERSION, name="qqp_checklist_config")]

    test_dummy_data = False

    def _info(self):
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "question1": nlp.Value("string"),
                    "question2": nlp.Value("string"),
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
        example_to_dict_fn = lambda x: {"question1": x[0], "question2": x[1]}
        d = suite.to_dict(example_to_dict_fn)
        keys = list(d.keys())
        for i in range(len(d[keys[0]])):
            yield i, {k: d[k][i] for k in keys}
