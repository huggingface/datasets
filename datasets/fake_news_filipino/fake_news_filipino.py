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
"""Fake News Filipino Dataset"""

import csv
import os

import datasets
from datasets.tasks import TextClassification


_DESCRIPTION = """\
    Low-Resource Fake News Detection Corpora in Filipino. The first of its kind. Contains 3,206 expertly-labeled news samples, half of which are real and half of which are fake.
"""

_CITATION = """\
    @inproceedings{cruz2020localization,
      title={Localization of Fake News Detection via Multitask Transfer Learning},
      author={Cruz, Jan Christian Blaise and Tan, Julianne Agatha and Cheng, Charibeth},
      booktitle={Proceedings of The 12th Language Resources and Evaluation Conference},
      pages={2596--2604},
      year={2020}
    }
"""

_HOMEPAGE = "https://github.com/jcblaisecruz02/Tagalog-fake-news"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

_URL = "https://s3.us-east-2.amazonaws.com/blaisecruz.com/datasets/fakenews/fakenews.zip"


class FakeNewsFilipino(datasets.GeneratorBasedBuilder):
    """Low-Resource Fake News Detection Corpora in Filipino"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {"label": datasets.features.ClassLabel(names=["0", "1"]), "article": datasets.Value("string")}
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[TextClassification(text_column="article", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        train_path = os.path.join(data_dir, "fakenews", "full.csv")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": train_path,
                    "split": "train",
                },
            )
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)
            for id_, row in enumerate(csv_reader):
                label, article = row
                yield id_, {"label": label, "article": article}
