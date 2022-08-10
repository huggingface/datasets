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
"""WozDialogue: a dataset for training task-oriented dialogue systems"""


import json

import datasets


_CITATION = """\
@misc{wen2017networkbased,
      title={A Network-based End-to-End Trainable Task-oriented Dialogue System},
      author={Tsung-Hsien Wen and David Vandyke and Nikola Mrksic and Milica Gasic and Lina M. Rojas-Barahona and Pei-Hao Su and Stefan Ultes and Steve Young},
      year={2017},
      eprint={1604.04562},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
Wizard-of-Oz (WOZ) is a dataset for training task-oriented dialogue systems. The dataset is designed around the \
task of finding a restaurant in the Cambridge, UK area. There are three informable slots (food, pricerange,area) \
that users can use to constrain the search and six requestable slots (address, phone, postcode plus the three informable slots) \
that the user can ask a value for once a restaurant has been offered.
"""

_HOMEPAGE = "https://github.com/nmrksic/neural-belief-tracker/tree/master/data/woz"

_BASE_URL = "https://raw.githubusercontent.com/nmrksic/neural-belief-tracker/master/data/woz"


class WozDialogue(datasets.GeneratorBasedBuilder):
    """WozDialogue: a dataset for training task-oriented dialogue systems"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="en",
            version=datasets.Version("1.0.0"),
            description="WOZ English dataset",
        ),
        datasets.BuilderConfig(name="de", version=datasets.Version("1.0.0"), description="WOZ German dataset"),
        datasets.BuilderConfig(
            name="de_en",
            version=datasets.Version("1.0.0"),
            description="WOZ German-English dataset. For this config, the dialogues are in German and the labels in English ",
        ),
        datasets.BuilderConfig(name="it", version=datasets.Version("1.0.0"), description="WOZ Italian dataset"),
        datasets.BuilderConfig(
            name="it_en",
            version=datasets.Version("1.0.0"),
            description="WOZ Italian-English dataset. For this config, the dialogues are in Italian and the labels in English ",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "dialogue_idx": datasets.Value("int32"),
                    "dialogue": [
                        {
                            "turn_label": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
                            "asr": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
                            "system_transcript": datasets.Value("string"),
                            "turn_idx": datasets.Value("int32"),
                            "belief_state": [
                                {
                                    "slots": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
                                    "act": datasets.Value("string"),
                                }
                            ],
                            "transcript": datasets.Value("string"),
                            "system_acts": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
                        }
                    ],
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls = {
            "train": f"{_BASE_URL}/woz_train_{self.config.name}.json",
            "dev": f"{_BASE_URL}/woz_validate_{self.config.name}.json",
            "test": f"{_BASE_URL}/woz_test_{self.config.name}.json",
        }
        downloaded_paths = dl_manager.download(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_paths["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": downloaded_paths["dev"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": downloaded_paths["test"]},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            examples = json.load(f)
            for i, example in enumerate(examples):
                for dialogue in example["dialogue"]:
                    # exclude the second element which is same for every instance and is of type int
                    dialogue["asr"] = [asr[:1] for asr in dialogue["asr"]]
                    # some system_acts is either to string or list of strings,
                    # converting all to list of strings
                    dialogue["system_acts"] = [
                        [act] if isinstance(act, str) else act for act in dialogue["system_acts"]
                    ]

                yield example["dialogue_idx"], example
