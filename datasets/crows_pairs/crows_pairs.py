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
"""CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models"""

from __future__ import absolute_import, division, print_function

import csv
import json

import datasets


_CITATION = """\
@inproceedings{nangia2020crows,
    title = "{CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models}",
    author = "Nangia, Nikita  and
      Vania, Clara  and
      Bhalerao, Rasika  and
      Bowman, Samuel R.",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics"
}
"""

_DESCRIPTION = """\
CrowS-Pairs, a challenge dataset for measuring the degree to which U.S. stereotypical biases present in the masked language models (MLMs).
"""


_URL = "https://raw.githubusercontent.com/nyu-mll/crows-pairs/master/data/crows_pairs_anonymized.csv"

_BIAS_TYPES = [
    "race-color",
    "socioeconomic",
    "gender",
    "disability",
    "nationality",
    "sexual-orientation",
    "physical-appearance",
    "religion",
    "age",
]

_STEREOTYPICAL_DIRECTIONS = ["stereo", "antistereo"]


class CrowsPairs(datasets.GeneratorBasedBuilder):
    "CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models"

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="crows_pairs",
            version=datasets.Version("1.0.0", ""),
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "sent_more": datasets.Value("string"),
                    "sent_less": datasets.Value("string"),
                    "stereo_antistereo": datasets.ClassLabel(names=_STEREOTYPICAL_DIRECTIONS),
                    "bias_type": datasets.ClassLabel(names=_BIAS_TYPES),
                    "annotations": datasets.Sequence(datasets.Sequence(datasets.ClassLabel(names=_BIAS_TYPES))),
                    "anon_writer": datasets.Value("string"),
                    "anon_annotators": datasets.Sequence(datasets.Value("string")),
                },
            ),
            supervised_keys=None,
            citation=_CITATION,
            homepage="https://github.com/nyu-mll/crows-pairs",
        )

    def _split_generators(self, dl_manager):
        filepath = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": filepath}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            rows = csv.DictReader(f)
            for i, row in enumerate(rows):
                row["annotations"] = json.loads(row["annotations"].replace("'", '"'))
                row["anon_annotators"] = json.loads(row["anon_annotators"].replace("'", '"'))
                row["id"] = int(row.pop(""))
                yield i, row
