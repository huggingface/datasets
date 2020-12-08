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
"""SWAG dataset."""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_CITATION = """\
@inproceedings{zellers2018swagaf,
    title={SWAG: A Large-Scale Adversarial Dataset for Grounded Commonsense Inference},
    author={Zellers, Rowan and Bisk, Yonatan and Schwartz, Roy and Choi, Yejin},
    booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    year={2018}
}
"""

_DESCRIPTION = """\
Given a partial description like "she opened the hood of the car,"
humans can reason about the situation and anticipate what might come
next ("then, she examined the engine"). SWAG (Situations With Adversarial Generations)
is a large-scale dataset for this task of grounded commonsense
inference, unifying natural language inference and physically grounded reasoning.

The dataset consists of 113k multiple choice questions about grounded situations
(73k training, 20k validation, 20k test).
Each question is a video caption from LSMDC or ActivityNet Captions,
with four answer choices about what might happen next in the scene.
The correct answer is the (real) video caption for the next event in the video;
the three incorrect answers are adversarially generated and human verified,
so as to fool machines but not humans. SWAG aims to be a benchmark for
evaluating grounded commonsense NLI and for learning representations.

The full data contain more information,
but the regular configuration will be more interesting for modeling
(note that the regular data are shuffled). The test set for leaderboard submission
is under the regular configuration.
"""

_LICENSE = "Unknown"

_URLs = {
    "full": {
        "train": "https://raw.githubusercontent.com/rowanz/swagaf/master/data/train_full.csv",
        "val": "https://raw.githubusercontent.com/rowanz/swagaf/master/data/val_full.csv",
    },
    "regular": {
        "train": "https://raw.githubusercontent.com/rowanz/swagaf/master/data/train.csv",
        "val": "https://raw.githubusercontent.com/rowanz/swagaf/master/data/val.csv",
        "test": "https://raw.githubusercontent.com/rowanz/swagaf/master/data/test.csv",
    },
}


class Swag(datasets.GeneratorBasedBuilder):
    """SWAG dataset"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="regular", description="The configuration to use for modeling."),
        datasets.BuilderConfig(name="full", description="The full data."),
    ]

    DEFAULT_CONFIG_NAME = "regular"

    def _info(self):
        if self.config.name == "regular":
            features = datasets.Features(
                {
                    "video-id": datasets.Value("string"),
                    "fold-ind": datasets.Value("string"),
                    "startphrase": datasets.Value("string"),
                    "sent1": datasets.Value("string"),
                    "sent2": datasets.Value("string"),
                    "gold-source": datasets.Value("string"),
                    "ending0": datasets.Value("string"),
                    "ending1": datasets.Value("string"),
                    "ending2": datasets.Value("string"),
                    "ending3": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["0", "1", "2", "3"]),
                }
            )
        else:
            features = datasets.Features(
                {
                    "video-id": datasets.Value("string"),
                    "fold-ind": datasets.Value("string"),
                    "startphrase": datasets.Value("string"),
                    "gold-ending": datasets.Value("string"),
                    "distractor-0": datasets.Value("string"),
                    "distractor-1": datasets.Value("string"),
                    "distractor-2": datasets.Value("string"),
                    "distractor-3": datasets.Value("string"),
                    "gold-source": datasets.Value("string"),
                    "gold-type": datasets.Value("string"),
                    "distractor-0-type": datasets.Value("string"),
                    "distractor-1-type": datasets.Value("string"),
                    "distractor-2-type": datasets.Value("string"),
                    "distractor-3-type": datasets.Value("string"),
                    "sent1": datasets.Value("string"),
                    "sent2": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://rowanzellers.com/swag/",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)

        splits = [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_dir["val"],
                    "split": "val",
                },
            ),
        ]
        if self.config.name == "regular":
            splits.append(
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"filepath": data_dir["test"], "split": "test"},
                )
            )

        return splits

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, "r", encoding="utf-8") as f:
            lines = list(csv.reader(f, delimiter=","))

            for id_, row in enumerate(lines[1:]):
                if self.config.name == "regular":
                    yield id_, {
                        "video-id": row[1],
                        "fold-ind": row[2],
                        "startphrase": row[3],
                        "sent1": row[4],
                        "sent2": row[5],
                        "gold-source": row[6],
                        "ending0": row[7],
                        "ending1": row[8],
                        "ending2": row[9],
                        "ending3": row[10],
                        "label": -1 if split == "test" else row[11],
                    }
                else:
                    yield id_, {
                        "video-id": row[0],
                        "fold-ind": row[1],
                        "startphrase": row[2],
                        "gold-ending": row[3],
                        "distractor-0": row[4],
                        "distractor-1": row[5],
                        "distractor-2": row[6],
                        "distractor-3": row[7],
                        "gold-source": row[8],
                        "gold-type": row[9],
                        "distractor-0-type": row[10],
                        "distractor-1-type": row[11],
                        "distractor-2-type": row[12],
                        "distractor-3-type": row[13],
                        "sent1": row[14],
                        "sent2": row[15],
                    }
