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
"""TED TALKS IWSLT: Web Inventory of Transcribed and Translated Ted Talks."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{cettolo-etal-2012-wit3,
    title = "{WIT}3: Web Inventory of Transcribed and Translated Talks",
    author = "Cettolo, Mauro  and
      Girardi, Christian  and
      Federico, Marcello",
    booktitle = "Proceedings of the 16th Annual conference of the European Association for Machine Translation",
    month = may # " 28{--}30",
    year = "2012",
    address = "Trento, Italy",
    publisher = "European Association for Machine Translation",
    url = "https://www.aclweb.org/anthology/2012.eamt-1.60",
    pages = "261--268",
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
The core of WIT3 is the TED Talks corpus, that basically redistributes the original content published by the TED Conference website (http://www.ted.com). Since 2007,
the TED Conference, based in California, has been posting all video recordings of its talks together with subtitles in English
and their translations in more than 80 languages. Aside from its cultural and social relevance, this content, which is published under the Creative Commons BYNC-ND license, also represents a precious
language resource for the machine translation research community, thanks to its size, variety of topics, and covered languages.
This effort repurposes the original content in a way which is more convenient for machine translation researchers.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://wit3.fbk.eu/"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "CC-BY-NC-4.0"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    # Data needs to be downloaded manually
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class TedTalksIWSLT(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
    \n    
    The file can be downloaded from: https://drive.google.com/file/d/1Cz1Un9p8Xn9IpEMMrg2kXSDt0dnjxc4z/view?usp=sharing
    Unzip the folder to obtain folder: XML_releases
    The folder structure is like this: 
    
    XML_releases
        |
        |---xml
        |    |---ted_af-20160408.zip
        |    |---ted_am-20160408.zip
        |    ...
        |    ...   
        |---xml-20150616
        |---xml-20140120
        |---wit3_data

    You can then specify the path to this folder for the `data_dir` argument in the datasets.load_dataset(...).
    The data can then be loaded using the following command: 
    `datasets.load_dataset("ted_talks_iwslt", data_dir="XML_releases", "ted_talks_2016_all")`

    """

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
            name="ted_talks_2016_all",
            version=VERSION,
            description="This part of the dataset covers all data files from April 2016",
        ),
        # datasets.BuilderConfig(name="second_domain", version=VERSION, description="This part of my dataset covers a second domain"),
    ]

    DEFAULT_CONFIG_NAME = (
        "ted_talks_2016_all"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if (
            self.config.name == "ted_talks_2016_all"
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "option1": datasets.Value("string"),
                    "answer": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "option2": datasets.Value("string"),
                    "second_domain_answer": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
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

        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('poleval2019_mt', name= .., data_dir=...)` where name can be {} Manual download instructions: {})".format(
                    path_to_manual_file, "en-pl/pl-en/pl-ru/ru-pl", self.manual_download_instructions
                )
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "xml-20140120/"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "xml/"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "xml-20150120/"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "first_domain":
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "answer": "" if split == "test" else data["answer"],
                    }
                else:
                    yield id_, {
                        "sentence": data["sentence"],
                        "option2": data["option2"],
                        "second_domain_answer": "" if split == "test" else data["second_domain_answer"],
                    }
