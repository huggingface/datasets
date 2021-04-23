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
"""LiMiT: The Literal Motion in Text Dataset"""


import json

import datasets


_CITATION = """\
@inproceedings{manotas-etal-2020-limit,
    title = "{L}i{M}i{T}: The Literal Motion in Text Dataset",
    author = "Manotas, Irene  and
      Vo, Ngoc Phuoc An  and
      Sheinin, Vadim",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.findings-emnlp.88",
    doi = "10.18653/v1/2020.findings-emnlp.88",
    pages = "991--1000",
    abstract = "Motion recognition is one of the basic cognitive capabilities of many life forms, yet identifying motion of physical entities in natural language have not been explored extensively and empirically. We present the Literal-Motion-in-Text (LiMiT) dataset, a large human-annotated collection of English text sentences describing physical occurrence of motion, with annotated physical entities in motion. We describe the annotation process for the dataset, analyze its scale and diversity, and report results of several baseline models. We also present future research directions and applications of the LiMiT dataset and share it publicly as a new resource for the research community.",
}
"""

_DESCRIPTION = """\
Motion recognition is one of the basic cognitive capabilities of many life forms, yet identifying \
motion of physical entities in natural language have not been explored extensively and empirically. \
Literal-Motion-in-Text (LiMiT) dataset, is a large human-annotated collection of English text sentences \
describing physical occurrence of motion, with annotated physical entities in motion.
"""

_HOMEPAGE = "https://github.com/ilmgut/limit_dataset"

_BASE_URL = "https://raw.githubusercontent.com/ilmgut/limit_dataset/0707d3989cd8848f0f11527c77dcf168fefd2b23/data"

_URLS = {
    "train": f"{_BASE_URL}/train.json",
    "test": f"{_BASE_URL}/test.json",
}


class Limit(datasets.GeneratorBasedBuilder):
    """LiMiT: The Literal Motion in Text Dataset"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = {
            "id": datasets.Value("int32"),
            "sentence": datasets.Value("string"),
            "motion": datasets.Value("string"),
            "motion_entities": [
                {
                    "entity": datasets.Value("string"),
                    "start_index": datasets.Value("int32"),
                }
            ],
        }
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_files = dl_manager.download(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": downloaded_files["test"]},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            examples = json.load(f)
            for idx, example in examples.items():
                if example["motion_entity"] == "":
                    motion_entities = []
                else:
                    motion_entities = example["motion_entity"].strip().split("\n")
                    motion_entities = [entity.split(":") for entity in motion_entities]
                    motion_entities = [
                        {"entity": entity, "start_index": int(start_idx)} for entity, start_idx in motion_entities
                    ]

                example.pop("motion_entity")
                example["motion_entities"] = motion_entities
                example["id"] = idx

                yield idx, example
