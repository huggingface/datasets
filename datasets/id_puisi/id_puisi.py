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

# Lint as: python3
"""ID Puisi: A Dataset for Indonesian Poem"""


import csv

import datasets


_DESCRIPTION = """\
Puisi (poem) is an Indonesian poetic form. The dataset contains 7223 Indonesian puisi with its title and author.
"""

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/ilhamfp/puisi-pantun-generator/main/data/puisi.csv"


class IDPuisi(datasets.GeneratorBasedBuilder):
    """ID Puisi: A Datases for Indonesian Poem"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "author": datasets.Value("string"),
                    "puisi": datasets.Value("string"),
                    "puisi_with_header": datasets.Value("string"),
                }
            ),
            homepage="https://github.com/ilhamfp/puisi-pantun-generator",
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": train_path,
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Generate ID Puisi examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file,
                delimiter=",",
                quoting=csv.QUOTE_ALL,
            )
            for id_, row in enumerate(csv_reader):
                if id_ == 0:
                    # Skip header
                    continue

                yield id_, {"puisi": row[0], "title": row[1], "author": row[2], "puisi_with_header": row[3]}
