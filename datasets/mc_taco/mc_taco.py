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
"""MC-TACO Dataset."""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_CITATION = """\
@inproceedings{ZKNR19,
    author = {Ben Zhou, Daniel Khashabi, Qiang Ning and Dan Roth},
    title = {“Going on a vacation” takes longer than “Going for a walk”: A Study of Temporal Commonsense Understanding },
    booktitle = {EMNLP},
    year = {2019},
}
"""

_DESCRIPTION = """\
MC-TACO (Multiple Choice TemporAl COmmonsense) is a dataset of 13k question-answer
pairs that require temporal commonsense comprehension. A system receives a sentence
providing context information, a question designed to require temporal commonsense
knowledge, and multiple candidate answers. More than one candidate answer can be plausible.

The task is framed as binary classification: givent he context, the question,
and the candidate answer, the task is to determine whether the candidate
answer is plausible ("yes") or not ("no")."""

_LICENSE = "Unknown"

_URLs = {
    "dev": "https://raw.githubusercontent.com/CogComp/MCTACO/master/dataset/dev_3783.tsv",
    "test": "https://raw.githubusercontent.com/CogComp/MCTACO/master/dataset/test_9442.tsv",
}


class McTaco(datasets.GeneratorBasedBuilder):
    """MC-TACO Dataset: temporal commonsense knowledge."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            description="Plain text",
            version=VERSION,
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["no", "yes"]),
                    "category": datasets.ClassLabel(
                        names=["Event Duration", "Event Ordering", "Frequency", "Typical Time", "Stationarity"]
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://cogcomp.seas.upenn.edu/page/resource_view/125",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": data_dir["test"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_dir["dev"],
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file,
                delimiter="\t",
            )
            for id_, row in enumerate(csv_reader):
                yield id_, {
                    "sentence": row[0],
                    "question": row[1],
                    "answer": row[2],
                    "label": row[3],
                    "category": row[4],
                }
