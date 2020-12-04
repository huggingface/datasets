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
"""The Rationalized English-French Semantic Divergences (REFreSD) dataset."""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_CITATION = """\
@inproceedings{briakou-carpuat-2020-detecting,
    title = "Detecting Fine-Grained Cross-Lingual Semantic Divergences without Supervision by Learning to Rank",
    author = "Briakou, Eleftheria and Carpuat, Marine",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.121",
    pages = "1563--1580",
}
"""

_DESCRIPTION = """\
The Rationalized English-French Semantic Divergences (REFreSD) dataset consists of 1,039 
English-French sentence-pairs annotated with sentence-level divergence judgments and token-level 
rationales. For any questions, write to ebriakou@cs.umd.edu.
"""

_HOMEPAGE = "https://github.com/Elbria/xling-SemDiv/tree/master/REFreSD"

_LICENSE = ""

_URL = "https://raw.githubusercontent.com/Elbria/xling-SemDiv/master/REFreSD/REFreSD_rationale"


class Refresd(datasets.GeneratorBasedBuilder):
    """The Rationalized English-French Semantic Divergences (REFreSD) dataset."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "sentence_en": datasets.Value("string"),
                "sentence_fr": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["divergent", "equivalent"]),
                "all_labels": datasets.features.ClassLabel(
                    names=["unrelated", "some_meaning_difference", "no_meaning_difference"]
                ),
                "rationale_en": datasets.Value(
                    "string"
                ),  # datasets.features.Sequence(datasets.Value(dtype='Int8Value')),
                "rationale_fr": datasets.Value(
                    "string"
                ),  # datasets.features.Sequence(datasets.Value(dtype='Int8Value')),
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
        my_urls = _URL
        data_file_path = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_file_path,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            change_labels = {
                "#english_sentence": "sentence_en",
                "#french_sentence": "sentence_fr",
                "#binary_label": "label",
                "#3_labels": "all_labels",
                "#english_rational": "rationale_en",
                "#french_rationale": "rationale_fr",
            }
            for idx, row in enumerate(reader):
                yield idx, {change_labels[k]: row[k] for k in row.keys()}
