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
"""MultiEURLEX - A multi-lingual and multi-label legal document classification dataset."""


import json
import os

import datasets


_CITATION = """\
@InProceedings{chalkidis-etal-2021-multieurlex,
  author = {Chalkidis, Ilias
                and Fergadiotis, Manos
                and Androutsopoulos, Ion},
  title = {MultiEURLEX -- A multi-lingual and multi-label legal document
               classification dataset for zero-shot cross-lingual transfer},
  booktitle = {Proceedings of the 2021 Conference on Empirical Methods
               in Natural Language Processing},
  year = {2021},
  publisher = {Association for Computational Linguistics},
  location = {Punta Cana, Dominican Republic},
}"""

_DESCRIPTION = """\
MultiEURLEX comprises 65k EU laws in 23 official EU languages (some low-ish resource).
Each EU law has been annotated with EUROVOC concepts (labels) by the Publication Office of EU.
As with the English EURLEX, the goal is to predict the relevant EUROVOC concepts (labels);
this is multi-label classification task (given the text, predict multiple labels).
"""

DATA_URL = "https://zenodo.org/record/5363165/files/multi_eurlex.tar.gz"

_LANGUAGES = [
    "en",
    "da",
    "de",
    "nl",
    "sv",
    "bg",
    "cs",
    "hr",
    "pl",
    "sk",
    "sl",
    "es",
    "fr",
    "it",
    "pt",
    "ro",
    "et",
    "fi",
    "hu",
    "lt",
    "lv",
    "el",
    "mt",
]


class MultiEURLEXConfig(datasets.BuilderConfig):
    """BuilderConfig for MultiEURLEX."""

    def __init__(self, language: str, languages=None, label_level="level_1", **kwargs):
        """BuilderConfig for MultiEURLEX.

        Args:
        language: One of ar,bg,de,el,en,es,fr,hi,ru,sw,th,tr,ur,vi,zh, or all_languages
          **kwargs: keyword arguments forwarded to super.
        """
        super(MultiEURLEXConfig, self).__init__(**kwargs)
        self.language = language
        self.label_level = label_level
        if language != "all_languages":
            self.languages = [language]
        else:
            self.languages = languages if languages is not None else _LANGUAGES


class MultiEURLEX(datasets.GeneratorBasedBuilder):
    """MultiEURLEX - A multi-lingual and multi-label legal document classification dataset. Version 1.0"""

    VERSION = datasets.Version("1.0.0", "")
    BUILDER_CONFIG_CLASS = MultiEURLEXConfig
    BUILDER_CONFIGS = [
        MultiEURLEXConfig(
            name=lang,
            language=lang,
            version=datasets.Version("1.0.0", ""),
            description=f"Plain text import of MultiEURLEX for the {lang} language",
        )
        for lang in _LANGUAGES
    ] + [
        MultiEURLEXConfig(
            name="all_languages",
            language="all_languages",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of MultiEURLEX for all languages",
        )
    ]

    def _info(self):
        if self.config.language == "all_languages":
            features = datasets.Features(
                {
                    "celex_id": datasets.Value("string"),
                    "text": datasets.Translation(languages=_LANGUAGES,),
                    "labels": datasets.features.Sequence(datasets.Value("string")),
                }
            )
        else:
            features = datasets.Features(
                {
                    "celex_id": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "labels": datasets.features.Sequence(datasets.Value("string")),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://github.io/iliaschalkidis",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(DATA_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "train.jsonl"), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "dev.jsonl"), "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """This function returns the examples in the raw (text) form."""

        if self.config.language == "all_languages":
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    yield id_, {
                        "celex_id": data["celex_id"],
                        "text": {lang: data["text"][lang] for lang in self.config.languages},
                        "labels": data["eurovoc_concepts"][self.config.label_level],
                    }
        else:
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    if data["text"][self.config.language] is not None:
                        yield id_, {
                            "celex_id": data["celex_id"],
                            "text": data["text"][self.config.language],
                            "labels": data["eurovoc_concepts"][self.config.label_level],
                        }
