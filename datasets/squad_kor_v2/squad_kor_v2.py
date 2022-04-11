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

"""KorQuAD v2.1:The Korean Question Answering Dataset"""


import json
import os

import datasets


_CITATION = """\
@article{NODE09353166,
    author={Youngmin Kim,Seungyoung Lim;Hyunjeong Lee;Soyoon Park;Myungji Kim},
    title={{KorQuAD 2.0: Korean QA Dataset for Web Document Machine Comprehension}},
    booltitle={{Journal of KIISE 제47권 제6호}},
    journal={{Journal of KIISE}},
    volume={{47}},
    issue={{6}},
    publisher={The Korean Institute of Information Scientists and Engineers},
    year={2020},
    ISSN={{2383-630X}},
    pages={577-586},
    url={http://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE09353166}}
"""

_DESCRIPTION = """\
KorQuAD 2.0 is a Korean question and answering dataset consisting of a total of 100,000+ pairs. There are three major differences from KorQuAD 1.0, which is the standard Korean Q & A data. The first is that a given document is a whole Wikipedia page, not just one or two paragraphs. Second, because the document also contains tables and lists, it is necessary to understand the document structured with HTML tags. Finally, the answer can be a long text covering not only word or phrase units, but paragraphs, tables, and lists. As a baseline model, BERT Multilingual is used, released by Google as an open source. It shows 46.0% F1 score, a very low score compared to 85.7% of the human F1 score. It indicates that this data is a challenging task. Additionally, we increased the performance by no-answer data augmentation. Through the distribution of this data, we intend to extend the limit of MRC that was limited to plain text to real world tasks of various lengths and formats.
"""
_HOMEPAGE = "https://korquad.github.io/"
_LICENSE = "CC BY-ND 2.0 KR"

_URL = "https://github.com/korquad/korquad.github.io/raw/master/dataset/KorQuAD_2.1"
_URLS = {
    "train": [
        _URL + "/train/KorQuAD_2.1_train_00.zip",
        _URL + "/train/KorQuAD_2.1_train_01.zip",
        _URL + "/train/KorQuAD_2.1_train_02.zip",
        _URL + "/train/KorQuAD_2.1_train_03.zip",
        _URL + "/train/KorQuAD_2.1_train_04.zip",
        _URL + "/train/KorQuAD_2.1_train_05.zip",
        _URL + "/train/KorQuAD_2.1_train_06.zip",
        _URL + "/train/KorQuAD_2.1_train_07.zip",
        _URL + "/train/KorQuAD_2.1_train_08.zip",
        _URL + "/train/KorQuAD_2.1_train_09.zip",
        _URL + "/train/KorQuAD_2.1_train_10.zip",
        _URL + "/train/KorQuAD_2.1_train_11.zip",
        _URL + "/train/KorQuAD_2.1_train_12.zip",
    ],
    "validation": [_URL + "/dev/KorQuAD_2.1_dev_00.zip", _URL + "/dev/KorQuAD_2.1_dev_01.zip"],
}


class SquadKorV2(datasets.GeneratorBasedBuilder):
    """KorQuAD 2.1 dataset"""

    VERSION = datasets.Version("2.1.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="squad_kor_v2", version=VERSION, description=_DESCRIPTION),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer": datasets.Features(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                            "html_answer_start": datasets.Value("int32"),
                        }
                    ),
                    "url": datasets.Value("string"),
                    "raw_html": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # download and extract URLs
        urls_to_download = _URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"dirs": downloaded_files["train"]}),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"dirs": downloaded_files["validation"]}
            ),
        ]

    def _generate_examples(self, dirs):
        """Yields examples."""

        for d in dirs:
            filepaths = sorted(os.scandir(d), key=lambda x: x.name)
            for filepath in filepaths:
                with open(filepath, encoding="utf-8") as f:
                    squad = json.load(f)
                    for example in squad["data"]:
                        title = example.get("title", "").strip()
                        url = example.get("url", "").strip()
                        raw_html = example.get("raw_html", "").strip()
                        context = example["context"].strip()
                        for qa in example["qas"]:
                            question = qa["question"].strip()
                            answer = qa["answer"]
                            id_ = qa["id"]

                            answer_start = answer["answer_start"]
                            html_answer_start = answer["html_answer_start"]
                            answer_text = answer["text"].strip()

                            yield id_, {
                                "title": title,
                                "context": context,
                                "question": question,
                                "id": id_,
                                "answer": {
                                    "answer_start": answer_start,
                                    "html_answer_start": html_answer_start,
                                    "text": answer_text,
                                },
                                "url": url,
                                "raw_html": raw_html,
                            }
