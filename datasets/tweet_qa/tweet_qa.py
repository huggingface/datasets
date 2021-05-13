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
"""TWEETQA: A Social Media Focused Question Answering Dataset"""


import json
import os

import datasets


_CITATION = """\
@misc{xiong2019tweetqa,
      title={TWEETQA: A Social Media Focused Question Answering Dataset},
      author={Wenhan Xiong and Jiawei Wu and Hong Wang and Vivek Kulkarni and Mo Yu and Shiyu Chang and Xiaoxiao Guo and William Yang Wang},
      year={2019},
      eprint={1907.06292},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
 TweetQA is the first dataset for QA on social media data by leveraging news media and crowdsourcing.
"""

_HOMEPAGE = "https://tweetqa.github.io/"

_LICENSE = "CC BY-SA 4.0"

_URL = "https://sites.cs.ucsb.edu/~xwhan/datasets/tweetqa.zip"


class TweetQA(datasets.GeneratorBasedBuilder):
    """TweetQA: first large-scale dataset for QA over social media data"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "Question": datasets.Value("string"),
                "Answer": datasets.Sequence(datasets.Value("string")),
                "Tweet": datasets.Value("string"),
                "qid": datasets.Value("string"),
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
        data_dir = dl_manager.download_and_extract(_URL)
        train_path = os.path.join(data_dir, "TweetQA_data", "train.json")
        test_path = os.path.join(data_dir, "TweetQA_data", "test.json")
        dev_path = os.path.join(data_dir, "TweetQA_data", "dev.json")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": train_path,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": test_path,
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": dev_path,
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            tweet_qa = json.load(f)
            for data in tweet_qa:
                id_ = data["qid"]

                yield id_, {
                    "Question": data["Question"],
                    "Answer": [] if split == "test" else data["Answer"],
                    "Tweet": data["Tweet"],
                    "qid": data["qid"],
                }
