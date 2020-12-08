# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""MedHop: Reading Comprehension with Multiple Hops"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@misc{welbl2018constructing,
      title={Constructing Datasets for Multi-hop Reading Comprehension Across Documents},
      author={Johannes Welbl and Pontus Stenetorp and Sebastian Riedel},
      year={2018},
      eprint={1710.06481},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
MedHop is based on research paper abstracts from PubMed, and the queries are about interactions between pairs of drugs. \
The correct answer has to be inferred by combining information from a chain of reactions of drugs and proteins.
"""

_URL = "https://drive.google.com/uc?export=download&id=1ytVZ4AhubFDOEL7o7XrIRIyhU8g9wvKA"


class MedHopConfig(datasets.BuilderConfig):
    """BuilderConfig for MedHop."""

    def __init__(self, masked=False, **kwargs):
        """BuilderConfig for MedHop.

        Args:
          masked: `bool`, original or maksed data.
          **kwargs: keyword arguments forwarded to super.
        """
        super(MedHopConfig, self).__init__(**kwargs)
        self.masked = masked


class MedHop(datasets.GeneratorBasedBuilder):
    """MedHop: Reading Comprehension with Multiple Hops"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        MedHopConfig(
            name="original",
            version=datasets.Version("1.0.0"),
            description="The un-maksed MedHop dataset",
            masked=False,
        ),
        MedHopConfig(
            name="masked", version=datasets.Version("1.0.0"), description="Masked MedHop dataset", masked=True
        ),
    ]
    BUILDER_CONFIG_CLASS = MedHopConfig
    DEFAULT_CONFIG_NAME = "original"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "candidates": datasets.Sequence(datasets.Value("string")),
                    "supports": datasets.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage="http://qangaroo.cs.ucl.ac.uk/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        extracted_path = dl_manager.download_and_extract(_URL)

        medhop_path = os.path.join(extracted_path, "qangaroo_v1.1", "medhop")
        train_file = "train.json" if self.config.name == "original" else "train.masked.json"
        dev_file = "dev.json" if self.config.name == "original" else "dev.masked.json"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(medhop_path, train_file)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(medhop_path, dev_file)},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            examples = json.load(f)
            for i, example in enumerate(examples):
                example["question"] = example.pop("query")
                yield example["id"], example
