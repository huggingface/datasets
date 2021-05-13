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
"""FACTCK.BR: A dataset to study Fake News in Portuguese."""


import csv

import datasets


_CITATION = """
    @inproceedings{10.1145/3323503.3361698,
    author = {Moreno, Jo\\~{a}o and Bressan, Gra\\c{c}a},
    title = {FACTCK.BR: A New Dataset to Study Fake News},
    year = {2019},
    isbn = {9781450367639},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3323503.3361698},
    doi = {10.1145/3323503.3361698},
    abstract = {Machine learning algorithms can be used to combat fake news propagation. For the news classification, labeled datasets are required, however, among the existing datasets, few separate verified false from skewed ones with a good variety of sources. This work presents FACTCK.BR, a new dataset to study Fake News in Portuguese, presenting a supposedly false News along with their respective fact check and classification. The data is collected from the ClaimReview, a structured data schema used by fact check agencies to share their results in search engines, enabling data collect in real time.},
    booktitle = {Proceedings of the 25th Brazillian Symposium on Multimedia and the Web},
    pages = {525–527},
    numpages = {3},
    keywords = {fake news, fact check, information extraction, dataset},
    location = {Rio de Janeiro, Brazil},
    series = {WebMedia '19}
}
"""

_DESCRIPTION = """\
A dataset to study Fake News in Portuguese, presenting a supposedly false News along with their respective fact check and classification.
The data is collected from the ClaimReview, a structured data schema used by fact check agencies to share their results in search engines, enabling data collect in real time.
The FACTCK.BR dataset contains 1309 claims with its corresponding label.
"""

_HOMEPAGE = "https://github.com/jghm-f/FACTCK.BR"

_LICENSE = "MIT"

_URL = "https://github.com/jghm-f/FACTCK.BR/raw/master/FACTCKBR.tsv"


class Factckbr(datasets.GeneratorBasedBuilder):
    """FACTCK.BR: A dataset to study Fake News in Portuguese."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "url": datasets.Value("string"),
                    "author": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "claim": datasets.Value("string"),
                    "review": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "rating": datasets.Value("float"),
                    "best_rating": datasets.Value("float"),
                    "label": datasets.ClassLabel(
                        names=[
                            "falso",
                            "distorcido",
                            "impreciso",
                            "exagerado",
                            "insustentável",
                            "verdadeiro",
                            "outros",
                            "subestimado",
                            "impossível provar",
                            "discutível",
                            "sem contexto",
                            "de olho",
                            "verdadeiro, mas",
                            "ainda é cedo para dizer",
                        ]
                    ),
                }
            ),
            supervised_keys=("claim", "label"),
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

        with open(filepath, encoding="utf-8") as tsv_file:
            reader = csv.reader(tsv_file, delimiter="\t")
            for id_, row in enumerate(reader):
                if id_ == 0:
                    continue

                label = row[8].lower()

                yield id_, {
                    "url": row[0],
                    "author": row[1],
                    "date": row[2],
                    "claim": row[3],
                    "review": row[4],
                    "title": row[5],
                    "rating": row[6] or 0,
                    "best_rating": row[7],
                    "label": -1 if label == "" else label,
                }
