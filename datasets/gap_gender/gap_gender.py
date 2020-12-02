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
"""GAP Coreference dataset"""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_CITATION = """\
@inproceedings{webster2018gap,
  title =     {Mind the GAP: A Balanced Corpus of Gendered Ambiguou},
  author =    {Webster, Kellie and Recasens, Marta and Axelrod, Vera and Baldridge, Jason},
  booktitle = {Transactions of the ACL},
  year =      {2018},
  pages =     {to appear},
}
"""

_DESCRIPTION = """\
Coreference resolution is an important task for natural language understanding
and the resolution of ambiguous pronouns a longstanding challenge. Nonetheless,
existing corpora do not capture ambiguous pronouns in sufficient volume or
diversity to accurately indicate the practical utility of models. Furthermore,
we find gender bias in existing corpora and systems favoring masculine entities.

GAP is a gender-balanced dataset containing 8,908 coreference-labeled pairs of
(ambiguous pronoun, antecedent name), sampled from Wikipedia and released
by Google AI Language for the evaluation of coreference resolution in practical applications."""

_LICENSE = "Unknown"

_URLs = {
    "train": "https://raw.githubusercontent.com/google-research-datasets/gap-coreference/master/gap-development.tsv",
    "validation": "https://raw.githubusercontent.com/google-research-datasets/gap-coreference/master/gap-validation.tsv",
    "test": "https://raw.githubusercontent.com/google-research-datasets/gap-coreference/master/gap-test.tsv",
}


class GapGender(datasets.GeneratorBasedBuilder):
    """Gap coreference dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="plain_text", description="Plain text", version=VERSION),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "ID": datasets.Value("string"),
                    "Text": datasets.Value("string"),
                    "Pronoun": datasets.Value("string"),
                    "Pronoun-offset": datasets.Value("int64"),
                    "A": datasets.Value("string"),
                    "A-offset": datasets.Value("int64"),
                    "A-coref": datasets.Value("string"),
                    "B": datasets.Value("string"),
                    "B-offset": datasets.Value("int64"),
                    "B-coref": datasets.Value("string"),
                    "URL": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="http://goo.gl/language/gap-coreference",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_dir["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": data_dir["test"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": data_dir["validation"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as tsv_file:
            tsv_reader = csv.reader(
                tsv_file,
                delimiter="\t",
            )
            next(tsv_reader)  # skipping header
            for id_, row in enumerate(tsv_reader):
                yield id_, {
                    "ID": row[0],
                    "Text": row[1],
                    "Pronoun": row[2],
                    "Pronoun-offset": row[3],
                    "A": row[4],
                    "A-offset": row[5],
                    "A-coref": row[6],
                    "B": row[7],
                    "B-offset": row[8],
                    "B-coref": row[9],
                    "URL": row[10],
                }
