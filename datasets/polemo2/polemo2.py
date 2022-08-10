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
"""PolEmo2.0 IN and OUT"""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{kocon-etal-2019-multi,
title = "Multi-Level Sentiment Analysis of {P}ol{E}mo 2.0: Extended Corpus of Multi-Domain Consumer Reviews",
author = "Koco{\'n}, Jan and
Milkowski, Piotr and
Za{\'s}ko-Zieli{\'n}ska, Monika",
booktitle = "Proceedings of the 23rd Conference on Computational Natural Language Learning (CoNLL)",
month = nov,
year = "2019",
address = "Hong Kong, China",
publisher = "Association for Computational Linguistics",
url = "https://www.aclweb.org/anthology/K19-1092",
doi = "10.18653/v1/K19-1092",
pages = "980--991",
}
"""

_DESCRIPTION = """\
The PolEmo2.0 is a set of online reviews from medicine and hotels domains. The task is to predict the sentiment of a review. There are two separate test sets, to allow for in-domain (medicine and hotels) as well as out-of-domain (products and university) validation.
"""

_HOMEPAGE = "https://clarin-pl.eu/dspace/handle/11321/710"

_LICENSE = "CC BY-NC-SA 4.0"

_URLs = {
    "in": "https://klejbenchmark.com/static/data/klej_polemo2.0-in.zip",
    "out": "https://klejbenchmark.com/static/data/klej_polemo2.0-out.zip",
}


class Polemo2(datasets.GeneratorBasedBuilder):
    """PolEmo2.0"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="in",
            version=VERSION,
            description="The PolEmo2.0 is a set of online reviews from medicine and hotels domains. The task is to predict the sentiment of a review. There are two separate test sets, to allow for in-domain (medicine and hotels) as well as out-of-domain (products and university) validation.",
        ),
        datasets.BuilderConfig(
            name="out",
            version=VERSION,
            description="The PolEmo2.0 is a set of online reviews from medicine and hotels domains. The task is to predict the sentiment of a review. There are two separate test sets, to allow for in-domain (medicine and hotels) as well as out-of-domain (products and university) validation.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "in"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "target": datasets.ClassLabel(
                        names=[
                            "__label__meta_amb",
                            "__label__meta_minus_m",
                            "__label__meta_plus_m",
                            "__label__meta_zero",
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
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for id_, row in enumerate(reader):
                yield id_, {
                    "sentence": row["sentence"],
                    "target": -1 if split == "test" else row["target"],
                }
