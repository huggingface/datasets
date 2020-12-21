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
"""The dataset contains a set of 2,972 Arabic newspaper articles alongwith metadata, extracted from various online Saudi newspapers."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@misc{hagrima2015,
author = "M. Alhagri",
title = "Saudi Newspapers Arabic Corpus (SaudiNewsNet)",
year = 2015,
url = "http://github.com/ParallelMazen/SaudiNewsNet"
}
"""


_DESCRIPTION = """The dataset contains a set of 2,972 Arabic newspaper articles alongwith metadata, \
extracted from various online Saudi newspapers and written in MSA."""


_HOMEPAGE = "https://github.com/parallelfold/SaudiNewsNet"


_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License."


_URL = "https://github.com/parallelfold/SaudiNewsNet/raw/master/dataset/2015-07-21.zip"


class SaudiNewsNet(datasets.GeneratorBasedBuilder):
    """a set of 2972 Arabic newspaper articles along with metadata"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "source": datasets.Value(
                        "string"
                    ),  # A string identifief of the newspaper from which the article was extracted.
                    "url": datasets.Value("string"),  # The full URL from which the article was extracted.
                    "date_extracted": datasets.Value(
                        "string"
                    ),  # The timestamp of the date on which the article was extracted.
                    "title": datasets.Value("string"),  # The title of the article. Can be empty.
                    "author": datasets.Value("string"),  # The author of the article. Can be empty.
                    "content": datasets.Value("string"),  # The content of the article.
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        datadir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(datadir, "2015-07-21.json"), "split": "train"},
            )
        ]

    def _generate_examples(self, filepath, split):
        """Generates examples"""
        with open(filepath, encoding="utf-8") as f:
            articles = json.load(f)
            for _id, article in enumerate(articles):
                title = article.get("title", "")
                source = article["source"]
                dt = article["date_extracted"]
                link = article["url"]
                author = article.get("author", "").strip("&nbsp;")
                content = article["content"].strip("/n")

                yield _id, {
                    "title": title,
                    "source": source,
                    "date_extracted": dt,
                    "url": link,
                    "author": author,
                    "content": content,
                }
