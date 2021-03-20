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


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset:stsb_multi_mt,
title = {Machine translated multilingual STS benchmark dataset.},
author={Philip May},
year={2021}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to solve this great NLP task and is crafted with a lot of care.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/PhilipMay/stsb-multi-mt"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_BASE_URL = "https://raw.githubusercontent.com/PhilipMay/stsb-multi-mt/main/data"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class StsbMultiMt(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.0.0")

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
        datasets.BuilderConfig(name="en", version=VERSION, description="This is the original English STS benchmark data set."),
        datasets.BuilderConfig(name="de", version=VERSION, description="This is the German STS benchmark data set."),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
                "similarity_score": datasets.Value("float")
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
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls_to_download = {
            "train": "{}/stsb-{}-train.csv".format(_BASE_URL, self.config.name),
            "dev": "{}/stsb-{}-dev.csv".format(_BASE_URL, self.config.name),
            "test": "{}/stsb-{}-test.csv".format(_BASE_URL, self.config.name),
        }
        downloaded_files = dl_manager.download(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": downloaded_files["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": downloaded_files["test"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.NamedSplit("dev"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": downloaded_files["dev"],
                },
            ),
        ]

    def _generate_examples(
        self, filepath  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """ Yields examples as (key, example) tuples. """
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.
        with open(filepath, newline='', encoding="utf-8") as csvfile:
            csv_dict_reader = csv.DictReader(
                csvfile,
                fieldnames=["sentence1", "sentence2", "similarity_score"],
            )
            for id_, row in enumerate(csv_dict_reader):
                # do asserts
                assert "sentence1" in row
                assert isinstance(row['sentence1'], str)
                assert len(row['sentence1'].strip()) > 0
                assert "sentence2" in row
                assert isinstance(row['sentence2'], str)
                assert len(row['sentence2'].strip()) > 0
                assert "similarity_score" in row
                assert isinstance(row['similarity_score'], str)
                assert len(row['similarity_score'].strip()) > 0

                # convert similarity_score from str to float
                row['similarity_score'] = float(row['similarity_score'])

                # do more asserts
                assert row['similarity_score'] >= 0.0
                assert row['similarity_score'] <= 5.0

                yield id_, row
