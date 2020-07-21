# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Authorship Analysis: Style Change Detection"""

from __future__ import absolute_import, division, print_function

import json
import os
import textwrap

import nlp


_CITATION = """\
@inproceedings{bevendorff2020shared,
  title={Shared Tasks on Authorship Analysis at PAN 2020},
  author={Bevendorff, Janek and Ghanem, Bilal and Giachanou, Anastasia and Kestemont, Mike and Manjavacas, Enrique and Potthast, Martin and Rangel, Francisco and Rosso, Paolo and Specht, G{\"u}nther and Stamatatos, Efstathios and others},
  booktitle={European Conference on Information Retrieval},
  pages={508--516},
  year={2020},
  organization={Springer}
}
"""

_DESCRIPTION = """\
The goal of the style change detection task is to identify text positions within a given multi-author document at which the author switches. Detecting these positions is a crucial part of the authorship identification process, and for multi-author document analysis in general.

Access to the dataset needs to be requested from zenodo.
"""


class StyleChangeDetection(nlp.GeneratorBasedBuilder):
    """Style Change Detection Dataset from PAN20"""

    VERSION = nlp.Version("1.0.0")
    BUILDER_CONFIGS = [
        nlp.BuilderConfig(
            name="narrow",
            version=nlp.Version("1.0.0", "Version 1"),
            description="The narrow subset contains texts from a relatively narrow set of subjects matters (all related to technology).",
        ),
        nlp.BuilderConfig(
            name="wide",
            version=nlp.Version("1.0.0", "Version 1"),
            description="The wide subset adds additional subject areas (travel, philosophy, economics, history, etc.).",
        ),
    ]

    @property
    def manual_download_instructions(self):
        return """\
  You should download the dataset from https://zenodo.org/record/3660984
  The dataset needs requesting.

  Download each file, extract it and place in a dir of your choice,
  which will be used as a manual_dir, e.g. `~/.manual_dirs/style_change_detection`
  Style Change Detection can then be loaded via:
  `nlp.load_dataset("style_change_detection", data_dir="~/.manual_dirs/style_change_detection")`.
  """

    def _info(self):
        features = {
            "id": nlp.Value("string"),
            "text": nlp.Value("string"),
            "authors": nlp.Value("int32"),
            "structure": nlp.features.Sequence(nlp.Value("string")),
            "site": nlp.Value("string"),
            "multi-author": nlp.Value("bool"),
            "changes": nlp.features.Sequence(nlp.Value("bool")),
        }

        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(features),
            homepage="https://pan.webis.de/clef20/pan20-web/style-change-detection.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        train_dir = os.path.join(data_dir, "train", "dataset-" + self.config.name)
        val_dir = os.path.join(data_dir, "validation", "dataset-" + self.config.name)

        if not os.path.exists(train_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `nlp.load_dataset('style_change_detection', data_dir=...)` that includes {}. Manual download instructions: {}".format(
                    train_dir, train_dir, self.manual_download_instructions
                )
            )


        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={
                    "articles": [f for f in os.listdir(train_dir) if f.endswith(".txt")],
                    "base_dir": train_dir,
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                gen_kwargs={"articles": [f for f in os.listdir(val_dir) if f.endswith(".txt")], "base_dir": val_dir},
            ),
        ]

    def _generate_examples(self, articles=None, base_dir=None):
        """Yields examples."""
        for idx, article_filename in enumerate(articles):
            label_path = os.path.join(base_dir, "truth-" + article_filename[:-4] + ".json")
            with open(label_path) as f:
                example = json.load(f)
                example["id"] = article_filename[8:-4]
                example["text"] = open(os.path.join(base_dir, article_filename)).read()

                # Convert integers into boolean
                example["multi-author"] = example["multi-author"] == 1
                for i in range(len(example["changes"])):
                    example["changes"][i] = example["changes"][i] == 1

                yield idx, example
