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
# TODO: Address all TODOs and remove all explanatory comments
"""MR (MR Movie Review) sentence classification dataset."""


import os
import re

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{Pang+Lee:05a,
  author =       {Bo Pang and Lillian Lee},
  title =        {Seeing stars: Exploiting class relationships for sentiment
                  categorization with respect to rating scales},
  booktitle =    {Proceedings of the ACL},
  year =         2005
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
MR Movie Reviews is a dataset for use in sentiment-analysis experiments. It contains sentences labeled with respect to their polarity."""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://www.cs.cornell.edu/people/pabo/movie-review-data/"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_DATA_URL = "https://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class MRPolarity(datasets.GeneratorBasedBuilder):
    """MR (Movie Review) sentiment classification dataset."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
                "label": datasets.features.ClassLabel(
                    names=[
                        "negative",
                        "positive",
                    ]
                ),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = _DATA_URL
        data_dir = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "folder": os.path.join(data_dir, "rt-polaritydata"),
                    "split": "train",
                },
            )
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, folder, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.

        def clean_line(line):
            if line is None:
                return None
            line = line.strip()
            line = line.replace("\n", " ")
            # remove whitespace before punctuation. "simplistic , silly and tedious ." => "simplistic, silly and tedious."
            line = re.sub(r"( [(])\s", r"\1", line)
            line = re.sub(r"\s+([?.,!):])", r"\1", line)
            return line

        key = 0
        with open(os.path.join(folder, "rt-polarity.neg"), encoding="windows-1252") as f:
            while True:
                line = clean_line(f.readline())
                if line is None or len(line) == 0:
                    break

                yield key, {
                    "text": line,
                    "label": 0,
                }
                key += 1

        with open(os.path.join(folder, "rt-polarity.pos"), encoding="windows-1252") as f:
            while True:
                line = clean_line(f.readline())
                if line is None or len(line) == 0:
                    break

                yield key, {
                    "text": line,
                    "label": 1,
                }
                key += 1
