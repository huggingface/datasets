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
"""Librispeech language modeling dataset."""

from __future__ import absolute_import, division, print_function

import nlp


_CITATION = """\
@inproceedings{panayotov2015librispeech,
  title={Librispeech: an ASR corpus based on public domain audio books},
  author={Panayotov, Vassil and Chen, Guoguo and Povey, Daniel and Khudanpur, Sanjeev},
  booktitle={Acoustics, Speech and Signal Processing (ICASSP), 2015 IEEE International Conference on},
  pages={5206--5210},
  year={2015},
  organization={IEEE}
}
"""

_DESCRIPTION = """\
Language modeling resources to be used in conjunction with the LibriSpeech ASR corpus.
"""

_URL = "http://www.openslr.org/11"

_DL_URL = "http://www.openslr.org/resources/11/librispeech-lm-norm.txt.gz"


class LibrispeechLm(nlp.GeneratorBasedBuilder):
    """Librispeech language modeling dataset."""

    VERSION = nlp.Version("0.1.0")

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({"text": nlp.Value("string"),}),
            supervised_keys=("text", "text"),
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        archive_path = dl_manager.download_and_extract(_DL_URL)
        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"archive_path": archive_path}),
        ]

    def _generate_examples(self, archive_path):
        """Yields examples."""
        with open(archive_path, "r") as f:
            for key, line in enumerate(f):
                text = line.strip()
                if text:  # Skip empty lines.
                    yield key, {"text": text}
