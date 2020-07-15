# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""Quora question pairs data"""

from __future__ import absolute_import, division, print_function

import collections
import csv

import nlp


_DESCRIPTION = "The Quora dataset is composed of question pairs, and the task is to determine if the questions are paraphrases of each other (have the same meaning)."

_URL = "http://qim.fs.quoracdn.net/quora_duplicate_questions.tsv"


class Quora(nlp.GeneratorBasedBuilder):
    """Quora Question Pairs dataset"""

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "questions": nlp.features.Sequence({"id": nlp.Value("int32"), "text": nlp.Value("string"),}),
                    "is_duplicate": nlp.Value("bool"),
                }
            ),
            homepage="https://www.quora.com/q/quoradata/First-Quora-Dataset-Release-Question-Pairs",
        )

    def _split_generators(self, dl_manager):
        data_file = dl_manager.download_and_extract({"data_file": _URL})
        return [nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs=data_file)]

    def _generate_examples(self, data_file):
        with open(data_file) as f:
            data = csv.DictReader(f, delimiter="\t")
            for idx, row in enumerate(data):
                yield idx, {
                    "questions": [
                        {"id": row["qid1"], "text": row["question1"]},
                        {"id": row["qid2"], "text": row["question2"]},
                    ],
                    "is_duplicate": row["is_duplicate"] == "1",
                }
