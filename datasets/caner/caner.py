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
"""A new corpus of tagged data that can be useful for handling the issues in recognition of Classical Arabic named entities"""


import csv
import os

import datasets


_CITATION = """\
@article{article,
author = {Salah, Ramzi and Zakaria, Lailatul},
year = {2018},
month = {12},
pages = {},
title = {BUILDING THE CLASSICAL ARABIC NAMED ENTITY RECOGNITION CORPUS (CANERCORPUS)},
volume = {96},
journal = {Journal of Theoretical and Applied Information Technology}
}
"""

_DESCRIPTION = """\
Classical Arabic Named Entity Recognition corpus as a new corpus of tagged data that can be useful for handling the issues in recognition of Arabic named entities.
"""

_HOMEPAGE = "https://github.com/RamziSalah/Classical-Arabic-Named-Entity-Recognition-Corpus"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

_URL = "https://github.com/RamziSalah/Classical-Arabic-Named-Entity-Recognition-Corpus/archive/master.zip"


class Caner(datasets.GeneratorBasedBuilder):
    """Classical Arabic Named Entity Recognition corpus as a new corpus of tagged data that can be useful for handling the issues in recognition of Arabic named entities"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        features = datasets.Features(
            {
                "token": datasets.Value("string"),
                "ner_tag": datasets.ClassLabel(
                    names=[
                        "Allah",
                        "Book",
                        "Clan",
                        "Crime",
                        "Date",
                        "Day",
                        "Hell",
                        "Loc",
                        "Meas",
                        "Mon",
                        "Month",
                        "NatOb",
                        "Number",
                        "O",
                        "Org",
                        "Para",
                        "Pers",
                        "Prophet",
                        "Rlig",
                        "Sect",
                        "Time",
                    ]
                ),
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

        my_urls = _URL
        data_dir = dl_manager.download_and_extract(my_urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir, "Classical-Arabic-Named-Entity-Recognition-Corpus-master/CANERCorpus.csv"
                    ),
                    "split": "train",
                },
            )
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            next(reader, None)

            for id_, row in enumerate(reader):

                yield id_, {
                    "token": row[0],
                    "ner_tag": row[1],
                }
