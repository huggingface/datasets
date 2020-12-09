# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
import json

import datasets


_DESCRIPTION = """\
TweetEval 2020 Dataset
"""
_HOMEPAGE_URL = "https://github.com/cardiffnlp/tweeteval"
_CITATION = """\

"""

_TRAIN_URL = ""


class TweetEval(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "uid": datasets.Value("string"),
                    "claim": datasets.Value("string"),
                    "supporting_facts": [
                        {
                            "key": datasets.Value("string"),
                            "value": datasets.Value("int32"),
                        }
                    ],
                    "label": datasets.Value("string"),
                    "num_hops": datasets.Value("int32"),
                    "hpqa_id": datasets.Value("string"),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_URL)
        valid_path = dl_manager.download_and_extract(_VALID_URL)
        test_path = dl_manager.download_and_extract(_TEST_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": train_path, "datatype": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"datapath": valid_path, "datatype": "valid"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"datapath": test_path, "datatype": "test"},
            ),
        ]

    def _generate_examples(self, datapath, datatype):
        with open(datapath, encoding="utf-8") as f:
            data = json.load(f)

        for sentence_counter, d in enumerate(data):
            resp = {
                "id": sentence_counter,
                "uid": d["uid"],
                "claim": d["claim"],
                "supporting_facts": [
                    {"key": x[0], "value": x[1]} for x in d["supporting_facts"]
                ],
                "label": d["label"],
                "num_hops": d["num_hops"],
                "hpqa_id": d["hpqa_id"],
            }
            yield sentence_counter, resp
