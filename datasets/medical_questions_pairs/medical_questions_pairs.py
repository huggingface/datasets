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
"""Medical Question Pairs (MQP) Dataset"""

from __future__ import absolute_import, division, print_function

import csv

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = ""

_DESCRIPTION = """\
This dataset consists of 3048 similar and dissimilar medical question pairs hand-generated and labeled by Curai's doctors.
"""

_HOMEPAGE = "https://github.com/curai/medical-question-pair-dataset"

_LICENSE = ""

_URL = "https://raw.githubusercontent.com/curai/medical-question-pair-dataset/master/mqp.csv"


class MedicalQuestionPairs(datasets.GeneratorBasedBuilder):
    """Medical Question Pairs (MQP) Dataset"""

    def _info(self):
        features = datasets.Features(
            {
                "dr_id": datasets.Value("int32"),
                "question_1": datasets.Value("string"),
                "question_2": datasets.Value("string"),
                "label": datasets.features.ClassLabel(num_classes=2, names=[0, 1]),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_file = dl_manager.download_and_extract({"data_file": _URL})
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs=data_file)]

    def _generate_examples(self, data_file):
        """ Yields examples. """
        with open(data_file, encoding="utf-8") as f:
            data = csv.reader(f)
            for id_, row in enumerate(data):
                yield id_, {
                    "dr_id": row[0],
                    "question_1": row[1],
                    "question_2": row[2],
                    "label": row[3],
                }
