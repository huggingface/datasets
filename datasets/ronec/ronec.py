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
"""Introduction in RONEC: Named Entity Corpus for ROmanian language"""

from __future__ import absolute_import, division, print_function

import logging
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{dumitrescu2019introducing,
  title={Introducing RONEC--the Romanian Named Entity Corpus},
  author={Dumitrescu, Stefan Daniel and Avram, Andrei-Marius},
  journal={arXiv preprint arXiv:1909.01247},
  year={2019}
}
"""

# You can copy an official description
_DESCRIPTION = """\
The RONEC (Named Entity Corpus for the Romanian language) dataset  contains over 26000 entities in ~5000 annotated sentence,
belonging to 16 distinct classes. It represents the first initiative in the Romanian language space specifically targeted for named entity recognition
"""

_HOMEPAGE = "https://github.com/dumitrescustefan/ronec"

_LICENSE = "MIT License"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://raw.githubusercontent.com/dumitrescustefan/ronec/master/ronec/conllup/raw/"
_TRAINING_FILE = "train.conllu"
_TEST_FILE = "test.conllu"
_DEV_FILE = "dev.conllu"


class RONECConfig(datasets.BuilderConfig):
    """BuilderConfig for RONEC dataset"""

    def __init__(self, **kwargs):
        super(RONECConfig, self).__init__(**kwargs)


class RONEC(datasets.GeneratorBasedBuilder):
    """RONEC dataset"""

    VERSION = datasets.Version("1.0.0")
    DEFAULT_CONFIG_NAME = "ronec"

    BUILDER_CONFIGS = [
        RONECConfig(name=DEFAULT_CONFIG_NAME, version=VERSION, description="RONEC dataset"),
    ]

    def _info(self):

        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "sentence": datasets.Sequence(datasets.Value("string")),
                "start": datasets.Sequence(datasets.Value("int32")),
                "end": datasets.Sequence(datasets.Value("int32")),
                "ronec_class": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "O",
                            "DATETIME",
                            "EVENT",
                            "FACILITY",
                            "GPE",
                            "LANGUAGE",
                            "LOC",
                            "MONEY",
                            "NAT_REL_POL",
                            "NUMERIC_VALUE",
                            "ORDINAL",
                            "ORGANIZATION",
                            "PERIOD",
                            "PERSON",
                            "PRODUCT",
                            "QUANTITY",
                            "WORK_OF_ART",
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
            "train": _URL + _TRAINING_FILE,
            "dev": _URL  +  _DEV_FILE,
            "test": _URL +  _TEST_FILE
        }

        downloaded_files = dl_manager.download(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["test"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["dev"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """

        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            sentence = []
            ronec_class = []
            start = []
            end = []
            sent = ""
            has_started = False
            for line in f:
                if "#" in line or line == "\n":
                    if sent:
                        sentence.append(sent)
                        yield guid, {
                            "id": str(guid),
                            "sentence": sentence,
                            "start": start,
                            "end": end,
                            "ronec_class": ronec_class,
                        }
                        guid += 1
                        sentence = []
                        start = []
                        end = []
                        ronec_class = []
                        sent = ""
                else:
                    # ronec words are tab separated
                    line = line.replace("\n", "")
                    splits = line.split("\t")
                    if splits[9] == "SpaceAfter=No":
                        sent += splits[1]
                    else:
                        sent += splits[1] + " "

                    if splits[10].startswith("O") and not has_started:
                        continue
                    elif splits[10].startswith("B-"):
                        begin = len(sent) - len(splits[1])
                        last = len(sent)
                        label = splits[10][2:]
                        has_started = True
                    elif splits[10].startswith("I-"):
                        last = len(sent)
                    elif splits[10].startswith("O") and begin:
                        ronec_class.append(label)
                        start.append(begin)
                        end.append(last)
                        has_started = False

            # last example
            yield guid, {
                "id": str(guid),
                "sentence": sentence,
                "start": start,
                "end": end,
                "ronec_class": ronec_class,
            }
