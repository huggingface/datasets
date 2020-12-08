# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""GoEmotions dataset"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_DESCRIPTION = """\
The GoEmotions dataset contains 58k carefully curated Reddit comments labeled for 27 emotion categories or Neutral.
The emotion categories are admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire,
disappointment, disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness,
optimism, pride, realization, relief, remorse, sadness, surprise.
"""

_CITATION = """\
@inproceedings{demszky2020goemotions,
 author = {Demszky, Dorottya and Movshovitz-Attias, Dana and Ko, Jeongwoo and Cowen, Alan and Nemade, Gaurav and Ravi, Sujith},
 booktitle = {58th Annual Meeting of the Association for Computational Linguistics (ACL)},
 title = {{GoEmotions: A Dataset of Fine-Grained Emotions}},
 year = {2020}
}
"""

_CLASS_NAMES = [
    "admiration",
    "amusement",
    "anger",
    "annoyance",
    "approval",
    "caring",
    "confusion",
    "curiosity",
    "desire",
    "disappointment",
    "disapproval",
    "disgust",
    "embarrassment",
    "excitement",
    "fear",
    "gratitude",
    "grief",
    "joy",
    "love",
    "nervousness",
    "optimism",
    "pride",
    "realization",
    "relief",
    "remorse",
    "sadness",
    "surprise",
    "neutral",
]

_BASE_DOWNLOAD_URL = "https://github.com/google-research/google-research/raw/master/goemotions/data/"
_RAW_DOWNLOAD_URLS = [
    "https://storage.googleapis.com/gresearch/goemotions/data/full_dataset/goemotions_1.csv",
    "https://storage.googleapis.com/gresearch/goemotions/data/full_dataset/goemotions_2.csv",
    "https://storage.googleapis.com/gresearch/goemotions/data/full_dataset/goemotions_3.csv",
]
_HOMEPAGE = "https://github.com/google-research/google-research/tree/master/goemotions"


class GoEmotionsConfig(datasets.BuilderConfig):
    @property
    def features(self):
        if self.name == "simplified":
            return {
                "text": datasets.Value("string"),
                "labels": datasets.Sequence(datasets.ClassLabel(names=_CLASS_NAMES)),
                "id": datasets.Value("string"),
            }
        elif self.name == "raw":
            d = {
                "text": datasets.Value("string"),
                "id": datasets.Value("string"),
                "author": datasets.Value("string"),
                "subreddit": datasets.Value("string"),
                "link_id": datasets.Value("string"),
                "parent_id": datasets.Value("string"),
                "created_utc": datasets.Value("float"),
                "rater_id": datasets.Value("int32"),
                "example_very_unclear": datasets.Value("bool"),
            }
            d.update({label: datasets.Value("int32") for label in _CLASS_NAMES})
            return d


class GoEmotions(datasets.GeneratorBasedBuilder):
    """GoEmotions dataset"""

    BUILDER_CONFIGS = [
        GoEmotionsConfig(
            name="raw",
        ),
        GoEmotionsConfig(
            name="simplified",
        ),
    ]
    BUILDER_CONFIG_CLASS = GoEmotionsConfig
    DEFAULT_CONFIG_NAME = "simplified"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(self.config.features),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        if self.config.name == "raw":
            paths = dl_manager.download_and_extract(_RAW_DOWNLOAD_URLS)
            return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepaths": paths, "raw": True})]
        if self.config.name == "simplified":
            train_path = dl_manager.download_and_extract(os.path.join(_BASE_DOWNLOAD_URL, "train.tsv"))
            dev_path = dl_manager.download_and_extract(os.path.join(_BASE_DOWNLOAD_URL, "dev.tsv"))
            test_path = dl_manager.download_and_extract(os.path.join(_BASE_DOWNLOAD_URL, "test.tsv"))
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepaths": [train_path]}),
                datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepaths": [dev_path]}),
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepaths": [test_path]}),
            ]

    def _generate_examples(self, filepaths, raw=False):
        """Generate AG News examples."""
        for filepath in filepaths:
            with open(filepath, "r", encoding="utf-8") as f:
                if raw:
                    reader = csv.DictReader(f)
                else:
                    reader = csv.DictReader(f, delimiter="\t", fieldnames=list(self.config.features.keys()))

                for irow, row in enumerate(reader):
                    if raw:
                        row["example_very_unclear"] = row["example_very_unclear"] == "TRUE"
                    else:
                        row["labels"] = [int(ind) for ind in row["labels"].split(",")]

                    yield irow, row
