# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3
"""CRD3  dataset"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """
@misc{campos2020doqa,
    title={DoQA -- Accessing Domain-Specific FAQs via Conversational QA},
    author={Jon Ander Campos and Arantxa Otegi and Aitor Soroa and Jan Deriu and Mark Cieliebak and Eneko Agirre},
    year={2020},
    eprint={2005.01328},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
 """

_DESCRIPTION = """
DoQA is a dataset for accessing Domain Specific FAQs via conversational QA that contains 2,437 information-seeking question/answer dialogues
(10,917 questions in total) on three different domains: cooking, travel and movies. Note that we include in the generic concept of FAQs also
Community Question Answering sites, as well as corporate information in intranets which is maintained in textual form similar to FAQs, often
referred to as internal “knowledge bases”.

These dialogues are created by crowd workers that play the following two roles: the user who asks questions about a given topic posted in Stack
Exchange (https://stackexchange.com/), and the domain expert who replies to the questions by selecting a short span of text from the long textual
reply in the original post. The expert can rephrase the selected span, in order to make it look more natural. The dataset covers unanswerable
questions and some relevant dialogue acts.

DoQA enables the development and evaluation of conversational QA systems that help users access the knowledge buried in domain specific FAQs.
"""

_URL = "https://ixa2.si.ehu.es/convai/doqa-v2.1.zip"


class DoqaConfig(datasets.BuilderConfig):
    """BuilderConfig for DoQA."""

    def __init__(self, **kwargs):
        """Constructs a DoQA.

        Args:
        **kwargs: keyword arguments forwarded to super.
        """

        super(DoqaConfig, self).__init__(version=datasets.Version("2.1.0", ""), **kwargs)


class Doqa(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        DoqaConfig(
            name="cooking",
        ),
        DoqaConfig(
            name="movies",
        ),
        DoqaConfig(
            name="travel",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "background": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "id": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                    "followup": datasets.Value("string"),
                    "yesno": datasets.Value("string"),
                    "orig_answer": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            homepage="http://ixa.eus/node/12931",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_URL)
        if self.config.name == "cooking":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(path, "doqa-v2.1", "doqa_dataset", "doqa-cooking-test-v2.1.json")
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": os.path.join(path, "doqa-v2.1", "doqa_dataset", "doqa-cooking-dev-v2.1.json")
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(path, "doqa-v2.1", "doqa_dataset", "doqa-cooking-train-v2.1.json")
                    },
                ),
            ]
        elif self.config.name == "movies":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(path, "doqa-v2.1", "doqa_dataset", "doqa-movies-test-v2.1.json")
                    },
                )
            ]
        elif self.config.name == "travel":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(path, "doqa-v2.1", "doqa_dataset", "doqa-travel-test-v2.1.json")
                    },
                )
            ]
        else:
            raise ValueError("Unknown config name")

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for row in data["data"]:
                title = row["title"]
                background = row["background"]
                paragraphs = row["paragraphs"]
                for p in paragraphs:
                    context = p["context"]
                    qas = p["qas"]
                    for qa in qas:
                        question = qa["question"]
                        answers = qa["answers"]
                        id1 = qa["id"]
                        yesno = qa["yesno"]
                        followup = qa["followup"]
                        answer_text = [answer["text"] for answer in answers]
                        answer_start = [answer["answer_start"] for answer in answers]

                        orig_answer_start = [qa["orig_answer"]["answer_start"]]
                        orig_answer_text = [qa["orig_answer"]["text"]]
                        yield id1, {
                            "title": title,
                            "background": background,
                            "context": context,
                            "question": question,
                            "id": id1,
                            "answers": {
                                "text": answer_text,
                                "answer_start": answer_start,
                            },
                            "followup": followup,
                            "yesno": yesno,
                            "orig_answer": {
                                "text": orig_answer_text,
                                "answer_start": orig_answer_start,
                            },
                        }
