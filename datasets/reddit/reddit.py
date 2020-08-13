# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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

# Lint as: python3
"""Reddit dataset using tldr as summaries."""

import json
import os

import nlp


_CITATION = """
@inproceedings{volske-etal-2017-tl,
    title = {TL;DR: Mining {R}eddit to Learn Automatic Summarization},
    author = {V{\"o}lske, Michael  and Potthast, Martin  and Syed, Shahbaz  and Stein, Benno},
    booktitle = {Proceedings of the Workshop on New Frontiers in Summarization},
    month = {sep},
    year = {2017},
    address = {Copenhagen, Denmark},
    publisher = {Association for Computational Linguistics},
    url = {https://www.aclweb.org/anthology/W17-4508},
    doi = {10.18653/v1/W17-4508},
    pages = {59--63},
    abstract = {Recent advances in automatic text summarization have used deep neural networks to generate high-quality abstractive summaries, but the performance of these models strongly depends on large amounts of suitable training data. We propose a new method for mining social media for author-provided summaries, taking advantage of the common practice of appending a {``}TL;DR{''} to long posts. A case study using a large Reddit crawl yields the Webis-TLDR-17 dataset, complementing existing corpora primarily from the news genre. Our technique is likely applicable to other social media sites and general web crawls.},
}
"""

_DESCRIPTION = """
This corpus contains preprocessed posts from the Reddit dataset.
The dataset consists of 3,848,330 posts with an average length of 270 words for content,
and 28 words for the summary.

Features includes strings: author, body, normalizedBody, content, summary, subreddit, subreddit_id.
Content is used as document and summary is used as summary.
"""

_URL = "https://zenodo.org/record/1043504/files/corpus-webis-tldr-17.zip?download=1"

_DOCUMENT = "content"
_SUMMARY = "summary"
_ADDITIONAL_FEATURES = ["author", "body", "normalizedBody", "subreddit", "subreddit_id", "id"]


class Reddit(nlp.GeneratorBasedBuilder):
    """Reddit Dataset."""

    VERSION = nlp.Version("1.0.0")

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({k: nlp.Value("string") for k in _ADDITIONAL_FEATURES + [_DOCUMENT, _SUMMARY]}),
            supervised_keys=None,
            homepage="https://github.com/webis-de/webis-tldr-17-corpus",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download_and_extract(_URL)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, gen_kwargs={"path": os.path.join(dl_path, "corpus-webis-tldr-17.json")},
            )
        ]

    def _generate_examples(self, path=None):
        """Yields examples."""
        with open(path, "rb") as f:
            for i, line in enumerate(f):
                # possible keys are:
                #   author: string (nullable = true)
                #   body: string (nullable = true)
                #   normalizedBody: string (nullable = true)
                #   content: string (nullable = true)
                #   content_len: long (nullable = true)
                #   summary: string (nullable = true)
                #   summary_len: long (nullable = true)
                #   id: string (nullable = true)
                #   subreddit: string (nullable = true)
                #   subreddit_id: string (nullable = true)
                #   title: string (nullable = true)
                d = json.loads(line)
                if _SUMMARY in d and _DOCUMENT in d:
                    yield i, {k: d.get(k, "") for k in _ADDITIONAL_FEATURES + [_DOCUMENT, _SUMMARY]}
