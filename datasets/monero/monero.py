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
"""MoNERo: a Biomedical Gold Standard Corpus for the RomanianLanguage"""

from __future__ import absolute_import, division, print_function

import logging
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{inproceedings,
author = {Mitrofan, Maria and Mititelu, Verginica and Grigorina, Mitrofan},
year = {2019},
month = {01},
pages = {71-79},
title = {MoNERo: a Biomedical Gold Standard Corpus for the Romanian Language},
doi = {10.18653/v1/W19-5008}
}
"""

# You can copy an official description
_DESCRIPTION = """\
 MoNERo comprises 154,825morphologically annotated tokens and 23,188entity annotations belonging to four entity se-mantic  groups  corresponding  to  UMLS  Se-mantic Groups.
"""

_HOMEPAGE = "https://slp.racai.ro/index.php/resources/monero-3/"

_LICENSE = "MIT License"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://raw.githubusercontent.com/iliemihai/MoNERo/main/"
_CARDIOLOGY_FILE = "MoNERo_cardiology.txt"
_DIABETES_FILE = "MoNERo_diabetes.txt"
_ENDOCRINOLOGY_FILE = "MoNERo_endocrinology.txt"
_MONERO_FILE = "MoNERo.txt"


class MONEROConfig(datasets.BuilderConfig):
    """BuilderConfig for RONEC dataset"""

    def __init__(self, **kwargs):
        super(MONEROConfig, self).__init__(**kwargs)


class MONERODataset(datasets.GeneratorBasedBuilder):
    """RONEC dataset"""

    VERSION = datasets.Version("1.0.0")
    DEFAULT_CONFIG_NAME = "monero"

    BUILDER_CONFIGS = [
        MONEROConfig(name=DEFAULT_CONFIG_NAME, version=VERSION, description="MONERO dataset"),
    ]

    def _info(self):

        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "words": datasets.Sequence(datasets.Value("string")),
                "start": datasets.Sequence(datasets.Value("int32")),
                "end": datasets.Sequence(datasets.Value("int32")),
                "ner": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "O",
                            "ANAT",
                            "CHEM",
                            "DISO",
                            "PROC",
                        ]
                    )
                ),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
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

        urls_to_download = {
            "monero": _URL + _MONERO_FILE,
            "cardiology": _URL + _CARDIOLOGY_FILE,
            "diabetes": _URL + _DIABETES_FILE,
            "endocrinology": _URL + _ENDOCRINOLOGY_FILE,
        }

        downloaded_files = dl_manager.download(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["endocrinology"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["cardiology"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["diabetes"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """

        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            words = []
            ner = []
            start = []
            end = []
            sent = ""
            has_started = False
            for line in f:
                if line == "\n":
                    if sent:
                        words.append(sent)
                        yield guid, {
                            "id": str(guid),
                            "words": words,
                            "start": start,
                            "end": end,
                            "ner": ner,
                        }
                        guid += 1
                        words = []
                        start = []
                        end = []
                        ner = []
                        sent = ""
                else:
                    # ronec words are tab separated
                    line = line.replace("\n", "")
                    splits = line.split("\t")
                    sent += splits[1] + " "

                    if splits[2].startswith("O") and not has_started:
                        continue
                    elif splits[2].startswith("B-"):
                        begin = len(sent) - len(splits[1])
                        last = len(sent)
                        label = splits[2][2:]
                        has_started = True
                    elif splits[2].startswith("I-"):
                        last = len(sent)
                    elif splits[2].startswith("O") and begin:
                        ner.append(label)
                        start.append(begin)
                        end.append(last)
                        has_started = False

            # last example
            yield guid, {
                "id": str(guid),
                "words": words,
                "start": start,
                "end": end,
                "ner": ner,
            }
