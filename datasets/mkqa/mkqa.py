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

"""MKQA: Multilingual Knowledge Questions & Answers"""


import json

import datasets


_CITATION = """\
@misc{mkqa,
    title = {MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering},
    author = {Shayne Longpre and Yi Lu and Joachim Daiber},
    year = {2020},
    URL = {https://arxiv.org/pdf/2007.15207.pdf}
}
"""

_DESCRIPTION = """\
We introduce MKQA, an open-domain question answering evaluation set comprising 10k question-answer pairs sampled from the Google Natural Questions dataset, aligned across 26 typologically diverse languages (260k question-answer pairs in total). For each query we collected new passage-independent answers. These queries and answers were then human translated into 25 Non-English languages.
"""
_HOMEPAGE = "https://github.com/apple/ml-mkqa"
_LICENSE = "CC BY-SA 3.0"


_URLS = {"train": "https://github.com/apple/ml-mkqa/raw/master/dataset/mkqa.jsonl.gz"}


class Mkqa(datasets.GeneratorBasedBuilder):
    """MKQA dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="mkqa",
            version=VERSION,
            description=_DESCRIPTION,
        ),
    ]

    def _info(self):
        langs = [
            "ar",
            "da",
            "de",
            "en",
            "es",
            "fi",
            "fr",
            "he",
            "hu",
            "it",
            "ja",
            "ko",
            "km",
            "ms",
            "nl",
            "no",
            "pl",
            "pt",
            "ru",
            "sv",
            "th",
            "tr",
            "vi",
            "zh_cn",
            "zh_hk",
            "zh_tw",
        ]

        # Preferring list type instead of datasets.Sequence
        queries_features = {lan: datasets.Value("string") for lan in langs}
        answer_feature = [
            {
                "type": datasets.ClassLabel(
                    names=[
                        "entity",
                        "long_answer",
                        "unanswerable",
                        "date",
                        "number",
                        "number_with_unit",
                        "short_phrase",
                        "binary",
                    ]
                ),
                "entity": datasets.Value("string"),
                "text": datasets.Value("string"),
                "aliases": [datasets.Value("string")],
            }
        ]
        answer_features = {lan: answer_feature for lan in langs}

        features = datasets.Features(
            {
                "example_id": datasets.Value("string"),
                "queries": queries_features,
                "query": datasets.Value("string"),
                "answers": answer_features,
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
        # download and extract URLs
        urls_to_download = _URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]})]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for row in f:
                data = json.loads(row)
                data["example_id"] = str(data["example_id"])
                id_ = data["example_id"]
                for language in data["answers"].keys():
                    # Add default values for possible missing keys
                    for a in data["answers"][language]:
                        if "aliases" not in a:
                            a["aliases"] = []
                        if "entity" not in a:
                            a["entity"] = ""

                yield id_, data
