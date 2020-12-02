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
""" **Person SenTiment, a challenge dataset for author sentiment prediction in the news domain **

PerSenT is a crowd-sourced dataset that captures the sentiment of an author towards the main entity in a news article. This dataset contains annotation for 5.3k documents and 38k paragraphs covering 3.2k unique entities.

"""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets
from datasets.splits import NamedSplit


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{bastan2020authors,
      title={Author's Sentiment Prediction}, 
      author={Mohaddeseh Bastan and Mahnaz Koupaee and Youngseo Son and Richard Sicoli and Niranjan Balasubramanian},
      year={2020},
      eprint={2011.06128},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Person SenTiment (PerSenT) is a crowd-sourced dataset that captures the sentiment of an author towards the main entity in a news article. This dataset contains annotation for 5.3k documents and 38k paragraphs covering 3.2k unique entities. 

To split the dataset, we separated the entities into 4 mutually exclusive sets. Due to the nature of news collections, some entities tend to dominate the collection. In our collection,there were four entities which were the main entity in nearly 800 articles. To avoid these entities from dominating the train or test splits, we moved them to a separate test collection. We split the remaining into a training, dev, and test sets at random. Thus our collection includes one standard test set consisting of articles drawn at random (Test Standard -- `test_random`), while the other is a test set which contains multiple articles about a small number of popular entities (Test Frequent -- `test_fixed`).
"""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    'train': "https://raw.githubusercontent.com/MHDBST/PerSenT/main/train.csv",
    'dev': "https://raw.githubusercontent.com/MHDBST/PerSenT/main/dev.csv",
    'test_random': 'https://raw.githubusercontent.com/MHDBST/PerSenT/main/random_test.csv',
    'test_fixed': 'https://raw.githubusercontent.com/MHDBST/PerSenT/main/fixed_test.csv'
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class PerSenT(datasets.GeneratorBasedBuilder):
    """Person SenTiment (PerSenT) is a crowd-sourced dataset that captures the sentiment of an author towards the main entity in a news article. This dataset contains annotation for 5.3k documents and 38k paragraphs covering 3.2k unique entities. 
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
    # BUILDER_CONFIGS = [
    #     datasets.BuilderConfig(name="train", description="This part of my dataset covers a first domain"),
    #     datasets.BuilderConfig(name="dev", description="This part of my dataset covers a second domain"),
    # ]

    # DEFAULT_CONFIG_NAME = "first_domain"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        label = datasets.features.ClassLabel(names=["","Negative", "Neutral", "Positive"])
        features = datasets.Features(
                {
                    'DOCUMENT_INDEX': datasets.Value("int64"),
                    'TITLE': datasets.Value("string"),
                    'TARGET_ENTITY': datasets.Value("string"),
                    'DOCUMENT': datasets.Value("string"),
                    'MASKED_DOCUMENT': datasets.Value("string"),
                    'TRUE_SENTIMENT': label,
                    'Paragraph0': label,
                    'Paragraph1': label,
                    'Paragraph2': label,
                    'Paragraph3': label,
                    'Paragraph4': label,
                    'Paragraph5': label,
                    'Paragraph6': label,
                    'Paragraph7': label,
                    'Paragraph8': label,
                    'Paragraph9': label,
                    'Paragraph10': label,
                    'Paragraph11': label,
                    'Paragraph12': label,
                    'Paragraph13': label,
                    'Paragraph14': label,
                    'Paragraph15': label,
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://stonybrooknlp.github.io/PerSenT",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download(_URLs['train'])
        dev_path = dl_manager.download(_URLs['dev'])
        test_fixed_path = dl_manager.download(_URLs['test_fixed'])
        test_random_path = dl_manager.download(_URLs['test_random'])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": train_path,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=NamedSplit("test_random"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": test_random_path,
                    "split": "test_random"
                },
            ),
            datasets.SplitGenerator(
                name=NamedSplit("test_fixed"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": test_fixed_path,
                    "split": "test_fixed"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": dev_path,
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath) as f:
            reader = csv.reader(f)
            header = next(reader)
            for id_, row in enumerate(reader):
                yield id_, dict(zip(header, row))
