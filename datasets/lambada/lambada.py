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
"""The LAMBADA dataset."""

from __future__ import absolute_import, division, print_function

import glob
import os
import tarfile

import datasets


_CITATION = """\
@InProceedings{paperno-EtAl:2016:P16-1,
  author    = {Paperno, Denis  and  Kruszewski, Germ\'{a}n  and  Lazaridou,
Angeliki  and  Pham, Ngoc Quan  and  Bernardi, Raffaella  and  Pezzelle,
Sandro  and  Baroni, Marco  and  Boleda, Gemma  and  Fernandez, Raquel},
  title     = {The {LAMBADA} dataset: Word prediction requiring a broad
discourse context},
  booktitle = {Proceedings of the 54th Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers)},
  month     = {August},
  year      = {2016},
  address   = {Berlin, Germany},
  publisher = {Association for Computational Linguistics},
  pages     = {1525--1534},
  url       = {http://www.aclweb.org/anthology/P16-1144}
}
"""

_DESCRIPTION = """
The LAMBADA evaluates the capabilities of computational models
for text understanding by means of a word prediction task.
LAMBADA is a collection of narrative passages sharing the characteristic
that human subjects are able to guess their last word if
they are exposed to the whole passage, but not if they
only see the last sentence preceding the target word.
To succeed on LAMBADA, computational models cannot
simply rely on local context, but must be able to
keep track of information in the broader discourse.

The LAMBADA dataset is extracted from BookCorpus and
consists of 10'022 passages, divided into 4'869 development
and 5'153 test passages. The training data for language
models to be tested on LAMBADA include the full text
of 2'662 novels (disjoint from those in dev+test),
comprising 203 million words.
"""

_URL = "https://zenodo.org/record/2630551/files/lambada-dataset.tar.gz"


class Lambada(datasets.GeneratorBasedBuilder):
    """LAMBADA dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            description="Plain text",
            version=VERSION,
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://zenodo.org/record/2630551#.X8UP76pKiIa",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)

        # Extracting (un-taring) the training data
        tar_file = tarfile.open(os.path.join(data_dir, "train-novels.tar"))
        tar_file.extractall(path=data_dir)
        tar_file.close()

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train-novels"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "lambada_test_plain_text.txt"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "lambada_development_plain_text.txt"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        if split == "train":
            recursion_pattern = f"{filepath}/*/*.txt"
            for idx, novel_path in enumerate(glob.iglob(recursion_pattern, recursive=True)):
                domain = os.path.dirname(novel_path).split("/")[-1]
                with open(novel_path, encoding="utf-8") as novel:
                    text = novel.read()
                    yield idx, {"text": text.strip(), "domain": domain}
        else:
            with open(filepath, encoding="utf-8") as f:
                data = f.read().splitlines()
                for idx, text in enumerate(data):
                    yield idx, {"text": text, "domain": None}
