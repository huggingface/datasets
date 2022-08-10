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
"""Did You Know? dataset"""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{marcinczuk2013open,
title={Open dataset for development of Polish Question Answering systems},
author={Marcinczuk, Michal and Ptak, Marcin and Radziszewski, Adam and Piasecki, Maciej},
booktitle={Proceedings of the 6th Language & Technology Conference: Human Language Technologies as a Challenge for Computer Science and Linguistics, Wydawnictwo Poznanskie, Fundacja Uniwersytetu im. Adama Mickiewicza},
year={2013}
}
"""

_DESCRIPTION = """\
The Did You Know (pol. Czy wiesz?) dataset consists of human-annotated question-answer pairs. The task is to predict if the answer is correct. We chose the negatives which have the largest token overlap with a question.
"""

_HOMEPAGE = "http://nlp.pwr.wroc.pl/en/tools-and-resources/resources/czy-wiesz-question-answering-dataset"

_LICENSE = "CC BY-SA 3.0"

_URLs = "https://klejbenchmark.com/static/data/klej_dyk.zip"


class DYK(datasets.GeneratorBasedBuilder):
    """Did You Know? Dataset"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "q_id": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "target": datasets.ClassLabel(names=["0", "1"]),
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
                    "q_id": row["q_id"],
                    "question": row["question"],
                    "answer": row["answer"],
                    "target": -1 if split == "test" else row["target"],
                }
