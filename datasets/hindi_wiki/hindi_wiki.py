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
"""It is publicly avilable dataset generated from wikipidia corpus for hindi text"""

from __future__ import absolute_import, division, print_function
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """
@misc{ goru001,
       authors = {"Gaurav Aurora"},
       title = {"nlp_for_hindi"},
       year = {2006}
       }
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to solve give hindi dataset for  NLP task and is crafted with a lot of care."""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://www.kaggle.com/disisbig/hindi-wikipedia-articles-55k"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "License CC BY-SA 4.0"

# TODO: Add link to the official dataset URLs herecd
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = "/home/rahul/datasets/datasets/hindi_wiki"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class HindiWiki(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="hindi_wiki",
            version=datasets.Version("1.0.1", ""),
            description="Plain text import of hindi_wiki",
        )
    ]
    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')

    # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method pecifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "sentence": datasets.Sequence(datasets.Value("string"))
                    # These are the features of your dataset like images, labels ...
                }
            ),  # Here we define them above because they are different between the two configurations
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
        # data_dir = dl_manager.manual_dir(_URLs)
        data_dir = os.path.join(_URLs, "archive")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "train.txt")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "valid.txt")},
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        # for filename in glob.glob(os.path.join(filepath, '*.txt')):
        with open(filepath, encoding="utf-8") as f:
            itr = 0
            tokens = []
            for line in f:
                splits = line.split(" ")
                for word in splits:
                    tokens.append(word)
                    itr += 1
                    # data = json.loads(row)
            yield itr, {
                "sentence": tokens,
            }


# python datasets-cli dummy_data datasets/hindi_wiki --auto_generate
