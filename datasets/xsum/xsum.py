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
"""XSum dataset."""

from __future__ import absolute_import, division, print_function

import os
import json

import datasets


_CITATION = """
@article{Narayan2018DontGM,
  title={Don't Give Me the Details, Just the Summary! Topic-Aware Convolutional Neural Networks for Extreme Summarization},
  author={Shashi Narayan and Shay B. Cohen and Mirella Lapata},
  journal={ArXiv},
  year={2018},
  volume={abs/1808.08745}
}
"""

_DESCRIPTION = """
Extreme Summarization (XSum) Dataset.

There are two features:
  - document: Input news article.
  - summary: One sentence summary of the article.

"""

# From https://github.com/EdinburghNLP/XSum/issues/12
_URL_DATA = "http://bollin.inf.ed.ac.uk/public/direct/XSUM-EMNLP18-Summary-Data-Original.tar.gz"
_URL_SPLITS = (
    "https://raw.githubusercontent.com/EdinburghNLP/XSum/master/XSum-Dataset/XSum-TRAINING-DEV-TEST-SPLIT-90-5-5.json"
)

_DOCUMENT = "document"
_SUMMARY = "summary"
_ID = "id"

_REMOVE_LINES = set(
    [
        "Share this with\n",
        "Email\n",
        "Facebook\n",
        "Messenger\n",
        "Twitter\n",
        "Pinterest\n",
        "WhatsApp\n",
        "Linkedin\n",
        "LinkedIn\n",
        "Copy this link\n",
        "These are external links and will open in a new window\n",
    ]
)


class Xsum(datasets.GeneratorBasedBuilder):
    """Extreme Summarization (XSum) Dataset."""

    # Version 1.1.0 removes web contents.
    VERSION = datasets.Version("1.1.0")
    SUPPORTED_VERSIONS = [datasets.Version("1.0.0", "Dataset without cleaning.")]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    _DOCUMENT: datasets.Value("string"),
                    _SUMMARY: datasets.Value("string"),
                    _ID: datasets.Value("string"),
                }
            ),
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage="https://github.com/EdinburghNLP/XSum/tree/master/XSum-Dataset",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_path = dl_manager.download_and_extract(_URL_DATA)
        splits_path = dl_manager.download(_URL_SPLITS)

        with open(splits_path, "r") as f:
            split_ids = json.load(f)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "split_ids": split_ids["train"],
                    "data_dir": os.path.join(data_path, "bbc-summary-data"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "split_ids": split_ids["validation"],
                    "data_dir": os.path.join(data_path, "bbc-summary-data"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "split_ids": split_ids["test"],
                    "data_dir": os.path.join(data_path, "bbc-summary-data")
                },
            ),
        ]

    def _generate_examples(self, split_ids=None, data_dir=None):
        """Yields examples."""
        missing = 0
        total_num = len(split_ids)
        for i in split_ids:
            filename = os.path.join(data_dir, i + ".summary")

            if os.path.exists(filename):
                with open(filename) as f:

                    text = "".join([line for line in f.readlines() if line not in _REMOVE_LINES and line.strip()])

                    # Each file follows below format:
                    # [SN]URL[SN]
                    # http://somelink
                    #
                    # [SN]TITLE[SN]
                    # some intro
                    #
                    # [SN]FIRST-SENTENCE[SN]
                    # some intro
                    #
                    # [SN]RESTBODY[SN]
                    # text line.
                    # another text line.
                    # "another text line."

                    # According to the following issue, FIRST-SENTENCE
                    # is the reference summary and TITLE is unused:
                    # https://github.com/EdinburghNLP/XSum/issues/22
                    segs = text.split("[SN]")
                    yield i, {_DOCUMENT: segs[8].strip(), _SUMMARY: segs[6].strip(), _ID: i}
            else:
                missing += 1
                logging.info("id %s missing.", i)
        if missing:
            logging.warning("%d out of %d examples are missing.", missing, total_num)
