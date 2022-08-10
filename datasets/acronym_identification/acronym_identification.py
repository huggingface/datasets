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
Acronym identification training and development sets for the acronym identification task at SDU@AAAI-21.
"""
_HOMEPAGE_URL = "https://github.com/amirveyseh/AAAI-21-SDU-shared-task-1-AI"
_CITATION = """\
@inproceedings{veyseh-et-al-2020-what,
   title={{What Does This Acronym Mean? Introducing a New Dataset for Acronym Identification and Disambiguation}},
   author={Amir Pouran Ben Veyseh and Franck Dernoncourt and Quan Hung Tran and Thien Huu Nguyen},
   year={2020},
   booktitle={Proceedings of COLING},
   link={https://arxiv.org/pdf/2010.14678v1.pdf}
}
"""

_TRAIN_URL = "https://raw.githubusercontent.com/amirveyseh/AAAI-21-SDU-shared-task-1-AI/master/dataset/train.json"
_VALID_URL = "https://raw.githubusercontent.com/amirveyseh/AAAI-21-SDU-shared-task-1-AI/master/dataset/dev.json"
_TEST_URL = "https://raw.githubusercontent.com/amirveyseh/AAAI-21-SDU-shared-task-1-AI/master/dataset/test.json"


class AcronymIdentification(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "labels": datasets.Sequence(
                        datasets.ClassLabel(names=["B-long", "B-short", "I-long", "I-short", "O"])
                    ),
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
                "id": d["id"],
                "tokens": d["tokens"],
            }
            if datatype != "test":
                resp["labels"] = d["labels"]
            else:
                resp["labels"] = ["O"] * len(d["tokens"])
            yield sentence_counter, resp
