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
"""TODO: Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
authors={huggingface, Inc.
},
year={2020}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to solve this great NLP task and is crafted with a lot of care. 
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = ""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://zenodo.org/record/3247731/files/raw.tar.bz2"

_CORPORA = ['JRC',
 'EMEA',
 'GlobalVoices',
 'ECB',
 'DOGC',
 'all_wikis',
 'TED',
 'multiUN',
 'Europarl',
 'NewsCommentary11',
 'UN',
 'EUBookShop',
 'ParaCrawl',
 'OpenSubtitles2018',
 'DGT']

_CORPORA_FILEPATHS = {
     corpus: os.path.join(
        "spanish-corpora/raw",
        f"{corpus}.txt"
        )
        for corpus in _CORPORA
        }

_VERSION = "1.1.0"

_COMBINED = "combined"

class LargeSpanishCorpusConfig(datasets.BuilderConfig):
    def __init__(self, corpora=None, **kwargs):
        super(LargeSpanishCorpusConfig, self).__init__(version=datasets.Version(_VERSION, ""), **kwargs)
        self.corpora = corpora

    @property
    def filepaths(self):
        return [_CORPORA_FILEPATHS[corpus] for corpus in self.corpora]


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class LargeSpanishCorpus(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    BUILDER_CONFIGS = [
        LargeSpanishCorpusConfig(name=corpus, corpora=[corpus], description=f"Spanish examples in corpus {corpus}.")
        for corpus in _CORPORA
    ] + [
        LargeSpanishCorpusConfig(
            name=_COMBINED, corpora=_CORPORA, description=f"Complete Spanish dataset with all corpora."
        )
    ]

    DEFAULT_CONFIG_NAME = _COMBINED

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive 
        data_dir = dl_manager.download_and_extract(_URL)
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"data_dir": data_dir})]

    def _generate_examples(self, data_dir):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        _id = 0
        print(self.config.filepaths)
        for filepath, corpus in zip(self.config.filepaths, self.config.corpora):
            filepath = os.path.join(data_dir, filepath)
            with open(filepath, mode='r', encoding="utf-8") as f:
                yield _id, {"title": corpus, "text": f.read()},
                _id += 1
