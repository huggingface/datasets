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
This is a collection of copyright free books aligned by Andras Farkas, which are available from http://www.farkastranslations.com/bilingual_books.php
Note that the texts are rather dated due to copyright issues and that some of them are manually reviewed (check the meta-data at the top of the corpus files in XML). The source is multilingually aligned, which is available from http://www.farkastranslations.com/bilingual_books.php. In OPUS, the alignment is formally bilingual but the multilingual alignment can be recovered from the XCES sentence alignment files. Note also that the alignment units from the original source may include multi-sentence paragraphs, which are split and sentence-aligned in OPUS.
All texts are freely available for personal, educational and research use. Commercial use (e.g. reselling as parallel books) and mass redistribution without explicit permission are not granted. Please acknowledge the source when using the data!

16 languages, 64 bitexts
total number of files: 158
total number of tokens: 19.50M
total number of sentence fragments: 0.91M
"""
_HOMEPAGE_URL = "http://opus.nlpl.eu/Books.php"
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

_VERSION = "1.0.0"
_BASE_NAME = "Books.{}.{}"
_BASE_URL = "https://object.pouta.csc.fi/OPUS-Books/v1/moses/{}-{}.txt.zip"

_LANGUAGE_PAIRS = [
    ("ca", "de"),
    ("ca", "en"),
    ("de", "en"),
    ("el", "en"),
    ("de", "eo"),
    ("en", "eo"),
    ("de", "es"),
    ("el", "es"),
    ("en", "es"),
    ("eo", "es"),
    ("en", "fi"),
    ("es", "fi"),
    ("de", "fr"),
    ("el", "fr"),
    ("en", "fr"),
    ("eo", "fr"),
    ("es", "fr"),
    ("fi", "fr"),
    ("ca", "hu"),
    ("de", "hu"),
    ("el", "hu"),
    ("en", "hu"),
    ("eo", "hu"),
    ("fr", "hu"),
    ("de", "it"),
    ("en", "it"),
    ("eo", "it"),
    ("es", "it"),
    ("fr", "it"),
    ("hu", "it"),
    ("ca", "nl"),
    ("de", "nl"),
    ("en", "nl"),
    ("es", "nl"),
    ("fr", "nl"),
    ("hu", "nl"),
    ("it", "nl"),
    ("en", "no"),
    ("es", "no"),
    ("fi", "no"),
    ("fr", "no"),
    ("hu", "no"),
    ("en", "pl"),
    ("fi", "pl"),
    ("fr", "pl"),
    ("hu", "pl"),
    ("de", "pt"),
    ("en", "pt"),
    ("eo", "pt"),
    ("es", "pt"),
    ("fr", "pt"),
    ("hu", "pt"),
    ("it", "pt"),
    ("de", "ru"),
    ("en", "ru"),
    ("es", "ru"),
    ("fr", "ru"),
    ("hu", "ru"),
    ("it", "ru"),
    ("en", "sv"),
    ("fr", "sv"),
    ("it", "sv"),
]


class OpusBooksConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class OpusBooks(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        OpusBooksConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = OpusBooksConfig

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
