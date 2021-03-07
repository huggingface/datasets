# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""MOROCO: The Moldavian and Romanian Dialectal Corpus"""

from __future__ import absolute_import, division, print_function

import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{ Butnaru-ACL-2019,
    author = {Andrei M. Butnaru and Radu Tudor Ionescu},
    title = "{MOROCO: The Moldavian and Romanian Dialectal Corpus}",
    booktitle = {Proceedings of ACL},
    year = {2019},
    pages={688--698},
}
"""

# You can copy an official description
_DESCRIPTION = """\
        The MOROCO (Moldavian and Romanian Dialectal Corpus) dataset contains 33564 samples of text collected from the news domain.
        The samples belong to one of the following six topics:
            - culture
            - finance
            - politics
            - science
            - sports
            - tech
"""

_HOMEPAGE = "https://github.com/butnaruandrei/MOROCO"

_LICENSE = "CC BY-SA 4.0 License"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://raw.githubusercontent.com/butnaruandrei/MOROCO/master/MOROCO/preprocessed/"
_URL_TRAIN = os.path.join(_URL, "train")
_URL_VAL = os.path.join(_URL, "validation")
_URL_TEST = os.path.join(_URL, "test")

_SAMPLES_FILE = "samples.txt"
_LABELS_FILE = "category_labels.txt"


class MOROCOConfig(datasets.BuilderConfig):
    """BuilderConfig for the MOROCO dataset"""

    def __init__(self, **kwargs):
        super(MOROCOConfig, self).__init__(**kwargs)


class MOROCO(datasets.GeneratorBasedBuilder):
    """MOROCO dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        MOROCOConfig(name="moroco", version=VERSION, description="MOROCO dataset"),
    ]

    def _info(self):

        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "category": datasets.features.ClassLabel(
                    names=[
                        "culture",
                        "finance",
                        "politics",
                        "science",
                        "sports",
                        "tech",
                    ]
                ),
                "sample": datasets.Value("string"),
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

        urls_to_download = {
            "train_samples": os.path.join(_URL_TRAIN, _SAMPLES_FILE),
            "train_labels": os.path.join(_URL_TRAIN, _LABELS_FILE),
            "val_samples": os.path.join(_URL_VAL, _SAMPLES_FILE),
            "val_labels": os.path.join(_URL_VAL, _LABELS_FILE),
            "test_samples": os.path.join(_URL_TEST, _SAMPLES_FILE),
            "test_labels": os.path.join(_URL_TEST, _LABELS_FILE),
        }

        downloaded_files = dl_manager.download(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "samples_filepath": downloaded_files["train_samples"],
                    "labels_filepath": downloaded_files["train_labels"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "samples_filepath": downloaded_files["test_samples"],
                    "labels_filepath": downloaded_files["test_labels"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "samples_filepath": downloaded_files["val_samples"],
                    "labels_filepath": downloaded_files["val_labels"],
                },
            ),
        ]

    def _generate_examples(self, samples_filepath, labels_filepath):
        """This function returns the examples in the raw (text) form."""

        with open(samples_filepath, "r") as fsamples:
            sample_rows = fsamples.read().splitlines()

        with open(labels_filepath, "r") as flabels:
            label_rows = flabels.readlines()

        for i, row in enumerate(sample_rows):
            samp_id = row.split("\t")[0]
            sample = "".join(row.split("\t")[1:])
            label = int(label_rows[i].split("\t")[1])

            yield i, {
                "id": samp_id,
                "category": label - 1,
                "sample": sample,
            }
