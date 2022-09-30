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


import csv

import datasets


_DESCRIPTION = """
Yahoo! Answers Topic Classification is text classification dataset. \
The dataset is the Yahoo! Answers corpus as of 10/25/2007. \
The Yahoo! Answers topic classification dataset is constructed using 10 largest main categories. \
From all the answers and other meta-information, this dataset only used the best answer content and the main category information.
"""

_URL = "https://s3.amazonaws.com/fast-ai-nlp/yahoo_answers_csv.tgz"

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
        archive = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": "yahoo_answers_csv/train.csv",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": "yahoo_answers_csv/test.csv",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, files):
        for path, f in files:
            if path == filepath:
                lines = (line.decode("utf-8") for line in f)
                rows = csv.reader(lines)
                for i, row in enumerate(rows):
                    yield i, {
                        "id": i,
                        "topic": int(row[0]) - 1,
                        "question_title": row[1],
                        "question_content": row[2],
                        "best_answer": row[3],
                    }
                break
