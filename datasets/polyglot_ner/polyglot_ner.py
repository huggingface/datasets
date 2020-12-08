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
"""The Polyglot-NER Dataset."""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """\
@article{polyglotner,
         author = {Al-Rfou, Rami and Kulkarni, Vivek and Perozzi, Bryan and Skiena, Steven},
         title = {{Polyglot-NER}: Massive Multilingual Named Entity Recognition},
         journal = {{Proceedings of the 2015 {SIAM} International Conference on Data Mining, Vancouver, British Columbia, Canada, April 30- May 2, 2015}},
         month     = {April},
         year      = {2015},
         publisher = {SIAM},
}
"""

_LANGUAGES = [
    "ca",
    "de",
    "es",
    "fi",
    "hi",
    "id",
    "ko",
    "ms",
    "pl",
    "ru",
    "sr",
    "tl",
    "vi",
    "ar",
    "cs",
    "el",
    "et",
    "fr",
    "hr",
    "it",
    "lt",
    "nl",
    "pt",
    "sk",
    "sv",
    "tr",
    "zh",
    "bg",
    "da",
    "en",
    "fa",
    "he",
    "hu",
    "ja",
    "lv",
    "no",
    "ro",
    "sl",
    "th",
    "uk",
]

_LANG_FILEPATHS = {
    lang: os.path.join(
        "acl_datasets",
        lang,
        "data" if lang != "zh" else "",  # they're all lang/data/lang_wiki.conll except "zh"
        f"{lang}_wiki.conll",
    )
    for lang in _LANGUAGES
}

_DESCRIPTION = """\
Polyglot-NER
A training dataset automatically generated from Wikipedia and Freebase the task
of named entity recognition. The dataset contains the basic Wikipedia based
training data for 40 languages we have (with coreference resolution) for the task of
named entity recognition. The details of the procedure of generating them is outlined in
Section 3 of the paper (https://arxiv.org/abs/1410.3791). Each config contains the data
corresponding to a different language. For example, "es" includes only spanish examples.
"""

_DATA_URL = "http://cs.stonybrook.edu/~polyglot/ner2/emnlp_datasets.tgz"
_HOMEPAGE_URL = "https://sites.google.com/site/rmyeid/projects/polylgot-ner"
_VERSION = "1.0.0"

_COMBINED = "combined"


class PolyglotNERConfig(datasets.BuilderConfig):
    def __init__(self, *args, languages=None, **kwargs):
        super().__init__(*args, version=datasets.Version(_VERSION, ""), **kwargs)
        self.languages = languages

    @property
    def filepaths(self):
        return [_LANG_FILEPATHS[lang] for lang in self.languages]


class PolyglotNER(datasets.GeneratorBasedBuilder):
    """The Polyglot-NER Dataset"""

    BUILDER_CONFIGS = [
        PolyglotNERConfig(name=lang, languages=[lang], description=f"Polyglot-NER examples in {lang}.")
        for lang in _LANGUAGES
    ] + [
        PolyglotNERConfig(
            name=_COMBINED, languages=_LANGUAGES, description=f"Complete Polyglot-NER dataset with all languages."
        )
    ]

    DEFAULT_CONFIG_NAME = _COMBINED

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "lang": datasets.Value("string"),
                    "words": datasets.Sequence(datasets.Value("string")),
                    "ner": datasets.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        path = dl_manager.download_and_extract(_DATA_URL)

        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"datapath": path})]

    def _generate_examples(self, datapath):
        sentence_counter = 0
        for filepath, lang in zip(self.config.filepaths, self.config.languages):
            filepath = os.path.join(datapath, filepath)
            with open(filepath, encoding="utf-8") as f:
                current_words = []
                current_ner = []
                for row in f:
                    row = row.rstrip()
                    if row:
                        token, label = row.split("\t")
                        current_words.append(token)
                        current_ner.append(label)
                    else:
                        # New sentence
                        if not current_words:
                            # Consecutive empty lines will cause empty sentences
                            continue
                        assert len(current_words) == len(current_ner), "💔 between len of words & ner"
                        sentence = (
                            sentence_counter,
                            {
                                "id": str(sentence_counter),
                                "lang": lang,
                                "words": current_words,
                                "ner": current_ner,
                            },
                        )
                        sentence_counter += 1
                        current_words = []
                        current_ner = []
                        yield sentence
                # Don't forget last sentence in dataset 🧐
                if current_words:
                    yield sentence_counter, {
                        "id": str(sentence_counter),
                        "lang": lang,
                        "words": current_words,
                        "ner": current_ner,
                    }
