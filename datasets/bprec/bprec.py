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
"""Brand-Product Relation Extraction Corpora"""


import json

import datasets


# DONE: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{inproceedings,
author = {Janz, Arkadiusz and Kopociński, Łukasz and Piasecki, Maciej and Pluwak, Agnieszka},
year = {2020},
month = {05},
pages = {},
title = {Brand-Product Relation Extraction Using Heterogeneous Vector Space Representations}
}
"""

# DONE: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Dataset consisting of Polish language texts annotated to recognize brand-product relations.
"""

# DONE: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://clarin-pl.eu/dspace/handle/11321/736"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "tele": "https://minio.clarin-pl.eu/semrel/corpora/ner_export_json/ner_tele_export.json",
    "electro": "https://minio.clarin-pl.eu/semrel/corpora/ner_export_json/ner_electro_export.json",
    "cosmetics": "https://minio.clarin-pl.eu/semrel/corpora/ner_export_json/ner_cosmetics_export.json",
    "banking": "https://minio.clarin-pl.eu/semrel/corpora/ner_export_json/ner_banking_export.json",
}

_CATEGORIES = {
    "tele": "telecommunications",
    "electro": "electronics",
    "cosmetics": "cosmetics",
    "banking": "banking",
}
_ALL_CATEGORIES = "all"
_VERSION = "1.1.0"


class BprecConfig(datasets.BuilderConfig):
    """BuilderConfig for BprecConfig."""

    def __init__(self, categories=None, **kwargs):
        super(BprecConfig, self).__init__(version=datasets.Version(_VERSION, ""), **kwargs),
        self.categories = categories


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Bprec(datasets.GeneratorBasedBuilder):
    """Brand-Product Relation Extraction Corpora in Polish"""

    BUILDER_CONFIGS = [
        BprecConfig(
            name=_ALL_CATEGORIES,
            categories=_CATEGORIES,
            description="A collection of Polish language texts annotated to recognize brand-product relations",
        )
    ] + [
        BprecConfig(
            name=cat,
            categories=[cat],
            description=f"{_CATEGORIES[cat]} examples from a collection of Polish language texts annotated to recognize brand-product relations",
        )
        for cat in _CATEGORIES
    ]
    BUILDER_CONFIG_CLASS = BprecConfig
    DEFAULT_CONFIG_NAME = _ALL_CATEGORIES

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "id": datasets.Value("int32"),
                "category": datasets.Value("string"),
                "text": datasets.Value("string"),
                "ner": datasets.features.Sequence(
                    {
                        "source": {
                            "from": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "to": datasets.Value("int32"),
                            "type": datasets.features.ClassLabel(
                                names=[
                                    "PRODUCT_NAME",
                                    "PRODUCT_NAME_IMP",
                                    "PRODUCT_NO_BRAND",
                                    "BRAND_NAME",
                                    "BRAND_NAME_IMP",
                                    "VERSION",
                                    "PRODUCT_ADJ",
                                    "BRAND_ADJ",
                                    "LOCATION",
                                    "LOCATION_IMP",
                                ]
                            ),
                        },
                        "target": {
                            "from": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "to": datasets.Value("int32"),
                            "type": datasets.features.ClassLabel(
                                names=[
                                    "PRODUCT_NAME",
                                    "PRODUCT_NAME_IMP",
                                    "PRODUCT_NO_BRAND",
                                    "BRAND_NAME",
                                    "BRAND_NAME_IMP",
                                    "VERSION",
                                    "PRODUCT_ADJ",
                                    "BRAND_ADJ",
                                    "LOCATION",
                                    "LOCATION_IMP",
                                ]
                            ),
                        },
                    }
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
        _my_urls = [_URLs[cat] for cat in self.config.categories]

        downloaded_files = dl_manager.download_and_extract(_my_urls)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filedirs": downloaded_files}),
        ]

    def _generate_examples(self, filedirs, split="tele"):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        cats = [cat for cat in self.config.categories]
        for cat, filepath in zip(cats, filedirs):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key in data.keys():
                    example = data[key]
                    id_ = example.get("id")
                    text = example.get("text")
                    ner = example.get("ner")
                    yield id_, {
                        "id": id_,
                        "category": cat,
                        "text": text,
                        "ner": ner,
                    }
