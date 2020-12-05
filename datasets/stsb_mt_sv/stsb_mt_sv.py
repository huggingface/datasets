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

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_DOWNLOAD_URL = "https://raw.githubusercontent.com/timpal0l/sts-benchmark-swedish/master/data/stsb-mt-sv.zip"
_TRAIN_FILE = "train-sv.tsv"
_VAL_FILE = "dev-sv.tsv"
_TEST_FILE = "test-sv.tsv"

_CITATION = """\
@article{isbister2020not,
  title={Why Not Simply Translate? A First Swedish Evaluation Benchmark for Semantic Similarity},
  author={Isbister, Tim and Sahlgren, Magnus},
  journal={arXiv preprint arXiv:2009.03116},
  year={2020}
}
"""

_DESCRIPTION = "Machine translated Swedish version of the original STS-B (http://ixa2.si.ehu.eus/stswiki)"


class StsbMtSv(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of the Swedish Machine Translated STS-B",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence1": datasets.Value("string"),
                    "sentence2": datasets.Value("string"),
                    "score": datasets.Value("float"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/timpal0l/sts-benchmark-swedish",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(dl_dir, _TEST_FILE)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(dl_dir, _VAL_FILE)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(dl_dir, _TRAIN_FILE)},
            ),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for idx, row in enumerate(reader):
                yield idx, {
                    "sentence1": row["sentence1"],
                    "sentence2": row["sentence2"],
                    "score": row["score"],
                }
