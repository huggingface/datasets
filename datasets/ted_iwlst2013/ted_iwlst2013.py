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
A parallel corpus of TED talk subtitles provided by CASMACAT: http://www.casmacat.eu/corpus/ted2013.html. The files are originally provided by https://wit3.fbk.eu.

15 languages, 14 bitexts
total number of files: 28
total number of tokens: 67.67M
total number of sentence fragments: 3.81M
"""
_HOMEPAGE_URL = "http://opus.nlpl.eu/TED2013.php"
_CITATION = """\
J. Tiedemann, 2012, Parallel Data, Tools and Interfaces in OPUS. In Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC 2012)
"""

_VERSION = "1.1.0"
_BASE_NAME = "TED2013.{}.{}"

_LANGUAGE_PAIRS = {
    ("ar", "en"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/ar-en.txt.zip",
    ("de", "en"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/de-en.txt.zip",
    ("en", "es"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-es.txt.zip",
    ("en", "fa"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-fa.txt.zip",
    ("en", "fr"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-fr.txt.zip",
    ("en", "it"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-it.txt.zip",
    ("en", "nl"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-nl.txt.zip",
    ("en", "pl"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-pl.txt.zip",
    ("en", "pt"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-pt.txt.zip",
    ("en", "ro"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-ro.txt.zip",
    ("en", "ru"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-ru.txt.zip",
    ("en", "sl"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-sl.txt.zip",
    ("en", "tr"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-tr.txt.zip",
    ("en", "zh"): "https://object.pouta.csc.fi/OPUS-TED2013/v1.1/moses/en-zh.txt.zip",
}


class TedIwlst2013Config(datasets.BuilderConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TedIwlst2013(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        TedIwlst2013Config(
            name=f"{lang1}-{lang2}",
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS.keys()
    ]
    BUILDER_CONFIG_CLASS = TedIwlst2013Config

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "translation": datasets.Translation(languages=tuple(self.config.name.split("-"))),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        download_url = _LANGUAGE_PAIRS.get(tuple(self.config.name.split("-")))
        path = dl_manager.download_and_extract(download_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    def _generate_examples(self, datapath):
        l1, l2 = self.config.name.split("-")
        l1_file = _BASE_NAME.format(self.config.name, l1)
        l2_file = _BASE_NAME.format(self.config.name, l2)
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
