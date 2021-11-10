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

import datasets


_DESCRIPTION = """\
SETimes – A Parallel Corpus of English and South-East European Languages
The corpus is based on the content published on the SETimes.com news portal. The news portal publishes “news and views from Southeast Europe” in ten languages: Bulgarian, Bosnian, Greek, English, Croatian, Macedonian, Romanian, Albanian and Serbian. This version of the corpus tries to solve the issues present in an older version of the corpus (published inside OPUS, described in the LREC 2010 paper by Francis M. Tyers and Murat Serdar Alperen). The following procedures were applied to resolve existing issues:

- stricter extraction process – no HTML residues present
- language identification on every non-English document – non-English online documents contain English material in case the article was not translated into that language
- resolving encoding issues in Croatian and Serbian – diacritics were partially lost due to encoding errors – text was rediacritized.
"""
_HOMEPAGE_URL = "http://nlp.ffzg.hr/resources/corpora/setimes/"
_CITATION = None

_VERSION = "1.0.0"
_BASE_NAME = "setimes.{}-{}.{}.txt"
_BASE_URL = "http://nlp.ffzg.hr/data/corpora/setimes/setimes.{}-{}.txt.tgz"

_LANGUAGE_PAIRS = [
    ("bg", "bs"),
    ("bg", "el"),
    ("bs", "el"),
    ("bg", "en"),
    ("bs", "en"),
    ("el", "en"),
    ("bg", "hr"),
    ("bs", "hr"),
    ("el", "hr"),
    ("en", "hr"),
    ("bg", "mk"),
    ("bs", "mk"),
    ("el", "mk"),
    ("en", "mk"),
    ("hr", "mk"),
    ("bg", "ro"),
    ("bs", "ro"),
    ("el", "ro"),
    ("en", "ro"),
    ("hr", "ro"),
    ("mk", "ro"),
    ("bg", "sq"),
    ("bs", "sq"),
    ("el", "sq"),
    ("en", "sq"),
    ("hr", "sq"),
    ("mk", "sq"),
    ("ro", "sq"),
    ("bg", "sr"),
    ("bs", "sr"),
    ("el", "sr"),
    ("en", "sr"),
    ("hr", "sr"),
    ("mk", "sr"),
    ("ro", "sr"),
    ("sq", "sr"),
    ("bg", "tr"),
    ("bs", "tr"),
    ("el", "tr"),
    ("en", "tr"),
    ("hr", "tr"),
    ("mk", "tr"),
    ("ro", "tr"),
    ("sq", "tr"),
    ("sr", "tr"),
]


class SetimesConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class Setimes(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        SetimesConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = SetimesConfig

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
        archive = dl_manager.download(download_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "l1_files": dl_manager.iter_archive(archive),
                    "l2_files": dl_manager.iter_archive(archive),
                },
            )
        ]

    def _generate_examples(self, l1_files, l2_files):
        l1, l2 = self.config.lang1, self.config.lang2
        l1_file = _BASE_NAME.format(l1, l2, l1)
        l2_file = _BASE_NAME.format(l1, l2, l2)
        for path1, f1 in l1_files:
            if path1 == l1_file:
                for path2, f2 in l2_files:
                    if path2 == l2_file:
                        for sentence_counter, (x, y) in enumerate(zip(f1, f2)):
                            x = x.decode("utf-8").strip()
                            y = y.decode("utf-8").strip()
                            result = (
                                sentence_counter,
                                {
                                    "id": str(sentence_counter),
                                    "translation": {l1: x, l2: y},
                                },
                            )
                            yield result
                        break
                break
