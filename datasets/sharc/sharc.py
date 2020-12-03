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
"""ShARC: A Conversational Question Answering dataset focussing on question answering from texts containing rules."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@misc{saeidi2018interpretation,
      title={Interpretation of Natural Language Rules in Conversational Machine Reading},
      author={Marzieh Saeidi and Max Bartolo and Patrick Lewis and Sameer Singh and Tim Rocktäschel and Mike Sheldon and Guillaume Bouchard and Sebastian Riedel},
      year={2018},
      eprint={1809.01494},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
ShARC is a Conversational Question Answering dataset focussing on question answering from texts containing rules. \
The goal is to answer questions by possibly asking follow-up questions first. It is assumed assume that the question is often underspecified, \
in the sense that the question does not provide enough information to be answered directly. However, an agent can use the supporting rule text to \
infer what needs to be asked in order to determine the final answer.
"""

_URL = "https://sharc-data.github.io/data/sharc1-official.zip"


class Sharc(datasets.GeneratorBasedBuilder):
    """ShARC: A Conversational Question Answering dataset focussing on question answering from texts containing rules."""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="sharc", version=datasets.Version("1.0.0")),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "utterance_id": datasets.Value("string"),
                    "source_url": datasets.Value("string"),
                    "snippet": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "scenario": datasets.Value("string"),
                    "history": [
                        {"follow_up_question": datasets.Value("string"), "follow_up_answer": datasets.Value("string")}
                    ],
                    "evidence": [
                        {"follow_up_question": datasets.Value("string"), "follow_up_answer": datasets.Value("string")}
                    ],
                    "answer": datasets.Value("string"),
                    "negative_question": datasets.Value("bool_"),
                    "negative_scenario": datasets.Value("bool_"),
                }
            ),
            supervised_keys=None,
            homepage="https://sharc-data.github.io/index.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        extracted_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_dir": os.path.join(extracted_path, "sharc1-official"), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"data_dir": os.path.join(extracted_path, "sharc1-official"), "split": "dev"},
            ),
        ]

    def _generate_examples(self, data_dir, split):
        with open(
            os.path.join(data_dir, "negative_sample_utterance_ids", "sharc_negative_scenario_utterance_ids.txt"),
            encoding="utf-8",
        ) as f:
            negative_scenario_ids = f.readlines()
            negative_scenario_ids = [id_.strip() for id_ in negative_scenario_ids]
        with open(
            os.path.join(data_dir, "negative_sample_utterance_ids", "sharc_negative_question_utterance_ids.txt"),
            encoding="utf-8",
        ) as f:
            negative_question_ids = f.readlines()
            negative_question_ids = [id_.strip() for id_ in negative_question_ids]

        data_file = os.path.join(data_dir, "json", f"sharc_{split}.json")
        with open(data_file, encoding="utf-8") as f:
            examples = json.load(f)
            for i, example in enumerate(examples):
                example.pop("tree_id")

                example["negative_question"] = example["utterance_id"] in negative_question_ids
                example["negative_scenario"] = example["utterance_id"] in negative_scenario_ids

                example["id"] = example["utterance_id"]

                # the keys are misspelled for one of the example in dev set
                # fix it here
                for evidence in example["evidence"]:
                    if evidence.get("followup_answer") is not None:
                        evidence["follow_up_answer"] = evidence.pop("followup_answer")
                    if evidence.get("followup_question") is not None:
                        evidence["follow_up_question"] = evidence.pop("followup_question")
                yield example["id"], example
