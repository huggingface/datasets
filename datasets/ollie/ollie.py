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
"""Ollie"""


import bz2

import datasets


_CITATION = """\
@inproceedings{ollie-emnlp12,
  author = {Mausam and Michael Schmitz and Robert Bart and Stephen Soderland and Oren Etzioni},
  title = {Open Language Learning for Information Extraction},
  booktitle = {Proceedings of Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning (EMNLP-CONLL)},
  year = {2012}
}"""


_DESCRIPTION = """The Ollie dataset includes two configs for the data
used to train the Ollie informatation extraction algorithm, for 18M
sentences and 3M sentences respectively.

This data is for academic use only. From the authors:

Ollie is a program that automatically identifies and extracts binary
relationships from English sentences. Ollie is designed for Web-scale
information extraction, where target relations are not specified in
advance.

Ollie is our second-generation information extraction system . Whereas
ReVerb operates on flat sequences of tokens, Ollie works with the
tree-like (graph with only small cycles) representation using
Stanford's compression of the dependencies. This allows Ollie to
capture expression that ReVerb misses, such as long-range relations.

Ollie also captures context that modifies a binary relation. Presently
Ollie handles attribution (He said/she believes) and enabling
conditions (if X then).

More information is available at the Ollie homepage:
https://knowitall.github.io/ollie/
"""


_LICENSE = """The University of Washington acamdemic license:
https://raw.githubusercontent.com/knowitall/ollie/master/LICENSE
"""

_URLs = {
    "ollie_lemmagrep": "http://knowitall.cs.washington.edu/ollie/data/lemmagrep.txt.bz2",
    "ollie_patterned": "http://knowitall.cs.washington.edu/ollie/data/patterned-all.txt.bz2",
}


class Ollie(datasets.GeneratorBasedBuilder):
    """Ollie dataset for knowledge bases and knowledge graphs and underlying sentences."""

    VERSION = datasets.Version("0.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="ollie_lemmagrep", description="The Ollie training data", version="1.1.0"),
        datasets.BuilderConfig(
            name="ollie_patterned", description="The Ollie data used in the Ollie paper.", version="1.1.0"
        ),
    ]

    DEFAULT_CONFIG_NAME = "ollie_lemmagrep"

    def _info(self):
        if self.config.name == "ollie_lemmagrep":
            features = datasets.Features(
                {
                    "arg1": datasets.Value("string"),
                    "arg2": datasets.Value("string"),
                    "rel": datasets.Value("string"),
                    "search_query": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "words": datasets.Value("string"),
                    "pos": datasets.Value("string"),
                    "chunk": datasets.Value("string"),
                    "sentence_cnt": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "rel": datasets.Value("string"),
                    "arg1": datasets.Value("string"),
                    "arg2": datasets.Value("string"),
                    "slot0": datasets.Value("string"),
                    "search_query": datasets.Value("string"),
                    "pattern": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "parse": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://knowitall.github.io/ollie/",
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
                    "filepath": data_dir,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples from the Ollie predicates and sentences."""

        with bz2.open(filepath, "rt") as f:
            id_ = -1
            if self.config.name == "ollie_lemmagrep":
                for row in f:
                    row = row.strip().split("\t")
                    id_ += 1
                    if len(row) == 8:
                        yield id_, {
                            "arg1": row[0].strip(),
                            "arg2": row[1].strip(),
                            "rel": "",
                            "search_query": row[2].strip(),
                            "sentence": row[3].strip(),
                            "words": row[4].strip(),
                            "pos": row[5].strip(),
                            "chunk": row[6].strip(),
                            "sentence_cnt": row[7].strip(),
                        }
                    else:
                        yield id_, {
                            "arg1": row[1].strip(),
                            "arg2": row[2].strip(),
                            "rel": row[0].strip(),
                            "search_query": row[3].strip(),
                            "sentence": row[4].strip(),
                            "words": row[5].strip(),
                            "pos": row[6].strip(),
                            "chunk": row[7].strip(),
                            "sentence_cnt": row[8].strip(),
                        }
            else:
                for row in f:
                    row = row.strip().split("\t")
                    id_ += 1
                    if len(row) == 7:
                        yield id_, {
                            "rel": row[0].strip(),
                            "arg1": row[1].strip(),
                            "arg2": row[2].strip(),
                            "slot0": "",
                            "search_query": row[3].strip(),
                            "pattern": row[4].strip(),
                            "sentence": row[5].strip(),
                            "parse": row[6].strip(),
                        }
                    else:
                        yield id_, {
                            "rel": row[0].strip(),
                            "arg1": row[1].strip(),
                            "arg2": row[2].strip(),
                            "slot0": row[7].strip(),
                            "search_query": row[3].strip(),
                            "pattern": row[4].strip(),
                            "sentence": row[5].strip(),
                            "parse": row[6].strip(),
                        }
