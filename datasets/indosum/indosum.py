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
"""Indosum: A New Benchmark Dataset for Indonesian Text Summarization."""

from __future__ import absolute_import, division, print_function

import logging
import os

import datasets
from datasets import load_dataset


_CITATION = """\
@inproceedings{kurniawan2018,
  place={Bandung, Indonesia},
  title={IndoSum: A New Benchmark Dataset for Indonesian Text Summarization},
  url={https://ieeexplore.ieee.org/document/8629109},
  DOI={10.1109/IALP.2018.8629109},
  booktitle={2018 International Conference on Asian Language Processing (IALP)},
  publisher={IEEE},
  author={Kurniawan, Kemal and Louvan, Samuel},
  year={2018},
  month={Nov},
  pages={215-220}
}
"""

_DESCRIPTION = """
Indosum contains Indonesian extractive text summarization dataset, \
roughly 19K tokenized news articles from (formerly) Shortir.com, a news aggregator site.

This dataset contains pre-tokenized sentences for the paragraphs and summary text, \
the authors didn't provide the raw sentences.
"""

_HOMEPAGE = "https://github.com/kata-ai/indosum"

_LICENSE = "CC BY-SA 4.0"

_URL = "https://drive.google.com/uc?export=download&id=1OgYbPfXFAv3TbwP1Qcwt_CC9cVWSJaco"


class Indosum(datasets.GeneratorBasedBuilder):
    """Indosum: A New Benchmark Dataset for Indonesian Text Summarization"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "paragraphs": datasets.Sequence(datasets.Sequence(datasets.Sequence(datasets.Value("string")))),
                "summary": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
                "gold_labels": datasets.Sequence(datasets.Sequence(datasets.Value("bool"))),
                "category": datasets.features.ClassLabel(
                    names=["hiburan", "inspirasi", "olahraga", "showbiz", "tajuk utama", "teknologi"]
                ),
                "source": datasets.Value("string"),
                "source_url": datasets.Value("string"),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URL
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": [
                        os.path.join(data_dir, "indosum", "train.01.jsonl"),
                        os.path.join(data_dir, "indosum", "train.02.jsonl"),
                        os.path.join(data_dir, "indosum", "train.03.jsonl"),
                        os.path.join(data_dir, "indosum", "train.04.jsonl"),
                        os.path.join(data_dir, "indosum", "train.05.jsonl"),
                    ],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": [
                        os.path.join(data_dir, "indosum", "test.01.jsonl"),
                        os.path.join(data_dir, "indosum", "test.02.jsonl"),
                        os.path.join(data_dir, "indosum", "test.03.jsonl"),
                        os.path.join(data_dir, "indosum", "test.04.jsonl"),
                        os.path.join(data_dir, "indosum", "test.05.jsonl"),
                    ],
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": [
                        os.path.join(data_dir, "indosum", "dev.01.jsonl"),
                        os.path.join(data_dir, "indosum", "dev.02.jsonl"),
                        os.path.join(data_dir, "indosum", "dev.03.jsonl"),
                        os.path.join(data_dir, "indosum", "dev.04.jsonl"),
                        os.path.join(data_dir, "indosum", "dev.05.jsonl"),
                    ],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepaths, split):
        """ Yields examples. """

        logging.info("⏳ Generating examples from = %s", filepaths)
        dataset = load_dataset("json", data_files=filepaths)

        for _id, data in enumerate(dataset["train"]):
            yield _id, {
                "id": data["id"],
                "paragraphs": data["paragraphs"],
                "summary": data["summary"],
                "gold_labels": data["gold_labels"],
                "category": data["category"],
                "source": data["source"],
                "source_url": data["source_url"],
            }
