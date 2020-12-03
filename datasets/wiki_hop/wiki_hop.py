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
"""WikiHop: Reading Comprehension with Multiple Hops"""

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
WikiHop is open-domain and based on Wikipedia articles; the goal is to recover Wikidata information by hopping through documents. \
The goal is to answer text understanding queries by combining multiple facts that are spread across different documents.
"""

_URL = "https://drive.google.com/uc?export=download&id=1ytVZ4AhubFDOEL7o7XrIRIyhU8g9wvKA"


class WikiHopConfig(datasets.BuilderConfig):
    """BuilderConfig for WikiHop."""

    def __init__(self, masked=False, **kwargs):
        """BuilderConfig for WikiHop.

        Args:
          masked: `bool`, original or maksed data.
          **kwargs: keyword arguments forwarded to super.
        """
        super(WikiHopConfig, self).__init__(**kwargs)
        self.masked = masked


class WikiHop(datasets.GeneratorBasedBuilder):
    """WikiHop: Reading Comprehension with Multiple Hops"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        WikiHopConfig(
            name="original",
            version=datasets.Version("1.0.0"),
            description="The un-maksed WikiHop dataset",
            masked=False,
        ),
        WikiHopConfig(
            name="masked", version=datasets.Version("1.0.0"), description="Masked WikiHop dataset", masked=True
        ),
    ]
    BUILDER_CONFIG_CLASS = WikiHopConfig
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
                    "annotations": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
                }
            ),
            supervised_keys=None,
            homepage="http://qangaroo.cs.ucl.ac.uk/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        extracted_path = dl_manager.download_and_extract(_URL)

        wikihop_path = os.path.join(extracted_path, "qangaroo_v1.1", "wikihop")
        train_file = "train.json" if self.config.name == "original" else "train.masked.json"
        dev_file = "dev.json" if self.config.name == "original" else "dev.masked.json"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(wikihop_path, train_file), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(wikihop_path, dev_file), "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            examples = json.load(f)
            for i, example in enumerate(examples):
                # there are no annotations for train split, setting it to empty list
                if split == "train":
                    example["annotations"] = []
                example["question"] = example.pop("query")
                yield example["id"], example
