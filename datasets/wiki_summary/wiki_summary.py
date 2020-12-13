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

from __future__ import absolute_import, division, print_function

import csv
import os

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

_TRAIN_FILENAME = "train.csv"
_TEST_FILENAME = "test.csv"
_DEV_FILENAME = "dev.csv"

_ID = "id"
_LINK = "link"
_TITLE = "title"
_ARTICLE = "article"
_HIGHLIGHTS = "highlights"

_HOMEPAGE = "https://github.com/m3hrdadfi/wiki-summary"


class WikiSummary(datasets.GeneratorBasedBuilder):
    """Wiki Summary"""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://github.com/m3hrdadfi/wiki-summary,
    and manually download Version 1.0.0 Train Set, Dev Set, Test Set. Once it is completed,
    3 files named train.csv, dev.csv and test.csv will appear in your Downloads folder
    or whichever folder your browser chooses to save files to.
    You can then move those files under <path/to/folder>.
    The <path/to/folder> can e.g. be "~/manual_data".
    wiki_summary can then be loaded using the following command `datasets.load_dataset("wiki_summary", data_dir="<path/to/folder>")`.
    """

    def _info(self):
        feature_names = [_ID, _LINK, _TITLE, _ARTICLE, _HIGHLIGHTS]
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({k: datasets.Value("string") for k in feature_names}),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path_train = os.path.join(os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), _TRAIN_FILENAME)
        path_test = os.path.join(os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), _DEV_FILENAME)
        path_dev = os.path.join(os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), _TEST_FILENAME)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": path_train}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": path_test}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": path_dev}),
        ]

    def _generate_examples(self, filepath):
        """Generate Wiki summary examples."""
        with open(filepath, encoding="utf8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            for id_, row in enumerate(csv_reader):
                row = row[0].split("\t")
                if len(row) == 5:
                    yield id_, {_ID: row[0], _LINK: row[1], _TITLE: row[2], _ARTICLE: row[3], _HIGHLIGHTS: row[4]}
