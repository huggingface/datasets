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
"""Cyberbullying detection task"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@article{ptaszynski2019results,
title={Results of the PolEval 2019 Shared Task 6: First Dataset and Open Shared Task for Automatic Cyberbullying Detection in Polish Twitter},
author={Ptaszynski, Michal and Pieciukiewicz, Agata and Dybala, Pawel},
journal={Proceedings of the PolEval 2019 Workshop},
publisher={Institute of Computer Science, Polish Academy of Sciences},
pages={89},
year={2019}
}
"""

_DESCRIPTION = """\
The Cyberbullying Detection task was part of 2019 edition of PolEval competition. The goal is to predict if a given Twitter message contains a cyberbullying (harmful) content.
"""

_HOMEPAGE = "https://github.com/ptaszynski/cyberbullying-Polish"

_LICENSE = "BSD 3-Clause"

_URLs = "https://klejbenchmark.com/static/data/klej_cbd.zip"


class Cdt(datasets.GeneratorBasedBuilder):
    """CyberbullyingDetectionTask"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "target": datasets.ClassLabel(names=["0", "1"]),
                }
            ),
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
                    "filepath": os.path.join(data_dir, "train.tsv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "test_features.tsv"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for id_, row in enumerate(reader):
                yield id_, {
                    "sentence": row["sentence"],
                    "target": -1 if split == "test" else row["target"],
                }
