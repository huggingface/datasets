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
"""HateSpeech Corpus for Polish"""


import csv

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = r"""\
@article{troszynski2017czy,
  title={Czy komputer rozpozna hejtera? Wykorzystanie uczenia maszynowego (ML) w jako{\'s}ciowej analizie danych},
  author={Troszy{\'n}ski, Marek and Wawer, Aleksandra},
  journal={Przegl{\k{a}}d Socjologii Jako{\'s}ciowej},
  volume={13},
  number={2},
  pages={62--80},
  year={2017},
  publisher={Uniwersytet {\L}{\'o}dzki, Wydzia{\l} Ekonomiczno-Socjologiczny, Katedra Socjologii~…}
}
"""

_DESCRIPTION = """\
HateSpeech corpus in the current version contains over 2000 posts crawled from public Polish web. They represent various types and degrees of offensive language, expressed toward minorities (eg. ethnical, racial). The data were annotated manually.
"""

_HOMEPAGE = "http://zil.ipipan.waw.pl/HateSpeech"

_LICENSE = "CC BY-NC-SA"

_URLs = [
    "https://raw.githubusercontent.com/aiembassy/hatespeech-corpus-pl/master/data/fragment_anotatora_2011_ZK.csv",
    "https://raw.githubusercontent.com/aiembassy/hatespeech-corpus-pl/master/data/fragment_anotatora_2011b.csv",
    "https://raw.githubusercontent.com/aiembassy/hatespeech-corpus-pl/master/data/fragment_anotatora_2012_luty.csv",
]


class HateSpeechPl(datasets.GeneratorBasedBuilder):
    """HateSpeech Corpus for Polish"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("uint16"),
                    "text_id": datasets.Value("uint32"),
                    "annotator_id": datasets.Value("uint8"),
                    "minority_id": datasets.Value("uint8"),
                    "negative_emotions": datasets.Value("bool"),
                    "call_to_action": datasets.Value("bool"),
                    "source_of_knowledge": datasets.Value("uint8"),
                    "irony_sarcasm": datasets.Value("bool"),
                    "topic": datasets.Value("uint8"),
                    "text": datasets.Value("string"),
                    "rating": datasets.Value("uint8"),
                }
            ),
            supervised_keys=None,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs
        filepaths = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepaths": filepaths,
                },
            ),
        ]

    def _generate_examples(self, filepaths):
        """Yields examples."""
        for file_id_, filepath in enumerate(filepaths):
            with open(filepath, encoding="utf-8") as f:
                csv_reader = csv.DictReader(f, delimiter=",", escapechar="\\")
                for id_, data in enumerate(csv_reader):
                    yield f"{file_id_}/{id_}", {
                        "id": data["id_fragmentu"],
                        "text_id": data["id_tekstu"],
                        "annotator_id": data["id_anotatora"],
                        "minority_id": data["id_mniejszosci"],
                        "negative_emotions": data["negatywne_emocje"],
                        "call_to_action": data["wezw_ddzial"],
                        "source_of_knowledge": data["typ_ramki"],
                        "irony_sarcasm": data["ironia_sarkazm"],
                        "topic": data["temat"],
                        "text": data["tekst"],
                        "rating": data["ocena"],
                    }
