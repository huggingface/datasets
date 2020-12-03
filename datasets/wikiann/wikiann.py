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

"""The WikiANN dataset for multilingual named entity recognition"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """@inproceedings{pan-etal-2017-cross,
    title = "Cross-lingual Name Tagging and Linking for 282 Languages",
    author = "Pan, Xiaoman  and
      Zhang, Boliang  and
      May, Jonathan  and
      Nothman, Joel  and
      Knight, Kevin  and
      Ji, Heng",
    booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P17-1178",
    doi = "10.18653/v1/P17-1178",
    pages = "1946--1958",
    abstract = "The ambitious goal of this work is to develop a cross-lingual name tagging and linking framework for 282 languages that exist in Wikipedia. Given a document in any of these languages, our framework is able to identify name mentions, assign a coarse-grained or fine-grained type to each mention, and link it to an English Knowledge Base (KB) if it is linkable. We achieve this goal by performing a series of new KB mining methods: generating {``}silver-standard{''} annotations by transferring annotations from English to other languages through cross-lingual links and KB properties, refining annotations through self-training and topic selection, deriving language-specific morphology features from anchor links, and mining word translation pairs from cross-lingual links. Both name tagging and linking results for 282 languages are promising on Wikipedia data and on-Wikipedia data.",
}"""

_DESCRIPTION = """WikiANN (sometimes called PAN-X) is a multilingual named entity recognition dataset consisting of Wikipedia articles annotated with LOC (location), PER (person), and ORG (organisation) tags in the IOB2 format. This version corresponds to the balanced train, dev, and test splits of Rahimi et al. (2019), which supports 176 of the 282 languages from the original WikiANN corpus."""

# use ?dl=1 to force browser to download data instead of displaying it
_DATA_URL = "https://www.dropbox.com/s/12h3qqog6q4bjve/panx_dataset.tar?dl=1"
_HOMEPAGE = "https://github.com/afshinrahimi/mmner"
_VERSION = "1.1.0"
_LANGS = [
    "ace",
    "af",
    "als",
    "am",
    "an",
    "ang",
    "ar",
    "arc",
    "arz",
    "as",
    "ast",
    "ay",
    "az",
    "ba",
    "bar",
    "bat-smg",
    "be",
    "be-x-old",
    "bg",
    "bh",
    "bn",
    "bo",
    "br",
    "bs",
    "ca",
    "cbk-zam",
    "cdo",
    "ce",
    "ceb",
    "ckb",
    "co",
    "crh",
    "cs",
    "csb",
    "cv",
    "cy",
    "da",
    "de",
    "diq",
    "dv",
    "el",
    "eml",
    "en",
    "eo",
    "es",
    "et",
    "eu",
    "ext",
    "fa",
    "fi",
    "fiu-vro",
    "fo",
    "fr",
    "frr",
    "fur",
    "fy",
    "ga",
    "gan",
    "gd",
    "gl",
    "gn",
    "gu",
    "hak",
    "he",
    "hi",
    "hr",
    "hsb",
    "hu",
    "hy",
    "ia",
    "id",
    "ig",
    "ilo",
    "io",
    "is",
    "it",
    "ja",
    "jbo",
    "jv",
    "ka",
    "kk",
    "km",
    "kn",
    "ko",
    "ksh",
    "ku",
    "ky",
    "la",
    "lb",
    "li",
    "lij",
    "lmo",
    "ln",
    "lt",
    "lv",
    "map-bms",
    "mg",
    "mhr",
    "mi",
    "min",
    "mk",
    "ml",
    "mn",
    "mr",
    "ms",
    "mt",
    "mwl",
    "my",
    "mzn",
    "nap",
    "nds",
    "ne",
    "nl",
    "nn",
    "no",
    "nov",
    "oc",
    "or",
    "os",
    "pa",
    "pdc",
    "pl",
    "pms",
    "pnb",
    "ps",
    "pt",
    "qu",
    "rm",
    "ro",
    "ru",
    "rw",
    "sa",
    "sah",
    "scn",
    "sco",
    "sd",
    "sh",
    "si",
    "simple",
    "sk",
    "sl",
    "so",
    "sq",
    "sr",
    "su",
    "sv",
    "sw",
    "szl",
    "ta",
    "te",
    "tg",
    "th",
    "tk",
    "tl",
    "tr",
    "tt",
    "ug",
    "uk",
    "ur",
    "uz",
    "vec",
    "vep",
    "vi",
    "vls",
    "vo",
    "wa",
    "war",
    "wuu",
    "xmf",
    "yi",
    "yo",
    "zea",
    "zh",
    "zh-classical",
    "zh-min-nan",
    "zh-yue",
]


class WikiannConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super(WikiannConfig, self).__init__(version=datasets.Version(_VERSION, ""), **kwargs)


class Wikiann(datasets.GeneratorBasedBuilder):
    """WikiANN is a multilingual named entity recognition dataset consisting of Wikipedia articles annotated with LOC, PER, and ORG tags"""

    VERSION = datasets.Version(_VERSION)
    # use two-letter ISO 639-1 language codes as the name for each corpus
    BUILDER_CONFIGS = [
        WikiannConfig(name=lang, description=f"WikiANN NER examples in language {lang}") for lang in _LANGS
    ]

    def _info(self):
        features = datasets.Features(
            {
                "tokens": datasets.Sequence(datasets.Value("string")),
                "ner_tags": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "O",
                            "B-PER",
                            "I-PER",
                            "B-ORG",
                            "I-ORG",
                            "B-LOC",
                            "I-LOC",
                        ]
                    )
                ),
                "langs": datasets.Sequence(datasets.Value("string")),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        wikiann_dl_dir = dl_manager.download_and_extract(_DATA_URL)
        lang = self.config.name
        lang_folder = dl_manager.extract(os.path.join(wikiann_dl_dir, lang + ".tar.gz"))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(lang_folder, "dev")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(lang_folder, "test")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(lang_folder, "train")},
            ),
        ]

    def _generate_examples(self, filepath):
        guid_index = 1
        with open(filepath, encoding="utf-8") as f:
            tokens = []
            ner_tags = []
            langs = []
            for line in f:
                if line.startswith("-DOCSTART-") or line == "" or line == "\n":
                    if tokens:
                        yield guid_index, {"tokens": tokens, "ner_tags": ner_tags, "langs": langs}
                        guid_index += 1
                        tokens = []
                        ner_tags = []
                        langs = []
                else:
                    # wikiann data is tab separated
                    splits = line.split("\t")
                    # strip out en: prefix
                    langs.append(splits[0][:2])
                    tokens.append(splits[0][3:])
                    if len(splits) > 1:
                        ner_tags.append(splits[-1].replace("\n", ""))
                    else:
                        # examples have no label in test set
                        ner_tags.append("O")
