# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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

import json
import logging
import os

import nlp


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

This data need to manaully downloaded and extracted as described in
https://github.com/EdinburghNLP/XSum/blob/master/XSum-Dataset/README.md.
The folder 'xsum-extracts-from-downloads' need to be compressed as
'xsum-extracts-from-downloads.tar.gz' and put in manually downloaded folder.
"""

_URL = (
    "https://raw.githubusercontent.com/EdinburghNLP/XSum/master/XSum-Dataset/XSum-TRAINING-DEV-TEST-SPLIT-90-5-5.json"
)

_DOCUMENT = "document"
_SUMMARY = "summary"

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


class Xsum(nlp.GeneratorBasedBuilder):
    """Extreme Summarization (XSum) Dataset."""

    # Version 1.1.0 removes web contents.
    VERSION = nlp.Version("1.1.0")
    SUPPORTED_VERSIONS = [nlp.Version("1.0.0", "Dataset without cleaning.")]

    MANUAL_DOWNLOAD_INSTRUCTIONS = """\
  Detailed download instructions (which require running a custom script) are
  here:
  https://github.com/EdinburghNLP/XSum/blob/master/XSum-Dataset/README.md . Please make sure you run download-bbc-articles.py and parse-bbc-html-data.py scripts
 

  """

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({_DOCUMENT: nlp.Value("string"), _SUMMARY: nlp.Value("string"),}),
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage="https://github.com/EdinburghNLP/XSum/tree/master/XSum-Dataset",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download_and_extract(_URL)
        with open(dl_path, "r") as json_file:
            split_ids = json.load(json_file)
        downloaded_path = os.path.join(dl_manager.manual_dir, "xsum-extracts-from-downloads")
        if not os.path.exists(downloaded_path):
            raise FileNotFoundError(
                "{} does not exist. Make sure you indicate the data_dir as  `nlp.load('xsum', data_dir=...), which points to your downloded dataset'. Manual download instructions: {})".format(
                    downloaded_path, self.MANUAL_DOWNLOAD_INSTRUCTIONS
                )
            )
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, gen_kwargs={"split_ids": split_ids["train"], "path": downloaded_path,},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"split_ids": split_ids["validation"], "path": downloaded_path,},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST, gen_kwargs={"split_ids": split_ids["test"], "path": downloaded_path,},
            ),
        ]

    def _generate_examples(self, split_ids=None, path=None):
        """Yields examples."""
        missing = 0
        total_num = len(split_ids)
        for i in split_ids:
            filename = os.path.join(path, i + ".data")
            print(filename)

            if os.path.exists(filename):
                with open(filename) as f:

                    text = "".join([line for line in f.readlines() if line not in _REMOVE_LINES and line.strip()])

                    # Each file follows below format:
                    # [XSUM]URL[XSUM]
                    # http://somelink
                    #
                    # [XSUM]INTRODUCTION[XSUM]
                    # some intro
                    #
                    # [XSUM]RESTBODY[XSUM]
                    # text line.
                    # another text line.
                    # "another text line."
                    segs = text.split("[XSUM]")
                    yield i, {_DOCUMENT: segs[6].strip(), _SUMMARY: segs[4].strip()}
            else:
                missing += 1
                logging.info("id %s missing.", i)
        if missing:
            logging.warning("%d out of %d examples are missing.", missing, total_num)
