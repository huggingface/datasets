# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the current dataset script contributor.
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
""" The Text REtrieval Conference (TREC) Question Classification dataset."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import nlp


_CITATION = """\
@inproceedings{li-roth-2002-learning,
    title = "Learning Question Classifiers",
    author = "Li, Xin  and
      Roth, Dan",
    booktitle = "{COLING} 2002: The 19th International Conference on Computational Linguistics",
    year = "2002",
    url = "https://www.aclweb.org/anthology/C02-1150",
}
@inproceedings{hovy-etal-2001-toward,
    title = "Toward Semantics-Based Answer Pinpointing",
    author = "Hovy, Eduard  and
      Gerber, Laurie  and
      Hermjakob, Ulf  and
      Lin, Chin-Yew  and
      Ravichandran, Deepak",
    booktitle = "Proceedings of the First International Conference on Human Language Technology Research",
    year = "2001",
    url = "https://www.aclweb.org/anthology/H01-1069",
}
"""

_DESCRIPTION = """\
The Text REtrieval Conference (TREC) Question Classification dataset contains 5500 labeled questions in training set and another 500 for test set. The dataset has 6 labels, 47 level-2 labels. Average length of each sentence is 10, vocabulary size of 8700.

Data are collected from four sources: 4,500 English questions published by USC (Hovy et al., 2001), about 500 manually constructed questions for a few rare classes, 894 TREC 8 and TREC 9 questions, and also 500 questions from TREC 10 which serves as the test set.
"""

_URLs = {
    "train": "http://cogcomp.org/Data/QA/QC/train_5500.label",
    "test": "http://cogcomp.org/Data/QA/QC/TREC_10.label",
}

_COARSE_LABELS = ["DESC", "ENTY", "ABBR", "HUM", "NUM", "LOC"]

_FINE_LABELS = [
    "manner",
    "cremat",
    "animal",
    "exp",
    "ind",
    "gr",
    "title",
    "def",
    "date",
    "reason",
    "event",
    "state",
    "desc",
    "count",
    "other",
    "letter",
    "religion",
    "food",
    "country",
    "color",
    "termeq",
    "city",
    "body",
    "dismed",
    "mount",
    "money",
    "product",
    "period",
    "substance",
    "sport",
    "plant",
    "techmeth",
    "volsize",
    "instru",
    "abb",
    "speed",
    "word",
    "lang",
    "perc",
    "code",
    "dist",
    "temp",
    "symbol",
    "ord",
    "veh",
    "weight",
    "currency",
]


class Trec(nlp.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = nlp.Version("1.1.0")

    def _info(self):
        # TODO: Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "label-coarse": nlp.ClassLabel(names=_COARSE_LABELS),
                    "label-fine": nlp.ClassLabel(names=_FINE_LABELS),
                    "text": nlp.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://cogcomp.seas.upenn.edu/Data/QA/QC/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_files = dl_manager.download_and_extract(_URLs)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_files["train"],},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_files["test"],},
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        # TODO: Yields (key, example) tuples from the dataset
        with open(filepath, "rb") as f:
            for id_, row in enumerate(f):
                # One non-ASCII byte: sisterBADBYTEcity. We replace it with a space
                label, _, text = row.replace(b"\xf0", b" ").strip().decode().partition(" ")
                coarse_label, _, fine_label = label.partition(":")
                yield id_, {
                    "label-coarse": coarse_label,
                    "label-fine": fine_label,
                    "text": text,
                }
