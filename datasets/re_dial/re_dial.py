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
"""Annotated dataset of dialogues where users recommend movies to each other."""


import json
import os

import datasets


_CITATION = """\
@inproceedings{li2018conversational,
  title={Towards Deep Conversational Recommendations},
  author={Li, Raymond and Kahou, Samira Ebrahimi and Schulz, Hannes and Michalski, Vincent and Charlin, Laurent and Pal, Chris},
  booktitle={Advances in Neural Information Processing Systems 31 (NIPS 2018)},
  year={2018}
}
"""

_DESCRIPTION = """\
ReDial (Recommendation Dialogues) is an annotated dataset of dialogues, where users
recommend movies to each other. The dataset was collected by a team of researchers working at
Polytechnique Montréal, MILA – Quebec AI Institute, Microsoft Research Montréal, HEC Montreal, and Element AI.

The dataset allows research at the intersection of goal-directed dialogue systems
(such as restaurant recommendation) and free-form (also called “chit-chat”) dialogue systems.
"""

_HOMEPAGE = "https://redialdata.github.io/website/"

_LICENSE = "CC BY 4.0 License."

_DATA_URL = "https://github.com/ReDialData/website/raw/data/redial_dataset.zip"


class ReDial(datasets.GeneratorBasedBuilder):
    """Annotated dataset of dialogues where users recommend movies to each other."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        question_features = {
            "movieId": datasets.Value("string"),
            "suggested": datasets.Value("int32"),
            "seen": datasets.Value("int32"),
            "liked": datasets.Value("int32"),
        }
        features = datasets.Features(
            {
                "movieMentions": [
                    {
                        "movieId": datasets.Value("string"),
                        "movieName": datasets.Value("string"),
                    },
                ],
                "respondentQuestions": [question_features],
                "messages": [
                    {
                        "timeOffset": datasets.Value("int32"),
                        "text": datasets.Value("string"),
                        "senderWorkerId": datasets.Value("int32"),
                        "messageId": datasets.Value("int32"),
                    },
                ],
                "conversationId": datasets.Value("int32"),
                "respondentWorkerId": datasets.Value("int32"),
                "initiatorWorkerId": datasets.Value("int32"),
                "initiatorQuestions": [question_features],
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_DATA_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train_data.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test_data.jsonl"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            examples = f.readlines()
            for id_, row in enumerate(examples):
                data = json.loads(row.strip())
                d = {}
                movieMentions_list = []
                for i in data["movieMentions"]:
                    d["movieId"] = i
                    d["movieName"] = data["movieMentions"][i]
                    movieMentions_list.append(d)
                    d = {}

                respondentQuestions_list = []
                for i in data["respondentQuestions"]:
                    d["movieId"] = i
                    alpha = data["respondentQuestions"][i]
                    z = {**d, **alpha}  # merging 2 dictionaries
                    respondentQuestions_list.append(z)
                    d = {}

                initiatorQuestions_list = []
                for i in data["initiatorQuestions"]:
                    d["movieId"] = i
                    alpha = data["initiatorQuestions"][i]
                    z = {**d, **alpha}  # merging 2 dictionaries
                    initiatorQuestions_list.append(z)
                    d = {}

                yield id_, {
                    "movieMentions": movieMentions_list,
                    "respondentQuestions": respondentQuestions_list,
                    "messages": data["messages"],
                    "conversationId": data["conversationId"],
                    "respondentWorkerId": data["respondentWorkerId"],
                    "initiatorWorkerId": data["initiatorWorkerId"],
                    "initiatorQuestions": initiatorQuestions_list,
                }
