# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""Yahoo! Answers Topic Classification Dataset"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_DESCRIPTION = """
Yahoo! Answers Topic Classification is text classification dataset. \
The dataset is the Yahoo! Answers corpus as of 10/25/2007. \
The Yahoo! Answers topic classification dataset is constructed using 10 largest main categories. \
From all the answers and other meta-information, this dataset only used the best answer content and the main category information.
"""

_URL = "https://drive.google.com/uc?export=download&id=0Bz8a_Dbh9Qhbd2JNdDBsQUdocVU"

_TOPICS = [
    "Society & Culture",
    "Science & Mathematics",
    "Health",
    "Education & Reference",
    "Computers & Internet",
    "Sports",
    "Business & Finance",
    "Entertainment & Music",
    "Family & Relationships",
    "Politics & Government",
]


class YahooAnswersTopics(datasets.GeneratorBasedBuilder):
    "Yahoo! Answers Topic Classification Dataset"

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="yahoo_answers_topics",
            version=datasets.Version("1.0.0", ""),
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "topic": datasets.features.ClassLabel(names=_TOPICS),
                    "question_title": datasets.Value("string"),
                    "question_content": datasets.Value("string"),
                    "best_answer": datasets.Value("string"),
                },
            ),
            supervised_keys=None,
            homepage="https://github.com/LC-John/Yahoo-Answers-Topic-Classification-Dataset",
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URL)

        # Extracting (un-taring) the training data
        data_dir = os.path.join(data_dir, "yahoo_answers_csv")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(data_dir, "train.csv")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": os.path.join(data_dir, "test.csv")}
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            rows = csv.reader(f)
            for i, row in enumerate(rows):
                yield i, {
                    "id": i,
                    "topic": int(row[0]) - 1,
                    "question_title": row[1],
                    "question_content": row[2],
                    "best_answer": row[3],
                }
