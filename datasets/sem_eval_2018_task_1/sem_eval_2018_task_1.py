# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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

import os

import datasets


_CITATION = """\
@InProceedings{SemEval2018Task1,
 author = {Mohammad, Saif M. and Bravo-Marquez, Felipe and Salameh, Mohammad and Kiritchenko, Svetlana},
 title = {SemEval-2018 {T}ask 1: {A}ffect in Tweets},
 booktitle = {Proceedings of International Workshop on Semantic Evaluation (SemEval-2018)},
 address = {New Orleans, LA, USA},
 year = {2018}}
"""

_DESCRIPTION = """\
 SemEval-2018 Task 1: Affect in Tweets: SubTask 5: Emotion Classification.
 This is a dataset for multilabel emotion classification for tweets.
 'Given a tweet, classify it as 'neutral or no emotion' or as one, or more, of eleven given emotions that best represent the mental state of the tweeter.'
 It contains 22467 tweets in three languages manually annotated by crowdworkers using Best–Worst Scaling.
"""

_HOMEPAGE = "https://competitions.codalab.org/competitions/17751"

_LICENSE = ""

_URLs = {
    "subtask5.english": ["https://saifmohammad.com/WebDocs/AIT-2018/AIT2018-DATA/SemEval2018-Task1-all-data.zip"],
    "subtask5.spanish": ["https://saifmohammad.com/WebDocs/AIT-2018/AIT2018-DATA/SemEval2018-Task1-all-data.zip"],
    "subtask5.arabic": ["https://saifmohammad.com/WebDocs/AIT-2018/AIT2018-DATA/SemEval2018-Task1-all-data.zip"],
}


class SemEval2018Task1(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="subtask5.english",
            version=VERSION,
            description="This is the English dataset of subtask 5: E-c: Detecting Emotions.",
        ),
        datasets.BuilderConfig(
            name="subtask5.spanish",
            version=VERSION,
            description="This is the Spanish dataset of subtask 5: E-c: Detecting Emotions.",
        ),
        datasets.BuilderConfig(
            name="subtask5.arabic",
            version=VERSION,
            description="This is the Arabic dataset of subtask 5: E-c: Detecting Emotions.",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "ID": datasets.Value("string"),
                "Tweet": datasets.Value("string"),
                "anger": datasets.Value("bool"),
                "anticipation": datasets.Value("bool"),
                "disgust": datasets.Value("bool"),
                "fear": datasets.Value("bool"),
                "joy": datasets.Value("bool"),
                "love": datasets.Value("bool"),
                "optimism": datasets.Value("bool"),
                "pessimism": datasets.Value("bool"),
                "sadness": datasets.Value("bool"),
                "surprise": datasets.Value("bool"),
                "trust": datasets.Value("bool"),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        if self.config.name == "subtask5.english":
            shortname = "En"
            longname = "English"
        if self.config.name == "subtask5.spanish":
            shortname = "Es"
            longname = "Spanish"
        if self.config.name == "subtask5.arabic":
            shortname = "Ar"
            longname = "Arabic"
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir[0],
                        "SemEval2018-Task1-all-data/" + longname + "/E-c/2018-E-c-" + shortname + "-train.txt",
                    ),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir[0],
                        "SemEval2018-Task1-all-data/" + longname + "/E-c/2018-E-c-" + shortname + "-test-gold.txt",
                    ),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir[0],
                        "SemEval2018-Task1-all-data/" + longname + "/E-c/2018-E-c-" + shortname + "-dev.txt",
                    ),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples as (key, example) tuples."""

        with open(filepath, encoding="utf-8") as f:
            next(f)  # skip header
            for id_, row in enumerate(f):
                data = row.split("\t")
                yield id_, {
                    "ID": data[0],
                    "Tweet": data[1],
                    "anger": int(data[2]),
                    "anticipation": int(data[3]),
                    "disgust": int(data[4]),
                    "fear": int(data[5]),
                    "joy": int(data[6]),
                    "love": int(data[7]),
                    "optimism": int(data[8]),
                    "pessimism": int(data[9]),
                    "sadness": int(data[10]),
                    "surprise": int(data[11]),
                    "trust": int(data[12]),
                }
