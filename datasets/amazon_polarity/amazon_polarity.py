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
"""The amazon polarity dataset for text classification."""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{mcauley2013hidden,
  title={Hidden factors and hidden topics: understanding rating dimensions with review text},
  author={McAuley, Julian and Leskovec, Jure},
  booktitle={Proceedings of the 7th ACM conference on Recommender systems},
  pages={165--172},
  year={2013}
}
"""

_DESCRIPTION = """\
The Amazon reviews dataset consists of reviews from amazon.
The data span a period of 18 years, including ~35 million reviews up to March 2013.
Reviews include product and user information, ratings, and a plaintext review.
"""

_HOMEPAGE = "https://registry.opendata.aws/"

_LICENSE = "Apache License 2.0"

_URLs = {
    "amazon_polarity": "https://drive.google.com/u/0/uc?id=0Bz8a_Dbh9QhbaW12WVVZS2drcnM&export=download",
}


class AmazonPolarityConfig(datasets.BuilderConfig):
    """BuilderConfig for AmazonPolarity."""

    def __init__(self, **kwargs):
        """BuilderConfig for AmazonPolarity.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(AmazonPolarityConfig, self).__init__(**kwargs)


class AmazonPolarity(datasets.GeneratorBasedBuilder):
    """Amazon Polarity Classification Dataset."""

    VERSION = datasets.Version("3.0.0")

    BUILDER_CONFIGS = [
        AmazonPolarityConfig(
            name="amazon_polarity", version=VERSION, description="Amazon Polarity Classification Dataset."
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "label": datasets.features.ClassLabel(
                    names=[
                        "negative",
                        "positive",
                    ]
                ),
                "title": datasets.Value("string"),
                "content": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "amazon_review_polarity_csv", "train.csv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "amazon_review_polarity_csv", "test.csv"),
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            data = csv.reader(f, delimiter=",", quoting=csv.QUOTE_ALL)
            for id_, row in enumerate(data):
                yield id_, {
                    "title": row[1],
                    "content": row[2],
                    "label": int(row[0]) - 1,
                }
