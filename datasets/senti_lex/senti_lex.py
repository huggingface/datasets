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
"""Sentiment lexicons for 81 languages generated via graph propagation based on a knowledge graph--a graphical representation of real-world entities and the links between them"""


import os

import datasets


_CITATION = """\
@inproceedings{inproceedings,
author = {Chen, Yanqing and Skiena, Steven},
year = {2014},
month = {06},
pages = {383-389},
title = {Building Sentiment Lexicons for All Major Languages},
volume = {2},
journal = {52nd Annual Meeting of the Association for Computational Linguistics, ACL 2014 - Proceedings of the Conference},
doi = {10.3115/v1/P14-2063}
}
"""

_DESCRIPTION = """\
This dataset add sentiment lexicons for 81 languages generated via graph propagation based on a knowledge graph--a graphical representation of real-world entities and the links between them.
"""

_HOMEPAGE = "https://sites.google.com/site/datascienceslab/projects/multilingualsentiment"

_LICENSE = "GNU General Public License v3"

_URLs = "https://www.kaggle.com/rtatman/sentiment-lexicons-for-81-languages"

LANGS = [
    "af",
    "an",
    "ar",
    "az",
    "be",
    "bg",
    "bn",
    "br",
    "bs",
    "ca",
    "cs",
    "cy",
    "da",
    "de",
    "el",
    "eo",
    "es",
    "et",
    "eu",
    "fa",
    "fi",
    "fo",
    "fr",
    "fy",
    "ga",
    "gd",
    "gl",
    "gu",
    "he",
    "hi",
    "hr",
    "ht",
    "hu",
    "hy",
    "ia",
    "id",
    "io",
    "is",
    "it",
    "ja",
    "ka",
    "km",
    "kn",
    "ko",
    "ku",
    "ky",
    "la",
    "lb",
    "lt",
    "lv",
    "mk",
    "mr",
    "ms",
    "mt",
    "nl",
    "nn",
    "no",
    "pl",
    "pt",
    "rm",
    "ro",
    "ru",
    "sk",
    "sl",
    "sq",
    "sr",
    "sv",
    "sw",
    "ta",
    "te",
    "th",
    "tk",
    "tl",
    "tr",
    "uk",
    "ur",
    "uz",
    "vi",
    "vo",
    "wa",
    "yi",
    "zh",
    "zhw",
]


class SentiLex(datasets.GeneratorBasedBuilder):
    """Sentiment lexicons for 81 different languages"""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
  You should download the dataset from https://www.kaggle.com/rtatman/sentiment-lexicons-for-81-languages
  The webpage requires registration.
  After downloading, please put the files in a dir of your choice,
  which will be used as a manual_dir, e.g. `~/.manual_dirs/senti_lex`
  SentiLex can then be loaded via:
  `datasets.load_dataset("newsroom", data_dir="~/.manual_dirs/senti_lex")`.
  """

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=i,
            version=datasets.Version("1.1.0"),
            description=("Lexicon of positive and negative words for the " + i + " language"),
        )
        for i in LANGS
    ]

    def _info(self):

        features = datasets.Features(
            {
                "word": datasets.Value("string"),
                "sentiment": datasets.ClassLabel(
                    names=[
                        "negative",
                        "positive",
                    ]
                ),
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
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('newsroom', data_dir=...)` that includes files unzipped from the reclor zip. Manual download instructions: {self.manual_download_instructions}"
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_dir": data_dir,
                },
            ),
        ]

    def _generate_examples(self, data_dir):
        """Yields examples."""

        filepaths = [
            os.path.join(data_dir, "sentiment-lexicons", "negative_words_" + self.config.name + ".txt"),
            os.path.join(data_dir, "sentiment-lexicons", "positive_words_" + self.config.name + ".txt"),
        ]

        for file_idx, filepath in enumerate(filepaths):

            with open(filepath, encoding="utf-8") as f:

                for id_, line in enumerate(f):

                    if "negative" in filepath:
                        yield f"{file_idx}_{id_}", {
                            "word": line.strip(" \n"),
                            "sentiment": "negative",
                        }
                    elif "positive" in filepath:
                        yield f"{file_idx}_{id_}", {
                            "word": line.strip(" \n"),
                            "sentiment": "positive",
                        }
