# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""Wiki Summary."""


import csv

import datasets


_DESCRIPTION = """\
The dataset extracted from Persian Wikipedia into the form of articles and highlights and cleaned the dataset into pairs of articles and highlights and reduced the articles' length (only version 1.0.0) and highlights' length to a maximum of 512 and 128, respectively, suitable for parsBERT.
"""

_CITATION = """\
@misc{Bert2BertWikiSummaryPersian,
  author = {Mehrdad Farahani},
  title = {Summarization using Bert2Bert model on WikiSummary dataset},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {https://github.com/m3hrdadfi/wiki-summary},
}
"""

_ID = "id"
_LINK = "link"
_TITLE = "title"
_ARTICLE = "article"
_HIGHLIGHTS = "highlights"

_HOMEPAGE = "https://github.com/m3hrdadfi/wiki-summary"

_TRAIN_DOWNLOAD_URL = "https://drive.google.com/u/0/uc?id=1-CaP3xHgZxOGjQ3pXC5tr9YnIajmel-t&export=download"
_TEST_DOWNLOAD_URL = "https://drive.google.com/u/0/uc?id=1-9G4yYP6YO8oMA-o4cTe9NJpEyr7x5jg&export=download"
_DEV_DOWNLOAD_URL = "https://drive.google.com/u/0/uc?id=1-2g2gkDeNaN-vth-8Mgit_ovmSkVh91u&export=download"


class WikiSummary(datasets.GeneratorBasedBuilder):
    """Wiki Summary"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        feature_names = [_ID, _LINK, _TITLE, _ARTICLE, _HIGHLIGHTS]
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({k: datasets.Value("string") for k in feature_names}),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path_train = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        path_test = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        path_dev = dl_manager.download_and_extract(_DEV_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": path_train}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": path_test}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": path_dev}),
        ]

    def _generate_examples(self, filepath):
        """Generate Wiki summary examples."""
        with open(filepath, encoding="utf8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            for id_, row in enumerate(csv_reader):
                if len(row) == 5:
                    yield id_, {_ID: row[0], _LINK: row[1], _TITLE: row[2], _ARTICLE: row[3], _HIGHLIGHTS: row[4]}
