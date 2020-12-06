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
"""Literal Motion in Text (LiMiT) dataset. """

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """\
@inproceedings{manotas-etal-2020-limit,
    title = "{L}i{M}i{T}: The Literal Motion in Text Dataset",
    author = "Manotas, Irene  and
      Vo, Ngoc Phuoc An  and
      Sheinin, Vadim",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.findings-emnlp.88",
    doi = "10.18653/v1/2020.findings-emnlp.88",
    pages = "991--1000",
    }
"""

_DESCRIPTION = """\
The Literal Motion in Text (LiMiT) dataset consists of ~24K sentences that
describe literal motion i.e. describes the movement of a physical entity (~14K sentences),
and sentences not describing motion or other type of motion (e.g. fictive motion).
Senteces were extracted from electronic books categorized as fiction or novels,
and a portion from the ActivityNet Captions Dataset.
"""

_HOMEPAGE = "https://github.com/ilmgut/limit_dataset"

_LICENSE = "CC BY-SA 4.0"

_REPO = "https://raw.githubusercontent.com/ilmgut/limit_dataset/master/data/"
_URLs = {"train": _REPO + "train.json", "test": _REPO + "test.json"}


class Limit(datasets.GeneratorBasedBuilder):
    """The Literal Motion in Text (LiMiT) dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "sentence": datasets.Value("string"),
                "motion": datasets.Value("bool"),
                "motion_entities": datasets.features.Sequence(
                    {
                        "text": datasets.Value("string"),
                        "entity_start": datasets.Value("int32"),
                    }
                ),
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
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": data_dir["test"], "split": "test"}
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for id_, x in data.items():
                id_ = int(id_)
                sentence = x["sentence"].strip()
                is_motion = x["motion"] == "yes"
                motion_entity_raw = x["motion_entity"]
                motion_entities = []
                if motion_entity_raw:
                    entities = [e for e in motion_entity_raw.split("\n") if e]
                    for entity in entities:
                        text, entity_start = entity.split(":")
                        motion_entities.append({"text": text, "entity_start": int(entity_start)})
                yield id_, {"sentence": sentence, "motion": is_motion, "motion_entities": motion_entities}
