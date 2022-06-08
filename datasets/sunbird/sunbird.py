# coding=utf-8
# Copyright 2021 Sunbird AI.
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
"""Sunbird AI machine translation benchmark dataset."""


import collections
import os
from posixpath import basename

import datasets


_DESCRIPTION = """\
Parallel train/test/eval dataset for low-resource machine translation Ugandan Languages.
"""

_CITATION = """\
  @inproceedings{akera2022machine,
  title={Machine Translation For African Languages: Community Creation Of Datasets And Models In Uganda},
  author={Akera, Benjamin and Mukiibi, Jonathan and Naggayi, Lydia Sanyu and Babirye, Claire and Owomugisha, Isaac and Nsumba, Solomon and Nakatumba-Nabende, Joyce and Bainomugisha, Engineer and Mwebaze, Ernest and Quinn, John},
  booktitle={3rd Workshop on African Natural Language Processing},
  year={2022}
}
"""

_VERSION = "4.0.0"

_URL = {
    "supervised": "https://sunbird-translate.s3.us-east-2.amazonaws.com/v7-dataset.zip",
}

# update inter-language pairs
language_pairs = [
    "en-lug", "en-nyn", "en-ach", "en-teo", "en-lgg", "lug-ach", "lug-nyn", "lug-lgg", 
    "lug-teo", "ach-nyn", "ach-lgg", "ach-teo", "teo-lgg", "teo-nyn", "nyn-lgg", "en-mul", "mul-en"
]

class SunbirdConfig(datasets.BuilderConfig):
    """Dataset config for Sunbird Dataset"""

    def __init__(self, language_pair, **kwargs):
        super().__init__(**kwargs)

        """
        Args:
            language_pair (str): language pair to use.
            **kwargs: keyword arguments to pass to the super class.
        """

        self.language_pair = language_pair

class Sunbird(datasets.GeneratorBasedBuilder):
    """Sunbird machine translation dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIG_CLASS = SunbirdConfig
    BUILDER_CONFIGS = [
        SunbirdConfig(name=pair, description=_DESCRIPTION, language_pair=pair)
        for pair in language_pairs
    ]

    def _info(self):
        src_tag, tgt_tag = self.config.language_pair.split("-")
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"translation": datasets.features.Translation(languages=(src_tag, tgt_tag))}),
            supervised_keys=(src_tag, tgt_tag),
            homepage="sunbird.ai",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        lang_pair = self.config.language_pair
        src_tag, tgt_tag = lang_pair.split("-")

        domain = "supervised"

        if domain=="supervised":
            print(_URL["supervised"].format(lang_pair))
            dl_dir = dl_manager.download_and_extract(_URL["supervised"].format(lang_pair))

        data_dir = os.path.join(dl_dir, os.path.join("v7-dataset/v7.0", domain, lang_pair))

        output=[]

        test = datasets.SplitGenerator(
            name=datasets.Split.TEST,
            gen_kwargs={
                "filepath": os.path.join(data_dir, f"test.{src_tag}"),
                "labelpath": os.path.join(data_dir, f"test.{tgt_tag}"),
            },
        )

        if f"test.{src_tag}" in os.listdir(data_dir):
            output.append(test)

        if domain == "supervised":

            train = datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, f"train.{src_tag}"),
                    "labelpath": os.path.join(data_dir, f"train.{tgt_tag}"),
                },
            )

            if f"train.{src_tag}" in os.listdir(data_dir):
                output.append(train)

            valid = datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, f"val.{src_tag}"),
                    "labelpath": os.path.join(data_dir, f"val.{tgt_tag}"),
                },
            )

            if f"val.{src_tag}" in os.listdir(data_dir):
                output.append(valid)

        return output

    def _generate_examples(self, filepath, labelpath):
        """Generates training/test examples."""
        src_tag, tgt_tag = self.config.language_pair.split("-")
        with open(filepath, encoding="utf-8") as f1, open(labelpath, encoding="utf-8") as f2:
            src = f1.read().split("\n")[:-1]
            tgt = f2.read().split("\n")[:-1]
            for idx, (s, t) in enumerate(zip(src, tgt)):
                yield idx, {"translation": {src_tag: s, tgt_tag: t}}



