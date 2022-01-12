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
"""LaRoSeDa: A Large Romanian Sentiment Data Set"""


import json

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{
    tache2101clustering,
    title={Clustering Word Embeddings with Self-Organizing Maps. Application on LaRoSeDa -- A Large Romanian Sentiment Data Set},
    author={Anca Maria Tache and Mihaela Gaman and Radu Tudor Ionescu},
    journal={ArXiv},
    year = {2021}
}
"""

# You can copy an official description
_DESCRIPTION = """\
        LaRoSeDa (A Large Romanian Sentiment Data Set) contains 15,000 reviews written in Romanian, of which 7,500 are positive and 7,500 negative.
        Star ratings of 1 and 2 and of 4 and 5 are provided for negative and positive reviews respectively.
        The current dataset uses star rating as the label for multi-class classification.
"""

_HOMEPAGE = "https://github.com/ancatache/LaRoSeDa"

_LICENSE = "CC BY-SA 4.0 License"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://raw.githubusercontent.com/ancatache/LaRoSeDa/main/data_splitted/"

_TRAIN_FILE = "laroseda_train.json"
_TEST_FILE = "laroseda_test.json"


class LarosedaConfig(datasets.BuilderConfig):
    """BuilderConfig for the LaRoSeDa dataset"""

    def __init__(self, **kwargs):
        super(LarosedaConfig, self).__init__(**kwargs)


class Laroseda(datasets.GeneratorBasedBuilder):
    """LaRoSeDa dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        LarosedaConfig(name="laroseda", version=VERSION, description="LaRoSeDa dataset"),
    ]

    def _info(self):

        features = datasets.Features(
            {
                "index": datasets.Value("string"),
                "title": datasets.Value("string"),
                "content": datasets.Value("string"),
                "starRating": datasets.Value("int64"),
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
            "train": _URL + _TRAIN_FILE,
            "test": _URL + _TEST_FILE,
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
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""

        with open(filepath, "r", encoding="utf-8") as f:
            data_list = json.load(f)["reviews"]

            for i, d in enumerate(data_list):
                yield i, {
                    "index": d["index"],
                    "title": d["title"],
                    "content": d["content"],
                    "starRating": int(d["starRating"]),
                }
