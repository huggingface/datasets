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
"""DUTCH SOCIAL: Annotated Covid19 tweets in Dutch language (sentiment, industry codes & province)."""


import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@data{FK2/MTPTL7_2020,
author = {Gupta, Aakash},
publisher = {COVID-19 Data Hub},
title = {{Dutch social media collection}},
year = {2020},
version = {DRAFT VERSION},
doi = {10.5072/FK2/MTPTL7},
url = {https://doi.org/10.5072/FK2/MTPTL7}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
The dataset contains around 271,342 tweets. The tweets are filtered via the official Twitter API to
contain tweets in Dutch language or by users who have specified their location information within Netherlands
geographical boundaries. Using natural language processing we have classified the tweets for their HISCO codes.
If the user has provided their location within Dutch boundaries, we have also classified them to their respective
provinces The objective of this dataset is to make research data available publicly in a FAIR (Findable, Accessible,
Interoperable, Reusable) way. Twitter's Terms of Service Licensed under Attribution-NonCommercial 4.0 International
(CC BY-NC 4.0) (2020-10-27)
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "http://datasets.coronawhy.org/dataset.xhtml?persistentId=doi:10.5072/FK2/MTPTL7"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "CC BY-NC 4.0"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {"dutch_social": "https://storage.googleapis.com/corona-tweet/dutch-tweets.zip"}

_LANG = ["nl", "en"]


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class DutchSocial(datasets.GeneratorBasedBuilder):
    """
    Annotated Covid19 tweets in Dutch language. The tweets were filtered for users who had indicated
    their location within Netherlands or if the tweets were in Dutch language. The purpose of curating
    these tweets is to measure the economic impact of the Covid19 pandemic
    """

    VERSION = datasets.Version("1.1.0")

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
        datasets.BuilderConfig(
            name="dutch_social",
            version=VERSION,
            description="This part of my dataset provides config for the entire dataset",
        )
        # datasets.BuilderConfig(name="second_domain", version=VERSION, description="This part of my dataset covers a second domain"),
    ]

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "full_text": datasets.Value("string"),
                "text_translation": datasets.Value("string"),
                "screen_name": datasets.Value("string"),
                "description": datasets.Value("string"),
                "desc_translation": datasets.Value("string"),
                "location": datasets.Value("string"),
                "weekofyear": datasets.Value("int64"),
                "weekday": datasets.Value("int64"),
                "month": datasets.Value("int64"),
                "year": datasets.Value("int64"),
                "day": datasets.Value("int64"),
                "point_info": datasets.Value("string"),
                "point": datasets.Value("string"),
                "latitude": datasets.Value("float64"),
                "longitude": datasets.Value("float64"),
                "altitude": datasets.Value("float64"),
                "province": datasets.Value("string"),
                "hisco_standard": datasets.Value("string"),
                "hisco_code": datasets.Value("string"),
                "industry": datasets.Value("bool_"),
                "sentiment_pattern": datasets.Value("float64"),
                "subjective_pattern": datasets.Value("float64"),
                "label": datasets.ClassLabel(num_classes=3, names=["neg", "neu", "pos"], names_file=None, id=None),
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
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split, key=None):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="utf-8") as f:
            for id_, data in enumerate(f):
                data = json.loads(data)
                yield id_, {
                    "full_text": "" if not isinstance(data["full_text"], str) else data["full_text"],
                    "text_translation": ""
                    if not isinstance(data["text_translation"], str)
                    else data["text_translation"],
                    "screen_name": "" if not isinstance(data["screen_name"], str) else data["screen_name"],
                    "description": "" if not isinstance(data["description"], str) else data["description"],
                    "desc_translation": ""
                    if not isinstance(data["desc_translation"], str)
                    else data["desc_translation"],
                    "location": "" if not isinstance(data["location"], str) else data["location"],
                    "weekofyear": -1 if data["weekofyear"] is None else data["weekofyear"],
                    "weekday": -1 if data["weekday"] is None else data["weekday"],
                    "month": -1 if data["month"] is None else data["month"],
                    "year": -1 if data["year"] is None else data["year"],
                    "day": -1 if data["day"] is None else data["day"],
                    "point_info": "" if isinstance(data["point_info"], str) else data["point_info"],
                    "point": "" if not isinstance(data["point"], str) else data["point"],
                    "latitude": -1 if data["latitude"] is None else data["latitude"],
                    "longitude": -1 if data["longitude"] is None else data["longitude"],
                    "altitude": -1 if data["altitude"] is None else data["altitude"],
                    "province": "" if not isinstance(data["province"], str) else data["province"],
                    "hisco_standard": "" if not isinstance(data["hisco_standard"], str) else data["hisco_standard"],
                    "hisco_code": "" if not isinstance(data["hisco_code"], str) else data["hisco_code"],
                    "industry": False if not isinstance(data["industry"], bool) else data["industry"],
                    "sentiment_pattern": -100 if data["sentiment_pattern"] is None else data["sentiment_pattern"],
                    "subjective_pattern": -1 if data["subjective_pattern"] is None else data["subjective_pattern"],
                    "label": data["label"],
                }
