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
"""LiveQA dataset."""


import json

import datasets


_CITATION = """\
@inproceedings{qianying-etal-2020-liveqa,
    title = "{L}ive{QA}: A Question Answering Dataset over Sports Live",
    author = "Qianying, Liu  and
      Sicong, Jiang  and
      Yizhong, Wang  and
      Sujian, Li",
    booktitle = "Proceedings of the 19th Chinese National Conference on Computational Linguistics",
    month = oct,
    year = "2020",
    address = "Haikou, China",
    publisher = "Chinese Information Processing Society of China",
    url = "https://www.aclweb.org/anthology/2020.ccl-1.98",
    pages = "1057--1067"
}
"""

_DESCRIPTION = """\
This is LiveQA, a Chinese dataset constructed from play-by-play live broadcast.
It contains 117k multiple-choice questions written by human commentators for over 1,670 NBA games,
which are collected from the Chinese Hupu website.
"""

_HOMEPAGE = "https://github.com/PKU-TANGENT/LiveQA"

_REPO = "https://raw.githubusercontent.com/PKU-TANGENT/LiveQA/master/"
_URLs = [f"{_REPO}LiveQA-{i}.json" for i in range(1, 6)]


class LiveQA(datasets.GeneratorBasedBuilder):
    """LiveQA dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("int64"),
                "passages": datasets.Sequence(
                    {
                        "is_question": datasets.Value("bool"),
                        "text": datasets.Value("string"),
                        "candidate1": datasets.Value("string"),
                        "candidate2": datasets.Value("string"),
                        "answer": datasets.Value("string"),
                    }
                ),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # No default split.
        # Data is separated into 5 files due to size restrictions,
        # but they must be concatenated to create a well-formed json.

        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepaths": data_dir, "split": "train"},
            )
        ]

    def _generate_examples(self, filepaths, split):
        """Yields examples."""

        data_raw = ""
        for filepath in filepaths:
            with open(filepath, "r", encoding="utf-8") as f:
                data_raw += f.read()

        data = json.loads(data_raw)
        games = data["passages"]

        game_id = -1  # "id" field is always 1 in the original dataset regardless of game
        for game in games:
            game_id += 1
            passages = []
            for passage in game["passage"]:
                is_question = "question" in passage
                text = passage["question"] if is_question else passage["text"]
                candidate_1 = passage["candidate1"] if is_question else ""
                candidate_2 = passage["candidate2"] if is_question else ""
                answer = passage["answer"] if is_question else ""

                passages.append(
                    {
                        "is_question": is_question,
                        "text": text,
                        "candidate1": candidate_1,
                        "candidate2": candidate_2,
                        "answer": answer,
                    }
                )

            yield game_id, {"id": game_id, "passages": passages}
