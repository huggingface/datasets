# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
import os

import datasets


_DESCRIPTION = """\
UMC005 English-Urdu is a parallel corpus of texts in English and Urdu language with sentence alignments. The corpus can be used for experiments with statistical machine translation.

The texts come from four different sources:
- Quran
- Bible
- Penn Treebank (Wall Street Journal)
- Emille corpus

The authors provide the religious texts of Quran and Bible for direct download. Because of licensing reasons, Penn and Emille texts cannot be redistributed freely. However, if you already hold a license for the original corpora, we are able to provide scripts that will recreate our data on your disk. Our modifications include but are not limited to the following:

- Correction of Urdu translations and manual sentence alignment of the Emille texts.
- Manually corrected sentence alignment of the other corpora.
- Our data split (training-development-test) so that our published experiments can be reproduced.
- Tokenization (optional, but needed to reproduce our experiments).
- Normalization (optional) of e.g. European vs. Urdu numerals, European vs. Urdu punctuation, removal of Urdu diacritics.
"""
_HOMEPAGE_URL = "http://ufal.ms.mff.cuni.cz/umc/005-en-ur/"
_URL = "http://ufal.ms.mff.cuni.cz/umc/005-en-ur/download.php?f=umc005-corpus.zip"
_CITATION = """\
@unpublished{JaZeWordOrderIssues2011,
author      = {Bushra Jawaid and Daniel Zeman},
title       = {Word-Order Issues in {English}-to-{Urdu} Statistical Machine Translation},
year        = {2011},
journal     = {The Prague Bulletin of Mathematical Linguistics},
number      = {95},
institution = {Univerzita Karlova},
address     = {Praha, Czechia},
issn        = {0032-6585},
}
"""

_ALL = "all"
_VERSION = "1.0.0"
_SOURCES = ["bible", "quran"]
_SOURCES_FILEPATHS = {
    s: {
        "train": {"urdu": "train.ur", "english": "train.en"},
        "dev": {"urdu": "dev.ur", "english": "dev.en"},
        "test": {"urdu": "test.ur", "english": "test.en"},
    }
    for s in _SOURCES
}


class UM005Config(datasets.BuilderConfig):
    def __init__(self, *args, sources=None, **kwargs):
        super().__init__(*args, version=datasets.Version(_VERSION, ""), **kwargs)
        self.sources = sources

    @property
    def language_pair(self):
        return ("ur", "en")


class UM005(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        UM005Config(name=source, sources=[source], description=f"Source: {source}.") for source in _SOURCES
    ] + [
        UM005Config(
            name=_ALL,
            sources=_SOURCES,
            description=f"All sources included: bible, quran",
        )
    ]
    BUILDER_CONFIG_CLASS = UM005Config
    DEFAULT_CONFIG_NAME = _ALL

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "translation": datasets.Translation(languages=self.config.language_pair),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path, "datatype": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"datapath": path, "datatype": "dev"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"datapath": path, "datatype": "test"},
            ),
        ]

    def _generate_examples(self, datapath, datatype):
        if datatype == "train":
            ur_file = "train.ur"
            en_file = "train.en"
        elif datatype == "dev":
            ur_file = "dev.ur"
            en_file = "dev.en"
        elif datatype == "test":
            ur_file = "test.ur"
            en_file = "test.en"
        else:
            raise Exception("Invalid dataype. Try one of: dev, train, test")

        for source in self.config.sources:
            urdu_path = os.path.join(datapath, source, ur_file)
            english_path = os.path.join(datapath, source, en_file)
            with open(urdu_path, encoding="utf-8") as u, open(english_path, encoding="utf-8") as e:
                for sentence_counter, (x, y) in enumerate(zip(u, e)):
                    x = x.strip()
                    y = y.strip()
                    result = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "translation": {"ur": x, "en": y},
                        },
                    )
                    sentence_counter += 1
                    yield result
