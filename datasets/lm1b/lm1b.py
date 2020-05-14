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
"""The Language Model 1 Billion dataset."""

from __future__ import absolute_import, division, print_function

import glob
import logging
import os

import nlp


_CITATION = """\
@article{DBLP:journals/corr/ChelbaMSGBK13,
  author    = {Ciprian Chelba and
               Tomas Mikolov and
               Mike Schuster and
               Qi Ge and
               Thorsten Brants and
               Phillipp Koehn},
  title     = {One Billion Word Benchmark for Measuring Progress in Statistical Language
               Modeling},
  journal   = {CoRR},
  volume    = {abs/1312.3005},
  year      = {2013},
  url       = {http://arxiv.org/abs/1312.3005},
  archivePrefix = {arXiv},
  eprint    = {1312.3005},
  timestamp = {Mon, 13 Aug 2018 16:46:16 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/ChelbaMSGBK13},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
A benchmark corpus to be used for measuring progress in statistical language \
modeling. This has almost one billion words in the training data.
"""

_DOWNLOAD_URL = "http://www.statmt.org/lm-benchmark/" "1-billion-word-language-modeling-benchmark-r13output.tar.gz"
_TOP_LEVEL_DIR = "1-billion-word-language-modeling-benchmark-r13output"
_TRAIN_FILE_FORMAT = os.path.join(_TOP_LEVEL_DIR, "training-monolingual.tokenized.shuffled", "news.en-*")
_HELDOUT_FILE_FORMAT = os.path.join(_TOP_LEVEL_DIR, "heldout-monolingual.tokenized.shuffled", "news.en.heldout-*")


class Lm1bConfig(nlp.BuilderConfig):
    """BuilderConfig for Lm1b."""

    def __init__(self, **kwargs):
        """BuilderConfig for Lm1b.

    Args:
      **kwargs: keyword arguments forwarded to super.
    """
        super(Lm1bConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )


def _train_data_filenames(tmp_dir):
    return glob.glob(os.path.join(tmp_dir, _TRAIN_FILE_FORMAT))


def _test_data_filenames(tmp_dir):
    return glob.glob(os.path.join(tmp_dir, _HELDOUT_FILE_FORMAT))


class Lm1b(nlp.GeneratorBasedBuilder):
    """1 Billion Word Language Model Benchmark dataset."""

    BUILDER_CONFIGS = [
        Lm1bConfig(name="plain_text", description="Plain text",),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({"text": nlp.Value("string"),}),
            supervised_keys=("text", "text"),
            homepage="http://www.statmt.org/lm-benchmark/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        lm1b_path = dl_manager.download_and_extract(_DOWNLOAD_URL)

        train_files = _train_data_filenames(lm1b_path)
        test_files = _test_data_filenames(lm1b_path)

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"files": train_files}),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"files": test_files}),
        ]

    def _generate_examples(self, files):
        for filepath in files:
            logging.info("generating examples from = %s", filepath)
            with open(filepath) as f:
                for idx, line in enumerate(f):
                    yield "%s_%d" % (os.path.basename(filepath), idx), {
                        "text": line.strip(),
                    }
