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
"""Korean Sarcasm Detection Dataset"""


import csv

import datasets
from datasets.tasks import TextClassification


_DESCRIPTION = """\
This is a dataset designed to detect sarcasm in Korean because it distorts the literal meaning of a sentence
and is highly related to sentiment classification.
"""

_HOMEPAGE = "https://github.com/SpellOnYou/korean-sarcasm"

_LICENSE = "MIT License"

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/SpellOnYou/korean-sarcasm/master/data/jiwon/train.csv"
_TEST_DOWNLOAD_URL = "https://raw.githubusercontent.com/SpellOnYou/korean-sarcasm/master/data/jiwon/test.csv"


class KorSarcasm(datasets.GeneratorBasedBuilder):
    """Korean Sarcasm Detection Dataset"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "tokens": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["no_sarcasm", "sarcasm"]),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            task_templates=[TextClassification(text_column="tokens", label_column="label")],
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
        """Generate Korean sarcasm examples"""

        with open(filepath, encoding="utf-8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            next(data, None)
            for id_, row in enumerate(data):
                row = row[1:3]
                tokens, label = row
                yield id_, {"tokens": tokens, "label": int(label)}
