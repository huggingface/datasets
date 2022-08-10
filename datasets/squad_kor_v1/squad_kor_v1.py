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

"""KorQuAD v1.0:The Korean Question Answering Dataset"""


import json

import datasets
from datasets.tasks import QuestionAnsweringExtractive


_CITATION = """\
@article{lim2019korquad1,
  title={Korquad1. 0: Korean qa dataset for machine reading comprehension},
  author={Lim, Seungyoung and Kim, Myungji and Lee, Jooyoul},
  journal={arXiv preprint arXiv:1909.07005},
  year={2019}
}
"""

_DESCRIPTION = """\
KorQuAD 1.0 is a large-scale Korean dataset for machine reading comprehension task consisting of human generated questions for Wikipedia articles. We benchmark the data collecting process of SQuADv1.0 and crowdsourced 70,000+ question-answer pairs. 1,637 articles and 70,079 pairs of question answers were collected. 1,420 articles are used for the training set, 140 for the dev set, and 77 for the test set. 60,407 question-answer pairs are for the training set, 5,774 for the dev set, and 3,898 for the test set.
"""
_HOMEPAGE = "https://korquad.github.io/KorQuad%201.0/"
_LICENSE = "CC BY-ND 2.0 KR"

_URL = "https://korquad.github.io/dataset/"
_URLS = {
    "train": _URL + "KorQuAD_v1.0_train.json",
    "dev": _URL + "KorQuAD_v1.0_dev.json",
}


class SquadKorV1(datasets.GeneratorBasedBuilder):
    """KorQuAD 1.0 dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="squad_kor_v1",
            version=VERSION,
            description=_DESCRIPTION,
        ),
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
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[
                QuestionAnsweringExtractive(
                    question_column="question", context_column="context", answers_column="answers"
                )
            ],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # download and extract URLs
        urls_to_download = _URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            squad = json.load(f)
            for example in squad["data"]:
                title = example.get("title", "").strip()
                for paragraph in example["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
