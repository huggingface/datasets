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

import csv

import datasets


_CITATION = """\
@dataset{davis_david_2020_5514203,
  author       = {Davis David},
  title        = {Swahili : News Classification Dataset},
  month        = dec,
  year         = 2020,
  note         = {{The news version contains both train and test sets.}},
  publisher    = {Zenodo},
  version      = {0.2},
  doi          = {10.5281/zenodo.5514203},
  url          = {https://doi.org/10.5281/zenodo.5514203}
}
"""

_DESCRIPTION = """\
Swahili is spoken by 100-150 million people across East Africa. In Tanzania, it is one of two national languages (the other is English) and it is the official language of instruction in all schools. News in Swahili is an important part of the media sphere in Tanzania.

News contributes to education, technology, and the economic growth of a country, and news in local languages plays an important cultural role in many Africa countries. In the modern age, African languages in news and other spheres are at risk of being lost as English becomes the dominant language in online spaces.

The Swahili news dataset was created to reduce the gap of using the Swahili language to create NLP technologies and help AI practitioners in Tanzania and across Africa continent to practice their NLP skills to solve different problems in organizations or societies related to Swahili language. Swahili News were collected from different websites that provide news in the Swahili language. I was able to find some websites that provide news in Swahili only and others in different languages including Swahili.

The dataset was created for a specific task of text classification, this means each news content can be categorized into six different topics (Local news, International news , Finance news, Health news, Sports news, and Entertainment news). The dataset comes with a specified train/test split. The train set contains 75% of the dataset and test set contains 25% of the dataset.
"""

_HOMEPAGE = "https://zenodo.org/record/4300294#.X84BQdgzZPb"

_LICENSE = "Creative Commons Attribution 4.0 International"

# The HuggingFace Datasets library don't host the datasets but only point to the original files
_URLS = {
    "train": "https://zenodo.org/record/5514203/files/train_v0.2.csv?download=1",
    "test": "https://zenodo.org/record/5514203/files/test_v0.2.csv?download=1",
}


class SwahiliNews(datasets.GeneratorBasedBuilder):
    """Swahili : News Classification Dataset"""

    VERSION = datasets.Version("0.2.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="swahili_news",
            version=VERSION,
            description="Swahili : News Classification Dataset",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=["uchumi", "kitaifa", "michezo", "kimataifa", "burudani", "afya"]
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        paths = dl_manager.download_and_extract(_URLS)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": paths["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": paths["test"]}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            for id_, row in enumerate(csv_reader):
                yield id_, row
