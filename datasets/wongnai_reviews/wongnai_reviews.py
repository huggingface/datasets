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
"""TODO: Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


# no BibTeX citation
_CITATION = ""

_DESCRIPTION = """\
Wongnai's review dataset contains restaurant reviews and ratings, mainly in Thai language.
The reviews are in 5 classes ranging from 1 to 5 stars.
"""

_LICENSE = "LGPL-3.0"

_URLs = {"default": "https://github.com/wongnai/wongnai-corpus/raw/master/review/review_dataset.zip"}


class WongnaiReviews(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.1")

    def _info(self):
        features = datasets.Features(
            {
                "review_body": datasets.Value("string"),
                "star_rating": datasets.Value("int32"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://github.com/wongnai/wongnai-corpus",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, "w_review_train.csv"), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "test_file.csv"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            rdr = csv.reader(f, delimiter=";")
            if split == "test":
                # drop test header
                next(rdr)
            rownum = 0
            for row in rdr:
                rownum += 1
                id = row[0] if split == "test" else rownum
                yield id, {
                    "review_body": row[1] if split == "test" else row[0],
                    "star_rating": -1 if split == "test" else int(row[1]),
                }
