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
"""Swahili : News Classification Dataset"""

from __future__ import absolute_import, division, print_function

import csv

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@dataset{davis_david_2020_4300294,
  author       = {Davis David},
  title        = {Swahili : News Classification Dataset},
  month        = dec,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {0.1},
  doi          = {10.5281/zenodo.4300294},
  url          = {https://doi.org/10.5281/zenodo.4300294}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Swahili is spoken by 100-150 million people across East Africa. In Tanzania, it is one of two national languages (the other is English) and it is the official language of instruction in all schools. News in Swahili is an important part of the media sphere in Tanzania.

News contributes to education, technology, and the economic growth of a country, and news in local languages plays an important cultural role in many Africa countries. In the modern age, African languages in news and other spheres are at risk of being lost as English becomes the dominant language in online spaces.

 The Swahili news dataset was created to reduce the gap of using the Swahili language to create NLP technologies and help AI practitioners in Tanzania and across Africa continent to practice their NLP skills to solve different problems in organizations or societies related to Swahili language. Swahili News were collected from different websites that provide news in the Swahili language. I was able to find some websites that provide news in Swahili only and others in different languages including Swahili.

The dataset was created for a specific task of text classification, this means each news content can be categorized into six different topics (Local news, International news , Finance news, Health news, Sports news, and Entertainment news). The dataset comes with a specified train/test split. The train set contains 75% of the dataset and test set contains 25% of the dataset.
"""


_HOMEPAGE = "https://zenodo.org/record/4300294#.X84BQdgzZPb"


_LICENSE = "Creative Commons Attribution 4.0 International"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://zenodo.org/record/4300294/files/train.csv?download=1"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class SwahiliNews(datasets.GeneratorBasedBuilder):
    """Swahili : News Classification Dataset"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="swahili_news",
            version=VERSION,
            description="Swahili : News Classification Dataset",
        )
    ]

    def _info(self):

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=["uchumi", "kitaifa", "michezo", "kimataifa", "burudani", "afya"]
                    ),
                }
            ),
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
        train_path = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
        ]

    def _generate_examples(self, filepath):

        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            for id_, row in enumerate(csv_reader):
                yield id_, {"id": row["id"], "text": row["content"], "label": row["category"]}
