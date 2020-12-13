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

from __future__ import absolute_import, division, print_function

import os

import pandas as pd

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

_DESCRIPTION = "Technologies for abusive language detection are being developed and applied with little consideration of their potential biases. We examine racial bias in five different sets of Twitter data annotated for hate speech and abusive language. We train classifiers on these datasets and compare the predictions of these classifiers on tweets written in African-American English with those written in Standard American English. The results show evidence of systematic racial bias in all datasets, as classifiers trained on them tend to predict that tweets written in African-American English are abusive at substantially higher rates. If these abusive language detection systems are used in the field they will therefore have a disproportionate negative impact on African-American social media users. Consequently, these systems may discriminate against the groups who are often the targets of the abuse we are trying to detect."

_HOMEPAGE = "https://arxiv.org/abs/1905.12516"

_LICENSE = "https://github.com/t-davidson/hate-speech-and-offensive-language/blob/master/LICENSE"

_URLs = "https://github.com/t-davidson/hate-speech-and-offensive-language/raw/master/data/labeled_data.csv"


class HateOffensive(datasets.GeneratorBasedBuilder):
    """Automated Hate Speech Detection and the Problem of Offensive Language """

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "count": datasets.Value("int32"),
                "hate_speech": datasets.Value("int32"),
                "offensive_language": datasets.Value("int32"),
                "neither": datasets.Value("int32"),
                "class": datasets.ClassLabel(
                    names=["0", "1", "2"]
                ),  # 0 - hate speech 1 - offensive language 2 - neither
                "tweet": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir)},
            )
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        f = pd.read_csv(filepath)
        for id_, row in f.iterrows():
            yield id_, {
                "count": row["count"],
                "hate_speech": row["hate_speech"],
                "offensive_language": row["offensive_language"],
                "neither": row["neither"],
                "class": row["class"],
                "tweet": str(row["tweet"]),
            }
