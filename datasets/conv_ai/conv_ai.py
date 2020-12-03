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
"""ConvAI: A Dataset of Topic-Oriented Human-to-Chatbot Dialogues"""

from __future__ import absolute_import, division, print_function

import json

import datasets


_DESCRIPTION = """\
ConvAI is a dataset of human-to-bot conversations labelled for quality. \
This data can be used to train a metric for evaluating dialogue systems. \
Moreover, it can be used in the development of chatbots themselves: it contains the information \
on the quality of utterances and entire dialogues, that can guide a dialogue system in search of better answers.
"""

_URL = "https://github.com/DeepPavlov/convai/raw/master/2017/data/train_full.json"


class ConvAi(datasets.GeneratorBasedBuilder):
    """ConvAI: A Dataset of Topic-Oriented Human-to-Chatbot Dialogues"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="conv_ai",
            version=datasets.Version("1.0.0"),
            description="Full training set",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "dialogId": datasets.Value("int32"),
                    "context": datasets.Value("string"),
                    "users": [{"userType": datasets.Value("string"), "id": datasets.Value("string")}],
                    "evaluation": [
                        {
                            "breadth": datasets.Value("int32"),
                            "userId": datasets.Value("string"),
                            "quality": datasets.Value("int32"),
                            "engagement": datasets.Value("int32"),
                        }
                    ],
                    "thread": [
                        {
                            "evaluation": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "userId": datasets.Value("string"),
                            "time": datasets.Value("int32"),
                        }
                    ],
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/DeepPavlov/convai/tree/master/2017",
        )

    def _split_generators(self, dl_manager):
        downloaded_file = dl_manager.download(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_file},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            examples = json.load(f)
            for example in examples:
                example["id"] = example["dialogId"]

                # for some threads, time key is missing
                # assing deafult time value for such threads
                for thread in example["thread"]:
                    if "time" not in thread.keys():
                        thread["time"] = -1

                yield example["id"], example
