# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""HebrewThisWorld: A corpus from https://thisworld.online/."""


import csv
import ctypes

import datasets


_DESCRIPTION = """\
HebrewThisWorld is a data set consists of 2028 issues of the newspaper 'This World' edited by Uri Avnery and were published between 1950 and 1989. Released under the AGPLv3 license."""

csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

_TRAIN_DOWNLOAD_URLS = [
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_0.csv",
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_1.csv",
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_2.csv",
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_3.csv",
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_4.csv",
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_5.csv",
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_6.csv",
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_7.csv",
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_8.csv",
    "https://github.com/imvladikon/datasets_additional/raw/master/data/thisworld1/metadata_9.csv",
]


class HebrewThisWorld(datasets.GeneratorBasedBuilder):
    """HebrewThisWorld: Corpus from the newspaper ThisWorld"""

    VERSION = datasets.Version("0.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "issue_num": datasets.Value("int64"),
                    "page_count": datasets.Value("int64"),
                    "date": datasets.Value("string"),
                    "date_he": datasets.Value("string"),
                    "year": datasets.Value("string"),
                    "href": datasets.Value("string"),
                    "pdf": datasets.Value("string"),
                    "coverpage": datasets.Value("string"),
                    "backpage": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "url": datasets.Value("string"),
                }
            ),
            homepage="https://github.com/thisworld1/thisworld.online/",
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URLS)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Hebrew ThisWorld examples."""
        for file in filepath:
            with open(file, encoding="utf-8") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for data in csv_reader:
                    id_ = data["issue_num"]
                    yield id_, {
                        "issue_num": data["issue_num"],
                        "page_count": data["page_count"],
                        "date": data["date"],
                        "date_he": data["date_he"],
                        "year": data["year"],
                        "href": data["href"],
                        "pdf": data["pdf"],
                        "coverpage": data["coverpage"],
                        "backpage": data["backpage"],
                        "content": data["content"],
                        "url": data["url"],
                    }
