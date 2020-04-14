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
"""The rockyou dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import nlp

_CITATION = """\
"""

_DESCRIPTION = """\
This dataset contains 14,344,391 passwords that were leaked or stolen from from various sites. The author of this dataset states that "I'm hosting them because it seems like nobody else does (hopefully it isn't because hosting them is illegal :)). Naturally, I'm not the one who stole these; I simply found them online, removed any names/email addresses/etc.". This dataset is used to train Machine Learning models for password guessing and cracking.
"""

_DOWNLOAD_URL = "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"


class RockYou(nlp.GeneratorBasedBuilder):
  """This dataset contains passwords that were leaked or stolen from from various sites."""

  VERSION = nlp.Version("0.1.0")

  def _info(self):
    return nlp.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=nlp.features.FeaturesDict({
            "password":
                nlp.features.Text(encoder=nlp.features.text.ByteTextEncoder()
                                  ),
        }),
        supervised_keys=None,
        homepage="https://wiki.skullsecurity.org/Passwords",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    dl_path = dl_manager.download(_DOWNLOAD_URL)
    return [
        nlp.SplitGenerator(
            name="train",
            gen_kwargs={
                "path": dl_path,
            },
        )
    ]

  def _generate_examples(self, path):

    with open(path, "rb") as f:
      blines = f.readlines()

    for i, bline in enumerate(blines):
      yield i, {
          "password": bline.strip(),
      }
