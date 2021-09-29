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
"""Campsite Negotiation Dialogues"""

import json

import datasets


_CITATION = """\
@inproceedings{chawla2021casino,
  title={CaSiNo: A Corpus of Campsite Negotiation Dialogues for Automatic Negotiation Systems},
  author={Chawla, Kushal and Ramirez, Jaysa and Clever, Rene and Lucas, Gale and May, Jonathan and Gratch, Jonathan},
  booktitle={Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies},
  pages={3167--3185},
  year={2021}
}
"""

_DESCRIPTION = """\
We provide a novel dataset (referred to as CaSiNo) of 1030 negotiation dialogues. Two participants take the role of campsite neighbors and negotiate for Food, Water, and Firewood packages, based on their individual preferences and requirements. This design keeps the task tractable, while still facilitating linguistically rich and personal conversations. This helps to overcome the limitations of prior negotiation datasets such as Deal or No Deal and Craigslist Bargain. Each dialogue consists of rich meta-data including participant demographics, personality, and their subjective evaluation of the negotiation in terms of satisfaction and opponent likeness.
"""

_HOMEPAGE = "https://github.com/kushalchawla/CaSiNo"

_LICENSE = "The project is licensed under CC-BY-4.0"

_URLs = {
    "train": "https://raw.githubusercontent.com/kushalchawla/CaSiNo/main/data/casino.json",
}


class Casino(datasets.GeneratorBasedBuilder):
    """Campsite Negotiation Dialogues"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        features = datasets.Features(
            {
                "chat_logs": [
                    {
                        "text": datasets.Value("string"),
                        "task_data": {
                            "data": datasets.Value("string"),
                            "issue2youget": {
                                "Firewood": datasets.Value("string"),
                                "Water": datasets.Value("string"),
                                "Food": datasets.Value("string"),
                            },
                            "issue2theyget": {
                                "Firewood": datasets.Value("string"),
                                "Water": datasets.Value("string"),
                                "Food": datasets.Value("string"),
                            },
                        },
                        "id": datasets.Value("string"),
                    },
                ],
                "participant_info": {
                    "mturk_agent_1": {
                        "value2issue": {
                            "Low": datasets.Value("string"),
                            "Medium": datasets.Value("string"),
                            "High": datasets.Value("string"),
                        },
                        "value2reason": {
                            "Low": datasets.Value("string"),
                            "Medium": datasets.Value("string"),
                            "High": datasets.Value("string"),
                        },
                        "outcomes": {
                            "points_scored": datasets.Value("int32"),
                            "satisfaction": datasets.Value("string"),
                            "opponent_likeness": datasets.Value("string"),
                        },
                        "demographics": {
                            "age": datasets.Value("int32"),
                            "gender": datasets.Value("string"),
                            "ethnicity": datasets.Value("string"),
                            "education": datasets.Value("string"),
                        },
                        "personality": {
                            "svo": datasets.Value("string"),
                            "big-five": {
                                "extraversion": datasets.Value("float"),
                                "agreeableness": datasets.Value("float"),
                                "conscientiousness": datasets.Value("float"),
                                "emotional-stability": datasets.Value("float"),
                                "openness-to-experiences": datasets.Value("float"),
                            },
                        },
                    },
                    "mturk_agent_2": {
                        "value2issue": {
                            "Low": datasets.Value("string"),
                            "Medium": datasets.Value("string"),
                            "High": datasets.Value("string"),
                        },
                        "value2reason": {
                            "Low": datasets.Value("string"),
                            "Medium": datasets.Value("string"),
                            "High": datasets.Value("string"),
                        },
                        "outcomes": {
                            "points_scored": datasets.Value("int32"),
                            "satisfaction": datasets.Value("string"),
                            "opponent_likeness": datasets.Value("string"),
                        },
                        "demographics": {
                            "age": datasets.Value("int32"),
                            "gender": datasets.Value("string"),
                            "ethnicity": datasets.Value("string"),
                            "education": datasets.Value("string"),
                        },
                        "personality": {
                            "svo": datasets.Value("string"),
                            "big-five": {
                                "extraversion": datasets.Value("float"),
                                "agreeableness": datasets.Value("float"),
                                "conscientiousness": datasets.Value("float"),
                                "emotional-stability": datasets.Value("float"),
                                "openness-to-experiences": datasets.Value("float"),
                            },
                        },
                    },
                },
                "annotations": [[datasets.Value("string")]],
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
        path = dl_manager.download_and_extract(_URLs["train"])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": path,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split="train"):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            all_data = json.load(f)

        for idx, item in enumerate(all_data):

            for chat_item in item["chat_logs"]:
                if "data" not in chat_item["task_data"]:
                    chat_item["task_data"]["data"] = ""
                if "issue2youget" not in chat_item["task_data"]:
                    chat_item["task_data"]["issue2youget"] = {
                        "Food": "",
                        "Firewood": "",
                        "Water": "",
                    }
                if "issue2theyget" not in chat_item["task_data"]:
                    chat_item["task_data"]["issue2theyget"] = {
                        "Food": "",
                        "Firewood": "",
                        "Water": "",
                    }

            item.pop("dialogue_id")
            yield idx, item
