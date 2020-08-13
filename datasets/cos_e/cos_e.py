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
"""Commonsense Explanations (CoS-E) Dataset."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


_CITATION = """
@inproceedings{rajani2019explain,
     title = {Explain Yourself! Leveraging Language models for Commonsense Reasoning},
    author = {Rajani, Nazneen Fatema  and
      McCann, Bryan  and
      Xiong, Caiming  and
      Socher, Richard}
      year={2019}
    booktitle = {Proceedings of the 2019 Conference of the Association for Computational Linguistics (ACL2019)}
    url ={https://arxiv.org/abs/1906.02361}
}
"""

_DESCRIPTION = """
Common Sense Explanations (CoS-E) allows for training language models to
automatically generate explanations that can be used during training and
inference in a novel Commonsense Auto-Generated Explanation (CAGE) framework.
"""

_COS_E_URL = "https://raw.githubusercontent.com/salesforce/cos-e/master/data/"

# COS E has explanations for the CQA dataset, which is joined by ID.
_CQA_V1_11_URL_TRAIN = "https://s3.amazonaws.com/commensenseqa/train_rand_split.jsonl"
_CQA_V1_11_URL_DEV = "https://s3.amazonaws.com/commensenseqa/dev_rand_split.jsonl"
_CQA_V1_11_URL_TEST = "https://s3.amazonaws.com/commensenseqa/test_rand_split_no_answers.jsonl"

_CQA_V1_0_URL_TRAIN = os.path.join(_COS_E_URL, "v1.0/train_rand_split.jsonl")
_CQA_V1_0_URL_DEV = os.path.join(_COS_E_URL, "v1.0/dev_rand_split.jsonl")
_CQA_V1_0_URL_TEST = os.path.join(_COS_E_URL, "v1.0/test_rand_split_no_answers.jsonl")


def _download_and_index_cqa(dl_manager, name):
    """Downloads CQA and returns it, indexed by id, for joining with Cos-E."""

    downloaded_files = dl_manager.download_and_extract(
        {
            "cqa_train": _CQA_V1_11_URL_TRAIN if name == "v1.11" else _CQA_V1_0_URL_TRAIN,
            "cqa_dev": _CQA_V1_11_URL_DEV if name == "v1.11" else _CQA_V1_0_URL_DEV,
            "cqa_test": _CQA_V1_11_URL_TEST if name == "v1.11" else _CQA_V1_0_URL_TEST,
        }
    )

    # NB: "cqa_test" is included in the files, but not in any of the CoS-E splits.
    cqa_splits = ["cqa_train", "cqa_dev"]
    cqa_complete = []
    for split in cqa_splits:
        with open(downloaded_files[split]) as f:
            for _, line in enumerate(f):
                d = json.loads(line)
                cqa_complete.append(d)

        # Index the CQA dataset by id for joining with Cos-E.
        cqa_indexed = {}
    for d in cqa_complete:
        cqa_indexed[d["id"]] = d
    return cqa_indexed


def _get_choices_and_answer(cqa):
    """Returns choices and the answer from a cqa example."""
    choices = []
    answer_key = cqa["answerKey"]
    answer = None
    for choice in cqa["question"]["choices"]:
        choices.append(choice["text"])
        if answer_key == choice["label"]:
            answer = choice["text"]
    return choices, answer


class CosEConfig(nlp.BuilderConfig):

    """ BuilderConfig for CosE"""

    def __init__(self, **kwargs):
        """

        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(CosEConfig, self).__init__(**kwargs)


class CosE(nlp.GeneratorBasedBuilder):
    """CoS-E: Common Sense Explanations corpus."""

    BUILDER_CONFIGS = [
        CosEConfig(
            name="v1.0",
            description="cos-e version 1.0",
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"),
        ),
        CosEConfig(
            name="v1.11",
            description="cos-e version 1.11",
            version=nlp.Version("1.11.0", "New split API (https://tensorflow.org/datasets/splits)"),
        ),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "choices": nlp.features.Sequence(nlp.Value("string")),
                    "answer": nlp.Value("string"),
                    "abstractive_explanation": nlp.Value("string"),
                    "extractive_explanation": nlp.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/salesforce/cos-e",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        # NB: The CQA Dataset should be read only once, and only by callers who
        # want to _create_ the Cos-E dataset from scratch.
        cqa_indexed = _download_and_index_cqa(dl_manager, self.config.name)

        if self.config.name == "v1.11":
            files = dl_manager.download_and_extract(
                {
                    "dev": [os.path.join(_COS_E_URL, "v1.11/cose_dev_v1.11_processed.jsonl")],
                    "train": [os.path.join(_COS_E_URL, "v1.11/cose_train_v1.11_processed.jsonl")],
                }
            )

        elif self.config.name == "v1.0":
            files = dl_manager.download_and_extract(
                {
                    "dev": [os.path.join(_COS_E_URL, "v1.0/cose_dev_v1.0_processed.jsonl")],
                    "train": [os.path.join(_COS_E_URL, "v1.0/cose_train_v1.0_processed.jsonl")],
                }
            )
        else:
            raise ValueError("Unknown config name")
        # We use the CoS-E/CQA dev set as our validation set.
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, gen_kwargs={"files": files["train"], "cqa_indexed": cqa_indexed},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"files": files["dev"], "cqa_indexed": cqa_indexed},
            ),
        ]

    def _generate_examples(self, files, **kwargs):
        """Yields examples."""
        cqa_indexed = kwargs["cqa_indexed"]
        for filepath in files:
            with open(filepath) as f:
                for line in f:
                    cos = json.loads(line)
                    cqa = cqa_indexed[cos["id"]]
                    choices, answer = _get_choices_and_answer(cqa)
                    yield cos["id"], {
                        "id": cos["id"],
                        "question": cqa["question"]["stem"],
                        "choices": choices,
                        "answer": answer,
                        "abstractive_explanation": cos["explanation"]["open-ended"],
                        "extractive_explanation": cos["explanation"]["selected"],
                    }
