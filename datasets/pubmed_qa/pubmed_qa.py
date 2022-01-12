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
"""PubMedQA: A Dataset for Biomedical Research Question Answering"""


import json

import datasets


_CITATION = """\
@inproceedings{jin2019pubmedqa,
  title={PubMedQA: A Dataset for Biomedical Research Question Answering},
  author={Jin, Qiao and Dhingra, Bhuwan and Liu, Zhengping and Cohen, William and Lu, Xinghua},
  booktitle={Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)},
  pages={2567--2577},
  year={2019}
}
"""

_DESCRIPTION = """\
PubMedQA is a novel biomedical question answering (QA) dataset collected from PubMed abstracts.
The task of PubMedQA is to answer research questions with yes/no/maybe (e.g.: Do preoperative
statins reduce atrial fibrillation after coronary artery bypass grafting?) using the corresponding abstracts.
PubMedQA has 1k expert-annotated, 61.2k unlabeled and 211.3k artificially generated QA instances.
Each PubMedQA instance is composed of (1) a question which is either an existing research article
title or derived from one, (2) a context which is the corresponding abstract without its conclusion,
(3) a long answer, which is the conclusion of the abstract and, presumably, answers the research question,
and (4) a yes/no/maybe answer which summarizes the conclusion.
PubMedQA is the first QA dataset where reasoning over biomedical research texts, especially their
quantitative contents, is required to answer the questions.
"""


_HOMEPAGE = "https://pubmedqa.github.io/"

_LICENSE = """\
MIT License
Copyright (c) 2019 pubmedqa
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "ori_pqal": "https://raw.githubusercontent.com/pubmedqa/pubmedqa/master/data/ori_pqal.json",
    "ori_pqau": "https://drive.google.com/uc?export=download&id=1RsGLINVce-0GsDkCLDuLZmoLuzfmoCuQ",
    "ori_pqaa": "https://drive.google.com/uc?export=download&id=15v1x6aQDlZymaHGP7cZJZZYFfeJt2NdS",
}


class PubMedQAConfig(datasets.BuilderConfig):
    """BuilderConfig for PubMedQA"""

    def __init__(self, **kwargs):
        """
        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(PubMedQAConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class PubmedQA(datasets.GeneratorBasedBuilder):
    """PubMedQA: A Dataset for Biomedical Research Question Answering"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        PubMedQAConfig(
            name="pqa_labeled",
            description="labeled: Two annotators labeled 1k instances with yes/no/maybe to build PQA-L(abeled) for fine-tuning",
        ),
        PubMedQAConfig(
            name="pqa_unlabeled",
            description="Unlabeled: Instances with yes/no/maybe answerable questions to build PQA-U(nlabeled)",
        ),
        PubMedQAConfig(
            name="pqa_artificial",
            description="Used simple heuristic to collect many noisily-labeled instances to build PQA-A for pretraining",
        ),
    ]

    def _info(self):
        if self.config.name == "pqa_labeled":
            return datasets.DatasetInfo(
                description=_DESCRIPTION,
                features=datasets.Features(
                    {
                        "pubid": datasets.Value("int32"),
                        "question": datasets.Value("string"),
                        "context": datasets.features.Sequence(
                            {
                                "contexts": datasets.Value("string"),
                                "labels": datasets.Value("string"),
                                "meshes": datasets.Value("string"),
                                "reasoning_required_pred": datasets.Value("string"),
                                "reasoning_free_pred": datasets.Value("string"),
                            }
                        ),
                        "long_answer": datasets.Value("string"),
                        "final_decision": datasets.Value("string"),
                    }
                ),
                supervised_keys=None,
                homepage=_HOMEPAGE,
                license=_LICENSE,
                citation=_CITATION,
            )
        elif self.config.name == "pqa_unlabeled":
            return datasets.DatasetInfo(
                description=_DESCRIPTION,
                features=datasets.Features(
                    {
                        "pubid": datasets.Value("int32"),
                        "question": datasets.Value("string"),
                        "context": datasets.features.Sequence(
                            {
                                "contexts": datasets.Value("string"),
                                "labels": datasets.Value("string"),
                                "meshes": datasets.Value("string"),
                            }
                        ),
                        "long_answer": datasets.Value("string"),
                    }
                ),
                supervised_keys=None,
                homepage=_HOMEPAGE,
                license=_LICENSE,
                citation=_CITATION,
            )
        elif self.config.name == "pqa_artificial":
            return datasets.DatasetInfo(
                description=_DESCRIPTION,
                features=datasets.Features(
                    {
                        "pubid": datasets.Value("int32"),
                        "question": datasets.Value("string"),
                        "context": datasets.features.Sequence(
                            {
                                "contexts": datasets.Value("string"),
                                "labels": datasets.Value("string"),
                                "meshes": datasets.Value("string"),
                            }
                        ),
                        "long_answer": datasets.Value("string"),
                        "final_decision": datasets.Value("string"),
                    }
                ),
                supervised_keys=None,
                homepage=_HOMEPAGE,
                license=_LICENSE,
                citation=_CITATION,
            )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        downloaded_files = dl_manager.download_and_extract(_URLs)
        if self.config.name == "pqa_labeled":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["ori_pqal"]}
                )
            ]
        elif self.config.name == "pqa_artificial":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["ori_pqaa"]}
                )
            ]
        elif self.config.name == "pqa_unlabeled":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["ori_pqau"]}
                )
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for id_, row in enumerate(data):
                if self.config.name == "pqa_artificial":
                    yield id_, {
                        "pubid": row,
                        "question": data[row]["QUESTION"],
                        "context": {
                            "contexts": data[row]["CONTEXTS"],
                            "labels": data[row]["LABELS"],
                            "meshes": data[row]["MESHES"],
                        },
                        "long_answer": data[row]["LONG_ANSWER"],
                        "final_decision": data[row]["final_decision"],
                    }
                elif self.config.name == "pqa_labeled":
                    yield id_, {
                        "pubid": row,
                        "question": data[row]["QUESTION"],
                        "context": {
                            "contexts": data[row]["CONTEXTS"],
                            "labels": data[row]["LABELS"],
                            "meshes": data[row]["MESHES"],
                            "reasoning_required_pred": data[row]["reasoning_required_pred"],
                            "reasoning_free_pred": data[row]["reasoning_free_pred"],
                        },
                        "long_answer": data[row]["LONG_ANSWER"],
                        "final_decision": data[row]["final_decision"],
                    }
                elif self.config.name == "pqa_unlabeled":
                    yield id_, {
                        "pubid": row,
                        "question": data[row]["QUESTION"],
                        "context": {
                            "contexts": data[row]["CONTEXTS"],
                            "labels": data[row]["LABELS"],
                            "meshes": data[row]["MESHES"],
                        },
                        "long_answer": data[row]["LONG_ANSWER"],
                    }
