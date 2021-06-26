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
"""Eduge news topic classification dataset."""


import csv

import datasets
from datasets.tasks import TextClassification


_DESCRIPTION = """\
Eduge news classification dataset is provided by Bolorsoft LLC. It is used for training the Eduge.mn production news classifier
75K news articles in 9 categories: урлаг соёл, эдийн засаг, эрүүл мэнд, хууль, улс төр, спорт, технологи, боловсрол and байгал орчин
"""

_TRAIN_DOWNLOAD_URL = "https://storage.googleapis.com/eduge_dataset/eduge_train.csv"
_TEST_DOWNLOAD_URL = "https://storage.googleapis.com/eduge_dataset/eduge_test.csv"


class Eduge(datasets.GeneratorBasedBuilder):
    """Eduge news topic classification dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "news": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "урлаг соёл",
                            "эдийн засаг",
                            "эрүүл мэнд",
                            "хууль",
                            "улс төр",
                            "спорт",
                            "технологи",
                            "боловсрол",
                            "байгал орчин",
                        ]
                    ),
                }
            ),
            homepage="http://eduge.mn",
            task_templates=[
                TextClassification(
                    text_column="news",
                    label_column="label",
                )
            ],
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Eduge news examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)
            for id_, row in enumerate(csv_reader):
                news, label = row[0], row[1]
                yield id_, {"news": news, "label": label}
