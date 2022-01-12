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
"""A redistributable subset of the ETH Py150 corpus"""


import json
import os

import datasets


_CITATION = """\
@inproceedings{kanade2020learning,
  title={Learning and Evaluating Contextual Embedding of Source Code},
  author={Kanade, Aditya and Maniatis, Petros and Balakrishnan, Gogul and Shi, Kensen},
  booktitle={International Conference on Machine Learning},
  pages={5110--5121},
  year={2020},
  organization={PMLR}
}
"""


_DESCRIPTION = """\
A redistributable subset of the ETH Py150 corpus, introduced in the ICML 2020 paper 'Learning and Evaluating Contextual Embedding of Source Code'
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/google-research-datasets/eth_py150_open"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "Apache License, Version 2.0"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://raw.githubusercontent.com/google-research-datasets/eth_py150_open/master/"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class EthPy150Open(datasets.GeneratorBasedBuilder):
    """A redistributable subset of the ETH Py150 corpus"""

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
            name="eth_py150_open", version=VERSION, description="A subset of the original Py150 corpus"
        ),
    ]

    def _info(self):
        features = datasets.Features({"filepath": datasets.Value("string"), "license": datasets.Value("string")})
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=("filepath", "license"),
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
        urls = {
            "train": _URL + "train__manifest.json",
            "dev": _URL + "dev__manifest.json",
            "test": _URL + "eval__manifest.json",
        }
        data_dir = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir["train"]), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir["test"]), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir["dev"]), "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(json.load(f)):
                yield id_, row
