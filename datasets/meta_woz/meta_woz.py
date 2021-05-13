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
"""MetaLWOz: A Dataset of Multi-Domain Dialogues for the Fast Adaptation of Conversation Models"""


import json
import os

import datasets


_CITATION = """\
@InProceedings{shalyminov2020fast,
author = {Shalyminov, Igor and Sordoni, Alessandro and Atkinson, Adam and Schulz, Hannes},
title = {Fast Domain Adaptation For Goal-Oriented Dialogue Using A Hybrid Generative-Retrieval Transformer},
booktitle = {2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
year = {2020},
month = {April},
url = {https://www.microsoft.com/en-us/research/publication/fast-domain-adaptation-for-goal-oriented-dialogue-using-a
-hybrid-generative-retrieval-transformer/},
}
"""

_DESCRIPTION = """\
MetaLWOz: A Dataset of Multi-Domain Dialogues for the Fast Adaptation of Conversation Models. \
We introduce the Meta-Learning Wizard of Oz (MetaLWOz) dialogue dataset for developing fast adaptation methods for \
conversation models. This data can be used to train task-oriented dialogue models, specifically to develop methods to \
quickly simulate user responses with a small amount of data. Such fast-adaptation models fall into the research areas \
of transfer learning and meta learning. The dataset consists of 37,884 crowdsourced dialogues recorded between two \
human users in a Wizard of Oz setup, in which one was instructed to behave like a bot, and the other a true human \
user. The users are assigned a task belonging to a particular domain, for example booking a reservation at a \
particular restaurant, and work together to complete the task. Our dataset spans 47 domains having 227 tasks total. \
Dialogues are a minimum of 10 turns long.
"""

_HOMEPAGE = "https://www.microsoft.com/en-us/research/project/metalwoz/"

_LICENSE = "Microsoft Research Data License Agreement"

_URLs = {
    "train": "https://download.microsoft.com/download/E/B/8/EB84CB1A-D57D-455F-B905-3ABDE80404E5/metalwoz-v1.zip",
    "test": "https://download.microsoft.com/download/0/c/4/0c4a8893-cbf9-4a43-a44a-09bab9539234/metalwoz-test-v1.zip",
}


class MetaWoz(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="dialogues", description="The dataset of dialogues from various domains."),
        datasets.BuilderConfig(
            name="tasks", description="The metadata for tasks corresponding to dialogues from " "various domains."
        ),
    ]

    DEFAULT_CONFIG_NAME = "dialogues"

    def _info(self):
        if self.config.name == "tasks":
            features = datasets.Features(
                {
                    "task_id": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                    "bot_prompt": datasets.Value("string"),
                    "bot_role": datasets.Value("string"),
                    "user_prompt": datasets.Value("string"),
                    "user_role": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "user_id": datasets.Value("string"),
                    "bot_id": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                    "task_id": datasets.Value("string"),
                    "turns": datasets.Sequence(datasets.Value("string")),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        data_dir["test"] = dl_manager.extract(os.path.join(data_dir["test"], "dstc8_metalwoz_heldout.zip"))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"data_dir": data_dir["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"data_dir": data_dir["test"]},
            ),
        ]

    def _generate_examples(self, data_dir):
        """Yields examples."""
        if self.config.name == "tasks":
            filepath = os.path.join(data_dir, "tasks.txt")
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    yield id_, {
                        "task_id": data["task_id"],
                        "domain": data["domain"],
                        "bot_prompt": data["bot_prompt"],
                        "bot_role": data["bot_role"],
                        "user_prompt": data["user_prompt"],
                        "user_role": data["user_role"],
                    }
        else:
            id_ = -1
            base_path = os.path.join(data_dir, "dialogues")
            file_list = sorted(
                [os.path.join(base_path, file) for file in os.listdir(base_path) if file.endswith(".txt")]
            )
            for filepath in file_list:
                with open(filepath, encoding="utf-8") as f:
                    for row in f:
                        id_ += 1
                        data = json.loads(row)
                        yield id_, {
                            "id": data["id"],
                            "user_id": data["user_id"],
                            "bot_id": data["bot_id"],
                            "domain": data["domain"],
                            "task_id": data["task_id"],
                            "turns": data["turns"],
                        }
