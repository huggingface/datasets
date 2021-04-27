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
"""This is humorous headline dataset called Humicroedit introduced in the Task-7 of SemEval 2020."""


import csv
import os

import datasets


_CITATION = """\
@article{hossain2019president,
  title={" President Vows to Cut< Taxes> Hair": Dataset and Analysis of Creative Text Editing for Humorous Headlines},
  author={Hossain, Nabil and Krumm, John and Gamon, Michael},
  journal={arXiv preprint arXiv:1906.00274},
  year={2019}
}
"""

_DESCRIPTION = """\
This new dataset is designed to assess the funniness of edited news headlines.
"""

_HOMEPAGE = "https://www.cs.rochester.edu/u/nhossain/humicroedit.html"
_LICENSE = ""

_URL = "https://cs.rochester.edu/u/nhossain/semeval-2020-task-7-dataset.zip"


class Humicroedit(datasets.GeneratorBasedBuilder):
    """This is humorous headline dataset called Humicroedit introduced in the Task-7 of SemEval 2020."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="subtask-1", description="This part of the dataset covers the data for subtask-1"),
        datasets.BuilderConfig(name="subtask-2", description="This part of the dataset covers the data for subtask-2"),
    ]

    def _info(self):
        if self.config.name == "subtask-1":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "original": datasets.Value("string"),
                    "edit": datasets.Value("string"),
                    "grades": datasets.Value("string"),
                    "meanGrade": datasets.Value("float"),
                    # These are the features of your dataset like images, labels ...
                }
            )
        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "original1": datasets.Value("string"),
                    "edit1": datasets.Value("string"),
                    "grades1": datasets.Value("string"),
                    "meanGrade1": datasets.Value("float"),
                    "original2": datasets.Value("string"),
                    "edit2": datasets.Value("string"),
                    "grades2": datasets.Value("string"),
                    "meanGrade2": datasets.Value("float"),
                    "label": datasets.ClassLabel(names=["equal", "sentence1", "sentence2"]),
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
        data_dir = dl_manager.download_and_extract(_URL)
        ROOT = "semeval-2020-task-7-dataset"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, ROOT, self.config.name, "train.csv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, ROOT, self.config.name, "test.csv"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, ROOT, self.config.name, "dev.csv"),
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("funlines"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, ROOT, self.config.name, "train_funlines.csv"),
                    "split": "funlines",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        label_names = ["equal", "sentence1", "sentence2"]

        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)

            for id_, row in enumerate(csv_reader):
                if self.config.name == "subtask-1":
                    row_id, original, edit, grades, meanGrade = row
                    yield id_, {
                        "id": row_id,
                        "original": original,
                        "edit": edit,
                        "grades": grades,
                        "meanGrade": meanGrade,
                    }
                else:
                    row_id, original1, edit1, grades1, meanGrade1, original2, edit2, grades2, meanGrade2, label = row
                    yield id_, {
                        "id": row_id,
                        "original1": original1,
                        "edit1": edit1,
                        "grades1": grades1,
                        "meanGrade1": meanGrade1,
                        "original2": original2,
                        "edit2": edit2,
                        "grades2": grades2,
                        "meanGrade2": meanGrade2,
                        "label": label_names[int(label)],
                    }
