# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""The LAMBADA dataset."""

from __future__ import absolute_import, division, print_function

import glob
import ossq
import tarfile

import datasets


_CITATION = """\
"""

_DESCRIPTION = """

"""

_URL = "https://zenodo.org/record/2630551/files/lambada-dataset.tar.gz"

_LABELS = [
"Society & Culture",
"Science & Mathematics",
"Health",
"Education & Reference",
"Computers & Internet",
"Sports",
"Business & Finance",
"Entertainment & Music",
"Family & Relationships",
"Politics & Government",
]

class YahooAnswersTopics(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "label": datasets.features.ClassLabel(names=_LABELS),
                    "question_title": datasets.Value("string"),
                    "question_content": datasets.Value("string"),
                    "best_answer": datasets.Value("string"),
                }
            )
        )

