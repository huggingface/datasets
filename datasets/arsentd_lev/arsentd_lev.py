# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""ArSenTD-Lev :  Arabic Sentiment Twitter Dataset for LEVantine dialect"""


import os

import datasets


_CITATION = """
@article{ArSenTDLev2018,
title={ArSentD-LEV: A Multi-Topic Corpus for Target-based Sentiment Analysis in Arabic Levantine Tweets},
author={Baly, Ramy, and Khaddaj, Alaa and Hajj, Hazem and El-Hajj, Wassim and Bashir Shaban, Khaled},
journal={OSACT3},
pages={},
year={2018}}
"""

_DESCRIPTION = """
The Arabic Sentiment Twitter Dataset for Levantine dialect (ArSenTD-LEV) contains 4,000 tweets written in Arabic and equally retrieved from Jordan, Lebanon, Palestine and Syria.
"""

_URL = "http://oma-project.com/ArSenL/ArSenTD-LEV.zip"
_FEATURES = ["Tweet", "Country", "Topic", "Sentiment", "Sentiment_Expression", "Sentiment_Target"]


class ArsentdLev(datasets.GeneratorBasedBuilder):
    """ "ArSenTD-Lev Dataset"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "Tweet": datasets.Value("string"),
                    "Country": datasets.ClassLabel(names=["jordan", "lebanon", "syria", "palestine"]),
                    "Topic": datasets.Value("string"),
                    "Sentiment": datasets.ClassLabel(
                        names=["negative", "neutral", "positive", "very_negative", "very_positive"]
                    ),
                    "Sentiment_Expression": datasets.ClassLabel(names=["explicit", "implicit", "none"]),
                    "Sentiment_Target": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="http://oma-project.com/ArSenL/ArSenTD_Lev_Intro",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"path": os.path.join(path, "ArSenTD-LEV.tsv")},
            ),
        ]

    def _generate_examples(self, path=None):
        """Yields examples."""
        with open(path, encoding="utf-8") as f:
            f.readline()  # skip first line
            for idx, line in enumerate(f):
                yield idx, {el[0]: el[1].strip() for el in zip(_FEATURES, line.split("\t"))}
