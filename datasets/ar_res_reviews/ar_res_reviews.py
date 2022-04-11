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
"""Dataset of 8364 restaurant reviews scrapped from qaym.com in Arabic for sentiment analysis"""


import csv

import datasets


_CITATION = """\
@InProceedings{10.1007/978-3-319-18117-2_2,
author="ElSahar, Hady
and El-Beltagy, Samhaa R.",
editor="Gelbukh, Alexander",
title="Building Large Arabic Multi-domain Resources for Sentiment Analysis",
booktitle="Computational Linguistics and Intelligent Text Processing",
year="2015",
publisher="Springer International Publishing",
address="Cham",
pages="23--34",
isbn="978-3-319-18117-2"
}
"""

_DESCRIPTION = """\
Dataset of 8364 restaurant reviews scrapped from qaym.com in Arabic for sentiment analysis
"""

_HOMEPAGE = "https://github.com/hadyelsahar/large-arabic-sentiment-analysis-resouces"

_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/hadyelsahar/large-arabic-sentiment-analysis-resouces/master/datasets/RES1.csv"
)


class ArResReviews(datasets.GeneratorBasedBuilder):
    """Dataset of 8364 restaurant reviews in Arabic for sentiment analysis"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "polarity": datasets.ClassLabel(names=["negative", "positive"]),
                    "text": datasets.Value("string"),
                    "restaurant_id": datasets.Value("string"),
                    "user_id": datasets.Value("string"),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_dir}),
        ]

    def _generate_examples(self, filepath):
        """Generate arabic restaurant reviews examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            next(csv_file)
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            for id_, row in enumerate(csv_reader):
                polarity, text, restaurant_id, user_id = row
                polarity = "negative" if polarity == "-1" else "positive"
                yield id_, {"polarity": polarity, "text": text, "restaurant_id": restaurant_id, "user_id": user_id}
