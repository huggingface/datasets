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
A parallel corpus of News Commentaries provided by WMT for training SMT. The source is taken from CASMACAT: http://www.casmacat.eu/corpus/news-commentary.html

12 languages, 63 bitexts
total number of files: 61,928
total number of tokens: 49.66M
total number of sentence fragments: 1.93M
"""
_HOMEPAGE_URL = "http://opus.nlpl.eu/News-Commentary.php"
_CITATION = """\
@InProceedings{TIEDEMANN12.463,
  author = {J�rg Tiedemann},
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

_VERSION = "11.0.0"
_BASE_NAME = "News-Commentary.{}.{}"
_BASE_URL = "https://object.pouta.csc.fi/OPUS-News-Commentary/v11/moses/{}-{}.txt.zip"

_LANGUAGE_PAIRS = [
    ("ar", "cs"),
    ("ar", "de"),
    ("cs", "de"),
    ("ar", "en"),
    ("cs", "en"),
    ("de", "en"),
    ("ar", "es"),
    ("cs", "es"),
    ("de", "es"),
    ("en", "es"),
    ("ar", "fr"),
    ("cs", "fr"),
    ("de", "fr"),
    ("en", "fr"),
    ("es", "fr"),
    ("ar", "it"),
    ("cs", "it"),
    ("de", "it"),
    ("en", "it"),
    ("es", "it"),
    ("fr", "it"),
    ("ar", "ja"),
    ("cs", "ja"),
    ("de", "ja"),
    ("en", "ja"),
    ("es", "ja"),
    ("fr", "ja"),
    ("ar", "nl"),
    ("cs", "nl"),
    ("de", "nl"),
    ("en", "nl"),
    ("es", "nl"),
    ("fr", "nl"),
    ("it", "nl"),
    ("ar", "pt"),
    ("cs", "pt"),
    ("de", "pt"),
    ("en", "pt"),
    ("es", "pt"),
    ("fr", "pt"),
    ("it", "pt"),
    ("nl", "pt"),
    ("ar", "ru"),
    ("cs", "ru"),
    ("de", "ru"),
    ("en", "ru"),
    ("es", "ru"),
    ("fr", "ru"),
    ("it", "ru"),
    ("ja", "ru"),
    ("nl", "ru"),
    ("pt", "ru"),
    ("ar", "zh"),
    ("cs", "zh"),
    ("de", "zh"),
    ("en", "zh"),
    ("es", "zh"),
    ("fr", "zh"),
    ("it", "zh"),
    ("ja", "zh"),
    ("nl", "zh"),
    ("pt", "zh"),
    ("ru", "zh"),
]


class NewsCommentaryConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class NewsCommentary(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        NewsCommentaryConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = NewsCommentaryConfig

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
