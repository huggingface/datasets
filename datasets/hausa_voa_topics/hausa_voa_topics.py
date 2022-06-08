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
"""Hausa VOA News Topic Classification dataset."""


import csv

import datasets
from datasets.tasks import TextClassification


_DESCRIPTION = """\
A collection of news article headlines in Hausa from VOA Hausa.
Each headline is labeled with one of the following classes: Nigeria,
Africa, World, Health or Politics.

The dataset was presented in the paper:
Hedderich, Adelani, Zhu, Alabi, Markus, Klakow: Transfer Learning and
Distant Supervision for Multilingual Transformer Models: A Study on
African Languages (EMNLP 2020).
"""

_CITATION = """\
@inproceedings{hedderich-etal-2020-transfer,
    title = "Transfer Learning and Distant Supervision for Multilingual Transformer Models: A Study on African Languages",
    author = "Hedderich, Michael A.  and
      Adelani, David  and
      Zhu, Dawei  and
      Alabi, Jesujoba  and
      Markus, Udia  and
      Klakow, Dietrich",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    year = "2020",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.204",
    doi = "10.18653/v1/2020.emnlp-main.204",
}
"""

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/uds-lsv/transfer-distant-transformer-african/master/data/hausa_newsclass/train_clean.tsv"
_VALIDATION_DOWNLOAD_URL = "https://raw.githubusercontent.com/uds-lsv/transfer-distant-transformer-african/master/data/hausa_newsclass/dev.tsv"
_TEST_DOWNLOAD_URL = "https://raw.githubusercontent.com/uds-lsv/transfer-distant-transformer-african/master/data/hausa_newsclass/test.tsv"


class HausaVOATopics(datasets.GeneratorBasedBuilder):
    """Hausa VOA News Topic Classification dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "news_title": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["Africa", "Health", "Nigeria", "Politics", "World"]),
                }
            ),
            homepage="https://github.com/uds-lsv/transfer-distant-transformer-african",
            citation=_CITATION,
            task_templates=[TextClassification(text_column="news_title", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        validation_path = dl_manager.download_and_extract(_VALIDATION_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": validation_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Hausa VOA News Topic examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter="\t")
            for id_, row in enumerate(csv_reader):
                yield id_, {"news_title": row["news_title"], "label": row["label"]}
