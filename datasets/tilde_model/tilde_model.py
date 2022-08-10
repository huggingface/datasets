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
This is the Tilde MODEL Corpus – Multilingual Open Data for European Languages.

The data has been collected from sites allowing free use and reuse of its content, as well as from Public Sector web sites. The activities have been undertaken as part of the ODINE Open Data Incubator for Europe, which aims to support the next generation of digital businesses and fast-track the development of new products and services. The corpus includes the following parts:
Tilde MODEL - EESC is a multilingual corpus compiled from document texts of European Economic and Social Committee document portal. Source: http://dm.eesc.europa.eu/
Tilde MODEL - RAPID multilingual parallel corpus is compiled from all press releases of Press Release Database of European Commission released between 1975 and end of 2016 as available from http://europa.eu/rapid/
Tilde MODEL - ECB multilingual parallel corpus is compiled from the multilingual pages of European Central Bank web site http://ebc.europa.eu/
Tilde MODEL - EMA is a corpus compiled from texts of European Medicines Agency document portal as available in http://www.ema.europa.eu/ at the end of 2016
Tilde MODEL - World Bank is a corpus compiled from texts of World Bank as available in http://www.worldbank.org/ in 2017
Tilde MODEL - AirBaltic.com Travel Destinations is a multilingual parallel corpus compiled from description texts of AirBaltic.com travel destinations as available in https://www.airbaltic.com/en/destinations/ in 2017
Tilde MODEL - LiveRiga.com is a multilingual parallel corpus compiled from Riga tourist attractions description texts of http://liveriga.com/ web site in 2017
Tilde MODEL - Lithuanian National Philharmonic Society is a parallel corpus compiled from texts of Lithuanian National Philharmonic Society web site http://www.filharmonija.lt/ in 2017
Tilde MODEL - mupa.hu is a parallel corpus from texts of Müpa Budapest - web site of Hungarian national culture house and concert venue https://www.mupa.hu/en/ compiled in spring of 2017
Tilde MODEL - fold.lv is a parallel corpus from texts of fold.lv portal http://www.fold.lv/en/ of the best of Latvian and foreign creative industries as compiled in spring of 2017
Tilde MODEL - czechtourism.com is a multilingual parallel corpus from texts of http://czechtourism.com/ portal compiled in spring of 2017
30 languages, 274 bitexts
total number of files: 125
total number of tokens: 1.43G
total number of sentence fragments: 62.44M
"""
_HOMEPAGE_URL = "http://opus.nlpl.eu/TildeMODEL.php"
_CITATION = """\
Roberts Rozis, Raivis Skadins, 2017, Tilde MODEL - Multilingual Open Data for EU Languages. Proceedings of the 21th Nordic Conference of Computational Linguistics NODALIDA 2017
"""

_VERSION = "2018.0.0"
_BASE_NAME = "TildeMODEL.{}.{}"
_BASE_URL = "https://object.pouta.csc.fi/OPUS-TildeMODEL/v2018/moses/{}-{}.txt.zip"

# Please note that only few pairs are shown here. You can use config to generate data for all language pairs
_LANGUAGE_PAIRS = [
    ("bg", "el"),
    ("cs", "en"),
    ("de", "hr"),
    ("en", "no"),
    ("es", "pt"),
]


class TildeModelConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class TildeModel(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        TildeModelConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = TildeModelConfig

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
