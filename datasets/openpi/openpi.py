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
""" OpenPI Dataset for tracking entities in open domain procedural text. """

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


_CITATION = """\
@inproceedings{tandon-etal-2020-dataset,
    title = "A Dataset for Tracking Entities in Open Domain Procedural Text",
    author = "Tandon, Niket  and
      Sakaguchi, Keisuke  and
      Dalvi, Bhavana  and
      Rajagopal, Dheeraj  and
      Clark, Peter  and
      Guerquin, Michal  and
      Richardson, Kyle  and
      Hovy, Eduard",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.520",
    doi = "10.18653/v1/2020.emnlp-main.520",
    pages = "6408--6417",
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
OpenPI dataset for tracking entities in open domain procedural text.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://allenai.org/data/openpi"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "MIT License"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_BASE_URL = "https://raw.githubusercontent.com/allenai/openpi-dataset/main/data/gold/"

class OpenpiConfig(datasets.BuilderConfig):
    """"BuilderConfig for OpenPI Dataset"""
    def __init__(self, mode, type_, **kwargs):    
        super(OpenpiConfig, self).__init__(**kwargs)
        self.mode = mode
        self.type_ = type_


class Openpi(datasets.GeneratorBasedBuilder):
    """A Dataset for Tracking Entities in Open Domain Procedural Text"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIG_CLASS = OpenpiConfig

    BUILDER_CONFIGS = [
        OpenpiConfig(name="questions", mode="question", type_="data", version=VERSION, description="Provides the question sentences"),
        OpenpiConfig(name="questions-metadata", mode="question", type_="metadata", version=VERSION, description="Provides the question metadata"),
        OpenpiConfig(name="answers", mode="answers", type_="data", version=VERSION, description="Provides the answer sentences"),
        OpenpiConfig(name="answers-metadata", mode="answers", type_="metadata", version=VERSION, description="Provides the answer metadata")
    ]

    DEFAULT_CONFIG_NAME = "answers"

    def _info(self):
        if self.config.mode == "question":
            if self.config.type_ == "metadata":
                features = datasets.Features(
                    {
                        "id": datasets.Value("string"),
                        "question_metadata": {
                            "url": datasets.Value("string"),
                            "step_id": datasets.ClassLabel(names=["0", "1", "2", "3", "4", "5", "6", "7"]),
                            "context": datasets.Value("string"),
                            "query": datasets.Value("string"),
                            "future_context": datasets.Value("string"),
                            "topic": datasets.ClassLabel(names=["Food and Entertaining", "Home and Garden", "Hobbies and Crafts", "Sports and Fitness", "Cars & Other Vehicles", "Health", "unknown"])
                        }
                    }
                )
            else:
                features = datasets.Features(
                    {
                        "id": datasets.Value("string"),
                        "question": datasets.Value("string")
                    }
                )
        else:
            if self.config.type_ == "metadata":
                features = datasets.Features(
                    {
                        "id": datasets.Value("string"),
                        "answers_metadata": datasets.features.Sequence(
                            {
                                "answer": datasets.Value("string"),
                                "entity": datasets.Value("string"),
                                "before": datasets.Value("string"),
                                "after": datasets.Value("string"),
                                "attr": datasets.Value("string"),
                                "modality": datasets.ClassLabel(names=["without_image", "with_image"])

                            }
                        )
                    }
                )
            else:
                features = datasets.Features(
                    {
                        "id": datasets.Value("string"),
                        "answers": datasets.Sequence(datasets.Value("string"))
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
        suffix = "_metadata" if self.config.type_ == "metadata" else ""
        fname = "id_{config}{suffix}.jsonl"
        urls = {
            "train": os.path.join(_BASE_URL, "train", fname.format(config=self.config.mode, suffix=suffix)),
            "dev": os.path.join(_BASE_URL, "dev", fname.format(config=self.config.mode, suffix=suffix)),
            "test": os.path.join(_BASE_URL, "test", fname.format(config=self.config.mode, suffix=suffix))
        }
        print(urls)
        data_dir = dl_manager.download_and_extract(urls)
        print(data_dir)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["test"],
                    "split": "test"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["dev"],
                    "split": "dev"
                },
            )
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if "question" in data:
                    result = {
                        "id": data["id"],
                        "question": data["question"]
                    }
                elif "question_metadata" in data:
                    result = {
                        "id": data["id"],
                        "question_metadata": {
                            "url": data["question_metadata"].get("url", ""),
                            "step_id": data["question_metadata"].get("step_id", "0"),
                            "context": data["question_metadata"].get("context", ""),
                            "query": data["question_metadata"].get("query", ""),
                            "future_context": data["question_metadata"].get("future_context", ""),
                            "topic": data["question_metadata"].get("topic", "unknown")
                        }
                    }
                elif "answers_metadata" in data:
                    result = {
                        "id": data["id"],
                        "answers_metadata": []
                    }
                    for item in data["answers_metadata"]:
                        result["answers_metadata"].append(
                            {
                                "answer": item.get("answer", ""),
                                "entity": item.get("entity", ""),
                                "before": item.get("before", ""),
                                "after": item.get("after", ""),
                                "attr": item.get("attr", ""),
                                "modality": item.get("modality")
                            }
                        )
                else:
                    result = {
                        "id": data["id"],
                        "answers":data["answers"]
                    }
                yield id_, result