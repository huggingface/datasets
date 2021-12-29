# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""QuALITY dataset."""


import csv
import json
import os

import datasets


_CITATION = """\
@article{pang2021quality,
    title        = {{QuALITY}: Question Answering with Long Input Texts, Yes!},
    author       = {Pang, Richard Yuanzhe and Parrish, Alicia and Joshi, Nitish and Nangia, Nikita and Phang, Jason and Chen, Angelica and Padmakumar, Vishakh and Ma, Johnny and Thompson, Jana and He, He and Bowman, Samuel R.},
    year         = 2021,
    journal      = {arXiv preprint arXiv:2112.08608}
}
"""

_DESCRIPTION = """\
QuALITY is a multiple-choice QA dataset with English context passages with an average 5000 tokens.
"""

_HOMEPAGE = """\
https://github.com/nyu-mll/quality
"""

_LICENSE = ""

_URL = "https://github.com/nyu-mll/quality/raw/main/data/QuALITY.v0.9.zip"


class QualityDataset(datasets.GeneratorBasedBuilder):
    """QuALITY dataset"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "article_id": datasets.Value("string"),
                    "set_unique_id": datasets.Value("string"),
                    "batch_num": datasets.Value("string"),
                    "writer_id": datasets.Value("string"),
                    "source": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "year": datasets.Value("string"),
                    "author": datasets.Value("string"),
                    "topic": datasets.Value("string"),
                    "article": datasets.Value("string"),
                    "questions": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "license": datasets.Value("string"),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "QuALITY.v0.9.htmlstripped.train"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "QuALITY.v0.9.htmlstripped.test"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "QuALITY.v0.9.htmlstripped.dev"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                yield key, data
