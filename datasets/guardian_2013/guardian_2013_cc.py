# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the current dataset script contributor.
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
"""This is an authorship attribution dataset based on the work of Stamatatos 2013. """

from __future__ import absolute_import, division, print_function


import json
import os

import nlp


_CITATION = """\
@article{article,
author = {Stamatatos, Efstathios},
year = {2013},
month = {01},
pages = {421-439},
title = {On the robustness of authorship attribution based on character n-gram features},
volume = {21},
journal = {Journal of Law and Policy}
}

@inproceedings{stamatatos2017authorship,
  title={Authorship attribution using text distortion},
  author={Stamatatos, Efstathios},
  booktitle={Proc. of the 15th Conf. of the European Chapter of the Association for Computational Linguistics},
  volume={1}
  pages={1138--1149},
  year={2017}
}
"""


_DESCRIPTION = """\
A dataset for same-topic and cross-topic authorship attribution.
"""

_URL = "https://www.dropbox.com/s/lc5mje0owl9shms/Guardian.zip?dl=1"

# _SUPPORTED_VERSIONS = [
#     # same topic
#     nlp.Version("1.1.0", "Same-topic scenario"),
#     nlp.Version("1.2.1", "Cross-topic scenario #1"),
#     nlp.Version("1.3.0", "Cross-genre scenario"),
#     ]

_CASES = ["same",
          "cross_1", "cross_2", "cross_3", "cross_4", "cross_5", "cross_6", "cross_7", "cross_8",  "cross_9",
          "cross_10", "cross_11", "cross_12",
          "genre_1", "genre_2", "genre_3", "genre_4",
         ]

_DEFAULT_VERSION = nlp.Version("1.1.0", "Same-topic scenario")

# additional funcitons

def get_topics(case):
    if case in _CASES:
        if case == "cross_1":
            return {"train":["P"], "valid":["S"], "test":["U", "W"]}

# Using a specific configuration class is optional, you can also use the base class if you don't need
# to add specific attributes.
# here we give an example for three sub-set of the dataset with difference sizes.
class Guardian2013Config(nlp.BuilderConfig):
    """ BuilderConfig for NewDataset"""

    def __init__(self, case, **kwargs):
        """
        Args:
            data_size: the size of the training set we want to use (xs, s, m, l, xl)
            **kwargs: keyword arguments forwarded to super.
        """
        self.case = case
        print("1", self.case)
        super(Guardian2013Config, self).__init__(**kwargs)


class Guardian2013(nlp.GeneratorBasedBuilder):
    """dataset for same- and cross-topic authorship attribution"""

    # VERSION = nlp.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    BUILDER_CONFIG_CLASS = Guardian2013Config
    BUILDER_CONFIGS = [
        Guardian2013Config(name="Guardian2013_" + case, description="An authorship dataset",
                           version=nlp.Version(str(i + 1) + '.0.0'),
                           case=case) for i, case in
        enumerate(["same",
                   "cross_1", "cross_2", "cross_3", "cross_4",
                   "cross_5", "cross_6", "cross_7", "cross_8",
                   "cross_9", "cross_10", "cross_11", "cross_12",
                   "genre_1", "genre_2", "genre_3", "genre_4",
                   ])
    ]

    # @property
    def _info(self):
        # TODO: Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "article": nlp.Value("string"),
                    "author":  nlp.features.ClassLabel(names=["catherinebennett", "georgemonbiot", "hugoyoung",
                                                              "jonathanfreedland", "martinkettle", "maryriddell",
                                                              "nickcohen", "peterpreston", "pollytoynbee",
                                                              "royhattersley", "simonhoggart", "willhutton",
                                                              "zoewilliams"]),
                    "topic":  nlp.features.ClassLabel(names=["Politics", "Society", "UK", "World"])
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            # supervised_keys=[("article", "author", "topic")],
            # Homepage of the dataset for documentation
            homepage="http://www.icsd.aegean.gr/lecturers/stamatatos/papers/JLP2013.pdf",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "4_Guardian_new")
        print("2", data_dir)
        print("2", self.config.case)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, self.config.case),
                    #'labelpath': os.path.join(data_dir, 'train_{}-labels.lst'.format(self.config.data_size)),
                    "split": "train",
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl"), "split": "test"},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    #'labelpath': os.path.join(data_dir, 'dev-labels.lst'),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: Yields (key, example) tuples from the dataset
        print("3", filepath, split)

        with open(filepath) as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if split == "test":
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "option2": data["option2"],
                        "answer": "",
                    }
                else:
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "option2": data["option2"],
                        "answer": data["answer"],
                    }