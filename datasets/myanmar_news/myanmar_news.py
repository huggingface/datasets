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

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


# no BibTeX citation
_CITATION = ""

_DESCRIPTION = """\
The Myanmar news dataset contains article snippets in four categories:
Business, Entertainment, Politics, and Sport.

These were collected in October 2017 by Aye Hninn Khine
"""

_LICENSE = "GPL-3.0"

_URLs = {"default": "https://github.com/Georeactor/MyanmarNewsClassificationSystem/archive/main.zip"}


class MyanmarNews(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.1")

    def _info(self):
        class_names = ["Sport", "Politic", "Business", "Entertainment"]
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
                "category": datasets.ClassLabel(names=class_names),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://github.com/ayehninnkhine/MyanmarNewsClassificationSystem",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "MyanmarNewsClassificationSystem-main", "topics.csv"),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            rdr = csv.reader(f, delimiter="\t")
            next(rdr)
            rownum = 0
            for row in rdr:
                rownum += 1
                yield rownum, {
                    "text": row[0],
                    "category": row[1],
                }
