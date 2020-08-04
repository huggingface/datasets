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
"""A CheckList suite for SQuAD"""

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
A CheckList for SQuAD.
Predictions: each prediction is a string, containing the answer
Confidences: not necessary for this checklist

Test names for Table 3 in the paper:
['A is COMP than B. Who is more / less COMP?', 'Intensifiers (very, super, extremely) and reducers (somewhat, kinda, etc)?', 'size, shape, age, color', 'Profession vs nationality', 'Animal vs Vehicle v2', 'A is COMP than B. Who is antonym(COMP)? B', 'A is more X than B. Who is more antonym(X)? B. Who is less X? B. Who is more X? A. Who is less antonym(X)? A.', 'Question typo', 'Add random sentence to context', 'There was a change in profession', 'Understanding before / after -> first / last.', 'Negation in context, may or may not be in question', 'Negation in question only.', 'M/F failure rates should be similar for different professions', 'Basic coref, he / she', 'Basic coref, his / her', 'Former / Latter', 'Agent / object distinction', 'Agent / object distinction with 3 agents']

Use with nlp.checklist.CheckListSuite
"""

_URL = "https://github.com/marcotcr/checklist/raw/master/release_suites/squad_suite.tar.gz"
_SUITE_NAME = "squad_suite.pkl"


class SquadCheckListConfig(nlp.BuilderConfig):
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
        super(SquadCheckListConfig, self).__init__(**kwargs)


class SquadCheckList(nlp.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = nlp.Version("1.1.0")

    BUILDER_CONFIG_CLASS = SquadCheckListConfig
    BUILDER_CONFIGS = [SquadCheckListConfig(_URL, _SUITE_NAME, version=VERSION, name="squad_checklist_config")]

    def _info(self):
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "context": nlp.Value("string"),
                    "question": nlp.Value("string"),
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
        example_to_dict_fn = lambda x: {"context": x[0], "question": x[1]}
        d = suite.to_dict(example_to_dict_fn)
        keys = list(d.keys())
        for i in range(len(d[keys[0]])):
            yield i, {k: d[k][i] for k in keys}
