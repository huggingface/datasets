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
"""Information Seeking in the Spirit of Learning: a Dataset for Conversational Curiosity"""


import json
import os

import datasets


_CITATION = """\
@inproceedings{rodriguez2020curiosity,
    title = {Information Seeking in the Spirit of Learning: a Dataset for Conversational Curiosity},
    author = {Pedro Rodriguez and Paul Crook and Seungwhan Moon and Zhiguang Wang},
    year = 2020,
    booktitle = {Empirical Methods in Natural Language Processing}
}
"""


_DESCRIPTION = """\
This dataset contains 14K dialogs (181K utterances) where users and assistants converse about geographic topics like
geopolitical entities and locations. This dataset is annotated with pre-existing user knowledge, message-level dialog
acts, grounding to Wikipedia, and user reactions to messages.
"""

_HOMEPAGE = "https://www.pedro.ai/curiosity"

_LICENSE = "https://github.com/facebookresearch/curiosity/blob/master/LICENSE"

_URL = "https://obj.umiacs.umd.edu/curiosity/"
_URLs = {
    "train": _URL + "curiosity_dialogs.train.json",
    "val": _URL + "curiosity_dialogs.val.json",
    "test": _URL + "curiosity_dialogs.test.json",
    "test_zero": _URL + "curiosity_dialogs.test_zero.json",
}


class CuriosityDialogsConfig(datasets.BuilderConfig):
    """BuilderConfig for Curiosity Dialogs dataset"""

    def __init__(self, **kwargs):
        """BuilderConfig for Curiosity Dialogs dataset.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(CuriosityDialogsConfig, self).__init__(**kwargs)


class CuriosityDialogs(datasets.GeneratorBasedBuilder):
    """Information Seeking in the Spirit of Learning: a Dataset for Conversational Curiosity"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        CuriosityDialogsConfig(
            name="curiosity_dialogs",
            version=datasets.Version("1.1.0"),
            description="Curiosity Dialog: A Dataset for Conversational Curiosity",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "messages": datasets.Sequence(
                        {
                            "message": datasets.Value("string"),
                            "liked": datasets.ClassLabel(names=["False", "True"]),
                            "sender": datasets.ClassLabel(names=["user", "assistant"]),
                            "facts": datasets.Sequence(
                                {
                                    "fid": datasets.Value("int32"),
                                    "used": datasets.ClassLabel(names=["False", "True"]),
                                    "source": datasets.ClassLabel(names=["section", "known", "random"]),
                                }
                            ),
                            "message_id": datasets.Value("string"),
                            "dialog_acts": datasets.Sequence(datasets.Value("string")),
                        }
                    ),
                    "known_entities": datasets.Sequence(datasets.Value("string")),
                    "focus_entity": datasets.Value("string"),
                    "dialog_id": datasets.Value("int32"),
                    "inferred_steps": datasets.ClassLabel(names=["False", "True"]),
                    "created_time": datasets.Value("int64"),
                    "aspects": datasets.Sequence(datasets.Value("string")),
                    "first_aspect": datasets.Value("string"),
                    "second_aspect": datasets.Value("string"),
                    "shuffle_facts": datasets.ClassLabel(names=["False", "True"]),
                    "related_entities": datasets.Sequence(datasets.Value("string")),
                    "tag": datasets.Value("string"),
                    "user_id": datasets.Value("int32"),
                    "assistant_id": datasets.Value("int32"),
                    "is_annotated": datasets.ClassLabel(names=["False", "True"]),
                    "user_dialog_rating": datasets.Value("int32"),
                    "user_other_agent_rating": datasets.Value("int32"),
                    "assistant_dialog_rating": datasets.Value("int32"),
                    "assistant_other_agent_rating": datasets.Value("int32"),
                    "reported": datasets.ClassLabel(names=["False", "True"]),
                    "annotated": datasets.ClassLabel(names=["False", "True"]),
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
                name="train",
                gen_kwargs={
                    "filepath": os.path.join(data_dir["train"]),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name="val",
                gen_kwargs={"filepath": os.path.join(data_dir["val"]), "split": "val"},
            ),
            datasets.SplitGenerator(
                name="test",
                gen_kwargs={
                    "filepath": os.path.join(data_dir["test"]),
                    "split": "test_zero",
                },
            ),
            datasets.SplitGenerator(
                name="test_zero",
                gen_kwargs={
                    "filepath": os.path.join(data_dir["test_zero"]),
                    "split": "test_zero",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        # Bool entries are converted to string entries because of PyArrow error
        with open(filepath, encoding="utf-8") as f:
            dataset = json.load(f)
            dialogs = dataset["dialogs"]

            for id_, data in enumerate(dialogs):
                messages = data["messages"]

                for message in messages:
                    message["liked"] = str(message["liked"])
                    facts = message["facts"]

                    for fact in facts:
                        fact["used"] = str(fact["used"])

                known_entities = data["known_entities"]
                focus_entity = data["focus_entity"]
                dialog_id = data["dialog_id"]
                inferred_steps = str(data["inferred_steps"])
                created_time = data["created_time"]
                aspects = data["aspects"]
                first_aspect = data["first_aspect"]
                second_aspect = data["second_aspect"]
                shuffle_facts = str(data["shuffle_facts"])
                related_entities = data["related_entities"]
                tag = data["tag"]
                user_id = data["user_id"]
                assistant_id = data["assistant_id"]
                is_annotated = str(data["is_annotated"])
                user_dialog_rating = data["user_dialog_rating"]
                user_other_agent_rating = data["user_other_agent_rating"]
                assistant_dialog_rating = data["assistant_dialog_rating"]
                assistant_other_agent_rating = data["assistant_other_agent_rating"]
                reported = str(data["reported"])
                annotated = str(data["annotated"])

                yield id_, {
                    "messages": messages,
                    "known_entities": known_entities,
                    "focus_entity": focus_entity,
                    "dialog_id": dialog_id,
                    "inferred_steps": inferred_steps,
                    "created_time": created_time,
                    "aspects": aspects,
                    "first_aspect": first_aspect,
                    "second_aspect": second_aspect,
                    "shuffle_facts": shuffle_facts,
                    "related_entities": related_entities,
                    "tag": tag,
                    "user_id": user_id,
                    "assistant_id": assistant_id,
                    "is_annotated": is_annotated,
                    "user_dialog_rating": user_dialog_rating,
                    "user_other_agent_rating": user_other_agent_rating,
                    "assistant_dialog_rating": assistant_dialog_rating,
                    "assistant_other_agent_rating": assistant_other_agent_rating,
                    "reported": reported,
                    "annotated": annotated,
                }
