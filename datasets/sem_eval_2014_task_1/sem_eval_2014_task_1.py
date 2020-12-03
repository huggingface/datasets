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
"""The SemEval-2014 Task 1 on Evaluation of Compositional Distributional Semantic Models on Full Sentences through Semantic Relatedness and Entailment"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """\
@inproceedings{inproceedings,
author = {Marelli, Marco and Bentivogli, Luisa and Baroni, Marco and Bernardi, Raffaella and Menini, Stefano and Zamparelli, Roberto},
year = {2014},
month = {08},
pages = {},
title = {SemEval-2014 Task 1: Evaluation of Compositional Distributional Semantic Models on Full Sentences through Semantic Relatedness and Textual Entailment},
doi = {10.3115/v1/S14-2001}
}
"""

_DESCRIPTION = """\
The SemEval-2014 Task 1 focuses on Evaluation of Compositional Distributional Semantic Models
on Full Sentences through Semantic Relatedness and Entailment. The task was designed to
predict the degree of relatedness between two sentences and to detect the entailment
relation holding between them.
"""

_HOMEPAGE = "https://alt.qcri.org/semeval2014/task1/"

_URLs = {
    "train": "https://alt.qcri.org/semeval2014/task1/data/uploads/sick_train.zip",
    "test": "https://alt.qcri.org/semeval2014/task1/data/uploads/sick_test_annotated.zip",
    "validation": "https://alt.qcri.org/semeval2014/task1/data/uploads/sick_trial.zip",
}


class SemEval2014Task1(datasets.GeneratorBasedBuilder):
    """The SemEval-2014 Task 1 on Evaluation of Compositional
    Distributional Semantic Models on Full Sentences through
    Semantic Relatedness and Entailment
    """

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "sentence_pair_id": datasets.Value("int64"),
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "relatedness_score": datasets.Value("float32"),
                    "entailment_judgment": datasets.features.ClassLabel(
                        names=["NEUTRAL", "ENTAILMENT", "CONTRADICTION"]
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://alt.qcri.org/semeval2014/task1/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(dl_dir["train"], "SICK_train.txt"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(dl_dir["test"], "SICK_test_annotated.txt"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(dl_dir["validation"], "SICK_trial.txt"),
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open(filepath, "r", encoding="us-ascii") as file:
            lines = file.readlines()

            for idx in range(1, len(lines)):
                features = lines[idx].split("\t")
                sentence_pair_id = features[0]
                premise = features[1]
                hypothesis = features[2]
                relatedness_score = float(features[3])
                entailment_judgment = features[4].strip("\n")

                yield idx, {
                    "sentence_pair_id": sentence_pair_id,
                    "premise": premise,
                    "hypothesis": hypothesis,
                    "relatedness_score": relatedness_score,
                    "entailment_judgment": entailment_judgment,
                }
