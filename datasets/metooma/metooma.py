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

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


_CITATION = """\
@inproceedings{gautam2020metooma,
    title={\# MeTooMA: Multi-Aspect Annotations of Tweets Related to the MeToo Movement},
    author={Gautam, Akash and Mathur, Puneet and Gosangi, Rakesh and Mahata, Debanjan and Sawhney, Ramit and Shah, Rajiv Ratn},
    booktitle={Proceedings of the International AAAI Conference on Web and Social Media},
    volume={14},
    pages={209--216},
    year={2020} }
"""

_DESCRIPTION = """\
The dataset consists of tweets belonging to #MeToo movement on Twitter, labelled into different categories.
Due to Twitter's development policies, we only provide the tweet ID's and corresponding labels, other data can be fetched via Twitter API.
The data has been labelled by experts, with the majority taken into the account for deciding the final label.
We provide these labels for each of the tweets. The labels provided for each data point includes -- Relevance, Directed Hate, Generalized Hate,
Sarcasm, Allegation, Justification, Refutation, Support, Oppose
"""


_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/akash418/public-data-repo/main/MeTooMMD_train.csv"
_TEST_DOWNLOAD_URL = "https://raw.githubusercontent.com/akash418/public-data-repo/main/MeTooMMD_test.csv"


class MeTooMA(datasets.GeneratorBasedBuilder):
    """MeTooMA dataset -- Dataset providing labeled information for tweets belonging to the MeToo movement"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        # This method pecifies the datasets.DatasetInfo object which contains informations and typings for the dataset

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "TweetId": datasets.Value("string"),
                    "Text_Only_Informative": datasets.Value("string"),
                    "Image_Only_Informative": datasets.Value("string"),
                    "Directed_Hate": datasets.Value("string"),
                    "Generalized_Hate": datasets.Value("string"),
                    "Sarcasm": datasets.Value("string"),
                    "Allegation": datasets.Value("string"),
                    "Justification": datasets.Value("string"),
                    "Refutation": datasets.Value("string"),
                    "Support": datasets.Value("string"),
                    "Oppose": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/JN4EYU",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file,
                quotechar='"',
                delimiter=",",
                quoting=csv.QUOTE_ALL,
                skipinitialspace=True,
            )
            for id_, row in enumerate(csv_reader):
                # print(row)
                (
                    tweet_id,
                    text_informative_label,
                    image_informative_label,
                    dir_hate_label,
                    gen_hate_label,
                    sarcasm_label,
                    allegtation_label,
                    justification_label,
                    refutation_label,
                    support_label,
                    oppose_label,
                ) = row
                # applicable_labels = []

                yield id_, {
                    "TweetId": tweet_id,
                    "Text_Only_Informative": text_informative_label,
                    "Image_Only_Informative": image_informative_label,
                    "Directed_Hate": dir_hate_label,
                    "Generalized_Hate": gen_hate_label,
                    "Sarcasm": sarcasm_label,
                    "Allegation": allegtation_label,
                    "Justification": justification_label,
                    "Refutation": refutation_label,
                    "Support": support_label,
                    "Oppose": oppose_label,
                }
