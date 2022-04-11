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
"""United nations general assembly resolutions: A six-language parallel corpus"""


import os

import datasets


_CITATION = """\
@inproceedings{title = "United Nations General Assembly Resolutions: a six-language parallel corpus",
abstract = "In this paper we describe a six-ways parallel public-domain corpus consisting of 2100 United Nations General Assembly Resolutions with translations in the six official languages of the United Nations, with an average of around 3 million tokens per language. The corpus is available in a preprocessed, formatting-normalized TMX format with paragraphs aligned across multiple languages. We describe the background to the corpus and its content, the process of its construction, and some of its interesting properties.",
author = "Alexandre Rafalovitch and Robert Dale",
year = "2009",
language = "English",
booktitle = "MT Summit XII proceedings",
publisher = "International Association of Machine Translation",
}"""

_HOMEPAGE = "http://opus.nlpl.eu/UN.php"


_LICENSE = ""

_VALID_LANGUAGE_PAIRS = {
    ("ar", "en"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/ar-en.txt.zip",
    ("ar", "es"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/ar-es.txt.zip",
    ("ar", "fr"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/ar-fr.txt.zip",
    ("ar", "ru"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/ar-ru.txt.zip",
    ("ar", "zh"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/ar-zh.txt.zip",
    ("en", "es"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/en-es.txt.zip",
    ("en", "fr"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/en-fr.txt.zip",
    ("en", "ru"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/en-ru.txt.zip",
    ("en", "zh"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/en-zh.txt.zip",
    ("es", "fr"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/es-fr.txt.zip",
    ("es", "ru"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/es-ru.txt.zip",
    ("es", "zh"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/es-zh.txt.zip",
    ("fr", "ru"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/fr-ru.txt.zip",
    ("fr", "zh"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/fr-zh.txt.zip",
    ("ru", "zh"): "http://opus.nlpl.eu/download.php?f=UN/v20090831/moses/ru-zh.txt.zip",
}

_VERSION = "2.0.0"

_DESCRIPTION = """\
United nations general assembly resolutions: A six-language parallel corpus.
This is a collection of translated documents from the United Nations originally compiled into a translation memory by Alexandre Rafalovitch, Robert Dale (see http://uncorpora.org).
6 languages, 15 bitexts
total number of files: 6
total number of tokens: 18.87M
total number of sentence fragments: 0.44M
"""

_BASE_NAME = "UN.{}-{}.{}"


class UnGaConfig(datasets.BuilderConfig):
    """BuilderConfig for United nations general assembly resolutions: A six-language parallel corpus"""

    def __init__(self, language_pair=(None, None), **kwargs):
        """BuilderConfig for United nations general assembly resolutions: A six-language parallel corpus.
        The first language in `language_pair` should consist of two strings joined by
        an underscore (e.g. "en-tr").
        Args:
          language_pair: pair of languages that will be used for translation.
          **kwargs: keyword arguments forwarded to super.
        """
        name = "%s_to_%s" % (language_pair[0], language_pair[1])

        description = ("Translation dataset from %s to %s or %s to %s.") % (
            language_pair[0],
            language_pair[1],
            language_pair[1],
            language_pair[0],
        )
        super(UnGaConfig, self).__init__(
            name=name, description=description, version=datasets.Version(_VERSION, ""), **kwargs
        )

        # Validate language pair.
        assert language_pair in _VALID_LANGUAGE_PAIRS, (
            "Config language pair (%s, " "%s) not supported"
        ) % language_pair

        self.language_pair = language_pair


class UnGa(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        UnGaConfig(
            language_pair=pair,
        )
        for pair in _VALID_LANGUAGE_PAIRS.keys()
    ]

    BUILDER_CONFIG_CLASS = UnGaConfig

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "translation": datasets.Translation(languages=tuple(self.config.language_pair)),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        download_url = _VALID_LANGUAGE_PAIRS.get(tuple(self.config.language_pair))
        path = dl_manager.download_and_extract(download_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    def _generate_examples(self, datapath):
        lang1, lang2 = self.config.language_pair
        lang1_file = _BASE_NAME.format(lang1, lang2, lang1)
        lang2_file = _BASE_NAME.format(lang1, lang2, lang2)
        lang1_path = os.path.join(datapath, lang1_file)
        lang2_path = os.path.join(datapath, lang2_file)

        with open(lang1_path, encoding="utf-8") as f1, open(lang2_path, encoding="utf-8") as f2:
            for sentence_counter, (x, y) in enumerate(zip(f1, f2)):
                x = x.strip()
                y = y.strip()
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "translation": {lang1: x, lang2: y},
                    },
                )
                yield result
