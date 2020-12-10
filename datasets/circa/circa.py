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
"""Dataset containing polar questions and indirect answers."""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_CITATION = """\
@InProceedings{louis_emnlp2020,
  author =      "Annie Louis and Dan Roth and Filip Radlinski",
  title =       ""{I}'d rather just go to bed": {U}nderstanding {I}ndirect {A}nswers",
  booktitle =   "Proceedings of the 2020 Conference on Empirical Methods
  in Natural Language Processing",
  year =        "2020",
}
"""

_DESCRIPTION = """\
The Circa (meaning ‘approximately’) dataset aims to help machine learning systems
to solve the problem of interpreting indirect answers to polar questions.

The dataset contains pairs of yes/no questions and indirect answers, together with
annotations for the interpretation of the answer. The data is collected in 10
different social conversational situations (eg. food preferences of a friend).

NOTE: There might be missing labels in the dataset and we have replaced them with -1.
The original dataset contains no train/dev/test splits.
"""

_LICENSE = "Creative Commons Attribution 4.0 License"

_DATA_URL = "https://raw.githubusercontent.com/google-research-datasets/circa/main/circa-data.tsv"


class Circa(datasets.GeneratorBasedBuilder):
    """Dataset containing polar questions and indirect answers."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "context": datasets.Value("string"),
                "question-X": datasets.Value("string"),
                "canquestion-X": datasets.Value("string"),
                "answer-Y": datasets.Value("string"),
                "judgements": datasets.Value("string"),
                "goldstandard1": datasets.features.ClassLabel(
                    names=[
                        "Yes",
                        "No",
                        "In the middle, neither yes nor no",
                        "Probably yes / sometimes yes",
                        "Probably no",
                        "Yes, subject to some conditions",
                        "Other",
                        "I am not sure how X will interpret Y’s answer",
                    ]
                ),
                "goldstandard2": datasets.features.ClassLabel(
                    names=[
                        "Yes",
                        "No",
                        "In the middle, neither yes nor no",
                        "Yes, subject to some conditions",
                        "Other",
                    ]
                ),
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/google-research-datasets/circa",
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_DATA_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": train_path,
                    "split": datasets.Split.TRAIN,
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            goldstandard1_labels = [
                "Yes",
                "No",
                "In the middle, neither yes nor no",
                "Probably yes / sometimes yes",
                "Probably no",
                "Yes, subject to some conditions",
                "Other",
                "I am not sure how X will interpret Y’s answer",
            ]
            goldstandard2_labels = [
                "Yes",
                "No",
                "In the middle, neither yes nor no",
                "Yes, subject to some conditions",
                "Other",
            ]
            data = csv.reader(f, delimiter="\t")
            next(data, None)  # skip the headers
            for id_, row in enumerate(data):
                row = [x if x != "nan" else -1 for x in row]
                _, context, question_X, canquestion_X, answer_Y, judgements, goldstandard1, goldstandard2 = row
                if goldstandard1 not in goldstandard1_labels:
                    goldstandard1 = -1
                if goldstandard2 not in goldstandard2_labels:
                    goldstandard2 = -1

                yield id_, {
                    "context": context,
                    "question-X": question_X,
                    "canquestion-X": canquestion_X,
                    "answer-Y": answer_Y,
                    "judgements": judgements,
                    "goldstandard1": goldstandard1,
                    "goldstandard2": goldstandard2,
                }
