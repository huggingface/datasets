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
"""Japanese-English Business Scene Dialogue (BSD) dataset. """


import json

import datasets


_CITATION = """\
@inproceedings{rikters-etal-2019-designing,
    title = "Designing the Business Conversation Corpus",
    author = "Rikters, Matīss  and
      Ri, Ryokan  and
      Li, Tong  and
      Nakazawa, Toshiaki",
    booktitle = "Proceedings of the 6th Workshop on Asian Translation",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-5204",
    doi = "10.18653/v1/D19-5204",
    pages = "54--61"
}
"""


_DESCRIPTION = """\
This is the Business Scene Dialogue (BSD) dataset,
a Japanese-English parallel corpus containing written conversations
in various business scenarios.

The dataset was constructed in 3 steps:
  1) selecting business scenes,
  2) writing monolingual conversation scenarios according to the selected scenes, and
  3) translating the scenarios into the other language.

Half of the monolingual scenarios were written in Japanese
and the other half were written in English.

Fields:
- id: dialogue identifier
- no: sentence pair number within a dialogue
- en_speaker: speaker name in English
- ja_speaker: speaker name in Japanese
- en_sentence: sentence in English
- ja_sentence: sentence in Japanese
- original_language: language in which monolingual scenario was written
- tag: scenario
- title: scenario title
"""

_HOMEPAGE = "https://github.com/tsuruoka-lab/BSD"

_LICENSE = "CC BY-NC-SA 4.0"

_REPO = "https://raw.githubusercontent.com/tsuruoka-lab/BSD/master/"

_URLs = {
    "train": _REPO + "train.json",
    "dev": _REPO + "dev.json",
    "test": _REPO + "test.json",
}


class BsdJaEn(datasets.GeneratorBasedBuilder):
    """Japanese-English Business Scene Dialogue (BSD) dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "tag": datasets.Value("string"),
                "title": datasets.Value("string"),
                "original_language": datasets.Value("string"),
                "no": datasets.Value("int32"),
                "en_speaker": datasets.Value("string"),
                "ja_speaker": datasets.Value("string"),
                "en_sentence": datasets.Value("string"),
                "ja_sentence": datasets.Value("string"),
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

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": data_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_dir["dev"],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

            for dialogue in data:
                id_ = dialogue["id"]
                tag = dialogue["tag"]
                title = dialogue["title"]
                original_language = dialogue["original_language"]
                conversation = dialogue["conversation"]

                for turn in conversation:
                    sent_no = int(turn["no"])
                    en_speaker = turn["en_speaker"]
                    ja_speaker = turn["ja_speaker"]
                    en_sentence = turn["en_sentence"]
                    ja_sentence = turn["ja_sentence"]

                    yield f"{id_}_{sent_no}", {
                        "id": id_,
                        "tag": tag,
                        "title": title,
                        "original_language": original_language,
                        "no": sent_no,
                        "en_speaker": en_speaker,
                        "ja_speaker": ja_speaker,
                        "en_sentence": en_sentence,
                        "ja_sentence": ja_sentence,
                    }
