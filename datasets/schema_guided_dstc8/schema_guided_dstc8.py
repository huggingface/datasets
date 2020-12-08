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
"""SGD: The Schema Guided Dialogue dataet"""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """\
@inproceedings{aaai/RastogiZSGK20,
  author    = {Abhinav Rastogi and
               Xiaoxue Zang and
               Srinivas Sunkara and
               Raghav Gupta and
               Pranav Khaitan},
  title     = {Towards Scalable Multi-Domain Conversational Agents: The Schema-Guided
               Dialogue Dataset},
  booktitle = {The Thirty-Fourth {AAAI} Conference on Artificial Intelligence, {AAAI}
               2020, The Thirty-Second Innovative Applications of Artificial Intelligence
               Conference, {IAAI} 2020, The Tenth {AAAI} Symposium on Educational
               Advances in Artificial Intelligence, {EAAI} 2020, New York, NY, USA,
               February 7-12, 2020},
  pages     = {8689--8696},
  publisher = {{AAAI} Press},
  year      = {2020},
  url       = {https://aaai.org/ojs/index.php/AAAI/article/view/6394}
}
"""

_DESCRIPTION = """\
The Schema-Guided Dialogue dataset (SGD) was developed for the Dialogue State Tracking task of the Eights Dialogue Systems Technology Challenge (dstc8).
The SGD dataset consists of over 18k annotated multi-domain, task-oriented conversations between a human and a virtual assistant.
These conversations involve interactions with services and APIs spanning 17 domains, ranging from banks and events to media, calendar, travel, and weather.
For most of these domains, the SGD dataset contains multiple different APIs, many of which have overlapping functionalities but different interfaces,
which reflects common real-world scenarios.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/dstc8-schema-guided-dialogue"

_LICENSE = "CC BY-SA 4.0"

_URL_LIST = [
    (
        "train_schema.json",
        "https://github.com/google-research-datasets/dstc8-schema-guided-dialogue/raw/master/train/schema.json",
    ),
    (
        "dev_schema.json",
        "https://github.com/google-research-datasets/dstc8-schema-guided-dialogue/raw/master/dev/schema.json",
    ),
    (
        "test_schema.json",
        "https://github.com/google-research-datasets/dstc8-schema-guided-dialogue/raw/master/test/schema.json",
    ),
]
_URL_LIST += [
    (
        f"train_dialogues_{i:03d}.json",
        f"https://github.com/google-research-datasets/dstc8-schema-guided-dialogue/raw/master/train/dialogues_{i:03d}.json",
    )
    for i in range(1, 128)
]
_URL_LIST += [
    (
        f"dev_dialogues_{i:03d}.json",
        f"https://github.com/google-research-datasets/dstc8-schema-guided-dialogue/raw/master/dev/dialogues_{i:03d}.json",
    )
    for i in range(1, 21)
]
_URL_LIST += [
    (
        f"test_dialogues_{i:03d}.json",
        f"https://github.com/google-research-datasets/dstc8-schema-guided-dialogue/raw/master/test/dialogues_{i:03d}.json",
    )
    for i in range(1, 35)
]

_URLs = dict(_URL_LIST)

_USER_ACTS = [
    "INFORM_INTENT",
    "NEGATE_INTENT",
    "AFFIRM_INTENT",
    "INFORM",
    "REQUEST",
    "AFFIRM",
    "NEGATE",
    "SELECT",
    "REQUEST_ALTS",
    "THANK_YOU",
    "GOODBYE",
]

_SYSTEM_ACTS = [
    "INFORM",
    "REQUEST",
    "CONFIRM",
    "OFFER",
    "NOTIFY_SUCCESS",
    "NOTIFY_FAILURE",
    "INFORM_COUNT",
    "OFFER_INTENT",
    "REQ_MORE",
    "GOODBYE",
]

_ALL_ACTS = sorted(list(set(_USER_ACTS + _SYSTEM_ACTS)))


class SchemaGuidedDstc8(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="dialogues", description="The dataset of annotated dialogues."),
        datasets.BuilderConfig(name="schema", description="The schemas corresponding to the API calls."),
    ]

    DEFAULT_CONFIG_NAME = "dialogues"

    def _info(self):
        if self.config.name == "schema":
            features = datasets.Features(
                {
                    "service_name": datasets.Value("string"),
                    "description": datasets.Value("string"),
                    "slots": datasets.Sequence(
                        {
                            "name": datasets.Value("string"),
                            "description": datasets.Value("string"),
                            "is_categorical": datasets.Value("bool"),
                            "possible_values": datasets.Sequence(datasets.Value("string")),
                        }
                    ),
                    "intents": datasets.Sequence(
                        {
                            "name": datasets.Value("string"),
                            "description": datasets.Value("string"),
                            "is_transactional": datasets.Value("bool"),
                            "required_slots": datasets.Sequence(datasets.Value("string")),
                            # optional_slots was originally a dictionary
                            "optional_slots": datasets.Sequence(
                                {
                                    "slot_name": datasets.Value("string"),
                                    "slot_value": datasets.Value("string"),
                                }
                            ),
                            "result_slots": datasets.Sequence(datasets.Value("string")),
                        },
                    ),
                }
            )
        else:
            features = datasets.Features(
                {
                    "dialogue_id": datasets.Value("string"),
                    "services": datasets.Sequence(datasets.Value("string")),
                    "turns": datasets.Sequence(
                        {
                            "speaker": datasets.ClassLabel(names=["USER", "SYSTEM"]),
                            "utterance": datasets.Value("string"),
                            "frames": datasets.Sequence(
                                {
                                    "service": datasets.Value("string"),
                                    "slots": datasets.Sequence(
                                        {
                                            "slot": datasets.Value("string"),
                                            "start": datasets.Value("int32"),
                                            "exclusive_end": datasets.Value("int32"),
                                        }
                                    ),
                                    # optional
                                    "state": {
                                        "active_intent": datasets.Value("string"),
                                        "requested_slots": datasets.Sequence(datasets.Value("string")),
                                        # slot_values was originally a dictionary
                                        "slot_values": datasets.Sequence(
                                            {
                                                "slot_name": datasets.Value("string"),
                                                "slot_value_list": datasets.Sequence(datasets.Value("string")),
                                            }
                                        ),
                                    },
                                    "actions": datasets.Sequence(
                                        {
                                            "act": datasets.ClassLabel(names=_ALL_ACTS),
                                            # optional
                                            "slot": datasets.Value("string"),
                                            # optional
                                            "canonical_values": datasets.Sequence(datasets.Value("string")),
                                            # optional
                                            "values": datasets.Sequence(datasets.Value("string")),
                                        }
                                    ),
                                    # optional
                                    "service_results": datasets.Sequence(
                                        # Arrow doesn't like Sequences of Sequences for default values so we need a Sequence of Features of Sequences
                                        {
                                            "service_results_list": datasets.Sequence(
                                                # originally each list item was a dictionary (optional)
                                                {
                                                    "service_slot_name": datasets.Value("string"),
                                                    "service_canonical_value": datasets.Value("string"),
                                                }
                                            )
                                        }
                                    ),
                                    # optional
                                    "service_call": {
                                        "method": datasets.Value("string"),
                                        # parameters was originally a dictionary
                                        "parameters": datasets.Sequence(
                                            {
                                                "parameter_slot_name": datasets.Value("string"),
                                                "parameter_canonical_value": datasets.Value("string"),
                                            }
                                        ),
                                    },
                                }
                            ),
                        }
                    ),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  # Here we define them above because they are different between the two configurations
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_files = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=spl_enum,
                gen_kwargs={
                    "filepaths": data_files,
                    "split": spl,
                },
            )
            for spl, spl_enum in [
                ("train", datasets.Split.TRAIN),
                ("dev", datasets.Split.VALIDATION),
                ("test", datasets.Split.TEST),
            ]
        ]

    def _generate_examples(self, filepaths, split):
        id_ = -1
        file_list = [fpath for fname, fpath in filepaths.items() if fname.startswith(f"{split}_{self.config.name}")]
        for filepath in file_list:
            examples = json.load(open(filepath, encoding="utf-8"))
            for example in examples:
                id_ += 1
                if self.config.name == "schema":
                    example["intents"] = example.get("intents", [])
                    for intent in example["intents"]:
                        optional_slots = intent.get("optional_slots", {})
                        intent["optional_slots"] = {
                            "slot_name": list(optional_slots.keys()),
                            "slot_value": list(optional_slots.values()),
                        }
                else:
                    for turn in example["turns"]:
                        for frame in turn["frames"]:
                            # add empty state if the key is missing from the dict
                            frame["state"] = frame.get(
                                "state",
                                {
                                    "active_intent": "",
                                    "requested_slots": [],
                                    "slot_values": {},
                                },
                            )
                            # linearize the optional slot_values dictionary
                            slot_values_dict = frame["state"].get("slot_values", {})
                            frame["state"]["slot_values"] = {
                                "slot_name": list(slot_values_dict.keys()),
                                "slot_value_list": list(slot_values_dict.values()),
                            }
                            # add default values for optional fields in actions
                            for action in frame["actions"]:
                                action["slot"] = action.get("slot", "")
                                action["canonical_values"] = action.get("canonical_values", [])
                                action["values"] = action.get("values", [])
                            # add "service_results" field when necessary and linearize the dictionaries in the list otherwise
                            service_results = []
                            for result in frame.get("service_results", []):
                                service_results += [
                                    {
                                        "service_slot_name": list(result.keys()),
                                        "service_canonical_value": list(result.values()),
                                    }
                                ]
                            frame["service_results"] = {
                                "service_results_list": service_results,
                            }
                            # add "service_call" field when necessary and linearize the parameters dictionary otherwise
                            frame["service_call"] = frame.get(
                                "service_call",
                                {
                                    "method": "",
                                    "parameters": {},
                                },
                            )
                            parameters_dict = frame["service_call"].get("parameters", {})
                            frame["service_call"]["parameters"] = {
                                "parameter_slot_name": list(parameters_dict.keys()),
                                "parameter_canonical_value": list(parameters_dict.values()),
                            }
                yield id_, example
