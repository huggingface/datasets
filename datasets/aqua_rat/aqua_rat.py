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
"""AQUA-RAT (Algebra Question Answering with Rationales) Dataset"""


import json

import datasets


_CITATION = """\
@InProceedings{ACL,
title = {Program induction by rationale generation: Learning to solve and explain algebraic word problems},
authors={Ling, Wang and Yogatama, Dani and Dyer, Chris and Blunsom, Phil},
year={2017}
}
"""

_DESCRIPTION = """\
A large-scale dataset consisting of approximately 100,000 algebraic word problems.
The solution to each question is explained step-by-step using natural language.
This data is used to train a program generation model that learns to generate the explanation,
while generating the program that solves the question.
"""

_LICENSE = """\
Copyright 2017 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

_BASE_URL = "https://raw.githubusercontent.com/deepmind/AQuA/master/"
_URLs = {
    "raw": {"train": _BASE_URL + "train.json", "dev": _BASE_URL + "dev.json", "test": _BASE_URL + "test.json"},
    "tokenized": {
        "train": _BASE_URL + "train.tok.json",
        "dev": _BASE_URL + "dev.tok.json",
        "test": _BASE_URL + "test.tok.json",
    },
}


class AquaRat(datasets.GeneratorBasedBuilder):
    """AQUA-RAT (Algebra Question Answering with Rationales) Dataset"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="raw", description="Untokenized Dataset"),
        datasets.BuilderConfig(name="tokenized", description="Tokenized Dataset"),
    ]

    DEFAULT_CONFIG_NAME = "raw"

    def _info(self):
        features = datasets.Features(
            {
                "question": datasets.Value("string"),
                "options": datasets.features.Sequence(datasets.Value("string")),
                "rationale": datasets.Value("string"),
                "correct": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://github.com/deepmind/AQuA",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_paths = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_paths["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": data_paths["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_paths["dev"],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "question": data["question"],
                    "options": data["options"],
                    "rationale": data["rationale"],
                    "correct": data["correct"],
                }
