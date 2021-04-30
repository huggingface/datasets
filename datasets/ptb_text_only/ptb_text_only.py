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
"""
    Load the Penn Treebank dataset.

    This is the Penn Treebank Project: Release 2 CDROM, featuring a million words of 1989 Wall
    Street Journal material.
"""


import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{marcus-etal-1993-building,
    title = "Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank",
    author = "Marcus, Mitchell P.  and
      Santorini, Beatrice  and
      Marcinkiewicz, Mary Ann",
    journal = "Computational Linguistics",
    volume = "19",
    number = "2",
    year = "1993",
    url = "https://www.aclweb.org/anthology/J93-2004",
    pages = "313--330",
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This is the Penn Treebank Project: Release 2 CDROM, featuring a million words of 1989 Wall Street Journal material. This corpus has been annotated for part-of-speech (POS) information. In addition, over half of it has been annotated for skeletal syntactic structure.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://catalog.ldc.upenn.edu/LDC99T42"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "LDC User Agreement for Non-Members"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://raw.githubusercontent.com/wojzaremba/lstm/master/data/"
_TRAINING_FILE = "ptb.train.txt"
_DEV_FILE = "ptb.valid.txt"
_TEST_FILE = "ptb.test.txt"


class PtbTextOnlyConfig(datasets.BuilderConfig):
    """BuilderConfig for PtbTextOnly"""

    def __init__(self, **kwargs):
        """BuilderConfig PtbTextOnly.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(PtbTextOnlyConfig, self).__init__(**kwargs)


class PtbTextOnly(datasets.GeneratorBasedBuilder):
    """Load the Penn Treebank dataset."""

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
        PtbTextOnlyConfig(
            name="penn_treebank",
            version=VERSION,
            description="Load the Penn Treebank dataset",
        ),
    ]

    def _info(self):
        features = datasets.Features({"sentence": datasets.Value("string")})
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
        my_urls = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_dir["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": data_dir["test"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": data_dir["dev"]}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        with open(filepath, encoding="utf-8") as f:
            for id_, line in enumerate(f):
                line = line.strip()
                yield id_, {"sentence": line}
