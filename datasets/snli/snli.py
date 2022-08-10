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
"""The Stanford Natural Language Inference (SNLI) Corpus."""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{snli:emnlp2015,
    Author = {Bowman, Samuel R. and Angeli, Gabor and Potts, Christopher, and Manning, Christopher D.},
    Booktitle = {Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
    Publisher = {Association for Computational Linguistics},
    Title = {A large annotated corpus for learning natural language inference},
    Year = {2015}
}
"""

_DESCRIPTION = """\
The SNLI corpus (version 1.0) is a collection of 570k human-written English
sentence pairs manually labeled for balanced classification with the labels
entailment, contradiction, and neutral, supporting the task of natural language
inference (NLI), also known as recognizing textual entailment (RTE).
"""

_DATA_URL = "https://nlp.stanford.edu/projects/snli/snli_1.0.zip"


class Snli(datasets.GeneratorBasedBuilder):
    """The Stanford Natural Language Inference (SNLI) Corpus."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of SNLI",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["entailment", "neutral", "contradiction"]),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://nlp.stanford.edu/projects/snli/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        data_dir = os.path.join(dl_dir, "snli_1.0")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": os.path.join(data_dir, "snli_1.0_test.txt")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": os.path.join(data_dir, "snli_1.0_dev.txt")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(data_dir, "snli_1.0_train.txt")}
            ),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for idx, row in enumerate(reader):
                label = -1 if row["gold_label"] == "-" else row["gold_label"]
                yield idx, {
                    "premise": row["sentence1"],
                    "hypothesis": row["sentence2"],
                    "label": label,
                }
