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
"""SAMSum dataset."""


import json

import py7zr

import datasets


_CITATION = """
@article{gliwa2019samsum,
  title={SAMSum Corpus: A Human-annotated Dialogue Dataset for Abstractive Summarization},
  author={Gliwa, Bogdan and Mochol, Iwona and Biesek, Maciej and Wawer, Aleksander},
  journal={arXiv preprint arXiv:1911.12237},
  year={2019}
}
"""

_DESCRIPTION = """
SAMSum Corpus contains over 16k chat dialogues with manually annotated
summaries.
There are two features:
  - dialogue: text of dialogue.
  - summary: human written summary of the dialogue.
  - id: id of a example.
"""

_HOMEPAGE = "https://arxiv.org/abs/1911.12237"

_LICENSE = "CC BY-NC-ND 4.0"

_URL = "https://huggingface.co/datasets/samsum/resolve/main/data/corpus.7z"


class Samsum(datasets.GeneratorBasedBuilder):
    """SAMSum Corpus dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="samsum"),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "dialogue": datasets.Value("string"),
                "summary": datasets.Value("string"),
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
        path = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": (path, "train.json"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": (path, "test.json"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": (path, "val.json"),
                    "split": "val",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        path, fname = filepath
        with open(path, "rb") as f:
            with py7zr.SevenZipFile(f, "r") as z:
                for name, bio in z.readall().items():
                    if name == fname:
                        data = json.load(bio)
        for example in data:
            yield example["id"], example
