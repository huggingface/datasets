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

ROOT_URL = "http://storage.googleapis.com/tfds-data/downloads/multi_nli/multinli_1.0.zip"


class MultiNLIMismatchConfig(datasets.BuilderConfig):
    """BuilderConfig for MultiNLI Mismatch."""

    def __init__(self, **kwargs):
        """BuilderConfig for MultiNLI Mismatch.

        Args:

          **kwargs: keyword arguments forwarded to super.
        """
        super(MultiNLIMismatchConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class MultiNliMismatch(datasets.GeneratorBasedBuilder):
    """MultiNLI: The Stanford Question Answering Dataset. Version 1.1."""

    BUILDER_CONFIGS = [
        MultiNLIMismatchConfig(
            name="plain_text",
            description="Plain text",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "label": datasets.Value("string"),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://www.nyu.edu/projects/bowman/multinli/",
            citation=_CITATION,
        )

    def _vocab_text_gen(self, filepath):
        for _, ex in self._generate_examples(filepath):
            yield " ".join([ex["premise"], ex["hypothesis"], ex["label"]])

    def _split_generators(self, dl_manager):

        downloaded_dir = dl_manager.download_and_extract(ROOT_URL)
        mnli_path = os.path.join(downloaded_dir, "multinli_1.0")
        train_path = os.path.join(mnli_path, "multinli_1.0_train.txt")

        validation_path = os.path.join(mnli_path, "multinli_1.0_dev_mismatched.txt")

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": validation_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate mnli mismatch examples.

        Args:
          filepath: a string

        Yields:
          dictionaries containing "premise", "hypothesis" and "label" strings
        """
        for idx, line in enumerate(open(filepath, "rb")):
            if idx == 0:
                continue
            line = line.strip().decode("utf-8")
            split_line = line.split("\t")
            yield idx, {"premise": split_line[5], "hypothesis": split_line[6], "label": split_line[0]}
