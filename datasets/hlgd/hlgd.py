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
"""
HLGD is a binary classification dataset consisting of 20,056 labeled news headlines pairs indicating
whether the two headlines describe the same underlying world event or not.
"""

import json
import os

import datasets


_CITATION = """\
@inproceedings{Laban2021NewsHG,
  title={News Headline Grouping as a Challenging NLU Task},
  author={Philippe Laban and Lucas Bandarkar},
  booktitle={NAACL 2021},
  publisher = {Association for Computational Linguistics},
  year={2021}
}
"""

_DESCRIPTION = """\
HLGD is a binary classification dataset consisting of 20,056 labeled news headlines pairs indicating
whether the two headlines describe the same underlying world event or not.
"""

_HOMEPAGE = "https://github.com/tingofurro/headline_grouping"
_LICENSE = "Apache-2.0 License"
_DOWNLOAD_URL = "https://github.com/tingofurro/headline_grouping/releases/download/0.1/hlgd_classification_0.1.zip"


class HLGD(datasets.GeneratorBasedBuilder):
    """Headline Grouping Dataset."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "timeline_id": datasets.features.ClassLabel(names=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                "headline_a": datasets.Value("string"),
                "headline_b": datasets.Value("string"),
                "date_a": datasets.Value("string"),
                "date_b": datasets.Value("string"),
                "url_a": datasets.Value("string"),
                "url_b": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["same_event", "different_event"]),
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
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive

        data_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.json"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "test.json"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.json"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        with open(filepath, encoding="utf-8") as f:
            dataset_split = json.load(f)

        for id_, row in enumerate(dataset_split):
            yield id_, {
                "timeline_id": row["timeline_id"],
                "headline_a": row["headline_a"],
                "headline_b": row["headline_b"],
                "date_a": row["date_a"],
                "date_b": row["date_b"],
                "url_a": row["url_a"],
                "url_b": row["url_b"],
                "label": row["label"],
            }
