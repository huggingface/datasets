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
@article{haouari2020arcov19,
  title={ArCOV-19: The First Arabic COVID-19 Twitter Dataset with Propagation Networks},
  author={Fatima Haouari and Maram Hasanain and Reem Suwaileh and Tamer Elsayed},
  journal={arXiv preprint arXiv:2004.05861},
  year={2020}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
ArCOV-19 is an Arabic COVID-19 Twitter dataset that covers the period from 27th of January till 30th of April 2020. ArCOV-19 is designed to enable research under several domains including natural language processing, information retrieval, and social computing, among others
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://gitlab.com/bigirqu/ArCOV-19"

# TODO: Add the licence for the dataset here if you can find it
#_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://gitlab.com/bigirqu/ArCOV-19/-/blob/master/dataset/all_tweets/"

class arcov19Config(datasets.BuilderConfig):
    """BuilderConfig for ArCOV19."""

    def __init__(self, **kwargs):
        """BuilderConfig for ArCOV19.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(arcov19Config, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class arcov19(datasets.GeneratorBasedBuilder):
    """ArCOV-19 is an Arabic COVID-19 Twitter dataset that covers the period from 27th of January till 30th of April 2020. ArCOV-19 is designed to enable research under several domains including natural language processing, information retrieval, and social computing, among others"""

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
      arcov19Config(
            name="ArCOV19",
            description="Plain text",
        )
    ]


    def _info(self):
       
        features={}
        features["tweetID"]= datasets.Value("string")
     
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(features),  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            #license=_LICENSE,
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
        #DF=pd.date_range(start="2020-01-27",end="2020-04-30")        
        #for i in range(len(DF)):

        #    urls_to_download = {
        #         "train": os.path.join(_URL, DF[i].date().strftime("%Y-%m-%d")),
        #    }
        #    downloaded_files = dl_manager.download(urls_to_download)
        #return [
         #   datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
        #]
        urls_to_download = {
            "train": os.path.join(_URL, "2020-01-27"),
        }
        print("urls_to_download")
        downloaded_files = dl_manager.download(urls_to_download)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
        ]
    def _generate_examples(self, filepath):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        df = pd.read_csv(filepath, names=["tweetID"])
        for id_, record in df.iterrows():
            tweetID= record["tweetID"]
            yield str(id_), {"tweetID": tweetID}
#        for i in range(len(df)):
            
#            tweetID= df["tweetID"]
#            yield  {"textID": tweetID}
