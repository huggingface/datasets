# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3
"""The Multi-Genre NLI Corpus."""


import json
import os

import datasets


_CITATION = """\
@InProceedings{N18-1101,
  author = {Williams, Adina
            and Nangia, Nikita
            and Bowman, Samuel},
  title = {A Broad-Coverage Challenge Corpus for
           Sentence Understanding through Inference},
  booktitle = {Proceedings of the 2018 Conference of
               the North American Chapter of the
               Association for Computational Linguistics:
               Human Language Technologies, Volume 1 (Long
               Papers)},
  year = {2018},
  publisher = {Association for Computational Linguistics},
  pages = {1112--1122},
  location = {New Orleans, Louisiana},
  url = {http://aclweb.org/anthology/N18-1101}
}
"""

_DESCRIPTION = """\
The Multi-Genre Natural Language Inference (MultiNLI) corpus is a
crowd-sourced collection of 433k sentence pairs annotated with textual
entailment information. The corpus is modeled on the SNLI corpus, but differs in
that covers a range of genres of spoken and written text, and supports a
distinctive cross-genre generalization evaluation. The corpus served as the
basis for the shared task of the RepEval 2017 Workshop at EMNLP in Copenhagen.
"""


class MultiNli(datasets.GeneratorBasedBuilder):
    """MultiNLI: The Stanford Question Answering Dataset. Version 1.1."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "promptID": datasets.Value("int32"),
                    "pairID": datasets.Value("string"),
                    "premise": datasets.Value("string"),
                    "premise_binary_parse": datasets.Value("string"),  # parses in unlabeled binary-branching format
                    "premise_parse": datasets.Value("string"),  # sentence as parsed by the Stanford PCFG Parser 3.5.2
                    "hypothesis": datasets.Value("string"),
                    "hypothesis_binary_parse": datasets.Value("string"),  # parses in unlabeled binary-branching format
                    "hypothesis_parse": datasets.Value(
                        "string"
                    ),  # sentence as parsed by the Stanford PCFG Parser 3.5.2
                    "genre": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["entailment", "neutral", "contradiction"]),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://www.nyu.edu/projects/bowman/multinli/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        downloaded_dir = dl_manager.download_and_extract("https://cims.nyu.edu/~sbowman/multinli/multinli_1.0.zip")
        mnli_path = os.path.join(downloaded_dir, "multinli_1.0")
        train_path = os.path.join(mnli_path, "multinli_1.0_train.jsonl")
        matched_validation_path = os.path.join(mnli_path, "multinli_1.0_dev_matched.jsonl")
        mismatched_validation_path = os.path.join(mnli_path, "multinli_1.0_dev_mismatched.jsonl")

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name="validation_matched", gen_kwargs={"filepath": matched_validation_path}),
            datasets.SplitGenerator(name="validation_mismatched", gen_kwargs={"filepath": mismatched_validation_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate mnli examples"""

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if data["gold_label"] == "-":
                    continue
                yield id_, {
                    "promptID": data["promptID"],
                    "pairID": data["pairID"],
                    "premise": data["sentence1"],
                    "premise_binary_parse": data["sentence1_binary_parse"],
                    "premise_parse": data["sentence1_parse"],
                    "hypothesis": data["sentence2"],
                    "hypothesis_binary_parse": data["sentence2_binary_parse"],
                    "hypothesis_parse": data["sentence2_parse"],
                    "genre": data["genre"],
                    "label": data["gold_label"],
                }
