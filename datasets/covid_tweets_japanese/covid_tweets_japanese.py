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
"""COVID-19 Japanese Tweets Dataset."""


import bz2
import csv

import datasets


_CITATION = """\
No paper about this dataset is published yet. \
Please cite this dataset as "鈴木 優: COVID-19 日本語 Twitter データセット （http://www.db.info.gifu-u.ac.jp/covid-19-twitter-dataset/）"
"""

_DESCRIPTION = """\
53,640 Japanese tweets with annotation if a tweet is related to COVID-19 or not. The annotation is by majority decision by 5 - 10 crowd workers. \
Target tweets include "COVID" or "コロナ". The period of the tweets is from around January 2020 to around June 2020. \
The original tweets are not contained. Please use Twitter API to get them, for example.
"""

_HOMEPAGE = "http://www.db.info.gifu-u.ac.jp/covid-19-twitter-dataset/"

_LICENSE = "CC-BY-ND 4.0"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "url": "http://www.db.info.gifu-u.ac.jp/data/covid19.csv.bz2",
}


class CovidTweetsJapanese(datasets.GeneratorBasedBuilder):
    """COVID-19 Japanese Tweets Dataset."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "tweet_id": datasets.Value("string"),
                "assessment_option_id": datasets.ClassLabel(names=["63", "64", "65", "66", "67", "68"]),
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

        my_urls = _URLs["url"]
        # data_url = dl_manager.download_and_extract(my_urls)
        data_url = dl_manager.download(my_urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_url, "split": "train"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with bz2.open(filepath, "rt") as f:
            data = csv.reader(f)
            _ = next(data)
            for id_, row in enumerate(data):
                yield id_, {
                    "tweet_id": row[0],
                    "assessment_option_id": row[1],
                }
