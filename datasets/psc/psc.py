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
"""Polish Summaries Corpus"""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{ogro:kop:14:lrec,
title={The {P}olish {S}ummaries {C}orpus},
author={Ogrodniczuk, Maciej and Kope{\'c}, Mateusz},
booktitle = "Proceedings of the Ninth International {C}onference on {L}anguage {R}esources and {E}valuation, {LREC}~2014",
year = "2014",
}
"""

_DESCRIPTION = """\
The Polish Summaries Corpus contains news articles and their summaries. We used summaries of the same article as positive pairs and sampled the most similar summaries of different articles as negatives.
"""

_HOMEPAGE = "http://zil.ipipan.waw.pl/PolishSummariesCorpus"

_LICENSE = "CC BY-SA 3.0"

_URLs = "https://klejbenchmark.com/static/data/klej_psc.zip"


class PSC(datasets.GeneratorBasedBuilder):
    """Polish Summaries Corpus"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "extract_text": datasets.Value("string"),
                    "summary_text": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["0", "1"]),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.tsv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "test_features.tsv"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for id_, row in enumerate(reader):
                yield id_, {
                    "extract_text": row["extract_text"],
                    "summary_text": row["summary_text"],
                    "label": -1 if split == "test" else row["label"],
                }
