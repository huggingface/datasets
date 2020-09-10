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
"""The Definite Pronoun Resolution Dataset."""

from __future__ import absolute_import, division, print_function

import datasets


_CITATION = """\
@inproceedings{rahman2012resolving,
  title={Resolving complex cases of definite pronouns: the winograd schema challenge},
  author={Rahman, Altaf and Ng, Vincent},
  booktitle={Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning},
  pages={777--789},
  year={2012},
  organization={Association for Computational Linguistics}
}"""

_DESCRIPTION = """\
Composed by 30 students from one of the author's undergraduate classes. These
sentence pairs cover topics ranging from real events (e.g., Iran's plan to
attack the Saudi ambassador to the U.S.) to events/characters in movies (e.g.,
Batman) and purely imaginary situations, largely reflecting the pop culture as
perceived by the American kids born in the early 90s. Each annotated example
spans four lines: the first line contains the sentence, the second line contains
the target pronoun, the third line contains the two candidate antecedents, and
the fourth line contains the correct antecedent. If the target pronoun appears
more than once in the sentence, its first occurrence is the one to be resolved.
"""

_DATA_URL_PATTERN = "http://www.hlt.utdallas.edu/~vince/data/emnlp12/{}.c.txt"


class DefinitePronounResolution(datasets.GeneratorBasedBuilder):
    """The Definite Pronoun Resolution Dataset."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of the Definite Pronoun Resolution Dataset.",  # pylint: disable=line-too-long
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "pronoun": datasets.Value("string"),
                    "candidates": datasets.features.Sequence(datasets.Value("string"), length=2),
                    "label": datasets.features.ClassLabel(num_classes=2),
                }
            ),
            supervised_keys=("sentence", "label"),
            homepage="http://www.hlt.utdallas.edu/~vince/data/emnlp12/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        files = dl_manager.download_and_extract(
            {
                "train": _DATA_URL_PATTERN.format("train"),
                "test": _DATA_URL_PATTERN.format("test"),
            }
        )
        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": files["test"]}),
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": files["train"]}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            line_num = -1
            while True:
                line_num += 1
                sentence = f.readline().strip()
                pronoun = f.readline().strip()
                candidates = [c.strip() for c in f.readline().strip().split(",")]
                correct = f.readline().strip()
                f.readline()
                if not sentence:
                    break
                yield line_num, {
                    "sentence": sentence,
                    "pronoun": pronoun,
                    "candidates": candidates,
                    "label": candidates.index(correct),
                }
