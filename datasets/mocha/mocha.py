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
"""MOCHA: A Dataset for Training and Evaluating Generative Reading Comprehension Metrics"""


import json

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{Chen2020MOCHAAD,
    author={Anthony Chen and Gabriel Stanovsky and Sameer Singh and Matt Gardner},
    title={MOCHA: A Dataset for Training and Evaluating Generative Reading Comprehension Metrics},
    booktitle={EMNLP},
    year={2020}
}
"""

_DESCRIPTION = """\
Posing reading comprehension as a generation problem provides a great deal of flexibility, allowing for \
open-ended questions with few restrictions on possible answers. However, progress is impeded by existing \
generation metrics, which rely on token overlap and are agnostic to the nuances of reading comprehension. \
To address this, we introduce a benchmark for training and evaluating generative reading comprehension metrics: \
MOdeling Correctness with Human Annotations. MOCHA contains 40K human judgement scores on model outputs from \
6 diverse question answering datasets and an additional set of minimal pairs for evaluation. Using MOCHA, \
we train an evaluation metric: LERC, a Learned Evaluation metric for Reading Comprehension, to mimic human \
judgement scores.
"""

_HOMEPAGE = "https://allennlp.org/mocha"

_LICENSE = "https://creativecommons.org/licenses/by-sa/4.0/legalcode"

_URL = "https://github.com/anthonywchen/MOCHA/raw/main/data/mocha.tar.gz"

_MINIMAL_PAIRS_SPLIT = "minimal_pairs"

SPLIT_FILENAMES = {
    datasets.Split.TRAIN: "train.json",
    datasets.Split.VALIDATION: "dev.json",
    datasets.Split.TEST: "test_no_labels.json",
    _MINIMAL_PAIRS_SPLIT: "minimal_pairs.json",
}


class Mocha(datasets.GeneratorBasedBuilder):
    """MOCHA: A Dataset for Training and Evaluating Generative Reading Comprehension Metrics"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "constituent_dataset": datasets.Value("string"),
                    "id": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "reference": datasets.Value("string"),
                    "candidate": datasets.Value("string"),
                    "score": datasets.Value("float"),
                    "metadata": {
                        "scores": datasets.features.Sequence(datasets.Value("int32")),
                        "source": datasets.Value("string"),
                    },
                    # features for minimal pairs
                    "candidate2": datasets.Value("string"),
                    "score2": datasets.Value("float"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(_URL)

        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={
                    "filepath": "mocha/" + SPLIT_FILENAMES[split],
                    "split": split,
                    "files": dl_manager.iter_archive(archive),
                },
            )
            for split in SPLIT_FILENAMES
        ]

    def _generate_examples(self, filepath, split, files):
        """This function returns the examples in the raw (text) form."""
        for path, f in files:
            if path == filepath:
                mocha = json.load(f)
                for constituent_dataset, samples in mocha.items():
                    for id_, sample in samples.items():
                        sample["id"] = id_
                        sample["constituent_dataset"] = constituent_dataset

                        # Add default values
                        if split == _MINIMAL_PAIRS_SPLIT:
                            sample["candidate"] = sample["candidate1"]
                            sample["score"] = sample["score1"]
                            del sample["candidate1"], sample["score1"]
                            sample["metadata"] = {"scores": [], "source": ""}
                        else:
                            if "score" not in sample:
                                sample["score"] = -1.0
                                sample["metadata"]["scores"] = []
                            sample["candidate2"] = ""
                            sample["score2"] = -1.0

                        yield id_, sample
                break
