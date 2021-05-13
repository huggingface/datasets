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
"""Offensive language identification in dravidian lanaguages dataset"""


import csv

import datasets


_HOMEPAGE = "https://competitions.codalab.org/competitions/27654#learn_the_details"


_CITATION = """\
@inproceedings{dravidianoffensive-eacl,
title={Findings of the Shared Task on {O}ffensive {L}anguage {I}dentification in {T}amil, {M}alayalam, and {K}annada},
author={Chakravarthi, Bharathi Raja and
Priyadharshini, Ruba and
Jose, Navya and
M, Anand Kumar and
Mandl, Thomas and
Kumaresan, Prasanna Kumar and
Ponnsamy, Rahul and
V,Hariharan and
Sherly, Elizabeth and
McCrae, John Philip },
booktitle = "Proceedings of the First Workshop on Speech and Language Technologies for Dravidian Languages",
month = April,
year = "2021",
publisher = "Association for Computational Linguistics",
year={2021}
}
"""

_DESCRIPTION = """\
Offensive language identification in dravidian lanaguages dataset. The goal of this task is to identify offensive language content of the code-mixed dataset of comments/posts in Dravidian Languages ( (Tamil-English, Malayalam-English, and Kannada-English)) collected from social media.
"""

_LICENSE = "Creative Commons Attribution 4.0 International Licence"

_URLs = {
    "tamil": {
        "TRAIN_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=15auwrFAlq52JJ61u7eSfnhT9rZtI5sjk&export=download",
        "VALIDATION_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1Jme-Oftjm7OgfMNLKQs1mO_cnsQmznRI&export=download",
    },
    "malayalam": {
        "TRAIN_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=13JCCr-IjZK7uhbLXeufptr_AxvsKinVl&export=download",
        "VALIDATION_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1J0msLpLoM6gmXkjC6DFeQ8CG_rrLvjnM&export=download",
    },
    "kannada": {
        "TRAIN_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1BFYF05rx-DK9Eb5hgoIgd6EcB8zOI-zu&export=download",
        "VALIDATION_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1V077dMQvscqpUmcWTcFHqRa_vTy-bQ4H&export=download",
    },
}


class OffensevalDravidian(datasets.GeneratorBasedBuilder):
    """Offensive language identification in dravidian lanaguages dataset"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="tamil", version=VERSION, description="This part of my dataset covers Tamil dataset"
        ),
        datasets.BuilderConfig(
            name="malayalam", version=VERSION, description="This part of my dataset covers Malayalam dataset"
        ),
        datasets.BuilderConfig(
            name="kannada", version=VERSION, description="This part of my dataset covers Kannada dataset"
        ),
    ]

    def _info(self):

        if self.config.name == "tamil":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "Not_offensive",
                            "Offensive_Untargetede",
                            "Offensive_Targeted_Insult_Individual",
                            "Offensive_Targeted_Insult_Group",
                            "Offensive_Targeted_Insult_Other",
                            "not-Tamil",
                        ]
                    ),
                }
            )
        elif self.config.name == "malayalam":
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "Not_offensive",
                            "Offensive_Untargetede",
                            "Offensive_Targeted_Insult_Individual",
                            "Offensive_Targeted_Insult_Group",
                            "Offensive_Targeted_Insult_Other",
                            "not-malayalam",
                        ]
                    ),
                }
            )

        # else self.config.name == "kannada":
        else:
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "Not_offensive",
                            "Offensive_Untargetede",
                            "Offensive_Targeted_Insult_Individual",
                            "Offensive_Targeted_Insult_Group",
                            "Offensive_Targeted_Insult_Other",
                            "not-Kannada",
                        ]
                    ),
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

        train_path = dl_manager.download_and_extract(my_urls["TRAIN_DOWNLOAD_URL"])
        validation_path = dl_manager.download_and_extract(my_urls["VALIDATION_DOWNLOAD_URL"])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": train_path,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": validation_path,
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Generate Offenseval_dravidian examples."""

        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_ALL, skipinitialspace=False
            )

            for id_, row in enumerate(csv_reader):

                if self.config.name == "kannada":
                    text, label = row
                else:
                    text, label, dummy = row

                yield id_, {"text": text, "label": label}
