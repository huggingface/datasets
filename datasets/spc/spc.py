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
This is a collection of parallel corpora collected by Hercules Dalianis and his research group for bilingual dictionary construction.
More information in: Hercules Dalianis, Hao-chun Xing, Xin Zhang: Creating a Reusable English-Chinese Parallel Corpus for Bilingual Dictionary Construction, In Proceedings of LREC2010 (source: http://people.dsv.su.se/~hercules/SEC/) and Konstantinos Charitakis (2007): Using Parallel Corpora to Create a Greek-English Dictionary with UPLUG, In Proceedings of NODALIDA 2007. Afrikaans-English: Aldin Draghoender and Mattias Kanhov: Creating a reusable English – Afrikaans parallel corpora for bilingual dictionary construction

4 languages, 3 bitexts
total number of files: 6
total number of tokens: 1.32M
total number of sentence fragments: 0.15M
"""
_HOMEPAGE_URL = "http://opus.nlpl.eu/SPC.php"
_CITATION = """\
@InProceedings{TIEDEMANN12.463,
  author = {J{\"o}rg Tiedemann},
  title = {Parallel Data, Tools and Interfaces in OPUS},
  booktitle = {Proceedings of the Eight International Conference on Language Resources and Evaluation (LREC'12)},
  year = {2012},
  month = {may},
  date = {23-25},
  address = {Istanbul, Turkey},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Mehmet Ugur Dogan and Bente Maegaard and Joseph Mariani and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  isbn = {978-2-9517408-7-7},
  language = {english}
 }
"""

_VERSION = "1.0.0"
_BASE_NAME = "SPC.{}.{}"
_BASE_URL = "https://object.pouta.csc.fi/OPUS-SPC/v1/moses/{}-{}.txt.zip"

_LANGUAGE_PAIRS = [
    ("af", "en"),
    ("el", "en"),
    ("en", "zh"),
]


class SpcConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class Spc(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        SpcConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = SpcConfig

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
