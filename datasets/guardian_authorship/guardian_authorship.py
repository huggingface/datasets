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


# Using a specific configuration class is optional, you can also use the base class if you don't need
# to add specific attributes.
# here we give an example for three sub-set of the dataset with difference sizes.
class Guardian2013Config(nlp.BuilderConfig):
    """ BuilderConfig for NewDataset"""

    def __init__(self,train_folder, valid_folder, test_folder, **kwargs):
        """
        Args:
            case: which cross-{} case to use [1-13] or [1-4]
            **kwargs: keyword arguments forwarded to super.
        """
        super(Guardian2013Config, self).__init__(**kwargs)
        self.train_folder = train_folder
        self.valid_folder = valid_folder
        self.test_folder = test_folder

class Guardian2013(nlp.GeneratorBasedBuilder):
    """dataset for same- and cross-topic authorship attribution"""

    # VERSION = nlp.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    config_counter = 0
    BUILDER_CONFIG_CLASS = Guardian2013Config
    BUILDER_CONFIGS = [
        # # same-topic
        # Guardian2013Config(name="same",
        #                    version=nlp.Version("0.0.0".format(0),
        #                                        description="The Original DS with the same-topic scenario"),
        #                    train_folder="", valid_folder="", test_folder=""
        #                    ),

        # cross-topic
        Guardian2013Config(name="cross_topic_{}".format(1),
                           version=nlp.Version("{}.0.0".format(1),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   1)),
                           train_folder="Politics", valid_folder="Society", test_folder="UK,World"),

        Guardian2013Config(name="cross_topic_{}".format(2),
                           version=nlp.Version("{}.0.0".format(2),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   2)),
                           train_folder="Politics", valid_folder="UK", test_folder="Society,World"),

        Guardian2013Config(name="cross_topic_{}".format(3),
                           version=nlp.Version("{}.0.0".format(3),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   3)),
                           train_folder="Politics", valid_folder="World", test_folder="Society,UK"),

        Guardian2013Config(name="cross_topic_{}".format(4),
                           version=nlp.Version("{}.0.0".format(4),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   4)),
                           train_folder="Society", valid_folder="Politics", test_folder="UK,World"),

        Guardian2013Config(name="cross_topic_{}".format(5),
                           version=nlp.Version("{}.0.0".format(5),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   5)),
                           train_folder="Society", valid_folder="UK", test_folder="Politics,World"),

        Guardian2013Config(name="cross_topic_{}".format(6),
                           version=nlp.Version("{}.0.0".format(6),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   6)),
                           train_folder="Society", valid_folder="World", test_folder="Politics,UK"),

        Guardian2013Config(name="cross_topic_{}".format(7),
                           version=nlp.Version("{}.0.0".format(7),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   7)),
                           train_folder="UK", valid_folder="Politics", test_folder="Society,World"),

        Guardian2013Config(name="cross_topic_{}".format(8),
                           version=nlp.Version("{}.0.0".format(8),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   8)),
                           train_folder="UK", valid_folder="Society", test_folder="Politics,World"),

        Guardian2013Config(name="cross_topic_{}".format(9),
                           version=nlp.Version("{}.0.0".format(9),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   9)),
                           train_folder="UK", valid_folder="World", test_folder="Politics,Society"),

        Guardian2013Config(name="cross_topic_{}".format(10),
                           version=nlp.Version("{}.0.0".format(10),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   10)),
                           train_folder="World", valid_folder="Politics", test_folder="Society,UK"),

        Guardian2013Config(name="cross_topic_{}".format(11),
                           version=nlp.Version("{}.0.0".format(11),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   11)),
                           train_folder="World", valid_folder="Society", test_folder="Politics,UK"),

        Guardian2013Config(name="cross_topic_{}".format(12),
                           version=nlp.Version("{}.0.0".format(12),
                                               description="The Original DS with the cross-topic scenario no.{}".format(
                                                   12)),
                           train_folder="World", valid_folder="UK", test_folder="Politics,Society"),

        # # cross-genre
        Guardian2013Config(name="cross_genre_{}".format(1),
                           version=nlp.Version("{}.0.0".format(1),
                                               description="The Original DS with the cross-genre scenario no.{}".format(
                                                   1)),
                           train_folder="Books", valid_folder="Politics", test_folder="Society,UK,World"),

        Guardian2013Config(name="cross_genre_{}".format(2),
                           version=nlp.Version("{}.0.0".format(2),
                                               description="The Original DS with the cross-genre scenario no.{}".format(
                                                   2)),
                           train_folder="Books", valid_folder="Society", test_folder="Politics,UK,World"),

        Guardian2013Config(name="cross_genre_{}".format(3),
                           version=nlp.Version("{}.0.0".format(3),
                                               description="The Original DS with the cross-genre scenario no.{}".format(
                                                   3)),

                           train_folder="Books", valid_folder="UK", test_folder="Politics,Society,World"),

        Guardian2013Config(name="cross-genre_{}".format(4),
                           version=nlp.Version("{}.0.0".format(4),
                                               description="The Original DS with the cross-genre scenario no.{}".format(
                                                   4)),
                           train_folder="Books", valid_folder="World", test_folder="Politics,Society,UK"),
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
                    # These are the features of your dataset like images, labels ...
                    "author": nlp.features.ClassLabel(names=["catherinebennett", "georgemonbiot", "hugoyoung",
                                                             "jonathanfreedland", "martinkettle", "maryriddell",
                                                             "nickcohen", "peterpreston", "pollytoynbee",
                                                             "royhattersley", "simonhoggart", "willhutton",
                                                             "zoewilliams"]),
                    "topic": nlp.features.ClassLabel(names=["Politics", "Society", "UK", "World", "Books"]),
                    "article": nlp.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=[("article", "author")],
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
        # print("-------------------------------")
        # print("dl_dir:", dl_dir)
        # print("cnfg_dir: ", self.config.data_dir)
        data_dir = os.path.join(dl_dir, "Guardian", "Guardian_original")

        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "data_dir": data_dir,
                    "samples_folders": self.config.train_folder,
                    "split": "train"
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "data_dir": data_dir,
                    "samples_folders": self.config.test_folder,
                    "split": "test"
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "data_dir": data_dir,
                    "samples_folders": self.config.valid_folder,
                    "split": "valid"
                },
            ),
        ]

    def _generate_examples(self, data_dir, samples_folders, split):
        """ Yields examples. """
        # TODO: Yields (key, example) tuples from the dataset
        # print("3", data_dir, split, case)
        # ds_dir = os.path.join(data_dir, self.name)
        # print(self.name)
        # print("data_dir", data_dir)
        # print("samples_folder", samples_folders)
        # if os.path.exists(data_dir):
        #     print("path exists")
        # else:
        #     print("path dne")

        if samples_folders.count(',') == 0:
            samples_folders = [samples_folders]
        else :
            samples_folders = samples_folders.split(',')

        # print(samples_folders)
        for topic in samples_folders:
            # print(topic)
            full_path = os.path.join(data_dir, topic)

            # print(full_path)
            for author in os.listdir(full_path):
                # print(author)

                list_articles = os.listdir(os.path.join(full_path, author))
                if len(list_articles) == 0:
                    # print("No articles")
                    continue

                for id_, article in enumerate(list_articles):
                    # print(os.path.join(full_path, author))
                    # print(article)
                    path_2_author = os.path.join(full_path, author)
                    path_2_article = os.path.join(path_2_author, article)
                    # print(path_2_article)
                    with open(path_2_article, 'r', encoding='utf8', errors='ignore') as f:
                        art = f.readlines()

                    # print(len(art))
                    # print(author, topic, art[0])
                    yield id_, {
                            "article": art[0],
                            "author": author,
                            "topic": topic,

                        }