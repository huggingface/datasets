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
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
authors={huggingface, Inc.
},
year={2020}
}
"""

# TODO: Add description of the dataset here
_DESCRIPTION = """\
This new dataset is designed to solve this great NLP task and is crafted with a lot of care. 
"""

_URL = "https://huggingface.co/great-new-dataset.zip"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
# Using a specific configuration class is optional, you can also use the base class if you don't need
# to add specific attributes.
# here we give an example for three sub-set of the dataset with difference sizes.
class NewDatasetConfig(datasets.BuilderConfig):
    """ BuilderConfig for NewDataset"""

    def __init__(self, data_size, **kwargs):
        """

        Args:
            data_size: the size of the training set we want to us (xs, s, m, l, xl)
            **kwargs: keyword arguments forwarded to super.
        """
        self.data_size = data_size


class NewDataset(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    BUILDER_CONFIG_CLASS = NewDatasetConfig
    BUILDER_CONFIGS = [
        NewDatasetConfig(name="my_dataset_" + size, description="A small dataset", data_size=size) for size in ["small", "medium", "large"]
    ]

    def _info(self):
        # TODO: Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "option1": datasets.Value("string"),
                    "option2": datasets.Value("string"),
                    "answer": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://huggingface.co/great-new-dataset",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "great-new-dataset")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train_{}.jsonl".format(self.config.data_size)),
                    #'labelpath': os.path.join(data_dir, 'train_{}-labels.lst'.format(self.config.data_size)),
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
                    #'labelpath': os.path.join(data_dir, 'dev-labels.lst'),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if split == "test":
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "option2": data["option2"],
                        "answer": "",
                    }
                else:
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "option2": data["option2"],
                        "answer": data["answer"],
                    }
