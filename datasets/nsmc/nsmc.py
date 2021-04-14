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
"""Naver movie review corpus for binary sentiment classification"""


import csv

import datasets


_CITATION = """\
@InProceedings{Park:2016,
  title        = "Naver Sentiment Movie Corpus",
  author       = "Lucy Park",
  year         = "2016",
  howpublished = {\\url{https://github.com/e9t/nsmc}}
}
"""

_DESCRIPTION = """\
This is a movie review dataset in the Korean language. Reviews were scraped from Naver movies. The dataset construction is based on the method noted in Large movie review dataset from Maas et al., 2011.
"""

_HOMEPAGE = "https://github.com/e9t/nsmc/"

_LICENSE = "CC0 1.0 Universal (CC0 1.0)"


_URL = "https://raw.githubusercontent.com/e9t/nsmc/master/"
_URLs = {
    "train": _URL + "ratings_train.txt",
    "test": _URL + "ratings_test.txt",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class NSMC(datasets.GeneratorBasedBuilder):
    """Korean Naver movie review dataset."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "document": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["negative", "positive"]),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_files = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": downloaded_files["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": downloaded_files["test"],
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            next(f)
            reader = csv.reader(f, delimiter="\t")
            for id_, row in enumerate(reader):
                yield id_, {
                    "id": row[0],
                    "document": row[1],
                    "label": int(row[2]),
                }
