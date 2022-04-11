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
"""Mutual friends dataset."""


import json

import datasets


_CITATION = """\
@inproceedings{he-etal-2017-learning,
    title = "Learning Symmetric Collaborative Dialogue Agents with Dynamic Knowledge Graph Embeddings",
    author = "He, He  and
      Balakrishnan, Anusha  and
      Eric, Mihail  and
      Liang, Percy",
    booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P17-1162",
    doi = "10.18653/v1/P17-1162",
    pages = "1766--1776",
    abstract = "We study a \textit{symmetric collaborative dialogue} setting in which two agents, each with private knowledge, must strategically communicate to achieve a common goal. The open-ended dialogue state in this setting poses new challenges for existing dialogue systems. We collected a dataset of 11K human-human dialogues, which exhibits interesting lexical, semantic, and strategic elements. To model both structured knowledge and unstructured language, we propose a neural model with dynamic knowledge graph embeddings that evolve as the dialogue progresses. Automatic and human evaluations show that our model is both more effective at achieving the goal and more human-like than baseline neural and rule-based models.",
}
"""

_DESCRIPTION = """\
Our goal is to build systems that collaborate with people by exchanging
information through natural language and reasoning over structured knowledge
base. In the MutualFriend task, two agents, A and B, each have a private
knowledge base, which contains a list of friends with multiple attributes
(e.g., name, school, major, etc.). The agents must chat with each other
to find their unique mutual friend."""

_HOMEPAGE = "https://stanfordnlp.github.io/cocoa/"

_LICENSE = "Unknown"

_URLs = {
    "train": "https://worksheets.codalab.org/rest/bundles/0x09c73c9db1134621bcc827689c6c3c61/contents/blob/train.json",
    "dev": "https://worksheets.codalab.org/rest/bundles/0x09c73c9db1134621bcc827689c6c3c61/contents/blob/dev.json",
    "test": "https://worksheets.codalab.org/rest/bundles/0x09c73c9db1134621bcc827689c6c3c61/contents/blob/test.json",
}


class MutualFriends(datasets.GeneratorBasedBuilder):
    """Mutual Friends dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            description="Plain text",
            version=VERSION,
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "uuid": datasets.Value("string"),
                    "scenario_uuid": datasets.Value("string"),
                    "scenario_alphas": datasets.Sequence(datasets.Value("float32")),
                    "scenario_attributes": datasets.Sequence(
                        {
                            "unique": datasets.Value("bool_"),
                            "value_type": datasets.Value("string"),
                            "name": datasets.Value("string"),
                        }
                    ),
                    "scenario_kbs": datasets.Sequence(
                        datasets.Sequence(
                            datasets.Sequence(
                                datasets.Sequence(datasets.Value("string")),
                            )
                        )
                    ),
                    "agents": {
                        "1": datasets.Value("string"),
                        "0": datasets.Value("string"),
                    },
                    "outcome_reward": datasets.Value("int32"),
                    "events": {
                        "actions": datasets.Sequence(datasets.Value("string")),
                        "start_times": datasets.Sequence(datasets.Value("float32")),
                        "data_messages": datasets.Sequence(datasets.Value("string")),
                        "data_selects": datasets.Sequence(
                            {
                                "attributes": datasets.Sequence(datasets.Value("string")),
                                "values": datasets.Sequence(datasets.Value("string")),
                            }
                        ),
                        "agents": datasets.Sequence(datasets.Value("int32")),
                        "times": datasets.Sequence(datasets.Value("float32")),
                    },
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": data_dir["test"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_dir["dev"],
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            mutualfriends = json.load(f)

            for id_, dialogue in enumerate(mutualfriends):
                uuid = dialogue["uuid"]
                scenario_uuid = dialogue["scenario_uuid"]

                scenario = dialogue["scenario"]
                # Note that scenario["uuid"] == scenario_uuid all the time in the data
                scenario_alphas = scenario["alphas"]
                scenario_attributes = scenario["attributes"]
                scenario_kbs = [
                    [
                        [
                            list(person.keys()),  # scenario_kbs_keys
                            list(person.values()),  # scenario_kbs_values
                        ]
                        for person in kb
                    ]
                    for kb in scenario["kbs"]
                ]  # The keys are not fixed, so "linearizing" the dictionaries

                agents = dialogue["agents"]
                outcome_reward = dialogue["outcome"]["reward"]

                events_actions = []
                events_start_times = []
                events_data_messages = []
                events_data_selects = []
                events_agents = []
                events_times = []
                for turn in dialogue["events"]:
                    act = turn["action"]
                    events_actions.append(act)
                    events_start_times.append(-1 if turn["start_time"] is None else turn["start_time"])
                    # Note that turn["start_time"] == None in the data
                    if act == "message":
                        events_data_messages.append(turn["data"])
                        events_data_selects.append({"attributes": [], "values": []})
                    elif act == "select":
                        events_data_messages.append("")
                        events_data_selects.append(
                            {
                                "attributes": list(turn["data"].keys()),
                                "values": list(turn["data"].values()),
                            }
                        )
                    events_agents.append(turn["agent"])
                    events_times.append(turn["time"])
                events = {
                    "actions": events_actions,
                    "start_times": events_start_times,
                    "data_messages": events_data_messages,
                    "data_selects": events_data_selects,
                    "agents": events_agents,
                    "times": events_times,
                }

                yield id_, {
                    "uuid": uuid,
                    "scenario_uuid": scenario_uuid,
                    "scenario_alphas": scenario_alphas,
                    "scenario_attributes": scenario_attributes,
                    "scenario_kbs": scenario_kbs,
                    "agents": agents,
                    "outcome_reward": outcome_reward,
                    "events": events,
                }
