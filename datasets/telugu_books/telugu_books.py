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
"""Telugu Books Dataset"""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


_CITATION = """\
@InProceedings{huggingface:dataset,
title = {Indic NLP - Natural Language Processing for Indian Languages},
authors = {Sudalai Rajkumar, Anusha Motamarri},
year={2019}
}
"""

_DESCRIPTION = """\
This dataset is created by scraping telugu novels from teluguone.com and can be used for nlp tasks like topic modeling, word embeddings, transfer learning etc
"""

_HOMEPAGE = "https://www.kaggle.com/sudalairajkumar/telugu-nlp"

_LICENSE = "Data files © Original Authors"


class TeluguBooks(datasets.GeneratorBasedBuilder):
    """Telugu novels"""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
      You should download the dataset from https://www.kaggle.com/sudalairajkumar/telugu-nlp
      The webpage requires registration. After downloading please unzip the file,
      and place telugu_books.csv in the dir of your choice and load the dataset
      by passing the same path Eg. if you place in 
      `~/datasets/telugu_nlp/telugu_books.csv` 
      the dataset can be loaded using the command
       `datasets.load_dataset("telugu_books", data_dir="~/datasets/telugu_nlp/telugu_books.csv")`.
      """

    def _info(self):
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via \
                 `datasets.load_dataset('telugu_books', data_dir=...)` that includes \
                  files unzipped. Manual download instructions: {}".format(
                    data_dir, self.manual_download_instructions,
                )
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "telugu_books.csv"),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for id_, row in enumerate(csv_reader):
                _, text = row
                yield id_, {"text": text}
