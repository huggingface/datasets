# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""ZEST: ZEroShot learning from Task descriptions"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_DESCRIPTION = """\
ZEST tests whether NLP systems can perform unseen tasks in a zero-shot way, given a natural language description of
the task. It is an instantiation of our proposed framework "learning from task descriptions". The tasks include
classification, typed entity extraction and relationship extraction, and each task is paired with 20 different
annotated (input, output) examples. ZEST's structure allows us to systematically test whether models can generalize
in five different ways.
"""

_CITATION = """\
@inproceedings{weller-etal-2020-learning,
    title = "Learning from Task Descriptions",
    author = "Weller, Orion  and
      Lourie, Nicholas  and
      Gardner, Matt  and
      Peters, Matthew",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.105",
    pages = "1361--1375",
    abstract = "Typically, machine learning systems solve new tasks by training on thousands of examples. In contrast, humans can solve new tasks by reading some instructions, with perhaps an example or two. To take a step toward closing this gap, we introduce a framework for developing NLP systems that solve new tasks after reading their descriptions, synthesizing prior work in this area. We instantiate this frame- work with a new English language dataset, ZEST, structured for task-oriented evaluation on unseen tasks. Formulating task descriptions as questions, we ensure each is general enough to apply to many possible inputs, thus comprehensively evaluating a model{'}s ability to solve each task. Moreover, the dataset{'}s structure tests specific types of systematic generalization. We find that the state-of-the-art T5 model achieves a score of 12% on ZEST, leaving a significant challenge for NLP researchers.",
}
"""

_DOWNLOAD_URL = "https://ai2-datasets.s3-us-west-2.amazonaws.com/zest/zest.zip"
_WEBPAGE = "https://allenai.org/data/zest"


class Zest(datasets.GeneratorBasedBuilder):
    """ZEST: ZEroShot learning from Task descriptions"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "task_id": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "generalization_type": datasets.Value("string"),
                    "derives_from": datasets.Sequence(datasets.Value("string")),
                    "domain": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "answer": datasets.Sequence(datasets.Value("string")),
                    "all_answers": datasets.Sequence(datasets.Value("string")),
                }
            ),
            homepage=_WEBPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        path = os.path.join(path, "zest")

        train_path = os.path.join(path, "train.jsonl")
        validation_path = os.path.join(path, "dev.jsonl")
        test_path = os.path.join(path, "test_unanswered.jsonl")

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": validation_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path, "is_labeled": False}),
        ]

    def _generate_examples(self, filepath, is_labeled=True):
        """Generate AG News examples."""
        counter = 0
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                task = json.loads(line)
                base_dict = {
                    "task_id": task["id"],
                    "question": task["question"],
                    "generalization_type": task["type"]["generalization_type"] if is_labeled else None,
                    "derives_from": task["type"]["derives_from"] if is_labeled else [],
                    "domain": task["type"]["domain"] if is_labeled else None,
                }

                for example in task["examples"]:
                    answer = example["answer"] if is_labeled else []
                    if isinstance(answer, str):
                        answer = [answer]
                    yield counter, dict(
                        context=example["context"],
                        answer=answer,
                        all_answers=example["all_answers"] if is_labeled else [],
                        **base_dict,
                    )
                    counter += 1
