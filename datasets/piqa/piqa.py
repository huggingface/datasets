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
"""PIQA dataset."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@inproceedings{Bisk2020,
  author = {Yonatan Bisk and Rowan Zellers and
            Ronan Le Bras and Jianfeng Gao
            and Yejin Choi},
  title = {PIQA: Reasoning about Physical Commonsense in
           Natural Language},
  booktitle = {Thirty-Fourth AAAI Conference on
               Artificial Intelligence},
  year = {2020},
}
"""

_DESCRIPTION = """\
To apply eyeshadow without a brush, should I use a cotton swab or a toothpick?
Questions requiring this kind of physical commonsense pose a challenge to state-of-the-art
natural language understanding systems. The PIQA dataset introduces the task of physical commonsense reasoning
and a corresponding benchmark dataset Physical Interaction: Question Answering or PIQA.

Physical commonsense knowledge is a major challenge on the road to true AI-completeness,
including robots that interact with the world and understand natural language.

PIQA focuses on everyday situations with a preference for atypical solutions.
The dataset is inspired by instructables.com, which provides users with instructions on how to build, craft,
bake, or manipulate objects using everyday materials.

The underlying task is formualted as multiple choice question answering:
given a question `q` and two possible solutions `s1`, `s2`, a model or
a human must choose the most appropriate solution, of which exactly one is correct.
The dataset is further cleaned of basic artifacts using the AFLite algorithm which is an improvement of
adversarial filtering. The dataset contains 16,000 examples for training, 2,000 for development and 3,000 for testing.
"""

_URLs = {
    "train-dev": "https://storage.googleapis.com/ai2-mosaic/public/physicaliqa/physicaliqa-train-dev.zip",
    "test": "https://yonatanbisk.com/piqa/data/tests.jsonl",
}


class Piqa(datasets.GeneratorBasedBuilder):
    """PIQA dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            description="Plain text",
            version=VERSION,
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "goal": datasets.Value("string"),
                    "sol1": datasets.Value("string"),
                    "sol2": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["0", "1"]),
                }
            ),
            supervised_keys=None,
            homepage="https://yonatanbisk.com/piqa/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "input_filepath": os.path.join(data_dir["train-dev"], "physicaliqa-train-dev", "train.jsonl"),
                    "label_filepath": os.path.join(data_dir["train-dev"], "physicaliqa-train-dev", "train-labels.lst"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "input_filepath": data_dir["test"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "input_filepath": os.path.join(data_dir["train-dev"], "physicaliqa-train-dev", "dev.jsonl"),
                    "label_filepath": os.path.join(data_dir["train-dev"], "physicaliqa-train-dev", "dev-labels.lst"),
                },
            ),
        ]

    def _generate_examples(self, input_filepath, label_filepath=None):
        """ Yields examples. """
        with open(input_filepath, encoding="utf-8") as input_file:
            inputs = input_file.read().splitlines()

            if label_filepath is not None:
                with open(label_filepath, encoding="utf-8") as label_file:
                    labels = label_file.read().splitlines()
            else:
                # Labels are not available for the test set.
                # Filling the `label` column with -1 by default
                labels = [-1] * len(inputs)

            for idx, (row, lab) in enumerate(zip(inputs, labels)):
                data = json.loads(row)
                goal = data["goal"]
                sol1 = data["sol1"]
                sol2 = data["sol2"]
                yield idx, {"goal": goal, "sol1": sol1, "sol2": sol2, "label": lab}
