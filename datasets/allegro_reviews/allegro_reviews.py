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
"""Allegro Reviews dataset"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@inproceedings{rybak-etal-2020-klej,
    title = "{KLEJ}: Comprehensive Benchmark for Polish Language Understanding",
    author = "Rybak, Piotr and Mroczkowski, Robert and Tracz, Janusz and Gawlik, Ireneusz",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.111",
    pages = "1191--1201",
}
"""

_DESCRIPTION = """\
Allegro Reviews is a sentiment analysis dataset, consisting of 11,588 product reviews written in Polish and extracted
from Allegro.pl - a popular e-commerce marketplace. Each review contains at least 50 words and has a rating on a scale
from one (negative review) to five (positive review).

We recommend using the provided train/dev/test split. The ratings for the test set reviews are kept hidden.
You can evaluate your model using the online evaluation tool available on klejbenchmark.com.
"""

_HOMEPAGE = "https://github.com/allegro/klejbenchmark-allegroreviews"

_LICENSE = "CC BY-SA 4.0"

_URLs = "https://klejbenchmark.com/static/data/klej_ar.zip"


class AllegroReviews(datasets.GeneratorBasedBuilder):
    """
    Allegro Reviews is a sentiment analysis dataset, consisting of 11,588 product reviews written in Polish
    and extracted from Allegro.pl - a popular e-commerce marketplace.
    """

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "rating": datasets.Value("float"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.tsv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "test_features.tsv"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.tsv"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for id_, row in enumerate(reader):
                yield id_, {
                    "text": row["text"],
                    "rating": "-1" if split == "test" else row["rating"],
                }
