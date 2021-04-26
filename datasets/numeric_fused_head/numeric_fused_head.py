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
"""NFH: Numeric Fused-Heads."""


import csv
import json

import datasets


_CITATION = """\
@article{elazar_head,
    author = {Elazar, Yanai and Goldberg, Yoav},
    title = {Where’s My Head? Definition, Data Set, and Models for Numeric Fused-Head Identification and Resolution},
    journal = {Transactions of the Association for Computational Linguistics},
    volume = {7},
    number = {},
    pages = {519-535},
    year = {2019},
    doi = {10.1162/tacl\\_a\\_00280},
    URL = {https://doi.org/10.1162/tacl_a_00280},
}
"""

_DESCRIPTION = """\
Fused Head constructions are noun phrases in which the head noun is \
missing and is said to be "fused" with its dependent modifier. This \
missing information is implicit and is important for sentence understanding.\
The missing heads are easily filled in by humans,  but pose a challenge for \
computational models.

For example, in the sentence: "I bought 5 apples but got only 4.", 4 is a \
Fused-Head, and the missing head is apples, which appear earlier in the sentence.

This is a crowd-sourced dataset of 10k numerical fused head examples (1M tokens).
"""

_HOMEPAGE = "https://nlp.biu.ac.il/~lazary/fh/"

_LICENSE = "MIT"

_URLs = {
    "identification": {
        "train": "https://raw.githubusercontent.com/yanaiela/num_fh/master/data/identification/processed/train.tsv",
        "test": "https://raw.githubusercontent.com/yanaiela/num_fh/master/data/identification/processed/test.tsv",
        "dev": "https://raw.githubusercontent.com/yanaiela/num_fh/master/data/identification/processed/dev.tsv",
    },
    "resolution": {
        "train": "https://raw.githubusercontent.com/yanaiela/num_fh/master/data/resolution/processed/nfh_train.jsonl",
        "test": "https://raw.githubusercontent.com/yanaiela/num_fh/master/data/resolution/processed/nfh_test.jsonl",
        "dev": "https://raw.githubusercontent.com/yanaiela/num_fh/master/data/resolution/processed/nfh_dev.jsonl",
    },
}


class NumericFusedHead(datasets.GeneratorBasedBuilder):
    """NFH: Numeric Fused-Heads"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="identification", description="Identify NFH anchors in a sentence"),
        datasets.BuilderConfig(name="resolution", description="Identify the head for the numeric anchor"),
    ]

    def _info(self):
        if self.config.name == "identification":
            features = datasets.Features(
                {
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "start_index": datasets.Value("int32"),
                    "end_index": datasets.Value("int32"),
                    "label": datasets.features.ClassLabel(names=["neg", "pos"]),
                }
            )
        else:
            features = datasets.Features(
                {
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "line_indices": datasets.Sequence(datasets.Value("int32")),
                    "head": datasets.Sequence(datasets.Value("string")),
                    "speakers": datasets.Sequence(datasets.Value("string")),
                    "anchors_indices": datasets.Sequence(datasets.Value("int32")),
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
        data_files = dl_manager.download_and_extract(_URLs[self.config.name])
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": data_files["test"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": data_files["dev"]}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            if self.config.name == "identification":
                r = csv.DictReader(f, delimiter="\t")
                for id_, row in enumerate(r):
                    data = {
                        "tokens": row["text"].split("_SEP_"),
                        "start_index": row["ind_s"],
                        "end_index": row["ind_e"],
                        "label": "neg" if row["y"] == "0" else "pos",
                    }
                    yield id_, data
            else:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    yield id_, {
                        "tokens": data["tokens"],
                        "line_indices": data["line_indices"],
                        "head": [str(s) for s in data["head"]],
                        "speakers": [str(s) for s in data["speakers"]],
                        "anchors_indices": data["anchors_indices"],
                    }
