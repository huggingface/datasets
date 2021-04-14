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
"""Taskmaster-1:Toward a Realistic and Diverse Dialog Dataset"""


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
Taskmaster-1 is a  goal-oriented conversational dataset. It includes 13,215 task-based \
dialogs comprising six domains. Two procedures were used to create this collection, \
each with unique advantages. The first involves a two-person, spoken "Wizard of Oz" (WOz) approach \
in which trained agents and crowdsourced workers interact to complete the task while the second is \
"self-dialog" in which crowdsourced workers write the entire dialog themselves.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/Taskmaster"

_BASE_URL = "https://raw.githubusercontent.com/google-research-datasets/Taskmaster/master/TM-1-2019/"
_DIALOGS_URLS = {
    "one_person_dialogs": _BASE_URL + "self-dialogs.json",
    "woz_dialogs": _BASE_URL + "woz-dialogs.json",
}
_SPLIT_IDS_URLS = {
    "train": _BASE_URL + "train-dev-test/train.csv",
    "dev": _BASE_URL + "train-dev-test/dev.csv",
    "test": _BASE_URL + "train-dev-test/test.csv",
}


class Taskmaster1(datasets.GeneratorBasedBuilder):
    """Taskmaster-1:Toward a Realistic and Diverse Dialog Dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="one_person_dialogs", version=datasets.Version("1.0.0"), description="Taskmaster-1 one-person dialogs"
        ),
        datasets.BuilderConfig(
            name="woz_dialogs", version=datasets.Version("1.0.0"), description="Taskmaster-1 WOz style dialogs"
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
        dialog_files = dl_manager.download(_DIALOGS_URLS)
        split_id_files = dl_manager.download(_SPLIT_IDS_URLS)

        if self.config.name == "woz_dialogs":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"filepath": dialog_files["woz_dialogs"], "split_ids_filepath": None},
                )
            ]

        dialogs_file = dialog_files["one_person_dialogs"]
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": dialogs_file, "split_ids_filepath": split_id_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": dialogs_file, "split_ids_filepath": split_id_files["dev"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": dialogs_file, "split_ids_filepath": split_id_files["test"]},
            ),
        ]

    def _generate_examples(self, filepath, split_ids_filepath):
        if self.config.name == "one_person_dialogs":
            with open(split_ids_filepath, encoding="utf-8") as f:
                ids = f.read().replace(",", "").split("\n")[:-1]

        with open(filepath, encoding="utf-8") as f:
            dialogs = json.load(f)

            if self.config.name == "one_person_dialogs":
                dialogs = [dialog for dialog in dialogs if dialog["conversation_id"] in ids]

            for dialog in dialogs:
                utterances = dialog["utterances"]
                for utterance in utterances:
                    if "segments" not in utterance:
                        utterance["segments"] = []
                yield dialog["conversation_id"], dialog
