# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

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


class Aeslc(tfds.core.GeneratorBasedBuilder):
  """Annotated Enron Subject Line Corpus Dataset."""

  VERSION = tfds.core.Version("1.0.0")

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            _DOCUMENT: tfds.features.Text(),
            _SUMMARY: tfds.features.Text()
        }),
        supervised_keys=(_DOCUMENT, _SUMMARY),
        homepage="https://github.com/ryanzhumich/AESLC",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    dl_path = dl_manager.download_and_extract(tfds.download.Resource(
        url=_URL,
        extract_method=tfds.download.ExtractMethod.ZIP))
    input_path = os.path.join(dl_path, "AESLC-master", "enron_subject_line")
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={
                "pattern": os.path.join(input_path, "train", "*.subject")
            },
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={
                "pattern": os.path.join(input_path, "dev", "*.subject")
            },
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={
                "pattern": os.path.join(input_path, "test", "*.subject")
            },
        ),
    ]

  def _generate_examples(self, pattern=None):
    """Yields examples."""
    for filename in tf.io.gfile.glob(pattern):
      email_body, subject_line = _parse_email_file(filename)
      key = os.path.basename(filename).rstrip(".subject")
      yield key, {_DOCUMENT: email_body, _SUMMARY: subject_line}


def _parse_email_file(filename):
  """Parse email file text for email body and subject."""
  with tf.io.gfile.GFile(filename) as f:
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
