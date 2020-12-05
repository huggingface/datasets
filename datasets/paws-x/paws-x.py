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
"""PAWS-X, a multilingual version of PAWS for six languages."""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@InProceedings{pawsx2019emnlp,
  title = {{PAWS-X: A Cross-lingual Adversarial Dataset for Paraphrase Identification}},
  author = {Yang, Yinfei and Zhang, Yuan and Tar, Chris and Baldridge, Jason},
  booktitle = {Proc. of EMNLP},
  year = {2019}
}
"""

_DESCRIPTION = """\
PAWS: Paraphrase Adversaries from Word Scrambling

This dataset contains 23,659 human translated PAWS evaluation pairs and 296,406 machine
translated training pairs in six typologically distinct languages: French, Spanish, German,
Chinese, Japanese, and Korean. English language is available by default. All translated
pairs are sourced from examples in PAWS-Wiki.

For further details, see the accompanying paper: PAWS-X: A Cross-lingual Adversarial Dataset
for Paraphrase Identification (https://arxiv.org/abs/1908.11828)

NOTE: There might be some missing or wrong labels in the dataset and we have replaced them with -1.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/paws/tree/master/pawsx"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = 'The dataset may be freely used for any purpose, although acknowledgement of Google LLC ("Google") as the data source would be appreciated. The dataset is provided "AS IS" without any warranty, express or implied. Google disclaims all liability for any damages, direct or indirect, resulting from the use of the dataset.'

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_DATA_OPTIONS = [
    "en",
    "de",
    "es",
    "fr",
    "ja",
    "ko",
    "zh",
]

_DATA_URL = "https://storage.googleapis.com/paws/pawsx/x-final.tar.gz"


class PAWSXConfig(datasets.BuilderConfig):
    """BuilderConfig for PAWSX."""

    def __init__(self, **kwargs):
        """Constructs a PAWSXConfig.
        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(PAWSXConfig, self).__init__(version=datasets.Version("1.1.0", ""), **kwargs),


class PAWSX(datasets.GeneratorBasedBuilder):
    """PAWS-X, a multilingual version of PAWS for six languages."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        PAWSXConfig(
            name=config_name,
            description=(f"This config contains samples in {config_name}."),
        )
        for config_name in _DATA_OPTIONS
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("int32"),
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["0", "1"]),
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

        data_dir = dl_manager.download_and_extract(_DATA_URL)

        _TEST_FILE_NAME = os.path.join(data_dir, f"x-final/{self.config.name}/test_2k.tsv")
        _VAL_FILE_NAME = os.path.join(data_dir, f"x-final/{self.config.name}/dev_2k.tsv")

        if self.config.name == "en":
            _TRAIN_FILE_NAME = os.path.join(data_dir, f"x-final/{self.config.name}/train.tsv")
        else:
            _TRAIN_FILE_NAME = os.path.join(data_dir, f"x-final/{self.config.name}/translated_train.tsv")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": _TRAIN_FILE_NAME,
                    "split": datasets.Split.TRAIN,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": _TEST_FILE_NAME,
                    "split": datasets.Split.TEST,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": _VAL_FILE_NAME,
                    "split": datasets.Split.VALIDATION,
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """

        with open(filepath, encoding="utf-8") as f:
            data = csv.DictReader(f, delimiter="\t")
            for id_, row in enumerate(data):
                if row["label"] not in ["0", "1"]:
                    row["label"] = -1
                yield id_, {
                    "id": row["id"],
                    "sentence1": row["sentence1"],
                    "sentence2": row["sentence2"],
                    "label": row["label"],
                }
