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
"""KdConv: Chinese multi-domain Knowledge-driven Conversionsation dataset"""


import json
import os

import datasets


_CITATION = """\
@inproceedings{zhou-etal-2020-kdconv,
    title = "{K}d{C}onv: A {C}hinese Multi-domain Dialogue Dataset Towards Multi-turn Knowledge-driven Conversation",
    author = "Zhou, Hao  and
      Zheng, Chujie  and
      Huang, Kaili  and
      Huang, Minlie  and
      Zhu, Xiaoyan",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.635",
    doi = "10.18653/v1/2020.acl-main.635",
    pages = "7098--7108",
}
"""


_DESCRIPTION = """\
KdConv is a Chinese multi-domain Knowledge-driven Conversionsation dataset, grounding the topics in multi-turn \
conversations to knowledge graphs. KdConv contains 4.5K conversations from three domains (film, music, and travel), \
and 86K utterances with an average turn number of 19.0. These conversations contain in-depth discussions on related \
topics and natural transition between multiple topics, while the corpus can also used for exploration of transfer \
learning and domain adaptation.\
"""


_HOMEPAGE = "https://github.com/thu-coai/KdConv"


_LICENSE = "Apache License 2.0"


_URL = "https://github.com/thu-coai/KdConv/archive/master.zip"

_DOMAINS = ["travel", "music", "film"]
_DATA_TYPES = ["dialogues", "knowledge_base"]


class KdConv(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.1.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=domain + "_" + type,
            description="This part of dataset covers {0} domain and {1} data " "of the corpus".format(domain, type),
        )
        for domain in _DOMAINS
        for type in _DATA_TYPES
    ] + [
        datasets.BuilderConfig(
            name="all_" + type,
            description="This part of dataset covers all domains and {0} data of " "the corpus".format(type),
        )
        for type in _DATA_TYPES
    ]

    DEFAULT_CONFIG_NAME = "all_dialogues"

    def _info(self):
        if "dialogues" in self.config.name:
            features = datasets.Features(
                {
                    "messages": datasets.Sequence(
                        {
                            "message": datasets.Value("string"),
                            "attrs": datasets.Sequence(
                                {
                                    "attrname": datasets.Value("string"),
                                    "attrvalue": datasets.Value("string"),
                                    "name": datasets.Value("string"),
                                }
                            ),
                        }
                    ),
                    "name": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "head_entity": datasets.Value("string"),
                    "kb_triplets": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
                    "domain": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_dir = dl_manager.download_and_extract(_URL)
        base_dir = os.path.join(os.path.join(data_dir, "KdConv-master"), "data")
        if "dialogues" in self.config.name:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "data_dir": base_dir,
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"data_dir": base_dir, "split": "test"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "data_dir": base_dir,
                        "split": "dev",
                    },
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "data_dir": base_dir,
                        "split": "train",
                    },
                ),
            ]

    def _generate_examples(self, data_dir, split):
        """Yields examples."""
        if "dialogues" in self.config.name:
            if "all" in self.config.name:
                file_dict = {
                    domain: os.path.join(os.path.join(data_dir, domain), split + ".json") for domain in _DOMAINS
                }
            else:
                domain = self.config.name.split("_")[0]
                file_dict = {domain: os.path.join(os.path.join(data_dir, domain), split + ".json")}
            id_ = -1
            for domain, filepath in file_dict.items():
                with open(filepath, encoding="utf-8") as f:
                    conversations = json.load(f)
                    for conversation in conversations:
                        id_ += 1
                        conversation["domain"] = domain
                        for turn in conversation["messages"]:
                            if "attrs" in turn:
                                attrnames = [kb_triplet.get("attrname", "") for kb_triplet in turn["attrs"]]
                                attrvalues = [kb_triplet.get("attrvalue", "") for kb_triplet in turn["attrs"]]
                                names = [kb_triplet.get("name", "") for kb_triplet in turn["attrs"]]
                            else:
                                attrnames, attrvalues, names = [], [], []
                            turn["attrs"] = {"attrname": attrnames, "attrvalue": attrvalues, "name": names}

                        yield id_, conversation
        else:
            if "all" in self.config.name:
                file_dict = {
                    domain: os.path.join(os.path.join(data_dir, domain), "kb_" + domain + ".json")
                    for domain in _DOMAINS
                }
            else:
                domain = self.config.name.split("_")[0]
                file_dict = {domain: os.path.join(os.path.join(data_dir, domain), "kb_" + domain + ".json")}

            id_ = -1
            for domain, filepath in file_dict.items():
                with open(filepath, encoding="utf-8") as f:
                    kb_dict = json.load(f)
                    for head_entity, kb_triplets in kb_dict.items():
                        id_ += 1
                        yield id_, {"head_entity": head_entity, "kb_triplets": kb_triplets, "domain": domain}
