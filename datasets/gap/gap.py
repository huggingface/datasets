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
"""GAP is a gender-balanced text data set."""


import csv

import datasets


_CITATION = """
@article{DBLP:journals/corr/abs-1810-05201,
  author    = {Kellie Webster and
               Marta Recasens and
               Vera Axelrod and
               Jason Baldridge},
  title     = {Mind the {GAP:} {A} Balanced Corpus of Gendered Ambiguous Pronouns},
  journal   = {CoRR},
  volume    = {abs/1810.05201},
  year      = {2018},
  url       = {http://arxiv.org/abs/1810.05201},
  archivePrefix = {arXiv},
  eprint    = {1810.05201},
  timestamp = {Tue, 30 Oct 2018 20:39:56 +0100},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1810-05201},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """
GAP is a gender-balanced dataset containing 8,908 coreference-labeled pairs of
(ambiguous pronoun, antecedent name), sampled from Wikipedia and released by
Google AI Language for the evaluation of coreference resolution in practical
applications.
"""

_TRAINURL = "https://raw.githubusercontent.com/google-research-datasets/gap-coreference/master/gap-development.tsv"
_VALIDATIONURL = "https://raw.githubusercontent.com/google-research-datasets/gap-coreference/master/gap-validation.tsv"
_TESTURL = "https://raw.githubusercontent.com/google-research-datasets/gap-coreference/master/gap-test.tsv"


class Gap(datasets.GeneratorBasedBuilder):
    """GAP is a gender-balanced dataset.

    It contains 8,908 coreference-labeled pairs
    of (ambiguous pronoun, antecedent name), sampled from Wikipedia.
    """

    VERSION = datasets.Version("0.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "ID": datasets.Value("string"),
                    "Text": datasets.Value("string"),
                    "Pronoun": datasets.Value("string"),
                    "Pronoun-offset": datasets.Value("int32"),
                    "A": datasets.Value("string"),
                    "A-offset": datasets.Value("int32"),
                    "A-coref": datasets.Value("bool"),
                    "B": datasets.Value("string"),
                    "B-offset": datasets.Value("int32"),
                    "B-coref": datasets.Value("bool"),
                    "URL": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/google-research-datasets/gap-coreference",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        directory = dl_manager.download_and_extract(
            {"train": _TRAINURL, "validation": _VALIDATIONURL, "test": _TESTURL}
        )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": directory["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": directory["validation"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": directory["test"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as tsvfile:
            reader = csv.DictReader(tsvfile, dialect="excel-tab")
            for i, row in enumerate(reader):
                row["A-coref"] = row["A-coref"] == "TRUE"
                row["B-coref"] = row["B-coref"] == "TRUE"
                row["A-offset"] = int(row["A-offset"])
                row["B-offset"] = int(row["B-offset"])
                row["Pronoun-offset"] = int(row["Pronoun-offset"])
                yield i, row
