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
"""XCSR: A dataset for cross-lingual commonsense reasoning."""


import json
import os

import datasets


_CITATION = """\
# X-CSR
@inproceedings{lin-etal-2021-xcsr,
    title = "Common Sense Beyond English: Evaluating and Improving Multilingual Language Models for Commonsense Reasoning",
    author = "Lin, Bill Yuchen and Lee, Seyeon and Qiao, Xiaoyang and Ren, Xiang",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL-IJCNLP 2021)",
    year = "2021",
    note={to appear}
}

# CSQA
@inproceedings{Talmor2019commonsenseqaaq,
    address = {Minneapolis, Minnesota},
    author = {Talmor, Alon  and Herzig, Jonathan  and Lourie, Nicholas and Berant, Jonathan},
    booktitle = {Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)},
    doi = {10.18653/v1/N19-1421},
    pages = {4149--4158},
    publisher = {Association for Computational Linguistics},
    title = {CommonsenseQA: A Question Answering Challenge Targeting Commonsense Knowledge},
    url = {https://www.aclweb.org/anthology/N19-1421},
    year = {2019}
}

# CODAH
@inproceedings{Chen2019CODAHAA,
    address = {Minneapolis, USA},
    author = {Chen, Michael  and D{'}Arcy, Mike  and Liu, Alisa  and Fernandez, Jared  and Downey, Doug},
    booktitle = {Proceedings of the 3rd Workshop on Evaluating Vector Space Representations for {NLP}},
    doi = {10.18653/v1/W19-2008},
    pages = {63--69},
    publisher = {Association for Computational Linguistics},
    title = {CODAH: An Adversarially-Authored Question Answering Dataset for Common Sense},
    url = {https://www.aclweb.org/anthology/W19-2008},
    year = {2019}
}
"""

_DESCRIPTION = """\
To evaluate multi-lingual language models (ML-LMs) for commonsense reasoning in a cross-lingual zero-shot transfer setting (X-CSR), i.e., training in English and test in other languages, we create two benchmark datasets, namely X-CSQA and X-CODAH. Specifically, we automatically translate the original CSQA and CODAH datasets, which only have English versions, to 15 other languages, forming development and test sets for studying X-CSR. As our goal is to evaluate different ML-LMs in a unified evaluation protocol for X-CSR, we argue that such translated examples, although might contain noise, can serve as a starting benchmark for us to obtain meaningful analysis, before more human-translated datasets will be available in the future.
"""

_HOMEPAGE = "https://inklab.usc.edu//XCSR/"

# TODO: Add the licence for the dataset here if you can find it
# _LICENSE = ""

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)

_URL = "https://inklab.usc.edu/XCSR/xcsr_datasets.zip"

_LANGUAGES = ("en", "zh", "de", "es", "fr", "it", "jap", "nl", "pl", "pt", "ru", "ar", "vi", "hi", "sw", "ur")


class XcsrConfig(datasets.BuilderConfig):
    """BuilderConfig for XCSR."""

    def __init__(self, subset: str, language: str, **kwargs):
        """BuilderConfig for XCSR.
        Args:
        language: One of {en, zh, de, es, fr, it, jap, nl, pl, pt, ru, ar, vi, hi, sw, ur}, or all_languages
          **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(name=f"{subset}-{language}", **kwargs)
        self.subset = subset
        self.language = language


class Xcsr(datasets.GeneratorBasedBuilder):
    """XCSR: A dataset for evaluating multi-lingual language models (ML-LMs) for commonsense reasoning in a
    cross-lingual zero-shot transfer setting"""

    BUILDER_CONFIG_CLASS = XcsrConfig
    BUILDER_CONFIGS = [
        XcsrConfig(
            subset="X-CSQA",
            language=lang,
            version=datasets.Version("1.1.0", ""),
            description=f"Plain text import of X-CSQA for the {lang} language",
        )
        for lang in _LANGUAGES
    ] + [
        XcsrConfig(
            subset="X-CODAH",
            language=lang,
            version=datasets.Version("1.1.0", ""),
            description=f"Plain text import of X-CODAH for the {lang} language",
        )
        for lang in _LANGUAGES
    ]

    def _info(self):
        if self.config.subset == "X-CSQA":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "lang": datasets.Value("string"),
                    "question": {
                        "stem": datasets.Value("string"),
                        "choices": datasets.features.Sequence(
                            {
                                "label": datasets.Value("string"),
                                "text": datasets.Value("string"),
                            }
                        ),
                    },
                    "answerKey": datasets.Value("string"),
                }
            )
        elif self.config.subset == "X-CODAH":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "lang": datasets.Value("string"),
                    "question_tag": datasets.Value("string"),
                    "question": {
                        "stem": datasets.Value("string"),
                        "choices": datasets.features.Sequence(
                            {
                                "label": datasets.Value("string"),
                                "text": datasets.Value("string"),
                            }
                        ),
                    },
                    "answerKey": datasets.Value("string"),
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        filepath = os.path.join(data_dir, "X-CSR_datasets", self.config.subset, self.config.language, "{split}.jsonl")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": filepath.format(split="test"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": filepath.format(split="dev"),
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples as (key, example) tuples."""
        with open(filepath, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                _ = data.setdefault("answerKey", "")
                yield key, data
