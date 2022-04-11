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
""" Middle Egyptian dataset as used in the paper  """
import json

import datasets


_CITATION = """\
@misc{OPUS4-2919,
title  = {Teilauszug der Datenbank des Vorhabens "Strukturen und Transformationen des Wortschatzes der {\"a}gyptischen Sprache" vom Januar 2018},
institution = {Akademienvorhaben Strukturen und Transformationen des Wortschatzes der {\"a}gyptischen Sprache. Text- und Wissenskultur im alten {\"A}gypten},
type = {other},
year = {2018},
}
"""

_DESCRIPTION = """\
This dataset comprises parallel sentences of hieroglyphic encodings, transcription and translation
as used in the paper Multi-Task Modeling of Phonographic Languages: Translating Middle Egyptian
Hieroglyph. The data triples are extracted from the digital corpus of Egyptian texts compiled by
the project "Strukturen und Transformationen des Wortschatzes der ägyptischen Sprache".
"""

_HOMEPAGE = "https://edoc.bbaw.de/frontdoor/index/index/docId/2919"

_LICENSE = "Creative Commons-Lizenz - CC BY-SA - 4.0 International"


class BbawEgyptian(datasets.GeneratorBasedBuilder):
    """
    The project `Strukturen und Transformationen des Wortschatzes der ägyptischen Sprache`
    is compiling an extensively annotated digital corpus of Egyptian texts.
    This publication comprises an excerpt of the internal database's contents.
    """

    _URL = "https://phiwi.github.io/"
    _URLS = {"all": _URL + "all.json"}

    def _info(self):
        features = datasets.Features(
            {
                "transcription": datasets.Value("string"),
                "translation": datasets.Value("string"),
                "hieroglyphs": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = self._URLS
        data_dir = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_dir["all"]},
            )
        ]

    def _generate_examples(self, filepath):
        """Yields examples as (key, example) tuples."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for id_, row in enumerate(data):
            yield id_, {
                "translation": row["translation"],
                "transcription": row["transcription"],
                "hieroglyphs": row["hieroglyphs"],
            }
