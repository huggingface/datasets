# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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

"""The NumerSense Dataset"""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_CITATION = """\
@inproceedings{lin2020numersense,
    title={Birds have four legs?! NumerSense: Probing Numerical Commonsense Knowledge of Pre-trained Language Models},
    author={Bill Yuchen Lin and Seyeon Lee and Rahul Khanna and Xiang Ren},
    booktitle={Proceedings of EMNLP},
    year={2020},
    note={to appear}
}
"""

_DESCRIPTION = """\
NumerSense is a new numerical commonsense reasoning probing task, with a diagnostic dataset consisting of 3,145 masked-word-prediction probes.

We propose to study whether numerical commonsense knowledge can be induced from pre-trained language models like BERT, and to what extent this access to knowledge robust against adversarial examples is. We hope this will be beneficial for tasks such as knowledge base completion and open-domain question answering.
"""

_HOMEPAGE_URL = "https://inklab.usc.edu/NumerSense/"
_BASE_DOWNLOAD_URL = "https://raw.githubusercontent.com/INK-USC/NumerSense/main/data/"


class NumerSense(datasets.GeneratorBasedBuilder):
    """The Multilingual Amazon Reviews Corpus"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "target": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_url = _BASE_DOWNLOAD_URL + "train.masked.tsv"
        test_core_url = _BASE_DOWNLOAD_URL + "test.core.masked.txt"
        test_all_url = _BASE_DOWNLOAD_URL + "test.all.masked.txt"

        train_path = dl_manager.download_and_extract(train_url)
        test_core_path = dl_manager.download_and_extract(test_core_url)
        test_all_path = dl_manager.download_and_extract(test_all_url)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"file_path": train_path, "is_test": False}),
            datasets.SplitGenerator(name="test_core", gen_kwargs={"file_path": test_core_path, "is_test": True}),
            datasets.SplitGenerator(name="test_all", gen_kwargs={"file_path": test_all_path, "is_test": True}),
        ]

    def _generate_examples(self, file_path, is_test):
        with open(file_path, "r", encoding="utf-8") as f:
            if is_test:
                for i, sentence in enumerate(f):
                    yield i, {"sentence": sentence.rstrip(), "target": ""}
            else:
                reader = csv.DictReader(f, delimiter="\t", fieldnames=["sentence", "target"])
                for i, row in enumerate(reader):
                    yield i, row
