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
"""Ten Thousand German News Articles Dataset"""


import csv

import datasets
from datasets.tasks import TextClassification


_DESCRIPTION = """\
This dataset is intended to advance topic classification for German texts. A classifier that is efffective in
English may not be effective in German dataset because it has a higher inflection and longer compound words.
The 10kGNAD dataset contains 10273 German news articles from an Austrian online newspaper categorized into
9 categories. Article titles and text are concatenated together and authors are removed to avoid a keyword-like
classification on authors that write frequently about one category. This dataset can be used as a benchmark
for German topic classification.
"""

_HOMEPAGE = "https://tblock.github.io/10kGNAD/"

_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 4.0"

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/tblock/10kGNAD/master/train.csv"
_TEST_DOWNLOAD_URL = "https://raw.githubusercontent.com/tblock/10kGNAD/master/test.csv"


class Gnad10(datasets.GeneratorBasedBuilder):
    """10k German news articles for topic classification"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "Web",
                            "Panorama",
                            "International",
                            "Wirtschaft",
                            "Sport",
                            "Inland",
                            "Etat",
                            "Wissenschaft",
                            "Kultur",
                        ]
                    ),
                }
            ),
            homepage="https://tblock.github.io/10kGNAD/",
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate German news articles examples."""

        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";", quotechar="'", quoting=csv.QUOTE_ALL)
            for id_, row in enumerate(csv_reader):
                label, text = row
                yield id_, {"text": text, "label": label}
