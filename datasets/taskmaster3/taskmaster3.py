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
"""Taskmaster-3: A goal oriented conversations dataset for movie ticketing domain """


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
Taskmaster is dataset for goal oriented conversations. The Taskmaster-3 dataset consists of 23,757 movie ticketing dialogs. \
By "movie ticketing" we mean conversations where the customer's goal is to purchase tickets after deciding \
on theater, time, movie name, number of tickets, and date, or opt out of the transaction. This collection \
was created using the "self-dialog" method. This means a single, crowd-sourced worker is \
paid to create a conversation writing turns for both speakers, i.e. the customer and the ticketing agent.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/Taskmaster/tree/master/TM-3-2020"

_BASE_URL = "https://raw.githubusercontent.com/google-research-datasets/Taskmaster/master/TM-3-2020/data"


class Taskmaster3(datasets.GeneratorBasedBuilder):
    """Taskmaster-3: A goal oriented conversations dataset for movie ticketing domain"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = {
            "conversation_id": datasets.Value("string"),
            "vertical": datasets.Value("string"),
            "instructions": datasets.Value("string"),
            "scenario": datasets.Value("string"),
            "utterances": [
                {
                    "index": datasets.Value("int32"),
                    "speaker": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "apis": [
                        {
                            "name": datasets.Value("string"),
                            "index": datasets.Value("int32"),
                            "args": [
                                {
                                    "arg_name": datasets.Value("string"),
                                    "arg_value": datasets.Value("string"),
                                }
                            ],
                            "response": [
                                {
                                    "response_name": datasets.Value("string"),
                                    "response_value": datasets.Value("string"),
                                }
                            ],
                        }
                    ],
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
        urls = [f"{_BASE_URL}/data_{i:02}.json" for i in range(20)]
        dialog_files = dl_manager.download(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"dialog_files": dialog_files},
            ),
        ]

    def _generate_examples(self, dialog_files):
        for filepath in dialog_files:
            with open(filepath, encoding="utf-8") as f:
                dialogs = json.load(f)
                for dialog in dialogs:
                    example = self._prepare_example(dialog)
                    yield example["conversation_id"], example

    def _prepare_example(self, dialog):
        utterances = dialog["utterances"]
        for utterance in utterances:
            if "segments" not in utterance:
                utterance["segments"] = []

            if "apis" in utterance:
                utterance["apis"] = self._transform_apis(utterance["apis"])
            else:
                utterance["apis"] = []
        return dialog

    def _transform_apis(self, apis):
        for api in apis:
            if "args" in api:
                api["args"] = [{"arg_name": k, "arg_value": v} for k, v in api["args"].items()]
            else:
                api["args"] = []

            if "response" in api:
                api["response"] = [{"response_name": k, "response_value": v} for k, v in api["response"].items()]
            else:
                api["response"] = []

        return apis
