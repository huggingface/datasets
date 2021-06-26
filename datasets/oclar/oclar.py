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
"""Opinion Corpus for Lebanese Arabic Reviews (OCLAR) Data Set"""


import csv

import datasets


_CITATION = """
@misc{Dua:2019 ,
author = "Dua, Dheeru and Graff, Casey",
year = "2017",
title = "{UCI} Machine Learning Repository",
url = "http://archive.ics.uci.edu/ml",
institution = "University of California, Irvine, School of Information and Computer Sciences" }

@InProceedings{AlOmari2019oclar,
title = {Sentiment Classifier: Logistic Regression for Arabic Services Reviews in Lebanon},
authors={Al Omari, M., Al-Hajj, M., Hammami, N., & Sabra, A.},
year={2019}
}
"""

_DESCRIPTION = """\
The researchers of OCLAR Marwan et al. (2019), they gathered Arabic costumer reviews from Google reviewsa and Zomato
website (https://www.zomato.com/lebanon) on wide scope of domain, including restaurants, hotels, hospitals, local shops,
etc.The corpus finally contains 3916 reviews in 5-rating scale. For this research purpose, the positive class considers
rating stars from 5 to 3 of 3465 reviews, and the negative class is represented from values of 1 and 2 of about
451 texts.
"""

_HOMEPAGE = "http://archive.ics.uci.edu/ml/datasets/Opinion+Corpus+for+Lebanese+Arabic+Reviews+%28OCLAR%29#"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

_URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/00499/OCLAR%20-%20Opinion%20Corpus%20for%20Lebanese%20Arabic%20Reviews.csv"


class Oclar(datasets.GeneratorBasedBuilder):
    """TOpinion Corpus for Lebanese Arabic Reviews (OCLAR) corpus is utilizable for Arabic sentiment classification on
    services reviews, including hotels, restaurants, shops, and others.
    """

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "pagename": datasets.Value("string"),
                    "review": datasets.Value("string"),
                    "rating": datasets.Value("int8"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_path,
                    "split": "train",
                },
            )
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", skipinitialspace=True)
            next(csv_reader, None)  # skipping headers
            for id_, row in enumerate(csv_reader):
                pagename, review, rating = row
                rating = int(rating)
                yield id_, {"pagename": pagename, "review": review, "rating": rating}
