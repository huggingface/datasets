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
"""The Atommic Dataset"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """Maarten Sap, Ronan LeBras, Emily Allaway, Chandra Bhagavatula, Nicholas Lourie, Hannah Rashkin, Brendan Roof, Noah A. Smith & Yejin Choi (2019). ATOMIC: An Atlas of Machine Commonsense for If-Then Reasoning. AAAI
"""


_DESCRIPTION = """This dataset provides the template sentences and
relationships defined in the ATOMIC common sense dataset. There are
three splits - train, test, and dev.

From the authors.

Disclaimer/Content warning: the events in atomic have been
automatically extracted from blogs, stories and books written at
various times. The events might depict violent or problematic actions,
which we left in the corpus for the sake of learning the (probably
negative but still important) commonsense implications associated with
the events. We removed a small set of truly out-dated events, but
might have missed some so please email us (msap@cs.washington.edu) if
you have any concerns.

"""

_HOMEPAGE = "https://homes.cs.washington.edu/~msap/atomic/"

_LICENSE = "The Creative Commons Attribution 4.0 International License. https://creativecommons.org/licenses/by/4.0/"

_URLs = {"atomic": "https://homes.cs.washington.edu/~msap/atomic/data/atomic_data.tgz"}


class Atomic(datasets.GeneratorBasedBuilder):
    """Atomic Common Sense Dataset"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="atomic", version=VERSION, description="The Atomic dataset"),
    ]

    DEFAULT_CONFIG_NAME = "atomic"

    def _info(self):
        features = datasets.Features(
            {
                "event": datasets.Value("string"),
                "oEffect": datasets.Value("string"),
                "oReact": datasets.Value("string"),
                "oWant": datasets.Value("string"),
                "xAttr": datasets.Value("string"),
                "xEffect": datasets.Value("string"),
                "xIntent": datasets.Value("string"),
                "xNeed": datasets.Value("string"),
                "xReact": datasets.Value("string"),
                "xWant": datasets.Value("string"),
                "prefix": datasets.Value("string"),
                "split": datasets.Value("string"),
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
                    "filepath": os.path.join(data_dir, "v4_atomic_trn.csv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "v4_atomic_tst.csv"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "v4_atomic_dev.csv"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples from the Atomic dataset. """

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                row = row.strip()
                row = row.split(",")
                if row[0] == "entity":
                    continue
                yield id_, {
                    "event": row[0],
                    "oEffect": row[1],
                    "oReact": row[2],
                    "oWant": row[3],
                    "xAttr": row[4],
                    "xEffect": row[5],
                    "xIntent": row[6],
                    "xNeed": row[7],
                    "xReact": row[8],
                    "xWant": row[9],
                    "prefix": row[10],
                    "split": row[11],
                }
