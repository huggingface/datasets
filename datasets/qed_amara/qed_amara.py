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
The QCRI Educational Domain Corpus (formerly QCRI AMARA Corpus) is an open multilingual collection of subtitles for educational videos and lectures collaboratively transcribed and translated over the AMARA web-based platform.
Developed by: Qatar Computing Research Institute, Arabic Language Technologies Group
The QED Corpus is made public for RESEARCH purpose only.
The corpus is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Copyright Qatar Computing Research Institute. All rights reserved.
225 languages, 9,291 bitexts
total number of files: 271,558
total number of tokens: 371.76M
total number of sentence fragments: 30.93M
"""
_HOMEPAGE_URL = "http://opus.nlpl.eu/QED.php"
_CITATION = """\
A. Abdelali, F. Guzman, H. Sajjad and S. Vogel, "The AMARA Corpus: Building parallel language resources for the educational domain", The Proceedings of the 9th International Conference on Language Resources and Evaluation (LREC'14). Reykjavik, Iceland, 2014. Pp. 1856-1862. Isbn. 978-2-9517408-8-4.
"""

_VERSION = "2.0.0"
_BASE_NAME = "QED.{}.{}"
_BASE_URL = "https://object.pouta.csc.fi/OPUS-QED/v2.0a/moses/{}-{}.txt.zip"

# Please note that only few pairs are shown here. You can use config to generate data for all language pairs
_LANGUAGE_PAIRS = [
    ("ar", "ko"),
    ("de", "fr"),
    ("es", "it"),
    ("en", "ja"),
    ("he", "nl"),
]


class QEDAmaraConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class QEDAmara(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        QEDAmaraConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = QEDAmaraConfig

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
                sentence_counter += 1
                yield result
