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
"""TruthfulQA dataset."""


import csv
import json

import datasets


_CITATION = """\
@misc{lin2021truthfulqa,
    title={TruthfulQA: Measuring How Models Mimic Human Falsehoods},
    author={Stephanie Lin and Jacob Hilton and Owain Evans},
    year={2021},
    eprint={2109.07958},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
TruthfulQA is a benchmark to measure whether a language model is truthful in
generating answers to questions. The benchmark comprises 817 questions that
span 38 categories, including health, law, finance and politics. Questions are
crafted so that some humans would answer falsely due to a false belief or
misconception. To perform well, models must avoid generating false answers
learned from imitating human texts.
"""

_HOMEPAGE = "https://github.com/sylinrl/TruthfulQA"

_LICENSE = "Apache License 2.0"


class TruthfulQaConfig(datasets.BuilderConfig):
    """BuilderConfig for TruthfulQA."""

    def __init__(self, url, features, **kwargs):
        """BuilderConfig for TruthfulQA.
        Args:
          url: *string*, the url to the configuration's data.
          features: *list[string]*, list of features that'll appear in the feature dict.
          **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(version=datasets.Version("1.1.0"), **kwargs)
        self.url = url
        self.features = features


class TruthfulQa(datasets.GeneratorBasedBuilder):
    """TruthfulQA is a benchmark to measure whether a language model is truthful in generating answers to questions."""

    BUILDER_CONFIGS = [
        TruthfulQaConfig(
            name="generation",
            url="https://raw.githubusercontent.com/sylinrl/TruthfulQA/013686a06be7a7bde5bf8223943e106c7250123c/TruthfulQA.csv",
            features=datasets.Features(
                {
                    "type": datasets.Value("string"),
                    "category": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "best_answer": datasets.Value("string"),
                    "correct_answers": datasets.features.Sequence(datasets.Value("string")),
                    "incorrect_answers": datasets.features.Sequence(datasets.Value("string")),
                    "source": datasets.Value("string"),
                }
            ),
            description="The Generation TruthfulQA (main) task tests a model's ability to generate 1-2 sentence answers for a given question truthfully.",
        ),
        TruthfulQaConfig(
            name="multiple_choice",
            url="https://raw.githubusercontent.com/sylinrl/TruthfulQA/013686a06be7a7bde5bf8223943e106c7250123c/data/mc_task.json",
            features=datasets.Features(
                {
                    "question": datasets.Value("string"),
                    "mc1_targets": {
                        "choices": datasets.features.Sequence(datasets.Value("string")),
                        "labels": datasets.features.Sequence(datasets.Value("int32")),
                    },
                    "mc2_targets": {
                        "choices": datasets.features.Sequence(datasets.Value("string")),
                        "labels": datasets.features.Sequence(datasets.Value("int32")),
                    },
                }
            ),
            description="The Multiple-Choice TruthfulQA task provides a multiple-choice option to test a model's ability to identify true statements.",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=self.config.features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(self.config.url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_dir,
                },
            ),
        ]

    def _split_csv_list(self, csv_list: str, delimiter: str = ";") -> str:
        """
        Splits a csv list field, delimited by `delimiter` (';'), into a list
        of strings.
        """
        csv_list = csv_list.strip().split(delimiter)
        return [item.strip() for item in csv_list]

    def _generate_examples(self, filepath):
        if self.config.name == "multiple_choice":
            # Multiple choice data is in a `JSON` file.
            with open(filepath, encoding="utf-8") as f:
                contents = json.load(f)
                for key, row in enumerate(contents):
                    yield key, {
                        "question": row["question"],
                        "mc1_targets": {
                            "choices": list(row["mc1_targets"].keys()),
                            "labels": list(row["mc1_targets"].values()),
                        },
                        "mc2_targets": {
                            "choices": list(row["mc2_targets"].keys()),
                            "labels": list(row["mc2_targets"].values()),
                        },
                    }
        else:
            # Generation data is in a `CSV` file.
            with open(filepath, newline="", encoding="utf-8-sig") as f:
                contents = csv.DictReader(f)
                for key, row in enumerate(contents):
                    # Ensure that references exist.
                    if not row["Correct Answers"] or not row["Incorrect Answers"]:
                        continue
                    yield key, {
                        "type": row["Type"],
                        "category": row["Category"],
                        "question": row["Question"],
                        "best_answer": row["Best Answer"],
                        "correct_answers": self._split_csv_list(row["Correct Answers"]),
                        "incorrect_answers": self._split_csv_list(row["Incorrect Answers"]),
                        "source": row["Source"],
                    }
