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
"""Bianet: A parallel news corpus in Turkish, Kurdish and English"""


import os

import datasets


_CITATION = """\
@InProceedings{ATAMAN18.6,
  author = {Duygu Ataman},
  title = {Bianet: A Parallel News Corpus in Turkish, Kurdish and English},
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
  year = {2018},
  month = {may},
  date = {7-12},
  location = {Miyazaki, Japan},
  editor = {Jinhua Du and Mihael Arcan and Qun Liu and Hitoshi Isahara},
  publisher = {European Language Resources Association (ELRA)},
  address = {Paris, France},
  isbn = {979-10-95546-15-3},
  language = {english}
  }"""

_HOMEPAGE = "http://opus.nlpl.eu/Bianet.php"


_LICENSE = "CC-BY-SA-4.0"

_VALID_LANGUAGE_PAIRS = {
    ("en", "ku"): "http://opus.nlpl.eu/download.php?f=Bianet/v1/moses/en-ku.txt.zip",
    ("en", "tr"): "http://opus.nlpl.eu/download.php?f=Bianet/v1/moses/en-tr.txt.zip",
    ("ku", "tr"): "http://opus.nlpl.eu/download.php?f=Bianet/v1/moses/ku-tr.txt.zip",
}

_VERSION = "1.0.0"

_DESCRIPTION = """\
A parallel news corpus in Turkish, Kurdish and English.
Bianet collects 3,214 Turkish articles with their sentence-aligned Kurdish or English translations from the Bianet online newspaper.
3 languages, 3 bitexts
total number of files: 6
total number of tokens: 2.25M
total number of sentence fragments: 0.14M
"""

_BASE_NAME = "Bianet.{}-{}.{}"


class BianetConfig(datasets.BuilderConfig):
    """BuilderConfig for Bianet: A parallel news corpus in Turkish, Kurdish and English"""

    def __init__(self, language_pair=(None, None), **kwargs):
        """BuilderConfig for Bianet: A parallel news corpus in Turkish, Kurdish and English.
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
        super(BianetConfig, self).__init__(
            name=name, description=description, version=datasets.Version(_VERSION, ""), **kwargs
        )

        # Validate language pair.
        assert language_pair in _VALID_LANGUAGE_PAIRS, (
            "Config language pair (%s, " "%s) not supported"
        ) % language_pair

        self.language_pair = language_pair


class Bianet(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        BianetConfig(
            language_pair=pair,
        )
        for pair in _VALID_LANGUAGE_PAIRS.keys()
    ]

    BUILDER_CONFIG_CLASS = BianetConfig

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
