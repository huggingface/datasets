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
"""QUAC (Question Answering in Context)."""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """\
@inproceedings{choi-etal-2018-quac,
title = "QUAC: Question answering in context",
abstract = "We present QuAC, a dataset for Question Answering in Context that contains 14K information-seeking QA dialogs (100K questions in total). The dialogs involve two crowd workers: (1) a student who poses a sequence of freeform questions to learn as much as possible about a hidden Wikipedia text, and (2) a teacher who answers the questions by providing short excerpts from the text. QuAC introduces challenges not found in existing machine comprehension datasets: its questions are often more open-ended, unanswerable, or only meaningful within the dialog context, as we show in a detailed qualitative evaluation. We also report results for a number of reference models, including a recently state-of-the-art reading comprehension architecture extended to model dialog context. Our best model underperforms humans by 20 F1, suggesting that there is significant room for future work on this data. Dataset, baseline, and leaderboard available at http://quac.ai.",
author = "Eunsol Choi and He He and Mohit Iyyer and Mark Yatskar and Yih, {Wen Tau} and Yejin Choi and Percy Liang and Luke Zettlemoyer",
year = "2018",
language = "English (US)",
series = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, EMNLP 2018",
publisher = "Association for Computational Linguistics",
pages = "2174--2184",
editor = "Ellen Riloff and David Chiang and Julia Hockenmaier and Jun'ichi Tsujii",
booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, EMNLP 2018",
note = "2018 Conference on Empirical Methods in Natural Language Processing, EMNLP 2018 ; Conference date: 31-10-2018 Through 04-11-2018",
}
"""

_DESCRIPTION = """\
Question Answering in Context is a dataset for modeling, understanding,
and participating in information seeking dialog. Data instances consist
of an interactive dialog between two crowd workers: (1) a student who
poses a sequence of freeform questions to learn as much as possible
about a hidden Wikipedia text, and (2) a teacher who answers the questions
by providing short excerpts (spans) from the text. QuAC introduces
challenges not found in existing machine comprehension datasets: its
questions are often more open-ended, unanswerable, or only meaningful
within the dialog context.
"""

_HOMEPAGE = "https://quac.ai/"

_LICENSE = "MIT"

_URLs = {
    "train": "https://s3.amazonaws.com/my89public/quac/train_v0.2.json",
    "validation": "https://s3.amazonaws.com/my89public/quac/val_v0.2.json",
}


class Quac(datasets.GeneratorBasedBuilder):
    """QuAC (Question Answering in Context)."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            description="Plain text",
            version=VERSION,
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "dialogue_id": datasets.Value("string"),
                    "wikipedia_page_title": datasets.Value("string"),
                    "background": datasets.Value("string"),
                    "section_title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "turn_ids": datasets.Sequence(datasets.Value("string")),
                    "questions": datasets.Sequence(datasets.Value("string")),
                    "followups": datasets.Sequence(datasets.ClassLabel(names=["y", "n", "m"])),
                    "yesnos": datasets.Sequence(datasets.ClassLabel(names=["y", "n", "x"])),
                    "answers": datasets.Sequence(
                        {
                            "texts": datasets.Sequence(datasets.Value("string")),
                            "answer_starts": datasets.Sequence(datasets.Value("int32")),
                        }
                    ),
                    "orig_answers": {
                        "texts": datasets.Sequence(datasets.Value("string")),
                        "answer_starts": datasets.Sequence(datasets.Value("int32")),
                    },
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
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_dir["validation"],
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            squad = json.load(f)
            for section in squad["data"]:
                wiki_page_title = section.get("title", "").strip()
                background = section.get("background", "").strip()
                section_title = section.get("section_title", "").strip()

                for dialogue in section["paragraphs"]:
                    context = dialogue["context"].strip()
                    dialogue_id = dialogue["id"]

                    followups = []
                    yesnos = []
                    questions = []
                    turn_ids = []
                    answers = []
                    orig_answers = {"texts": [], "answer_starts": []}

                    for turn in dialogue["qas"]:
                        followups.append(turn["followup"])
                        yesnos.append(turn["yesno"])
                        questions.append(turn["question"])
                        turn_ids.append(turn["id"])

                        ans_ = {
                            "texts": [t["text"].strip() for t in turn["answers"]],
                            "answer_starts": [t["answer_start"] for t in turn["answers"]],
                        }
                        answers.append(ans_)

                        orig_answers["texts"].append(turn["orig_answer"]["text"])
                        orig_answers["answer_starts"].append(turn["orig_answer"]["answer_start"])

                    yield dialogue_id, {
                        "dialogue_id": dialogue_id,
                        "wikipedia_page_title": wiki_page_title,
                        "background": background,
                        "section_title": section_title,
                        "context": context,
                        "turn_ids": turn_ids,
                        "questions": questions,
                        "followups": followups,
                        "yesnos": yesnos,
                        "answers": answers,
                        "orig_answers": orig_answers,
                    }
