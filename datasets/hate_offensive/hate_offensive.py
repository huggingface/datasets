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
"""Automated Hate Speech Detection and the Problem of Offensive Language."""


import csv
import os

import datasets


_CITATION = """
@article{article,
author = {Davidson, Thomas and Warmsley, Dana and Macy, Michael and Weber, Ingmar},
year = {2017},
month = {03},
pages = {},
title = {Automated Hate Speech Detection and the Problem of Offensive Language}
}
"""

_DESCRIPTION = "This dataset contains annotated tweets for automated hate-speech recognition"

_HOMEPAGE = "https://arxiv.org/abs/1905.12516"

_LICENSE = "MIT License"

_URLs = "https://github.com/t-davidson/hate-speech-and-offensive-language/raw/master/data/labeled_data.csv"


class HateOffensive(datasets.GeneratorBasedBuilder):
    """Automated Hate Speech Detection and the Problem of Offensive Language"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "total_annotation_count": datasets.Value("int32"),
                "hate_speech_annotations": datasets.Value("int32"),
                "offensive_language_annotations": datasets.Value("int32"),
                "neither_annotations": datasets.Value("int32"),
                "label": datasets.ClassLabel(names=["hate-speech", "offensive-language", "neither"]),
                "tweet": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=("tweet", "label"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(data_dir)})]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, lineterminator="\n", delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader, None)
            for id_, row in enumerate(csv_reader):
                yield id_, {
                    "total_annotation_count": row[1],
                    "hate_speech_annotations": row[2],
                    "offensive_language_annotations": row[3],
                    "neither_annotations": row[4],
                    "label": int(row[5]),
                    "tweet": str(row[6]),
                }
