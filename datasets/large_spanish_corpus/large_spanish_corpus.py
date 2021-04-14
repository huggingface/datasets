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
"""The Large Spanish Corpus is a compilation of Spanish corpora spanning Wikipedia to European parliament notes."""


import os

import datasets


_CITATION = """\
@dataset{jose_canete_2019_3247731,
  author       = {José Cañete},
  title        = {Compilation of Large Spanish Unannotated Corpora},
  month        = may,
  year         = 2019,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.3247731},
  url          = {https://doi.org/10.5281/zenodo.3247731}
}
"""

_DESCRIPTION = """\
The Large Spanish Corpus is a compilation of 15 unlabelled Spanish corpora spanning Wikipedia to European parliament \
notes. Each config contains the data corresponding to a different corpus. For example, "all_wiki" only includes \
examples from Spanish Wikipedia. By default, the config is set to "combined" which loads all the corpora; with this \
setting you can also specify the number of samples to return per corpus by configuring the "split" argument.
"""

_HOMEPAGE = "https://github.com/josecannete/spanish-corpora"

_LICENSE = "MIT"

_URL = "https://zenodo.org/record/3247731/files/raw.tar.bz2"

_CORPORA = [
    "JRC",
    "EMEA",
    "GlobalVoices",
    "ECB",
    "DOGC",
    "all_wikis",
    "TED",
    "multiUN",
    "Europarl",
    "NewsCommentary11",
    "UN",
    "EUBookShop",
    "ParaCrawl",
    "OpenSubtitles2018",
    "DGT",
]

_CORPORA_FILEPATHS = {corpus: os.path.join("spanish-corpora", "raw", f"{corpus}.txt") for corpus in _CORPORA}

_VERSION = "1.1.0"

_COMBINED = "combined"


class LargeSpanishCorpusConfig(datasets.BuilderConfig):
    def __init__(self, corpora=None, **kwargs):
        super(LargeSpanishCorpusConfig, self).__init__(version=datasets.Version(_VERSION, ""), **kwargs)
        self.corpora = corpora

    @property
    def filepaths(self):
        return [_CORPORA_FILEPATHS[corpus] for corpus in self.corpora]


class LargeSpanishCorpus(datasets.GeneratorBasedBuilder):
    """The Large Spanish Corpus."""

    BUILDER_CONFIGS = [
        LargeSpanishCorpusConfig(name=corpus, corpora=[corpus], description=f"Spanish examples in corpus {corpus}.")
        for corpus in _CORPORA
    ] + [
        LargeSpanishCorpusConfig(
            name=_COMBINED, corpora=_CORPORA, description="Complete Spanish dataset with all corpora."
        )
    ]
    BUILDER_CONFIG_CLASS = LargeSpanishCorpusConfig
    DEFAULT_CONFIG_NAME = _COMBINED

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URL)
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"data_dir": data_dir})]

    def _generate_examples(self, data_dir):
        for filepath in self.config.filepaths:
            filepath = os.path.join(data_dir, filepath)
            _id = 0
            with open(filepath, mode="r", encoding="utf-8") as f:
                for line in f:
                    yield _id, {"text": line.strip()},
                    _id += 1
