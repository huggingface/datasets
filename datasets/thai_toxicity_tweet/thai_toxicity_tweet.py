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
# Lint as: python3


import json
import os

import datasets


_CITATION = """\
@article{sirihattasak2019annotation,
  title={Annotation and Classification of Toxicity for Thai Twitter},
  author={Sirihattasak, Sugan and Komachi, Mamoru and Ishikawa, Hiroshi},
  year={2019}
}
"""

_DESCRIPTION = """\
Thai Toxicity Tweet Corpus contains 3,300 tweets annotated by humans with guidelines including a 44-word dictionary.
The author obtained 2,027 and 1,273 toxic and non-toxic tweets, respectively; these were labeled by three annotators. The result of corpus
analysis indicates that tweets that include toxic words are not always toxic. Further, it is more likely that a tweet is toxic, if it contains
toxic words indicating their original meaning. Moreover, disagreements in annotation are primarily because of sarcasm, unclear existing
target, and word sense ambiguity.

Notes from data cleaner: The data is included into [huggingface/datasets](https://www.github.com/huggingface/datasets) in Dec 2020.
By this time, 506 of the tweets are not available publicly anymore. We denote these by `TWEET_NOT_FOUND` in `tweet_text`.
Processing can be found at [this PR](https://github.com/tmu-nlp/ThaiToxicityTweetCorpus/pull/1).
"""


class ThaiToxicityTweetConfig(datasets.BuilderConfig):
    """BuilderConfig"""

    def __init__(self, **kwargs):
        """BuilderConfig

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ThaiToxicityTweetConfig, self).__init__(**kwargs)


class ThaiToxicityTweet(datasets.GeneratorBasedBuilder):

    _DOWNLOAD_URL = "https://archive.org/download/ThaiToxicityTweetCorpus/data.zip"
    _TRAIN_FILE = "train.jsonl"

    BUILDER_CONFIGS = [
        ThaiToxicityTweetConfig(
            name="thai_toxicity_tweet",
            version=datasets.Version("1.0.0"),
            description=_DESCRIPTION,
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "tweet_id": datasets.Value("string"),
                    "tweet_text": datasets.Value("string"),
                    "toxic_votes": datasets.Value("int32"),
                    "nontoxic_votes": datasets.Value("int32"),
                    "is_toxic": datasets.features.ClassLabel(names=["neg", "pos"]),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/tmu-nlp/ThaiToxicityTweetCorpus/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(self._DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "data")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TRAIN_FILE)},
            ),
        ]

    def _generate_examples(self, filepath):
        """Generate examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "tweet_id": str(data["tweet_id"]),
                    "tweet_text": data["tweet_text"],
                    "toxic_votes": data["toxic_votes"],
                    "nontoxic_votes": data["nontoxic_votes"],
                    "is_toxic": data["is_toxic"],
                }
