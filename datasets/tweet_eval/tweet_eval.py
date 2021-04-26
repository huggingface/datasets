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
"""The Tweet Eval Datasets"""


import datasets


_CITATION = """\
@inproceedings{barbieri2020tweeteval,
  title={{TweetEval:Unified Benchmark and Comparative Evaluation for Tweet Classification}},
  author={Barbieri, Francesco and Camacho-Collados, Jose and Espinosa-Anke, Luis and Neves, Leonardo},
  booktitle={Proceedings of Findings of EMNLP},
  year={2020}
}
"""

_DESCRIPTION = """\
TweetEval consists of seven heterogenous tasks in Twitter, all framed as multi-class tweet classification. All tasks have been unified into the same benchmark, with each dataset presented in the same format and with fixed training, validation and test splits.
"""

_HOMEPAGE = "https://github.com/cardiffnlp/tweeteval"

_LICENSE = ""

URL = "https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/"

_URLs = {
    "emoji": {
        "train_text": URL + "emoji/train_text.txt",
        "train_labels": URL + "emoji/train_labels.txt",
        "test_text": URL + "emoji/test_text.txt",
        "test_labels": URL + "emoji/test_labels.txt",
        "val_text": URL + "emoji/val_text.txt",
        "val_labels": URL + "emoji/val_labels.txt",
    },
    "emotion": {
        "train_text": URL + "emotion/train_text.txt",
        "train_labels": URL + "emotion/train_labels.txt",
        "test_text": URL + "emotion/test_text.txt",
        "test_labels": URL + "emotion/test_labels.txt",
        "val_text": URL + "emotion/val_text.txt",
        "val_labels": URL + "emotion/val_labels.txt",
    },
    "hate": {
        "train_text": URL + "hate/train_text.txt",
        "train_labels": URL + "hate/train_labels.txt",
        "test_text": URL + "hate/test_text.txt",
        "test_labels": URL + "hate/test_labels.txt",
        "val_text": URL + "hate/val_text.txt",
        "val_labels": URL + "hate/val_labels.txt",
    },
    "irony": {
        "train_text": URL + "irony/train_text.txt",
        "train_labels": URL + "irony/train_labels.txt",
        "test_text": URL + "irony/test_text.txt",
        "test_labels": URL + "irony/test_labels.txt",
        "val_text": URL + "irony/val_text.txt",
        "val_labels": URL + "irony/val_labels.txt",
    },
    "offensive": {
        "train_text": URL + "offensive/train_text.txt",
        "train_labels": URL + "offensive/train_labels.txt",
        "test_text": URL + "offensive/test_text.txt",
        "test_labels": URL + "offensive/test_labels.txt",
        "val_text": URL + "offensive/val_text.txt",
        "val_labels": URL + "offensive/val_labels.txt",
    },
    "sentiment": {
        "train_text": URL + "sentiment/train_text.txt",
        "train_labels": URL + "sentiment/train_labels.txt",
        "test_text": URL + "sentiment/test_text.txt",
        "test_labels": URL + "sentiment/test_labels.txt",
        "val_text": URL + "sentiment/val_text.txt",
        "val_labels": URL + "sentiment/val_labels.txt",
    },
    "stance": {
        "abortion": {
            "train_text": URL + "stance/abortion/train_text.txt",
            "train_labels": URL + "stance/abortion/train_labels.txt",
            "test_text": URL + "stance/abortion/test_text.txt",
            "test_labels": URL + "stance/abortion/test_labels.txt",
            "val_text": URL + "stance/abortion/val_text.txt",
            "val_labels": URL + "stance/abortion/val_labels.txt",
        },
        "atheism": {
            "train_text": URL + "stance/atheism/train_text.txt",
            "train_labels": URL + "stance/atheism/train_labels.txt",
            "test_text": URL + "stance/atheism/test_text.txt",
            "test_labels": URL + "stance/atheism/test_labels.txt",
            "val_text": URL + "stance/atheism/val_text.txt",
            "val_labels": URL + "stance/atheism/val_labels.txt",
        },
        "climate": {
            "train_text": URL + "stance/climate/train_text.txt",
            "train_labels": URL + "stance/climate/train_labels.txt",
            "test_text": URL + "stance/climate/test_text.txt",
            "test_labels": URL + "stance/climate/test_labels.txt",
            "val_text": URL + "stance/climate/val_text.txt",
            "val_labels": URL + "stance/climate/val_labels.txt",
        },
        "feminist": {
            "train_text": URL + "stance/feminist/train_text.txt",
            "train_labels": URL + "stance/feminist/train_labels.txt",
            "test_text": URL + "stance/feminist/test_text.txt",
            "test_labels": URL + "stance/feminist/test_labels.txt",
            "val_text": URL + "stance/feminist/val_text.txt",
            "val_labels": URL + "stance/feminist/val_labels.txt",
        },
        "hillary": {
            "train_text": URL + "stance/hillary/train_text.txt",
            "train_labels": URL + "stance/hillary/train_labels.txt",
            "test_text": URL + "stance/hillary/test_text.txt",
            "test_labels": URL + "stance/hillary/test_labels.txt",
            "val_text": URL + "stance/hillary/val_text.txt",
            "val_labels": URL + "stance/hillary/val_labels.txt",
        },
    },
}


class TweetEvalConfig(datasets.BuilderConfig):
    def __init__(self, *args, type=None, sub_type=None, **kwargs):
        super().__init__(
            *args,
            name=f"{type}" if type != "stance" else f"{type}_{sub_type}",
            **kwargs,
        )
        self.type = type
        self.sub_type = sub_type


class TweetEval(datasets.GeneratorBasedBuilder):
    """TweetEval Dataset."""

    BUILDER_CONFIGS = [
        TweetEvalConfig(
            type=key,
            sub_type=None,
            version=datasets.Version("1.1.0"),
            description=f"This part of my dataset covers {key} part of TweetEval Dataset.",
        )
        for key in list(_URLs.keys())
        if key != "stance"
    ] + [
        TweetEvalConfig(
            type="stance",
            sub_type=key,
            version=datasets.Version("1.1.0"),
            description=f"This part of my dataset covers stance_{key} part of TweetEval Dataset.",
        )
        for key in list(_URLs["stance"].keys())
    ]

    def _info(self):
        if self.config.type == "stance":
            names = ["none", "against", "favor"]
        elif self.config.type == "sentiment":
            names = ["negative", "neutral", "positive"]
        elif self.config.type == "offensive":
            names = ["non-offensive", "offensive"]
        elif self.config.type == "irony":
            names = ["non_irony", "irony"]
        elif self.config.type == "hate":
            names = ["non-hate", "hate"]
        elif self.config.type == "emoji":
            names = [
                "❤",
                "😍",
                "😂",
                "💕",
                "🔥",
                "😊",
                "😎",
                "✨",
                "💙",
                "😘",
                "📷",
                "🇺🇸",
                "☀",
                "💜",
                "😉",
                "💯",
                "😁",
                "🎄",
                "📸",
                "😜",
            ]

        else:
            names = ["anger", "joy", "optimism", "sadness"]

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"text": datasets.Value("string"), "label": datasets.features.ClassLabel(names=names)}
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        if self.config.type != "stance":
            my_urls = _URLs[self.config.type]
        else:
            my_urls = _URLs[self.config.type][self.config.sub_type]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"text_path": data_dir["train_text"], "labels_path": data_dir["train_labels"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"text_path": data_dir["test_text"], "labels_path": data_dir["test_labels"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"text_path": data_dir["val_text"], "labels_path": data_dir["val_labels"]},
            ),
        ]

    def _generate_examples(self, text_path, labels_path):
        """Yields examples."""

        with open(text_path, encoding="utf-8") as f:
            texts = f.readlines()
        with open(labels_path, encoding="utf-8") as f:
            labels = f.readlines()
        for i, text in enumerate(texts):
            yield i, {"text": text.strip(), "label": int(labels[i].strip())}
