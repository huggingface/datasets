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
"""PAWS, a dataset for paraphrase identification"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@InProceedings{paws2019naacl,
  title = {{PAWS: Paraphrase Adversaries from Word Scrambling}},
  author = {Zhang, Yuan and Baldridge, Jason and He, Luheng},
  booktitle = {Proc. of NAACL},
  year = {2019}
}
"""

_DESCRIPTION = """\
PAWS: Paraphrase Adversaries from Word Scrambling

This dataset contains 108,463 human-labeled and 656k noisily labeled pairs that feature
the importance of modeling structure, context, and word order information for the problem
of paraphrase identification. The dataset has two subsets, one based on Wikipedia and the
other one based on the Quora Question Pairs (QQP) dataset.

For further details, see the accompanying paper: PAWS: Paraphrase Adversaries from Word Scrambling
(https://arxiv.org/abs/1904.01130)

PAWS-QQP is not available due to license of QQP. It must be reconstructed by downloading the original
data and then running our scripts to produce the data and attach the labels.

NOTE: There might be some missing or wrong labels in the dataset and we have replaced them with -1.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/paws"

_LICENSE = 'The dataset may be freely used for any purpose, although acknowledgement of Google LLC ("Google") as the data source would be appreciated. The dataset is provided "AS IS" without any warranty, express or implied. Google disclaims all liability for any damages, direct or indirect, resulting from the use of the dataset.'

_DATA_OPTIONS = [
    "labeled_final",
    "labeled_swap",
    "unlabeled_final",
]


class PAWSConfig(datasets.BuilderConfig):
    """BuilderConfig for PAWS."""

    def __init__(self, **kwargs):
        """Constructs a PAWSConfig.
        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(PAWSConfig, self).__init__(version=datasets.Version("1.1.0", ""), **kwargs),


class PAWS(datasets.GeneratorBasedBuilder):
    """PAWS, a dataset for paraphrase identification"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        PAWSConfig(
            name=config_name,
            description=(f"This config contains samples of {config_name}."),
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

        _DATA_URL = f"https://storage.googleapis.com/paws/english/paws_wiki_{self.config.name}.tar.gz"
        data_dir = dl_manager.download_and_extract(_DATA_URL)

        if self.config.name == "labeled_final":
            _TRAIN_FILE_NAME = os.path.join(data_dir, "final", "train.tsv")
            _VAL_FILE_NAME = os.path.join(data_dir, "final", "dev.tsv")
            _TEST_FILE_NAME = os.path.join(data_dir, "final", "test.tsv")
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

        elif self.config.name == "labeled_swap":
            _TRAIN_FILE_NAME = os.path.join(data_dir, "swap", "train.tsv")
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": _TRAIN_FILE_NAME,
                        "split": datasets.Split.TRAIN,
                    },
                ),
            ]

        elif self.config.name == "unlabeled_final":
            _TRAIN_FILE_NAME = os.path.join(data_dir, "unlabeled", "final", "train.tsv")
            _VAL_FILE_NAME = os.path.join(data_dir, "unlabeled", "final", "dev.tsv")
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
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": _VAL_FILE_NAME,
                        "split": datasets.Split.VALIDATION,
                    },
                ),
            ]
        else:
            raise NotImplementedError("{} does not exist".format(self.config.name))

    def _generate_examples(self, filepath, split):
        """ Yields examples. """

        with open(filepath, encoding="utf-8") as f:
            data = csv.DictReader(f, delimiter="\t")
            for id_, row in enumerate(data):
                if self.config.name != "unlabeled_final":
                    if row["label"] not in ["0", "1"]:
                        row["label"] = -1
                    yield id_, {
                        "id": row["id"],
                        "sentence1": row["sentence1"],
                        "sentence2": row["sentence2"],
                        "label": row["label"],
                    }
                else:
                    if row["noisy_label"] not in ["0", "1"]:
                        row["noisy_label"] = -1
                    yield id_, {
                        "id": row["id"],
                        "sentence1": row["sentence1"],
                        "sentence2": row["sentence2"],
                        "label": row["noisy_label"],
                    }
