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

from __future__ import absolute_import, division, print_function

import json

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

_DESCRIPTION = "The Diplomacy dataset contains pairwise conversations annotated by the sender and the receiver for deception (and conversely truthfulness).   The 17,289 messages are gathered from 12 games.  We train baseline and neural models to predict lies."

_HOMEPAGE = "https://sites.google.com/view/qanta/projects/diplomacy"

# _LICENSE = ""

_TEST_DOWNLOAD_URL = "https://github.com/DenisPeskov/2020_acl_diplomacy/raw/master/data/test.jsonl"
_TRAIN_DOWNLOAD_URL = "https://github.com/DenisPeskov/2020_acl_diplomacy/raw/master/data/train.jsonl"
_VALIDATION_DOWNLOAD_URL = "https://github.com/DenisPeskov/2020_acl_diplomacy/raw/master/data/validation.jsonl"


class DiplomacyDetection(datasets.GeneratorBasedBuilder):
    """Diplomacy: A Dataset for Deception Detection. """

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "messages": datasets.Value("string"),
                "sender_labels": datasets.Value("string"),
                "receiver_labels": datasets.Value("string"),
                "speakers": datasets.Value("string"),
                "receivers": datasets.Value("string"),
                "absolute_message_index": datasets.Value("string"),
                "relative_message_index": datasets.Value("string"),
                "seasons": datasets.Value("string"),
                "years": datasets.Value("string"),
                "game_score": datasets.Value("string"),
                "game_score_delta": datasets.Value("string"),
                "players": datasets.Value("string"),
                "game_id": datasets.Value("string"),
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
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        validation_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": validation_path}),
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "messages": str(data["messages"]),
                    "sender_labels": str(data["sender_labels"]),
                    "receiver_labels": str(data["receiver_labels"]),
                    "speakers": str(data["speakers"]),
                    "receivers": str(data["receivers"]),
                    "absolute_message_index": str(data["absolute_message_index"]),
                    "relative_message_index": str(data["relative_message_index"]),
                    "seasons": str(data["seasons"]),
                    "years": str(data["years"]),
                    "game_score": str(data["game_score"]),
                    "game_score_delta": str(data["game_score_delta"]),
                    "players": str(data["players"]),
                    "game_id": str(data["game_id"]),
                }
