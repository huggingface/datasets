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
"""Grade School Math 8k dataset."""

import json
import textwrap

import datasets


_CITATION = """\
@misc{cobbe2021training,
      title={Training Verifiers to Solve Math Word Problems},
      author={Karl Cobbe and Vineet Kosaraju and Mohammad Bavarian and Jacob Hilton and Reiichiro Nakano and Christopher Hesse and John Schulman},
      year={2021},
      eprint={2110.14168},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
"""

_DESCRIPTION = """\
GSM8K (Grade School Math 8K) is a dataset of 8.5K high quality
linguistically diverse grade school math word problems. The
dataset was created to support the task of question answering
on basic mathematical problems that require multi-step reasoning.
"""

_HOMEPAGE = "https://openai.com/blog/grade-school-math"

_LICENSE = "MIT"

_BASE_URL = "https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/"


class Gsm8kConfig(datasets.BuilderConfig):
    """BuilderConfig for GSM8K."""

    def __init__(self, urls, **kwargs):
        """BuilderConfig for GSM8K.

        Args:
        urls: *dict[string]*, the urls for each split of the GSM8k set.
        """
        super().__init__(version=datasets.Version("1.1.0"), **kwargs)
        self.urls = urls


class Gsm8k(datasets.GeneratorBasedBuilder):
    """Grade School Math 8k (GSM8K)"""

    BUILDER_CONFIGS = [
        Gsm8kConfig(
            name="main",
            description=textwrap.dedent(
                """
                It is segmented into 7.5K training problems and 1K test problems.
                These problems take between 2 and 8 steps to solve, and solutions
                primarily involve performing a sequence of elementary calculations
                using basic arithmetic operations (+ - / *) to reach the final
                answer. A bright middle school student should be able to solve
                every problem.
                """,
            ),
            urls={
                "train": _BASE_URL + "train.jsonl",
                "test": _BASE_URL + "test.jsonl",
            },
        ),
        Gsm8kConfig(
            name="socratic",
            description=textwrap.dedent(
                """
                Additionally, there is a modified solution format that injects
                automatically generated "Socratic subquestions" before each step.
                """
            ),
            urls={
                "train": _BASE_URL + "train_socratic.jsonl",
                "test": _BASE_URL + "test_socratic.jsonl",
            },
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "question": datasets.Value("string"),
                "answer": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(self.config.urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": data_dir["test"],
                },
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                yield key, {
                    "question": data["question"],
                    "answer": data["answer"],
                }
