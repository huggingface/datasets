# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""Euroconst: A parallel corpus collected from the European Constitution for 21 language"""


import itertools
import os

import datasets


_CITATION = """\
J. Tiedemann, 2012, Parallel Data, Tools and Interfaces in OPUS. \
In Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC 2012)
"""


_DESCRIPTION = """\
A parallel corpus collected from the European Constitution for 21 language.
"""


_HOMEPAGE = "http://opus.nlpl.eu/EUconst.php"

_LANGUAGES = [
    "cs",
    "da",
    "de",
    "el",
    "en",
    "es",
    "et",
    "fi",
    "fr",
    "ga",
    "hu",
    "it",
    "lt",
    "lv",
    "mt",
    "nl",
    "pl",
    "pt",
    "sk",
    "sl",
    "sv",
]
_LANGUAGE_PAIRS = list(itertools.combinations(_LANGUAGES, 2))

_BASE_URL = "http://opus.nlpl.eu/download.php?f=EUconst/v1/moses"
_URLS = {f"{l1}-{l2}": f"{_BASE_URL}/{l1}-{l2}.txt.zip" for l1, l2 in _LANGUAGE_PAIRS}


class OpusEuconst(datasets.GeneratorBasedBuilder):
    """Euroconst: A parallel corpus collected from the European Constitution for 21 language"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=f"{l1}-{l2}", version=datasets.Version("1.0.0"), description=f"OPUS EUconst {l1}-{l2}"
        )
        for l1, l2 in _LANGUAGE_PAIRS
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=tuple(self.config.name.split("-")))}
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        lang_pair = self.config.name.split("-")
        data_dir = dl_manager.download_and_extract(_URLS[self.config.name])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "source_file": os.path.join(data_dir, f"EUconst.{self.config.name}.{lang_pair[0]}"),
                    "target_file": os.path.join(data_dir, f"EUconst.{self.config.name}.{lang_pair[1]}"),
                },
            ),
        ]

    def _generate_examples(self, source_file, target_file):
        with open(source_file, encoding="utf-8") as f:
            source_sentences = f.read().split("\n")
        with open(target_file, encoding="utf-8") as f:
            target_sentences = f.read().split("\n")

        assert len(target_sentences) == len(source_sentences), "Sizes do not match: %d vs %d for %s vs %s." % (
            len(source_sentences),
            len(target_sentences),
            source_file,
            target_file,
        )

        source, target = tuple(self.config.name.split("-"))
        for idx, (l1, l2) in enumerate(zip(source_sentences, target_sentences)):
            result = {"translation": {source: l1, target: l2}}
            yield idx, result
