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

import pandas as pd

import datasets

# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{clickbait_news_bg,
title = {Dataset with clickbait and fake news in Bulgarian. Introduced for the Hack the Fake News 2017.},
authors={Data Science Society},
year={2017},
url={https://gitlab.com/datasciencesociety/case_fake_news/}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Dataset with clickbait and fake news in Bulgarian. Introduced for the Hack the Fake News 2017.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://gitlab.com/datasciencesociety/case_fake_news/"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    'default_train': "https://gitlab.com/datasciencesociety/case_fake_news/-/raw/master/data/FN_Training_Set.xlsx",
    'default_validation': "https://gitlab.com/datasciencesociety/case_fake_news/-/raw/master/data/FN_Validation_Set.xlsx",
    # 'default': "https://drive.google.com/file/d/1QCuaM6mi1OJYg13hCTAUA7NEy-c8QVZW/view?usp=sharing"
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class ClickbaitNewsBGDataset(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    ##############################
    #####  No need for multiple domains at this point.
    ##############################

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    # BUILDER_CONFIGS = [
    #     datasets.BuilderConfig(name="training_set", version=VERSION, description="Training data file"),
    #     datasets.BuilderConfig(name="validation_set", version=VERSION, description="Validation data file"),
    # ]

    DEFAULT_CONFIG_NAME = "default"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        
        if (
            self.config.name == "default"
        ):
            features = datasets.Features(
                {
                    "fake_news_score": datasets.Value("int8"),
                    "click_bait_score": datasets.Value("int8"),
                    "content_title": datasets.Value("string"),
                    "content_url": datasets.Value("string"),
                    "content_published_time": datasets.Value("date64"),
                    "content": datasets.Value("string")
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
        # my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download(_URLs)

        return [
                datasets.SplitGenerator(
                    name=spl_enum,
                    gen_kwargs={
                        "filepath": data_dir[f"{self.config.name}_{spl}"],
                        "split": spl,
                    },
                )
                for spl, spl_enum in [
                    ("train", datasets.Split.TRAIN),
                    ("validation", datasets.Split.VALIDATION),
                ]
            ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        print('generating examples with filepath:', filepath, split)

        if self.config.name == "default":
            keys = ["fake_news_score", "click_bait_score", "content_title", "content_url", "content_published_time", "content"]
            data = pd.read_excel(filepath)
            for id_, row in enumerate(data.itertuples()):
                # print(id_, dict(zip(keys, row[1:])))
                yield id_, dict(zip(keys, row[1:]))

                
