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


import csv
import os

import datasets


_CITATION = """\
@article{hendryckstest2021,
      title={Measuring Massive Multitask Language Understanding},
      author={Dan Hendrycks and Collin Burns and Steven Basart and Andy Zou and Mantas Mazeika and Dawn Song and Jacob Steinhardt},
      journal={Proceedings of the International Conference on Learning Representations (ICLR)},
      year={2021}
    }
"""

_DESCRIPTION = """\
This is a massive multitask test consisting of multiple-choice questions from various branches of knowledge, covering 57 tasks including elementary mathematics, US history, computer science, law, and more.
"""

_HOMEPAGE = "https://github.com/hendrycks/test"

_URL = "https://people.eecs.berkeley.edu/~hendrycks/data.tar"

_SUBJECTS = [
    "abstract_algebra",
    "anatomy",
    "astronomy",
    "business_ethics",
    "clinical_knowledge",
    "college_biology",
    "college_chemistry",
    "college_computer_science",
    "college_mathematics",
    "college_medicine",
    "college_physics",
    "computer_security",
    "conceptual_physics",
    "econometrics",
    "electrical_engineering",
    "elementary_mathematics",
    "formal_logic",
    "global_facts",
    "high_school_biology",
    "high_school_chemistry",
    "high_school_computer_science",
    "high_school_european_history",
    "high_school_geography",
    "high_school_government_and_politics",
    "high_school_macroeconomics",
    "high_school_mathematics",
    "high_school_microeconomics",
    "high_school_physics",
    "high_school_psychology",
    "high_school_statistics",
    "high_school_us_history",
    "high_school_world_history",
    "human_aging",
    "human_sexuality",
    "international_law",
    "jurisprudence",
    "logical_fallacies",
    "machine_learning",
    "management",
    "marketing",
    "medical_genetics",
    "miscellaneous",
    "moral_disputes",
    "moral_scenarios",
    "nutrition",
    "philosophy",
    "prehistory",
    "professional_accounting",
    "professional_law",
    "professional_medicine",
    "professional_psychology",
    "public_relations",
    "security_studies",
    "sociology",
    "us_foreign_policy",
    "virology",
    "world_religions",
]


class HendrycksTest(datasets.GeneratorBasedBuilder):
    """Massive multitask MC test cosisting of 57 tasks"""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=sub, version=datasets.Version("1.0.0"), description=f"Hendrycks Test Subject {sub}"
        )
        for sub in _SUBJECTS
    ]

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "question": datasets.Value("string"),
                "choices": datasets.features.Sequence(datasets.Value("string")),
                "answer": datasets.features.ClassLabel(num_classes=4, names=["A", "B", "C", "D"]),
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split("auxiliary_train"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "datadir": os.path.join(data_dir, "data", "auxiliary_train"),
                    "split": "auxiliary_train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"datadir": os.path.join(data_dir, "data", "test"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "datadir": os.path.join(data_dir, "data", "val"),
                    "split": "val",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("dev"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "datadir": os.path.join(data_dir, "data", "dev"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, datadir, split):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        id_ = 0
        if split == "auxiliary_train":
            for f in sorted(os.listdir(datadir)):
                reader = csv.reader(
                    open(os.path.join(datadir, f), "r", encoding="utf-8"), quotechar='"', delimiter=","
                )
                for data in reader:
                    yield id_, {"question": data[0], "choices": data[1:5], "answer": data[5]}
                    id_ += 1
        else:
            reader = csv.reader(
                open(os.path.join(datadir, f"{self.config.name}_{split}.csv"), "r", encoding="utf-8"),
                quotechar='"',
                delimiter=",",
            )
            for data in reader:
                yield id_, {"question": data[0], "choices": data[1:5], "answer": data[5]}
                id_ += 1
