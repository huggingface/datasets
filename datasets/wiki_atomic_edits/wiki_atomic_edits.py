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
import datasets


_CITATION = """\
@InProceedings{WikiAtomicEdits,
  title = {{WikiAtomicEdits: A Multilingual Corpus of Wikipedia Edits for Modeling Language and Discourse}},
  author = {Faruqui, Manaal and Pavlick, Ellie and Tenney, Ian and Das, Dipanjan},
  booktitle = {Proc. of EMNLP},
  year = {2018}
}
"""

_DESCRIPTION = """\
A dataset of atomic wikipedia edits containing insertions and deletions of a contiguous chunk of text in a sentence. This dataset contains ~43 million edits across 8 languages.

An atomic edit is defined as an edit e applied to a natural language expression S as the insertion, deletion, or substitution of a sub-expression P such that both the original expression S and the resulting expression e(S) are well-formed semantic constituents (MacCartney, 2009). In this corpus, we release such atomic insertions and deletions made to sentences in wikipedia.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/wiki-atomic-edits"
_VERSION = "1.0.0"

_URL = {
    "german": {
        "insertions": "https://storage.googleapis.com/wiki-atomic-edits/german/insertions.tsv.gz",
        "deletions": "https://storage.googleapis.com/wiki-atomic-edits/german/deletions.tsv.gz",
    },
    "english": {
        "insertions": "https://storage.googleapis.com/wiki-atomic-edits/english/insertions.tsv.gz",
        "deletions": "https://storage.googleapis.com/wiki-atomic-edits/english/deletions.tsv.gz",
    },
    "spanish": {
        "insertions": "https://storage.googleapis.com/wiki-atomic-edits/spanish/insertions.tsv.gz",
        "deletions": "https://storage.googleapis.com/wiki-atomic-edits/spanish/deletions.tsv.gz",
    },
    "french": {
        "insertions": "https://storage.googleapis.com/wiki-atomic-edits/french/insertions.tsv.gz",
        "deletions": "https://storage.googleapis.com/wiki-atomic-edits/french/deletions.tsv.gz",
    },
    "italian": {
        "insertions": "https://storage.googleapis.com/wiki-atomic-edits/italian/insertions.tsv.gz",
        "deletions": "https://storage.googleapis.com/wiki-atomic-edits/italian/deletions.tsv.gz",
    },
    "japanese": {
        "insertions": "https://storage.googleapis.com/wiki-atomic-edits/japanese/insertions.tsv.gz",
        "deletions": "https://storage.googleapis.com/wiki-atomic-edits/japanese/deletions.tsv.gz",
    },
    "russian": {
        "insertions": "https://storage.googleapis.com/wiki-atomic-edits/russian/insertions.tsv.gz",
        "deletions": "https://storage.googleapis.com/wiki-atomic-edits/russian/deletions.tsv.gz",
    },
    "chinese": {
        "insertions": "https://storage.googleapis.com/wiki-atomic-edits/chinese/insertions.tsv.gz",
        "deletions": "https://storage.googleapis.com/wiki-atomic-edits/chinese/deletions.tsv.gz",
    },
}

_LANG_EDITS = [
    ("german", "insertions"),
    ("german", "deletions"),
    ("english", "insertions"),
    ("english", "deletions"),
    ("spanish", "insertions"),
    ("spanish", "deletions"),
    ("french", "insertions"),
    ("french", "deletions"),
    ("italian", "insertions"),
    ("italian", "deletions"),
    ("japanese", "insertions"),
    ("japanese", "deletions"),
    ("russian", "insertions"),
    ("russian", "deletions"),
    ("chinese", "insertions"),
    ("chinese", "deletions"),
]


class WikiAtomicEditsConfig(datasets.BuilderConfig):
    def __init__(self, *args, language=None, edit_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = language
        self.edit_type = edit_type


class WikiAtomicEdits(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        WikiAtomicEditsConfig(
            name=f"{lang}_{edit_type}",
            language=lang,
            edit_type=edit_type,
            description=f"Language: {lang}, Edit type: {edit_type}",
            version=datasets.Version(_VERSION),
        )
        for lang, edit_type in _LANG_EDITS
    ]
    BUILDER_CONFIG_CLASS = WikiAtomicEditsConfig

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "base_sentence": datasets.Value("string"),
                    "phrase": datasets.Value("string"),
                    "edited_sentence": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        datapath = dl_manager.download_and_extract(_URL[self.config.language][self.config.edit_type])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": datapath},
            )
        ]

    def _generate_examples(self, datapath):
        with open(datapath, "r", encoding="utf-8") as data_file:
            next(data_file)
            for sentence_counter, sent in enumerate(data_file):
                sent = sent.split("\t")
                res = {
                    "id": sentence_counter,
                    "base_sentence": sent[0],
                    "phrase": sent[1],
                    "edited_sentence": sent[2],
                }
                yield sentence_counter, res
