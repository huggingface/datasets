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


import json

import datasets


_CITATION = """@article{Sap2019ATOMICAA,
  title={ATOMIC: An Atlas of Machine Commonsense for If-Then Reasoning},
  author={Maarten Sap and Ronan Le Bras and Emily Allaway and Chandra Bhagavatula and Nicholas Lourie and Hannah Rashkin and Brendan Roof and Noah A. Smith and Yejin Choi},
  journal={ArXiv},
  year={2019},
  volume={abs/1811.00146}
}
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

    def _info(self):
        features = datasets.Features(
            {
                "event": datasets.Value("string"),
                "oEffect": datasets.Sequence(datasets.Value("string")),
                "oReact": datasets.Sequence(datasets.Value("string")),
                "oWant": datasets.Sequence(datasets.Value("string")),
                "xAttr": datasets.Sequence(datasets.Value("string")),
                "xEffect": datasets.Sequence(datasets.Value("string")),
                "xIntent": datasets.Sequence(datasets.Value("string")),
                "xNeed": datasets.Sequence(datasets.Value("string")),
                "xReact": datasets.Sequence(datasets.Value("string")),
                "xWant": datasets.Sequence(datasets.Value("string")),
                "prefix": datasets.Sequence(datasets.Value("string")),
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
        archive = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": "v4_atomic_trn.csv",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": "v4_atomic_tst.csv",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": "v4_atomic_dev.csv",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, files):
        """Yields examples from the Atomic dataset."""

        for path, f in files:
            if path == filepath:
                for id_, row in enumerate(f):
                    row = row.decode("utf-8")
                    if row.startswith("event"):
                        continue
                    row = row.replace('"[', "[").replace(']"', "]")
                    sent, rest = row.split("[", 1)
                    sent = sent.strip(', "')
                    rest = "[" + rest
                    rest = rest.replace('""', '"').replace('\\\\"]', '"]')
                    rest = rest.split(",")
                    rest[-1] = '"' + rest[-1].strip() + '"'
                    rest = ",".join(rest)
                    row = '["' + sent + '",' + rest + "]"
                    row = json.loads(row)
                    yield id_, {
                        "event": str(row[0]),
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
                        "split": str(row[11]),
                    }
                break
