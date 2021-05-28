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
"""Roman Urdu data corpus with 20,000 polarity labeled records"""


import csv
import os

import datasets
from datasets.tasks import TextClassification


_CITATION = """\
@InProceedings{Sharf:2018,
title = "Performing Natural Language Processing on Roman Urdu Datasets",
authors = "Zareen Sharf and Saif Ur Rahman",
booktitle = "International Journal of Computer Science and Network Security",
volume = "18",
number = "1",
pages = "141-148",
year = "2018"
}

@misc{Dua:2019,
author = "Dua, Dheeru and Graff, Casey",
year = "2017",
title = "{UCI} Machine Learning Repository",
url = "http://archive.ics.uci.edu/ml",
institution = "University of California, Irvine, School of Information and Computer Sciences"
}
"""

_DESCRIPTION = """\
This is an extensive compilation of Roman Urdu Dataset (Urdu written in Latin/Roman script) tagged for sentiment analysis.
"""

_HOMEPAGE = "https://archive.ics.uci.edu/ml/datasets/Roman+Urdu+Data+Set"

_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00458/Roman%20Urdu%20DataSet.csv"


class RomanUrdu(datasets.GeneratorBasedBuilder):
    """Roman Urdu sentences gathered from reviews of various e-commerce websites, comments on public Facebook pages, and twitter accounts, with positive, neutral, and negative polarity labels per each row."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "sentiment": datasets.features.ClassLabel(names=["Positive", "Negative", "Neutral"]),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
            task_templates=[TextClassification(text_column="sentence", label_column="sentiment")],
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            for id_, row in enumerate(reader):
                yield id_, {
                    "sentence": row[0],
                    # 'Neative' typo in original dataset
                    "sentiment": "Negative" if row[1] == "Neative" else row[1],
                }
