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


import csv
import os

import datasets


_CITATION = """\
@InProceedings{kaggle:dataset,
title = {Telugu News - Natural Language Processing for Indian Languages},
authors={Sudalai Rajkumar, Anusha Motamarri},
year={2019}
}
"""

# You can copy an official description
_DESCRIPTION = """\
This dataset contains Telugu language news articles along with respective
topic labels (business, editorial, entertainment, nation, sport) extracted from
the daily Andhra Jyoti. This dataset could be used to build Classification and Language Models.
"""

_HOMEPAGE = "https://www.kaggle.com/sudalairajkumar/telugu-nlp"

_LICENSE = "Data files © Original Authors"


class TeluguNews(datasets.GeneratorBasedBuilder):
    """Telugu News Articles with Topics."""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
    You need to visit Kaggle @ https://www.kaggle.com/sudalairajkumar/telugu-nlp,
    and manually download the `telugu_news` dataset. This will download a file called
    `telugu_news.zip` to your laptop. Unzip the file and move the two CSV files
    (train and test) files to <path/to/folder>. You can then use
    `datasets.load_dataset("telugu_news", data_dir="<path/to/folder>")` to load the datset.
    """

    def _info(self):
        features = datasets.Features(
            {
                "sno": datasets.Value("int32"),
                "date": datasets.Value("string"),
                "heading": datasets.Value("string"),
                "body": datasets.Value("string"),
                "topic": datasets.features.ClassLabel(
                    names=["business", "editorial", "entertainment", "nation", "sports"],
                ),
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
                f"{data_dir} does not exist. Download instructions: {self.manual_download_instructions} "
            )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train_telugu_news.csv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test_telugu_news.csv"),
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)  # skip the headers

            for id_, row in enumerate(csv_reader):
                sno, date, heading, body, topic = row
                yield id_, {
                    "sno": sno,
                    "date": date,
                    "heading": heading,
                    "body": body,
                    "topic": topic,
                }
