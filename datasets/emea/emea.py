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
This is a parallel corpus made out of PDF documents from the European Medicines Agency. All files are automatically converted from PDF to plain text using pdftotext with the command line arguments -layout -nopgbrk -eol unix. There are some known problems with tables and multi-column layouts - some of them are fixed in the current version.

source: http://www.emea.europa.eu/

22 languages, 231 bitexts
total number of files: 41,957
total number of tokens: 311.65M
total number of sentence fragments: 26.51M
"""
_HOMEPAGE_URL = "http://opus.nlpl.eu/EMEA.php"
_CITATION = """\
J. Tiedemann, 2012, Parallel Data, Tools and Interfaces in OPUS. In Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC 2012)
"""

_VERSION = "3.0.0"
_BASE_NAME = "EMEA.{}.{}"
_BASE_URL = "https://object.pouta.csc.fi/OPUS-EMEA/v3/moses/{}-{}.txt.zip"

# Please note that only few pairs are shown here. You can use config to generate data for all language pairs
_LANGUAGE_PAIRS = [
    ("bg", "el"),
    ("cs", "et"),
    ("de", "mt"),
    ("fr", "sk"),
    ("es", "lt"),
]


class EmeaConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class Emea(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        EmeaConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = EmeaConfig

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "translation": datasets.Translation(languages=(self.config.lang1, self.config.lang2)),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        def _base_url(lang1, lang2):
            return _BASE_URL.format(lang1, lang2)

        download_url = _base_url(self.config.lang1, self.config.lang2)
        path = dl_manager.download_and_extract(download_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    def _generate_examples(self, datapath):
        l1, l2 = self.config.lang1, self.config.lang2
        folder = l1 + "-" + l2
        l1_file = _BASE_NAME.format(folder, l1)
        l2_file = _BASE_NAME.format(folder, l2)
        l1_path = os.path.join(datapath, l1_file)
        l2_path = os.path.join(datapath, l2_file)
        with open(l1_path, encoding="utf-8") as f1, open(l2_path, encoding="utf-8") as f2:
            for sentence_counter, (x, y) in enumerate(zip(f1, f2)):
                x = x.strip()
                y = y.strip()
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "translation": {l1: x, l2: y},
                    },
                )
                yield result
