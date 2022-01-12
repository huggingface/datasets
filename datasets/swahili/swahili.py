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
"""A Swahili dataset developed specifically for language modelling task.

The dataset contains 28,000 unique words with 6.84 M, 970k, and 2 M words for the train, valid and
test partitions respectively which represent the ratio 80:10:10.
The entire dataset is lowercased, has no punctuation marks and,
the start and end of sentence markers have been incorporated to facilitate easy tokenization during language modelling."""


import os

import datasets


_CITATION = """\
@InProceedings{huggingface:dataset,
title = Language modeling data for Swahili (Version 1),
authors={Shivachi Casper Shikali, & Mokhosi Refuoe.
},
year={2019},
link = http://doi.org/10.5281/zenodo.3553423
}
"""

_DESCRIPTION = """\
The Swahili dataset developed specifically for language modeling task.
The dataset contains 28,000 unique words with 6.84M, 970k, and 2M words for the train,
valid and test partitions respectively which represent the ratio 80:10:10.
The entire dataset is lowercased, has no punctuation marks and,
the start and end of sentence markers have been incorporated to facilitate easy tokenization during language modeling.
"""

_HOMEPAGE = "https://zenodo.org/record/3553423"

_LICENSE = "Attribution 4.0 International"

_URLs = "https://zenodo.org/record/3553423/files/Swahili%20data.zip?download=1"


class Swahili(datasets.GeneratorBasedBuilder):
    """The Swahili dataset developed specifically for language modeling task."""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="swahili", version=VERSION, description="Swahili data for language modeling"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "Swahili data/train.txt"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "Swahili data/test.txt"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "Swahili data/valid.txt"),
                    "split": "valid",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        _id = 0
        with open(filepath, mode="r", encoding="utf-8") as f:
            for line in f:
                yield _id, {"text": line.strip()},
                _id += 1
