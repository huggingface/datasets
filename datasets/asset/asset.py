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
"""ASSET: a dataset for sentence simplification evaluation"""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_CITATION = """\
@inproceedings{alva-manchego-etal-2020-asset,
    title = "{ASSET}: {A} Dataset for Tuning and Evaluation of Sentence Simplification Models with Multiple Rewriting Transformations",
    author = "Alva-Manchego, Fernando  and
      Martin, Louis  and
      Bordes, Antoine  and
      Scarton, Carolina  and
      Sagot, Benoit  and
      Specia, Lucia",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.424",
    pages = "4668--4679",
}
"""

_DESCRIPTION = """\
ASSET is a dataset for evaluating Sentence Simplification systems with multiple rewriting transformations,
as described in "ASSET: A Dataset for Tuning and Evaluation of Sentence Simplification Models with Multiple Rewriting Transformations".
The corpus is composed of 2000 validation and 359 test original sentences that were each simplified 10 times by different annotators.
The corpus also contains human judgments of meaning preservation, fluency and simplicity for the outputs of several automatic text simplification systems.
"""

_HOMEPAGE = "https://github.com/facebookresearch/asset"

_LICENSE = "Creative Common Attribution-NonCommercial 4.0 International"

_URL_LIST = [
    ("human_ratings.csv", "https://github.com/facebookresearch/asset/raw/master/human_ratings/human_ratings.csv"),
    ("asset.valid.orig", "https://github.com/facebookresearch/asset/raw/master/dataset/asset.valid.orig"),
    ("asset.test.orig", "https://github.com/facebookresearch/asset/raw/master/dataset/asset.test.orig"),
]
_URL_LIST += [
    (
        f"asset.{spl}.simp.{i}",
        f"https://github.com/facebookresearch/asset/raw/master/dataset/asset.{spl}.simp.{i}",
    )
    for spl in ["valid", "test"]
    for i in range(10)
]

_URLs = dict(_URL_LIST)


class Asset(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="simplification",
            version=VERSION,
            description="A set of original sentences aligned with 10 possible simplifications for each.",
        ),
        datasets.BuilderConfig(
            name="ratings", version=VERSION, description="Human ratings of automatically produced text implification."
        ),
    ]

    DEFAULT_CONFIG_NAME = "simplification"

    def _info(self):
        if self.config.name == "simplification":
            features = datasets.Features(
                {
                    "original": datasets.Value("string"),
                    "simplifications": datasets.Sequence(datasets.Value("string")),
                }
            )
        else:
            features = datasets.Features(
                {
                    "original": datasets.Value("string"),
                    "simplification": datasets.Value("string"),
                    "original_sentence_id": datasets.Value("int32"),
                    "aspect": datasets.ClassLabel(names=["meaning", "fluency", "simplicity"]),
                    "worker_id": datasets.Value("int32"),
                    "rating": datasets.Value("int32"),
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
        data_dir = dl_manager.download_and_extract(_URLs)
        if self.config.name == "simplification":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepaths": data_dir,
                        "split": "valid",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"filepaths": data_dir, "split": "test"},
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name="full",
                    gen_kwargs={
                        "filepaths": data_dir,
                        "split": "full",
                    },
                ),
            ]

    def _generate_examples(self, filepaths, split):
        """ Yields examples. """
        if self.config.name == "simplification":
            files = [open(filepaths[f"asset.{split}.orig"], encoding="utf-8")] + [
                open(filepaths[f"asset.{split}.simp.{i}"], encoding="utf-8") for i in range(10)
            ]
            for id_, lines in enumerate(zip(*files)):
                yield id_, {"original": lines[0].strip(), "simplifications": [line.strip() for line in lines[1:]]}
        else:
            with open(filepaths[f"human_ratings.csv"], encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=",")
                for id_, row in enumerate(reader):
                    if id_ == 0:
                        keys = row[:]
                    else:
                        res = dict([(k, v) for k, v in zip(keys, row)])
                        for k in ["original_sentence_id", "worker_id", "rating"]:
                            res[k] = int(res[k])
                        yield (id_ - 1), res
