# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os

import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """
@inproceedings{rajani2019explain,
     title = "Explain Yourself! Leveraging Language models for Commonsense Reasoning",
    author = "Rajani, Nazneen Fatema  and
      McCann, Bryan  and
      Xiong, Caiming  and
      Socher, Richard",
      year="2019",
    booktitle = "Proceedings of the 2019 Conference of the Association for Computational Linguistics (ACL2019)",
    url ="https://arxiv.org/abs/1906.02361"
}
"""

_DESCRIPTION = """
Common Sense Explanations (CoS-E) allows for training language models to
automatically generate explanations that can be used during training and
inference in a novel Commonsense Auto-Generated Explanation (CAGE) framework.
"""

_COS_E_URL = "https://raw.githubusercontent.com/salesforce/cos-e/master/data/"

# COS E has explanations for the CQA dataset, which is joined by ID.
_CQA_URL_TRAIN = "https://s3.amazonaws.com/commensenseqa/train_rand_split.jsonl"
_CQA_URL_DEV = "https://s3.amazonaws.com/commensenseqa/dev_rand_split.jsonl"
_CQA_URL_TEST = "https://s3.amazonaws.com/commensenseqa/test_rand_split_no_answers.jsonl"


def _download_and_index_cqa(dl_manager):
  """Downloads CQA and returns it, indexed by id, for joining with Cos-E."""

  downloaded_files = dl_manager.download_and_extract({
      "cqa_train": _CQA_URL_TRAIN,
      "cqa_dev": _CQA_URL_DEV,
      "cqa_test": _CQA_URL_TEST
  })

  # NB: "cqa_test" is included in the files, but not in any of the CoS-E splits.
  cqa_splits = ["cqa_train", "cqa_dev"]
  cqa_complete = []
  for split in cqa_splits:
    with tf.io.gfile.GFile(downloaded_files[split]) as f:
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


class CosE(tfds.core.GeneratorBasedBuilder):
  """CoS-E: Common Sense Explanations corpus."""

  VERSION = tfds.core.Version("0.0.1")

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            "id": tfds.features.Text(),
            "question": tfds.features.Text(),
            "choices": tfds.features.Sequence(tfds.features.Text()),
            "answer": tfds.features.Text(),
            "abstractive_explanation": tfds.features.Text(),
            "extractive_explanation": tfds.features.Text(),
        }),
        supervised_keys=None,
        homepage="https://github.com/salesforce/cos-e",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""

    # NB: The CQA Dataset should be read only once, and only by callers who
    # want to _create_ the Cos-E dataset from scratch.
    cqa_indexed = _download_and_index_cqa(dl_manager)

    files = dl_manager.download_and_extract({
        "dev": [
            os.path.join(_COS_E_URL, "v1.11/dev/cose_dev_v1.11_processed.jsonl")
        ],
        "train": [
            os.path.join(_COS_E_URL,
                         "v1.11/train/cose_train_v1.11_processed.jsonl")
        ]
    })

    # We use the CoS-E/CQA dev set as our validation set.
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={"files": files["dev"],
                        "cqa_indexed": cqa_indexed},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={"files": files["train"],
                        "cqa_indexed": cqa_indexed},
        ),
    ]

  def _generate_examples(self, files, **kwargs):
    """Yields examples."""
    cqa_indexed = kwargs["cqa_indexed"]
    for filepath in files:
      with tf.io.gfile.GFile(filepath) as f:
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
