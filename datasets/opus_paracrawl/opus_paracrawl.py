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
Parallel corpora from Web Crawls collected in the ParaCrawl project.

42 languages, 43 bitexts
total number of files: 59,996
total number of tokens: 56.11G
total number of sentence fragments: 3.13G
"""
_HOMEPAGE = "http://opus.nlpl.eu/ParaCrawl.php"
_CITATION = r"""\
@inproceedings{banon-etal-2020-paracrawl,
    title = "{P}ara{C}rawl: Web-Scale Acquisition of Parallel Corpora",
    author = "Ba{\~n}{\'o}n, Marta  and
      Chen, Pinzhen  and
      Haddow, Barry  and
      Heafield, Kenneth  and
      Hoang, Hieu  and
      Espl{\`a}-Gomis, Miquel  and
      Forcada, Mikel L.  and
      Kamran, Amir  and
      Kirefu, Faheem  and
      Koehn, Philipp  and
      Ortiz Rojas, Sergio  and
      Pla Sempere, Leopoldo  and
      Ram{\'\i}rez-S{\'a}nchez, Gema  and
      Sarr{\'\i}as, Elsa  and
      Strelec, Marek  and
      Thompson, Brian  and
      Waites, William  and
      Wiggins, Dion  and
      Zaragoza, Jaume",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.acl-main.417",
    doi = "10.18653/v1/2020.acl-main.417",
    pages = "4555--4567",
}
@InProceedings{TIEDEMANN12.463,
  author = {Jörg Tiedemann},
  title = {Parallel Data, Tools and Interfaces in OPUS},
  booktitle = {Proceedings of the Eight International Conference on Language Resources and Evaluation (LREC'12)},
  year = {2012},
  month = {may},
  date = {23-25},
  address = {Istanbul, Turkey},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Mehmet Uğur Doğan and Bente Maegaard and Joseph Mariani and Asuncion Moreno and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  isbn = {978-2-9517408-7-7},
  language = {english}
}
"""

_VERSION = "9.0.0"
_BASE_NAME = "ParaCrawl.{}.{}"
_BASE_URL = "https://object.pouta.csc.fi/OPUS-ParaCrawl/v9/moses/{}-{}.txt.zip"
# Please note that only few pairs are shown here. You can use config to generate data for all language pairs
_LANGUAGE_PAIRS = [
    ("el", "en"),
    ("en", "km"),
    ("en", "so"),
    ("de", "pl"),
    ("fr", "nl"),
    ("en", "sw"),
    ("en", "tl"),
    ("es", "gl"),
]


class ParaCrawlConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        assert lang1 != lang2, "'language 1' & 'language 2' should be different from each other"
        self.lang1 = lang1
        self.lang2 = lang2


class OpusParaCrawl(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        ParaCrawlConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = ParaCrawlConfig

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
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        download_url = _BASE_URL.format(self.config.lang1, self.config.lang2)
        path = dl_manager.download_and_extract(download_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    def _generate_examples(self, datapath):
        lang1, lang2 = self.config.lang1, self.config.lang2
        folder = lang1 + "-" + lang2
        lang1_filename = _BASE_NAME.format(folder, lang1)
        lang2_filename = _BASE_NAME.format(folder, lang2)
        lang1_path = os.path.join(datapath, lang1_filename)
        lang2_path = os.path.join(datapath, lang2_filename)
        with open(lang1_path, encoding="utf-8") as f1, open(lang2_path, encoding="utf-8") as f2:
            for id_, (lang1_sentence, lang2_sentence) in enumerate(zip(f1, f2)):
                lang1_sentence = lang1_sentence.strip()
                lang2_sentence = lang2_sentence.strip()
                yield id_, {
                    "id": str(id_),
                    "translation": {lang1: lang1_sentence, lang2: lang2_sentence},
                }
