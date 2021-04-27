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
"""NewsPH-NLI Sentence Entailment Dataset in Filipino"""

import csv
import os

import datasets


_DESCRIPTION = """\
First benchmark dataset for sentence entailment in the low-resource Filipino language.
Constructed through exploting the structure of news articles. Contains 600,000 premise-hypothesis pairs,
in 70-15-15 split for training, validation, and testing.
"""

_CITATION = """\
@article{cruz2020investigating,
    title={Investigating the True Performance of Transformers in Low-Resource Languages: A Case Study in Automatic Corpus Creation},
    author={Jan Christian Blaise Cruz and Jose Kristian Resabal and James Lin and Dan John Velasco and Charibeth Cheng},
    journal={arXiv preprint arXiv:2010.11574},
    year={2020}
}
"""

_HOMEPAGE = "https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "Filipino-Text-Benchmarks is licensed under the GNU General Public License v3.0"

_URL = "https://s3.us-east-2.amazonaws.com/blaisecruz.com/datasets/newsph/newsph-nli.zip"


class NewsphNli(datasets.GeneratorBasedBuilder):
    """NewsPH-NLI Sentence Entailment Dataset in Filipino"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "premise": datasets.Value("string"),
                "hypothesis": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["0", "1"]),
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
        data_dir = dl_manager.download_and_extract(_URL)
        download_path = os.path.join(data_dir, "newsph-nli")
        train_path = os.path.join(download_path, "train.csv")
        test_path = os.path.join(download_path, "test.csv")
        validation_path = os.path.join(download_path, "valid.csv")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": train_path,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": test_path,
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": validation_path,
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)
            for id_, row in enumerate(csv_reader):
                premise, hypothesis, label = row
                yield id_, {"premise": premise, "hypothesis": hypothesis, "label": label}
