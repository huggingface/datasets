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
"""cdsc-e & cdsc-r"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@inproceedings{wroblewska2017polish,
title={Polish evaluation dataset for compositional distributional semantics models},
author={Wr{\'o}blewska, Alina and Krasnowska-Kiera{\'s}, Katarzyna},
booktitle={Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
pages={784--792},
year={2017}
}
"""

_DESCRIPTION = """\
Polish CDSCorpus consists of 10K Polish sentence pairs which are human-annotated for semantic relatedness and entailment. The dataset may be used for the evaluation of compositional distributional semantics models of Polish. The dataset was presented at ACL 2017. Please refer to the Wróblewska and Krasnowska-Kieraś (2017) for a detailed description of the resource.
"""

_HOMEPAGE = "http://zil.ipipan.waw.pl/Scwad/CDSCorpus"

_LICENSE = "CC BY-NC-SA 4.0"

_URLs = {
    "cdsc-e": "https://klejbenchmark.com/static/data/klej_cdsc-e.zip",
    "cdsc-r": "https://klejbenchmark.com/static/data/klej_cdsc-r.zip",
}


class Cdsc(datasets.GeneratorBasedBuilder):
    """CDSCorpus"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="cdsc-e",
            version=VERSION,
            description="Polish CDSCorpus consists of 10K Polish sentence pairs which are human-annotated for semantic entailment.",
        ),
        datasets.BuilderConfig(
            name="cdsc-r",
            version=VERSION,
            description="Polish CDSCorpus consists of 10K Polish sentence pairs which are human-annotated for semantic relatedness.",
        ),
    ]

    def _info(self):
        if self.config.name == "cdsc-e":
            features = datasets.Features(
                {
                    "pair_ID": datasets.Value("int32"),
                    "sentence_A": datasets.Value("string"),
                    "sentence_B": datasets.Value("string"),
                    "entailment_judgment": datasets.ClassLabel(
                        names=[
                            "NEUTRAL",
                            "CONTRADICTION",
                            "ENTAILMENT",
                        ]
                    ),
                }
            )
        elif self.config.name == "cdsc-r":
            features = datasets.Features(
                {
                    "pair_ID": datasets.Value("int32"),
                    "sentence_A": datasets.Value("string"),
                    "sentence_B": datasets.Value("string"),
                    "relatedness_score": datasets.Value("float"),
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
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
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
                if self.config.name == "cdsc-e":
                    yield id_, {
                        "pair_ID": row["pair_ID"],
                        "sentence_A": row["sentence_A"],
                        "sentence_B": row["sentence_B"],
                        "entailment_judgment": -1 if split == "test" else row["entailment_judgment"],
                    }
                elif self.config.name == "cdsc-r":
                    yield id_, {
                        "pair_ID": row["pair_ID"],
                        "sentence_A": row["sentence_A"],
                        "sentence_B": row["sentence_B"],
                        "relatedness_score": "-1" if split == "test" else row["relatedness_score"],
                    }
