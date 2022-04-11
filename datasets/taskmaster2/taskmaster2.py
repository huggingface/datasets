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
"""Taskmaster: A dataset for goal oriented conversations."""


import json

import datasets


_CITATION = """\
@inproceedings{48484,
title	= {Taskmaster-1: Toward a Realistic and Diverse Dialog Dataset},
author	= {Bill Byrne and Karthik Krishnamoorthi and Chinnadhurai Sankar and Arvind Neelakantan and Daniel Duckworth and Semih Yavuz and Ben Goodrich and Amit Dubey and Kyu-Young Kim and Andy Cedilnik},
year	= {2019}
}
"""

_DESCRIPTION = """\
Taskmaster is dataset for goal oriented conversations. The Taskmaster-2 dataset consists of 17,289 dialogs \
in the seven domains which include restaurants, food ordering, movies, hotels, flights, music and sports. \
Unlike Taskmaster-1, which includes both written "self-dialogs" and spoken two-person dialogs, \
Taskmaster-2 consists entirely of spoken two-person dialogs. In addition, while Taskmaster-1 is \
almost exclusively task-based, Taskmaster-2 contains a good number of search- and recommendation-oriented dialogs. \
All dialogs in this release were created using a Wizard of Oz (WOz) methodology in which crowdsourced \
workers played the role of a 'user' and trained call center operators played the role of the 'assistant'. \
In this way, users were led to believe they were interacting with an automated system that “spoke” \
using text-to-speech (TTS) even though it was in fact a human behind the scenes. \
As a result, users could express themselves however they chose in the context of an automated interface.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/Taskmaster/tree/master/TM-2-2020"

_BASE_URL = "https://raw.githubusercontent.com/google-research-datasets/Taskmaster/master/TM-2-2020/data"


class Taskmaster2(datasets.GeneratorBasedBuilder):
    """Taskmaster: A dataset for goal oriented conversations."""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="flights", version=datasets.Version("1.0.0"), description="Taskmaster-2 flights domain."
        ),
        datasets.BuilderConfig(
            name="food-ordering", version=datasets.Version("1.0.0"), description="Taskmaster-2 food-ordering domain"
        ),
        datasets.BuilderConfig(
            name="hotels", version=datasets.Version("1.0.0"), description="Taskmaster-2 hotel domain"
        ),
        datasets.BuilderConfig(
            name="movies", version=datasets.Version("1.0.0"), description="Taskmaster-2 movies domain"
        ),
        datasets.BuilderConfig(
            name="music", version=datasets.Version("1.0.0"), description="Taskmaster-2 music domain"
        ),
        datasets.BuilderConfig(
            name="restaurant-search",
            version=datasets.Version("1.0.0"),
            description="Taskmaster-2 restaurant-search domain",
        ),
        datasets.BuilderConfig(
            name="sports", version=datasets.Version("1.0.0"), description="Taskmaster-2 sports domain"
        ),
    ]

    def _info(self):
        features = {
            "conversation_id": datasets.Value("string"),
            "instruction_id": datasets.Value("string"),
            "utterances": [
                {
                    "index": datasets.Value("int32"),
                    "speaker": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "segments": [
                        {
                            "start_index": datasets.Value("int32"),
                            "end_index": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "annotations": [{"name": datasets.Value("string")}],
                        }
                    ],
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
        url = f"{_BASE_URL}/{self.config.name}.json"
        dialogs_file = dl_manager.download(url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": dialogs_file},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            dialogs = json.load(f)
            for dialog in dialogs:
                utterances = dialog["utterances"]
                for utterance in utterances:
                    if "segments" not in utterance:
                        utterance["segments"] = []
                yield dialog["conversation_id"], dialog
