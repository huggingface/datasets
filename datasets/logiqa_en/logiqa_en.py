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
"""LogiQA, which is sourced from expert written questions for testing human logical reasoning. It consists of 8,678 QA instances, covering multiple types of deductive reasoning."""

from __future__ import absolute_import, division, print_function

import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@misc{liu2020logiqa,
      title={LogiQA: A Challenge Dataset for Machine Reading Comprehension with Logical Reasoning},
      author={Jian Liu and Leyang Cui and Hanmeng Liu and Dandan Huang and Yile Wang and Yue Zhang},
      year={2020},
      eprint={2007.08124},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

# You can copy an official description
_DESCRIPTION = """\
LogiQA, which contains 8,678 paragraph-question pairs, each with four candidate answers. The dataset is sourced from publically available logical examination papers for reading comprehension, which are designed by domain experts for evaluating the logical reasoning ability and test participants.
"""
_HOMEPAGE = "https://github.com/lgw863/LogiQA-dataset"
_LICENSE = "N/A"


# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {"default": "https://github.com/lgw863/LogiQA-dataset/archive/master.zip"}


class LogiQAEn(datasets.GeneratorBasedBuilder):
    """LogiQA, which is sourced from expert written questions for testing human logical reasoning. It consists of 8,678 QA instances, covering multiple types of deductive reasoning."""

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
    #     datasets.BuilderConfig(name="first_domain", version=VERSION, description="This part of my dataset covers a first domain"),
    #     datasets.BuilderConfig(name="second_domain", version=VERSION, description="This part of my dataset covers a second domain"),
    # ]
    #
    # DEFAULT_CONFIG_NAME = "first_domain"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        features = datasets.Features(
            {
                "answer": datasets.Value("string"),
                "context": datasets.Value("string"),
                "question": datasets.Value("string"),
                "choice_a": datasets.Value("string"),
                "choice_b": datasets.Value("string"),
                "choice_c": datasets.Value("string"),
                "choice_d": datasets.Value("string"),
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
        my_urls = _URLs["default"]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "LogiQA-dataset-master", "Train.txt"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "LogiQA-dataset-master", "Test.txt"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "LogiQA-dataset-master", "Eval.txt"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        # counter = 0
        with open(filepath, encoding="utf-8") as f:
            lines = []
            for id_, row in enumerate(f):
                lines.append(row.strip())
                if len(lines) >= 8:
                    yield id_, {
                        "answer": lines[1],
                        "context": lines[2],
                        "question": lines[3],
                        "choice_a": lines[4],
                        "choice_b": lines[5],
                        "choice_c": lines[6],
                        "choice_d": lines[7],
                    }
                    # if counter < 4:
                    #     print(lines)
                    #     print('-'*50)
                    # counter += 1
                    lines = []
