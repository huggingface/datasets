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
"""TaPaCo: A Corpus of Sentential Paraphrases for 73 Languages"""


import csv
import os

import datasets


_CITATION = """\
@dataset{scherrer_yves_2020_3707949,
  author       = {Scherrer, Yves},
  title        = {{TaPaCo: A Corpus of Sentential Paraphrases for 73 Languages}},
  month        = mar,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.3707949},
  url          = {https://doi.org/10.5281/zenodo.3707949}
}
"""


_DESCRIPTION = """\
A freely available paraphrase corpus for 73 languages extracted from the Tatoeba database. \
Tatoeba is a crowdsourcing project mainly geared towards language learners. Its aim is to provide example sentences \
and translations for particular linguistic constructions and words. The paraphrase corpus is created by populating a \
graph with Tatoeba sentences and equivalence links between sentences “meaning the same thing”. This graph is then \
traversed to extract sets of paraphrases. Several language-independent filters and pruning steps are applied to \
remove uninteresting sentences. A manual evaluation performed on three languages shows that between half and three \
quarters of inferred paraphrases are correct and that most remaining ones are either correct but trivial, \
or near-paraphrases that neutralize a morphological distinction. The corpus contains a total of 1.9 million \
sentences, with 200 – 250 000 sentences per language. It covers a range of languages for which, to our knowledge,\
no other paraphrase dataset exists."""


_HOMEPAGE = "https://zenodo.org/record/3707949#.X9Dh0cYza3I"


_LICENSE = "Creative Commons Attribution 2.0 Generic"


_URLs = {
    "train": "https://zenodo.org/record/3707949/files/tapaco_v1.0.zip?download=1",
}

_VERSION = "1.0.0"
_LANGUAGES = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "ber": "Berber languages",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "br": "Breton",
    "ca": "Catalan; Valencian",
    "cbk": "Chavacano",
    "cmn": "Mandarin",
    "cs": "Czech",
    "da": "Danish",
    "de": "German",
    "el": "Greek, Modern (1453-)",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish; Castilian",
    "et": "Estonian",
    "eu": "Basque",
    "fi": "Finnish",
    "fr": "French",
    "gl": "Galician",
    "gos": "Gronings",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "ia": "Interlingua (International Auxiliary Language Association)",
    "id": "Indonesian",
    "ie": "Interlingue; Occidental",
    "io": "Ido",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jbo": "Lojban",
    "kab": "Kabyle",
    "ko": "Korean",
    "kw": "Cornish",
    "la": "Latin",
    "lfn": "Lingua Franca Nova\t",
    "lt": "Lithuanian",
    "mk": "Macedonian",
    "mr": "Marathi",
    "nb": "Bokmål, Norwegian; Norwegian Bokmål",
    "nds": "Low German; Low Saxon; German, Low; Saxon, Low",
    "nl": "Dutch; Flemish",
    "orv": "Old Russian",
    "ota": "Turkish, Ottoman (1500-1928)",
    "pes": "Iranian Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "rn": "Rundi",
    "ro": "Romanian; Moldavian; Moldovan",
    "ru": "Russian",
    "sl": "Slovenian",
    "sr": "Serbian",
    "sv": "Swedish",
    "tk": "Turkmen",
    "tl": "Tagalog",
    "tlh": "Klingon; tlhIngan-Hol",
    "toki": "Toki Pona",
    "tr": "Turkish",
    "tt": "Tatar",
    "ug": "Uighur; Uyghur",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "vo": "Volapük",
    "war": "Waray",
    "wuu": "Wu Chinese",
    "yue": "Yue Chinese",
}
_ALL_LANGUAGES = "all_languages"


class TapacoConfig(datasets.BuilderConfig):
    """BuilderConfig for TapacoConfig."""

    def __init__(self, languages=None, **kwargs):
        super(TapacoConfig, self).__init__(version=datasets.Version(_VERSION, ""), **kwargs),
        self.languages = languages


class Tapaco(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        TapacoConfig(
            name=_ALL_LANGUAGES,
            languages=_LANGUAGES,
            description="A collection of paraphrase corpus for 73 languages to aid paraphrase "
            "detection and generation.",
        )
    ] + [
        TapacoConfig(
            name=lang,
            languages=[lang],
            description=f"{_LANGUAGES[lang]} A collection of paraphrase corpus for 73 languages to "
            f"aid paraphrase "
            "detection and generation.",
        )
        for lang in _LANGUAGES
    ]
    BUILDER_CONFIG_CLASS = TapacoConfig
    DEFAULT_CONFIG_NAME = _ALL_LANGUAGES

    def _info(self):
        features = datasets.Features(
            {
                "paraphrase_set_id": datasets.Value("string"),
                "sentence_id": datasets.Value("string"),
                "paraphrase": datasets.Value("string"),
                "lists": datasets.Sequence(datasets.Value("string")),
                "tags": datasets.Sequence(datasets.Value("string")),
                "language": datasets.Value("string"),
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
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_dir": data_dir["train"]},
            ),
        ]

    def _generate_examples(self, data_dir):
        """Yields examples."""
        base_path = os.path.join(data_dir, "tapaco_v1.0")
        file_dict = {lang: os.path.join(base_path, lang + ".txt") for lang in self.config.languages}
        id_ = -1
        for language, filepath in file_dict.items():
            with open(filepath, encoding="utf-8") as csv_file:
                csv_reader = csv.reader(
                    csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_ALL, skipinitialspace=True
                )
                for row in csv_reader:
                    id_ += 1
                    paraphrase_set_id, sentence_id, paraphrase, lists, tags = row[: len(row)] + [""] * (5 - len(row))
                    yield id_, {
                        "paraphrase_set_id": paraphrase_set_id,
                        "sentence_id": sentence_id,
                        "paraphrase": paraphrase,
                        "lists": lists.split(";"),
                        "tags": tags.split(";"),
                        "language": language,
                    }
