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
"""The Spanish Billion Words Corpus."""


import os

import datasets


_CITATION = """\
@misc{cardellinoSBWCE,
     author = {Cardellino, Cristian},
     title = {Spanish {B}illion {W}ords {C}orpus and {E}mbeddings},
     url = {https://crscardellino.github.io/SBWCE/},
     month = {August},
     year = {2019}
}
"""

_DESCRIPTION = """\
An unannotated Spanish corpus of nearly 1.5 billion words, compiled from different resources from the web.
This resources include the spanish portions of SenSem, the Ancora Corpus, some OPUS Project Corpora and the Europarl,
the Tibidabo Treebank, the IULA Spanish LSP Treebank, and dumps from the Spanish Wikipedia, Wikisource and Wikibooks.
This corpus is a compilation of 100 text files. Each line of these files represents one of the 50 million sentences from the corpus.
"""

_HOMEPAGE = "https://crscardellino.github.io/SBWCE/"

_LICENSE = "https://creativecommons.org/licenses/by-sa/4.0/"

_URL = "http://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/clean_corpus.tar.bz2"


class SpanishBillionWords(datasets.GeneratorBasedBuilder):
    """The Spanish Billion Words Corpus."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="corpus",
            version=VERSION,
            description="100 text files where each line represents a sentence from the corpus",
        ),
    ]

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
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"directory": os.path.join(data_dir, "spanish_billion_words")}
            )
        ]

    def _generate_examples(self, directory):
        """Yields examples."""
        files = os.listdir(directory)
        files = sorted(files)
        _id = 0

        for file in files:
            file_path = os.path.join(directory, file)
            with open(file_path, mode="r", encoding="utf-8") as f:
                for line in f:
                    yield _id, {"text": line.strip()}
                    _id += 1
