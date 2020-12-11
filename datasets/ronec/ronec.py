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

import csv
import json
import os
import logging
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

_FILE_FORMAT = "ronec.conllup"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = (
    "https://raw.githubusercontent.com/dumitrescustefan/ronec/master/ronec/conllup/raw/"
)
_TRAINING_FILE = "train.conllu"
_TEST_FILE = "test.conllu"
_DEV_FILE = "dev.conllu"


class RONECConfig(datasets.BuilderConfig):
    """BuilderConfig for RONEC dataset"""

    def __init__(self, **kwargs):
        super(RONECConfig, self).__init__(**kwargs)


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class RONEC(datasets.GeneratorBasedBuilder):
    """RONEC dataset"""

    VERSION = datasets.Version("1.0.0")
    DEFAULT_CONFIG_NAME = "ronec"
    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        RONECConfig(
            name=DEFAULT_CONFIG_NAME, version=VERSION, description="RONEC dataset"
        ),
    ]

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset

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
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls_to_download = {
            "train": os.path.join(_URL, _TRAINING_FILE),
            "dev": os.path.join(_URL, _DEV_FILE),
            "test": os.path.join(_URL, _TEST_FILE),
        }

        # Download .zip file
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
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
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
                        # print("AICIA4",sent, ronec_class)
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
