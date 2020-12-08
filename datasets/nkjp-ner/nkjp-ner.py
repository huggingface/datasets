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
"""NKJP-NER"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@book{przepiorkowski2012narodowy,
title={Narodowy korpus jezyka polskiego},
author={Przepi{\'o}rkowski, Adam},
year={2012},
publisher={Naukowe PWN}
}
"""

_DESCRIPTION = """\
The NKJP-NER is based on a human-annotated part of National Corpus of Polish (NKJP). We extracted sentences with named entities of exactly one type. The task is to predict the type of the named entity.
"""

_HOMEPAGE = "https://klejbenchmark.com/tasks/"

_LICENSE = "GNU GPL v.3"

_URLs = "https://klejbenchmark.com/static/data/klej_nkjp-ner.zip"


class NkjpNer(datasets.GeneratorBasedBuilder):
    """NKJP-NER"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "target": datasets.ClassLabel(
                        names=[
                            "geogName",
                            "noEntity",
                            "orgName",
                            "persName",
                            "placeName",
                            "time",
                        ]
                    ),
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
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.tsv"),
                    "split": "dev",
                },
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
