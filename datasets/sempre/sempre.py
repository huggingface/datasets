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
"""SEMPRE dataset."""

from __future__ import absolute_import, division, print_function

import json
import logging
import os

import nlp

_CITATION = """
@inproceedings{berant-etal-2013-semantic,
    title = "Semantic Parsing on {F}reebase from Question-Answer Pairs",
    author = "Berant, Jonathan  and
      Chou, Andrew  and
      Frostig, Roy  and
      Liang, Percy",
    booktitle = "Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing",
    month = oct,
    year = "2013",
    address = "Seattle, Washington, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D13-1160",
    pages = "1533--1544",
}
"""

_DESCRIPTION = """
SEMPRE is a toolkit for training semantic parsers, which map natural language utterances to denotations (answers) via intermediate logical forms. Here's an example for querying databases:
Utterance: Which college did Obama go to?
Logical form: (and (Type University) (Education BarackObama))
Denotation: Occidental College, Columbia University
Here's another example for programming via natural language:
Utterance: Compute three plus four.
Logical form: (call + 3 4)
Denotation: 7

SEMPRE has the following functionality:
It supports many types of logical forms (e.g., lambda calculus, lambda DCS, Java expressions, etc.), so you can choose whichever one suits your task.
It is agnostic to the construction procedure for building logical forms, which include Combinatory Categorical Grammar (CCG) or something more simplistic. You just specify the combination rules in a domain specific language. Here's a toy subset of CCG.
It supports various online learning algorithms that discriminatively train a classifier to maximize denotation accuracy.
It comes with a full copy of Freebase (41M entities, 19K properties, 596M assertions), which has been indexed by Virtuoso SPARQL engine. This allows you to immediately start executing logical forms on Freebase.

"""
_URLS = {
    'webquestions.train': "https://nlp.stanford.edu/static/software/sempre/release-emnlp2013/lib/data/webquestions/dataset_11/webquestions.examples.train.json.bz2",
    'webquestions.test': "https://nlp.stanford.edu/static/software/sempre/release-emnlp2013/lib/data/webquestions/dataset_11/webquestions.examples.test.json.bz2",
    "free917.train":  "https://nlp.stanford.edu/static/software/sempre/release-emnlp2013/data/free917.train.examples.canonicalized.json.bz2",
    "free917.test":  "https://nlp.stanford.edu/static/software/sempre/release-emnlp2013/data/free917.test.examples.canonicalized.json.bz2"
}

_TEXT_FEATURES = [
    "utterance"
]

class SempreConfig(nlp.BuilderConfig):
    """BuilderConfig for BlogAuthorship."""

    def __init__(self, data_urls, **kwargs):
        """BuilderConfig for SEMPRE

        Args:
          data_urls: `dict`, urls to the train and test dataset 
          **kwargs: keyword arguments forwarded to super.
        """
        super(SempreConfig, self).__init__(version=nlp.Version("1.0.0",), **kwargs)
        self.data_urls = data_urls
        
class Sempre(nlp.GeneratorBasedBuilder):
    """Semantic Parsing with Execution (SEMPRE) Dataset."""

    # Version 1.1.0 removes web contents.
    VERSION = nlp.Version("1.1.0")
    BUILDER_CONFIGS = [
        SempreConfig(
            name='free917',
            description="Free917 contains 641 training example and 276 test examples.",
            data_urls={key:_URLS[key] for key in ['free917.train', 'free917.test']}
        ),
        SempreConfig(
            name='webquestions',
            description="WebQuestions contains 3,778 training examples and 2,032 test examples",
            data_urls={key:_URLS[key] for key in ['webquestions.train', 'webquestions.test']}
        )
    ]

    def _info(self):
        features = {
            feature: nlp.Value('string') for feature in _TEXT_FEATURES
        }
        if self.config.name == 'webquestions':
            features['url'] = nlp.Value('string')
            features['targetValue'] = nlp.Value('string')
        if self.config.name == 'free917':
            features['targetFormula'] = nlp.Value('string')
        return nlp.DatasetInfo(
            description=_DESCRIPTION + '\n' + self.config.description,
            features=nlp.Features(features),
            homepage="https://nlp.stanford.edu/software/sempre/",
            citation=_CITATION,
        )
    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_path = dl_manager.download_and_extract(self.config.data_urls)
        
      
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(dl_path[self.config.name+'.train']),
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(dl_path[self.config.name+'.test']),
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, 'rb') as f:
            data = json.load(f)
            for _id, row in enumerate(data):
               yield _id, row
               
        