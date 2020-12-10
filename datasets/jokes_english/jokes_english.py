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
"""English Plaintext Jokes"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@misc{pungas,
    title={A dataset of English plaintext jokes.},
    url={https://github.com/taivop/joke-dataset},
    author={Pungas, Taivo},
    year={2017},
    publisher = {GitHub},
    journal = {GitHub repository}
}
"""

_DESCRIPTION = """\
A dataset of 200k English plaintext Jokes scraped from three sources: Reddit, Stupidstuff and Wocka.
"""

_HOMEPAGE = "https://github.com/taivop/joke-dataset"

_LICENSE = ""

_URL = "https://github.com/taivop/joke-dataset/archive/master.zip"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class JokesEnglish(datasets.GeneratorBasedBuilder):
    """A dataset of 200k English plaintext Jokes scraped from three sources: Reddit, Stupidstuff and Wocka."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="reddit", version=VERSION, description="These jokes are from /r/jokes on Reddit."),
        datasets.BuilderConfig(
            name="stupidstuff", version=VERSION, description="These jokes are from stupidstuff.org"
        ),
        datasets.BuilderConfig(name="wocka", version=VERSION, description="These jokes are from wocka.com"),
    ]

    def _info(self):
        if self.config.name == "reddit":
            features = datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "body": datasets.Value("string"),
                    "id": datasets.Value("string"),
                    "score": datasets.Value("int32"),
                }
            )
        elif self.config.name == "stupidstuff":
            features = datasets.Features(
                {
                    "category": datasets.Value("string"),
                    "body": datasets.Value("string"),
                    "id": datasets.Value("int32"),
                    "rating": datasets.Value("float32"),
                }
            )
        elif self.config.name == "wocka":
            features = datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "body": datasets.Value("string"),
                    "category": datasets.Value("string"),
                    "id": datasets.Value("int32"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(data_dir, "joke-dataset-master")
        if self.config.name == "reddit":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "reddit_jokes.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "stupidstuff":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "stupidstuff.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "wocka":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "wocka.json"),
                        "split": "train",
                    },
                ),
            ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        if self.config.name == "reddit":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for _id, data in enumerate(json_data):
                    yield _id, {"title": data["title"], "body": data["body"], "id": data["id"], "score": data["score"]}
        elif self.config.name == "stupidstuff":
            with open(filepath, encoding="utf-8") as f:
                json_data = json.load(f)
                for _id, data in enumerate(json_data):
                    yield _id, {
                        "category": data["category"],
                        "body": data["body"],
                        "id": data["id"],
                        "rating": data["rating"],
                    }
        elif self.config.name == "wocka":
            with open(filepath, encoding="utf-8") as f:
                json_data = json.load(f)
                for _id, data in enumerate(json_data):
                    yield _id, {
                        "title": data["title"],
                        "body": data["body"],
                        "category": data["category"],
                        "id": data["id"],
                    }
