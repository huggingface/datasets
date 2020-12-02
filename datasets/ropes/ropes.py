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
"""ROPES dataset.
Code is heavily inspired from https://github.com/huggingface/datasets/blob/master/datasets/squad/squad.py"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@inproceedings{Lin2019ReasoningOP,
  title={Reasoning Over Paragraph Effects in Situations},
  author={Kevin Lin and Oyvind Tafjord and Peter Clark and Matt Gardner},
  booktitle={MRQA@EMNLP},
  year={2019}
}
"""

_DESCRIPTION = """\
ROPES (Reasoning Over Paragraph Effects in Situations) is a QA dataset
which tests a system's ability to apply knowledge from a passage
of text to a new situation. A system is presented a background
passage containing a causal or qualitative relation(s) (e.g.,
"animal pollinators increase efficiency of fertilization in flowers"),
a novel situation that uses this background, and questions that require
reasoning about effects of the relationships in the background
passage in the background of the situation.
"""

_LICENSE = "CC BY 4.0"

_URLs = {
    "train+dev": "https://ropes-dataset.s3-us-west-2.amazonaws.com/train_and_dev/ropes-train-dev-v1.0.tar.gz",
    "test": "https://ropes-dataset.s3-us-west-2.amazonaws.com/test/ropes-test-questions-v1.0.tar.gz",
}


class Ropes(datasets.GeneratorBasedBuilder):
    """ROPES datset: testing a system's ability
    to apply knowledge from a passage of text to a new situation.."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="plain_text", description="Plain text", version=VERSION),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "background": datasets.Value("string"),
                    "situation": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://allenai.org/data/ropes",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir["train+dev"], "ropes-train-dev-v1.0", "train-v1.0.json"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir["test"], "ropes-test-questions-v1.0", "test-1.0.json"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir["train+dev"], "ropes-train-dev-v1.0", "dev-v1.0.json"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            ropes = json.load(f)
            for article in ropes["data"]:
                for paragraph in article["paragraphs"]:
                    background = paragraph["background"].strip()
                    situation = paragraph["situation"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]
                        answers = [] if split == "test" else [answer["text"].strip() for answer in qa["answers"]]

                        yield id_, {
                            "background": background,
                            "situation": situation,
                            "question": question,
                            "id": id_,
                            "answers": {
                                "text": answers,
                            },
                        }
