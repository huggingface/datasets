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
"""Hope Speech dataset for Equality, Diversity and Inclusion (HopeEDI)"""


import csv

import datasets


_HOMEPAGE = "https://competitions.codalab.org/competitions/27653#learn_the_details"


_CITATION = """\
@inproceedings{chakravarthi-2020-hopeedi,
title = "{H}ope{EDI}: A Multilingual Hope Speech Detection Dataset for Equality, Diversity, and Inclusion",
author = "Chakravarthi, Bharathi Raja",
booktitle = "Proceedings of the Third Workshop on Computational Modeling of People's Opinions, Personality, and Emotion's in Social Media",
month = dec,
year = "2020",
address = "Barcelona, Spain (Online)",
publisher = "Association for Computational Linguistics",
url = "https://www.aclweb.org/anthology/2020.peoples-1.5",
pages = "41--53",
abstract = "Over the past few years, systems have been developed to control online content and eliminate abusive, offensive or hate speech content. However, people in power sometimes misuse this form of censorship to obstruct the democratic right of freedom of speech. Therefore, it is imperative that research should take a positive reinforcement approach towards online content that is encouraging, positive and supportive contents. Until now, most studies have focused on solving this problem of negativity in the English language, though the problem is much more than just harmful content. Furthermore, it is multilingual as well. Thus, we have constructed a Hope Speech dataset for Equality, Diversity and Inclusion (HopeEDI) containing user-generated comments from the social media platform YouTube with 28,451, 20,198 and 10,705 comments in English, Tamil and Malayalam, respectively, manually labelled as containing hope speech or not. To our knowledge, this is the first research of its kind to annotate hope speech for equality, diversity and inclusion in a multilingual setting. We determined that the inter-annotator agreement of our dataset using Krippendorff{'}s alpha. Further, we created several baselines to benchmark the resulting dataset and the results have been expressed using precision, recall and F1-score. The dataset is publicly available for the research community. We hope that this resource will spur further research on encouraging inclusive and responsive speech that reinforces positiveness.",
}
"""

_DESCRIPTION = """\
A Hope Speech dataset for Equality, Diversity and Inclusion (HopeEDI) containing user-generated comments from the social media platform YouTube with 28,451, 20,198 and 10,705 comments in English, Tamil and Malayalam, respectively, manually labelled as containing hope speech or not.
"""

_LICENSE = "Creative Commons Attribution 4.0 International Licence"

_URLs = {
    "english": {
        "TRAIN_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1ydsOTvBZXKqcRvXawOuePrJ99slOEbkk&export=download",
        "VALIDATION_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1pvpPA97kybx5IyotR9HNuqP4T5ktEtr4&export=download",
    },
    "tamil": {
        "TRAIN_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1R1jR4DcH2UEaM1ZwDSRHdfTGvkCNu6NW&export=download",
        "VALIDATION_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1cTaA6OCZUaepl5D-utPw2ZmbonPcw52v&export=download",
    },
    "malayalam": {
        "TRAIN_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1wxwqnWGRzwvc_-ugRoFX8BPgpO3Q7sch&export=download",
        "VALIDATION_DOWNLOAD_URL": "https://drive.google.com/u/0/uc?id=1uZ0U9VJQEUPQItPpTJKXH8u_6jXppvJ1&export=download",
    },
}


class HopeEdi(datasets.GeneratorBasedBuilder):
    """HopeEDI dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="english", version=VERSION, description="This part of my dataset covers English dataset"
        ),
        datasets.BuilderConfig(
            name="tamil", version=VERSION, description="This part of my dataset covers Tamil dataset"
        ),
        datasets.BuilderConfig(
            name="malayalam", version=VERSION, description="This part of my dataset covers Tamil dataset"
        ),
    ]

    def _info(self):

        if self.config.name == "english":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["Hope_speech", "Non_hope_speech", "not-English"]),
                }
            )
        elif self.config.name == "tamil":
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["Hope_speech", "Non_hope_speech", "not-Tamil"]),
                }
            )

        # else self.config.name == "malayalam":
        else:
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["Hope_speech", "Non_hope_speech", "not-malayalam"]),
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
        """Generate HopeEDI examples."""

        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_NONE, skipinitialspace=False
            )

            for id_, row in enumerate(csv_reader):
                text, label, dummy = row
                yield id_, {"text": text, "label": label}
