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
"""The ECtHR Cases dataset is designed for experimentation of neural judgment prediction and rationale extraction considering ECtHR cases."""


import json
import os

import datasets


_CITATION = """\
@InProceedings{chalkidis-et-al-2021-ecthr,
    title = "Paragraph-level Rationale Extraction through Regularization: A case study on European Court of Human Rights Cases",
    author = "Chalkidis, Ilias and Fergadiotis, Manos and Tsarapatsanis, Dimitrios and Aletras, Nikolaos and Androutsopoulos, Ion and Malakasiotis, Prodromos",
    booktitle = "Proceedings of the Annual Conference of the North American Chapter of the Association for Computational Linguistics",
    year = "2021",
    address = "Mexico City, Mexico",
    publisher = "Association for Computational Linguistics"
}
"""

_DESCRIPTION = """\
The ECtHR Cases dataset is designed for experimentation of neural judgment prediction and rationale extraction considering ECtHR cases.
"""

_HOMEPAGE = "http://archive.org/details/ECtHR-NAACL2021/"

_LICENSE = "CC BY-NC-SA (Creative Commons / Attribution-NonCommercial-ShareAlike)"

_URLs = {
    "alleged-violation-prediction": "http://archive.org/download/ECtHR-NAACL2021/dataset.zip",
    "violation-prediction": "http://archive.org/download/ECtHR-NAACL2021/dataset.zip",
}

ARTICLES = {
    "2": "Right to life",
    "3": "Prohibition of torture",
    "4": "Prohibition of slavery and forced labour",
    "5": "Right to liberty and security",
    "6": "Right to a fair trial",
    "7": "No punishment without law",
    "8": "Right to respect for private and family life",
    "9": "Freedom of thought, conscience and religion",
    "10": "Freedom of expression",
    "11": "Freedom of assembly and association",
    "12": "Right to marry",
    "13": "Right to an effective remedy",
    "14": "Prohibition of discrimination",
    "15": "Derogation in time of emergency",
    "16": "Restrictions on political activity of aliens",
    "17": "Prohibition of abuse of rights",
    "18": "Limitation on use of restrictions on rights",
    "34": "Individual applications",
    "38": "Examination of the case",
    "39": "Friendly settlements",
    "46": "Binding force and execution of judgments",
    "P1-1": "Protection of property",
    "P1-2": "Right to education",
    "P1-3": "Right to free elections",
    "P3-1": "Right to free elections",
    "P4-1": "Prohibition of imprisonment for debt",
    "P4-2": "Freedom of movement",
    "P4-3": "Prohibition of expulsion of nationals",
    "P4-4": "Prohibition of collective expulsion of aliens",
    "P6-1": "Abolition of the death penalty",
    "P6-2": "Death penalty in time of war",
    "P6-3": "Prohibition of derogations",
    "P7-1": "Procedural safeguards relating to expulsion of aliens",
    "P7-2": "Right of appeal in criminal matters",
    "P7-3": "Compensation for wrongful conviction",
    "P7-4": "Right not to be tried or punished twice",
    "P7-5": "Equality between spouses",
    "P12-1": "General prohibition of discrimination",
    "P13-1": "Abolition of the death penalty",
    "P13-2": "Prohibition of derogations",
    "P13-3": "Prohibition of reservations",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class EcthrCases(datasets.GeneratorBasedBuilder):
    """The ECtHR Cases dataset is designed for experimentation of neural judgment prediction and rationale extraction considering ECtHR cases."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="alleged-violation-prediction",
            version=VERSION,
            description="This part of the dataset covers alleged violation prediction",
        ),
        datasets.BuilderConfig(
            name="violation-prediction",
            version=VERSION,
            description="This part of the dataset covers violation prediction",
        ),
    ]

    DEFAULT_CONFIG_NAME = "alleged-violation-prediction"

    def _info(self):
        if self.config.name == "alleged-violation-prediction":
            features = datasets.Features(
                {
                    "facts": datasets.features.Sequence(datasets.Value("string")),
                    "labels": datasets.features.Sequence(datasets.Value("string")),
                    "silver_rationales": datasets.features.Sequence(datasets.Value("int32")),
                    "gold_rationales": datasets.features.Sequence(datasets.Value("int32"))
                    # These are the features of your dataset like images, labels ...
                }
            )
        else:
            features = datasets.Features(
                {
                    "facts": datasets.features.Sequence(datasets.Value("string")),
                    "labels": datasets.features.Sequence(datasets.Value("string")),
                    "silver_rationales": datasets.features.Sequence(datasets.Value("int32"))
                    # These are the features of your dataset like images, labels ...
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
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "alleged-violation-prediction":
                    yield id_, {
                        "facts": data["facts"],
                        "labels": data["allegedly_violated_articles"],
                        "silver_rationales": data["silver_rationales"],
                        "gold_rationales": data["gold_rationales"],
                    }
                else:
                    yield id_, {
                        "facts": data["facts"],
                        "labels": data["violated_articles"],
                        "silver_rationales": data["silver_rationales"],
                    }
