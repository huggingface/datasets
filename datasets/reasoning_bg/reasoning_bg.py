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
"""TODO: Add a description here."""


import json
import os

import datasets


_CITATION = """\
@article{hardalov2019beyond,
  title={Beyond english-only reading comprehension: Experiments in zero-shot multilingual transfer for bulgarian},
  author={Hardalov, Momchil and Koychev, Ivan and Nakov, Preslav},
  journal={arXiv preprint arXiv:1908.01519},
  year={2019}
}
"""

_DESCRIPTION = """\
This new dataset is designed to do reading comprehension in Bulgarian language.
"""

_HOMEPAGE = "https://github.com/mhardalov/bg-reason-BERT"

_LICENSE = "Apache-2.0 License"

_URL = "https://raw.githubusercontent.com/mhardalov/bg-reason-BERT/master/data/bg_rc-v1.0.json"


class ReasoningBg(datasets.GeneratorBasedBuilder):
    """To test reasoning comprehension in Bulgarian Language"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="biology-12th", version=VERSION, description="MCQs in Biology of 12th Grade Matriculation Exam"
        ),
        datasets.BuilderConfig(
            name="philosophy-12th", version=VERSION, description="MCQs in Philosophy of 12th Grade Matriculation Exam"
        ),
        datasets.BuilderConfig(
            name="geography-12th", version=VERSION, description="MCQs in Geography of 12th Grade Matriculation Exam"
        ),
        datasets.BuilderConfig(
            name="history-12th", version=VERSION, description="MCQs in History of 12th Grade Matriculation Exam"
        ),
        datasets.BuilderConfig(
            name="history-quiz", version=VERSION, description="MCQs in Bulgarian History from Online History Quizzes"
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "url": datasets.Value("string"),
                "qid": datasets.Value("int32"),
                "question": datasets.Value("string"),
                "answers": datasets.Sequence(datasets.Value("string")),
                "correct": datasets.Value("string"),
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

        downloaded_path = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(downloaded_path),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
            data = json.loads(content)["data"][self.config.name]
            for page in data:
                url = page["url"]
                for question in page["questions"]:
                    yield str(question["id"]), {
                        "url": url,
                        "id": question["id"],
                        "qid": question["qid"],
                        "question": question["question"],
                        "answers": question["answers"],
                        "correct": question["correct"],
                    }
