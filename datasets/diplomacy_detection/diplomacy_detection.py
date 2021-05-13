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
"""Diplomacy: A Dataset for Deception Detection. It Takes Two to Lie: One to Lie, and One to Listen."""


import json
import os

import datasets


_CITATION = """
@inproceedings{peskov-etal-2020-takes,
    title = "It Takes Two to Lie: One to Lie, and One to Listen",
    author = "Peskov, Denis  and
      Cheng, Benny  and
      Elgohary, Ahmed  and
      Barrow, Joe  and
      Danescu-Niculescu-Mizil, Cristian  and
      Boyd-Graber, Jordan",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.353",
    doi = "10.18653/v1/2020.acl-main.353",
    pages = "3811--3854",
    abstract = "Trust is implicit in many online text conversations{---}striking up new friendships, or asking for tech support. But trust can be betrayed through deception. We study the language and dynamics of deception in the negotiation-based game Diplomacy, where seven players compete for world domination by forging and breaking alliances with each other. Our study with players from the Diplomacy community gathers 17,289 messages annotated by the sender for their intended truthfulness and by the receiver for their perceived truthfulness. Unlike existing datasets, this captures deception in long-lasting relationships, where the interlocutors strategically combine truth with lies to advance objectives. A model that uses power dynamics and conversational contexts can predict when a lie occurs nearly as well as human players.",
}
"""

_DESCRIPTION = "The Diplomacy dataset contains pairwise conversations annotated by the sender and the receiver for deception (and conversely truthfulness).   The 17,289 messages are gathered from 12 games. "

_HOMEPAGE = "https://sites.google.com/view/qanta/projects/diplomacy"

# _LICENSE = ""

_URL = "https://github.com/DenisPeskov/2020_acl_diplomacy/raw/master/data/"

_PLAYABLE_COUNTRIES = ["italy", "turkey", "russia", "england", "austria", "germany", "france"]
_SEASONS = ["spring", "fall", "winter", "Spring", "Fall", "Winter"]
_YEARS = [
    "1901",
    "1902",
    "1903",
    "1904",
    "1905",
    "1906",
    "1907",
    "1908",
    "1909",
    "1910",
    "1911",
    "1912",
    "1913",
    "1914",
    "1915",
    "1916",
    "1917",
    "1918",
]
_GAME_SCORE = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
_GAME_SCORE_DELTA = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "-1",
    "-2",
    "-3",
    "-4",
    "-5",
    "-6",
    "-7",
    "-8",
    "-9",
    "-10",
    "-11",
    "-12",
    "-13",
    "-14",
    "-15",
    "-16",
    "-17",
    "-18",
]


class DiplomacyDetection(datasets.GeneratorBasedBuilder):
    """Diplomacy: A Dataset for Deception Detection."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "messages": datasets.Sequence(datasets.Value("string")),
                "sender_labels": datasets.Sequence(datasets.ClassLabel(names=["false", "true"])),
                "receiver_labels": datasets.Sequence(datasets.ClassLabel(names=["false", "true", "noannotation"])),
                "speakers": datasets.Sequence(datasets.ClassLabel(names=_PLAYABLE_COUNTRIES)),
                "receivers": datasets.Sequence(datasets.ClassLabel(names=_PLAYABLE_COUNTRIES)),
                "absolute_message_index": datasets.Sequence(datasets.Value("int64")),
                "relative_message_index": datasets.Sequence(datasets.Value("int64")),
                "seasons": datasets.Sequence(datasets.ClassLabel(names=_SEASONS)),
                "years": datasets.Sequence(datasets.ClassLabel(names=_YEARS)),
                "game_score": datasets.Sequence(datasets.ClassLabel(names=_GAME_SCORE)),
                "game_score_delta": datasets.Sequence(datasets.ClassLabel(names=_GAME_SCORE_DELTA)),
                "players": datasets.Sequence(datasets.ClassLabel(names=_PLAYABLE_COUNTRIES)),
                "game_id": datasets.Value("int64"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": os.path.join(_URL, "train.jsonl"),
            "test": os.path.join(_URL, "test.jsonl"),
            "validation": os.path.join(_URL, "validation.jsonl"),
        }
        downloaded_filepath = dl_manager.download(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_filepath["validation"]}
            ),
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_filepath["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_filepath["test"]}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "messages": data["messages"],
                    "sender_labels": [str(v).lower() for v in data["sender_labels"]],
                    "receiver_labels": [str(v).lower() for v in data["receiver_labels"]],
                    "speakers": data["speakers"],
                    "receivers": data["receivers"],
                    "absolute_message_index": data["absolute_message_index"],
                    "relative_message_index": data["relative_message_index"],
                    "seasons": data["seasons"],
                    "years": data["years"],
                    "game_score": data["game_score"],
                    "game_score_delta": data["game_score_delta"],
                    "players": data["players"],
                    "game_id": data["game_id"],
                }
