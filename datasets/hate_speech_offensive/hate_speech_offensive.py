# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""An annotated dataset for hate speech and offensive language detection on tweets."""


import csv

import datasets


_CITATION = """\
@inproceedings{hateoffensive,
title = {Automated Hate Speech Detection and the Problem of Offensive Language},
author = {Davidson, Thomas and Warmsley, Dana and Macy, Michael and Weber, Ingmar},
booktitle = {Proceedings of the 11th International AAAI Conference on Web and Social Media},
series = {ICWSM '17},
year = {2017},
location = {Montreal, Canada},
pages = {512-515}
}
"""

_DESCRIPTION = """\
An annotated dataset for hate speech and offensive language detection on tweets.
"""

_HOMEPAGE = "https://github.com/t-davidson/hate-speech-and-offensive-language"

_LICENSE = "MIT"

_URL = "https://raw.githubusercontent.com/t-davidson/hate-speech-and-offensive-language/master/data/labeled_data.csv"

_CLASS_MAP = {
    "0": "hate speech",
    "1": "offensive language",
    "2": "neither",
}


class HateSpeechOffensive(datasets.GeneratorBasedBuilder):
    """An annotated dataset for hate speech and offensive language detection on tweets."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "count": datasets.Value("int64"),
                    "hate_speech_count": datasets.Value("int64"),
                    "offensive_language_count": datasets.Value("int64"),
                    "neither_count": datasets.Value("int64"),
                    "class": datasets.ClassLabel(names=["hate speech", "offensive language", "neither"]),
                    "tweet": datasets.Value("string"),
                }
            ),
            supervised_keys=("tweet", "class"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_file = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_file,
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f)
            for id_, row in enumerate(reader):
                if id_ == 0:
                    continue

                yield id_, {
                    "count": row[1],
                    "hate_speech_count": row[2],
                    "offensive_language_count": row[3],
                    "neither_count": row[4],
                    "class": _CLASS_MAP[row[5]],
                    "tweet": row[6],
                }
