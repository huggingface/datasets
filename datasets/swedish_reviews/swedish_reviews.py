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


import csv
import os

import datasets
from datasets.tasks import TextClassification


_DOWNLOAD_URL = "https://raw.githubusercontent.com/timpal0l/swedish-sentiment/main/swedish_sentiment.zip"
_TRAIN_FILE = "train.csv"
_VAL_FILE = "dev.csv"
_TEST_FILE = "test.csv"

_CITATION = ""

_DESCRIPTION = "Swedish reviews scarped from various public available websites"


class SwedishReviews(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of the Swedish Reviews dataset",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"text": datasets.Value("string"), "label": datasets.ClassLabel(names=["negative", "positive"])}
            ),
            supervised_keys=None,
            homepage="https://github.com/timpal0l/swedish-sentiment",
            citation=_CITATION,
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(dl_dir, _TEST_FILE)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(dl_dir, _VAL_FILE)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(dl_dir, _TRAIN_FILE)},
            ),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                yield idx, {
                    "text": row["text"],
                    "label": row["sentiment"],
                }
