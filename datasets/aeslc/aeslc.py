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
"""Annotated Enron Subject Line Corpus Dataset."""

from __future__ import absolute_import, division, print_function

import glob
import os

import nlp


_CITATION = """
@misc{zhang2019email,
    title={This Email Could Save Your Life: Introducing the Task of Email Subject Line Generation},
    author={Rui Zhang and Joel Tetreault},
    year={2019},
    eprint={1906.03497},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """
A collection of email messages of employees in the Enron Corporation.

There are two features:
  - email_body: email body text.
  - subject_line: email subject text.
"""

_URL = "https://github.com/ryanzhumich/AESLC/archive/master.zip"

_DOCUMENT = "email_body"
_SUMMARY = "subject_line"


class Aeslc(nlp.GeneratorBasedBuilder):
    """Annotated Enron Subject Line Corpus Dataset."""

    VERSION = nlp.Version("1.0.0")

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({_DOCUMENT: nlp.Value("string"), _SUMMARY: nlp.Value("string")}),
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage="https://github.com/ryanzhumich/AESLC",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download_and_extract(_URL)
        input_path = os.path.join(dl_path, "AESLC-master", "enron_subject_line")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, gen_kwargs={"pattern": os.path.join(input_path, "train", "*.subject")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"pattern": os.path.join(input_path, "dev", "*.subject")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST, gen_kwargs={"pattern": os.path.join(input_path, "test", "*.subject")},
            ),
        ]

    def _generate_examples(self, pattern=None):
        """Yields examples."""
        for filename in glob.glob(pattern):
            email_body, subject_line = _parse_email_file(filename)
            key = os.path.basename(filename).rstrip(".subject")
            yield key, {_DOCUMENT: email_body, _SUMMARY: subject_line}


def _parse_email_file(filename):
    """Parse email file text for email body and subject."""
    with open(filename) as f:
        email_body = ""
        for line in f:
            if line == "\n":
                break
            email_body += line
        line = next(f)
        subject = ""
        for line in f:
            if line == "\n":
                break
            subject += line
    return email_body, subject
