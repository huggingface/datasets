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
"""Reddit Jokes"""

from __future__ import absolute_import, division, print_function

import json

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
A jokes dataset contains 195k english plaintext jokes scraped from Reddit /r/jokes. Contains all submissions to the subreddit as of 13.02.2017. This dataset is a subset of "A dataset of English plaintext jokes."
"""

_HOMEPAGE = "https://github.com/taivop/joke-dataset"
_LICENSE = ""

_TITLE = "title"
_BODY = "body"
_ID = "id"
_SCORE = "score"

_URLs = {
    "url": "https://github.com/taivop/joke-dataset/raw/master/reddit_jokes.json",
}


class RedditJokes(datasets.GeneratorBasedBuilder):
    """Reddit Jokes: A dataset containing 195k english plaintext jokes."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        feature_names = [_TITLE, _BODY, _ID, _SCORE]

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({k: datasets.Value("string") for k in feature_names}),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        my_urls = _URLs["url"]
        data_url = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_url, "split": "train"},
            )
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """

        with open(filepath, encoding="utf8") as f:
            data = json.loads(f.read())
            for id_, entry in enumerate(data):
                yield id_, {
                    _TITLE: entry["title"],
                    _BODY: entry["body"],
                    _ID: entry["id"],
                    _SCORE: str(entry["score"]),
                }
