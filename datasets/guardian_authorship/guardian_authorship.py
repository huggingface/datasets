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
"""This is an authorship attribution dataset based on the work of Stamatatos 2013. """

from __future__ import absolute_import, division, print_function

import os

import datasets


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
A dataset cross-topic authorship attribution. The dataset is provided by Stamatatos 2013.
1- The cross-topic scenarios are based on Table-4 in Stamatatos 2017 (Ex. cross_topic_1 => row 1:P S U&W ).
2- The cross-genre scenarios are based on Table-5 in the same paper. (Ex. cross_genre_1 => row 1:B P S&U&W).

3- The same-topic/genre scenario is created by grouping all the datasts as follows.
For ex., to use same_topic and split the data 60-40 use:
train_ds = load_dataset('guardian_authorship', name="cross_topic_<<#>>",
                        split='train[:60%]+validation[:60%]+test[:60%]')
tests_ds = load_dataset('guardian_authorship', name="cross_topic_<<#>>",
                        split='train[-40%:]+validation[-40%:]+test[-40%:]')

IMPORTANT: train+validation+test[:60%] will generate the wrong splits becasue the data is imbalanced

* See https://huggingface.co/docs/datasets/splits.html for detailed/more examples
"""

_URL = "https://www.dropbox.com/s/lc5mje0owl9shms/Guardian.zip?dl=1"


# Using a specific configuration class is optional, you can also use the base class if you don't need
# to add specific attributes.
# here we give an example for three sub-set of the dataset with difference sizes.
class GuardianAuthorshipConfig(datasets.BuilderConfig):
    """ BuilderConfig for NewDataset"""

    def __init__(self, train_folder, valid_folder, test_folder, **kwargs):
        """
        Args:
            Train_folder: Topic/genre used for training
            valid_folder:       ~      ~   for validation
            test_folder:        ~      ~   for testing

            **kwargs: keyword arguments forwarded to super.
        """
        super(GuardianAuthorshipConfig, self).__init__(**kwargs)
        self.train_folder = train_folder
        self.valid_folder = valid_folder
        self.test_folder = test_folder


class GuardianAuthorship(datasets.GeneratorBasedBuilder):
    """dataset for same- and cross-topic authorship attribution"""

    config_counter = 0
    BUILDER_CONFIG_CLASS = GuardianAuthorshipConfig
    BUILDER_CONFIGS = [
        # cross-topic
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(1),
            version=datasets.Version(
                "{}.0.0".format(1), description="The Original DS with the cross-topic scenario no.{}".format(1)
            ),
            train_folder="Politics",
            valid_folder="Society",
            test_folder="UK,World",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(2),
            version=datasets.Version(
                "{}.0.0".format(2), description="The Original DS with the cross-topic scenario no.{}".format(2)
            ),
            train_folder="Politics",
            valid_folder="UK",
            test_folder="Society,World",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(3),
            version=datasets.Version(
                "{}.0.0".format(3), description="The Original DS with the cross-topic scenario no.{}".format(3)
            ),
            train_folder="Politics",
            valid_folder="World",
            test_folder="Society,UK",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(4),
            version=datasets.Version(
                "{}.0.0".format(4), description="The Original DS with the cross-topic scenario no.{}".format(4)
            ),
            train_folder="Society",
            valid_folder="Politics",
            test_folder="UK,World",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(5),
            version=datasets.Version(
                "{}.0.0".format(5), description="The Original DS with the cross-topic scenario no.{}".format(5)
            ),
            train_folder="Society",
            valid_folder="UK",
            test_folder="Politics,World",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(6),
            version=datasets.Version(
                "{}.0.0".format(6), description="The Original DS with the cross-topic scenario no.{}".format(6)
            ),
            train_folder="Society",
            valid_folder="World",
            test_folder="Politics,UK",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(7),
            version=datasets.Version(
                "{}.0.0".format(7), description="The Original DS with the cross-topic scenario no.{}".format(7)
            ),
            train_folder="UK",
            valid_folder="Politics",
            test_folder="Society,World",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(8),
            version=datasets.Version(
                "{}.0.0".format(8), description="The Original DS with the cross-topic scenario no.{}".format(8)
            ),
            train_folder="UK",
            valid_folder="Society",
            test_folder="Politics,World",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(9),
            version=datasets.Version(
                "{}.0.0".format(9), description="The Original DS with the cross-topic scenario no.{}".format(9)
            ),
            train_folder="UK",
            valid_folder="World",
            test_folder="Politics,Society",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(10),
            version=datasets.Version(
                "{}.0.0".format(10), description="The Original DS with the cross-topic scenario no.{}".format(10)
            ),
            train_folder="World",
            valid_folder="Politics",
            test_folder="Society,UK",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(11),
            version=datasets.Version(
                "{}.0.0".format(11), description="The Original DS with the cross-topic scenario no.{}".format(11)
            ),
            train_folder="World",
            valid_folder="Society",
            test_folder="Politics,UK",
        ),
        GuardianAuthorshipConfig(
            name="cross_topic_{}".format(12),
            version=datasets.Version(
                "{}.0.0".format(12), description="The Original DS with the cross-topic scenario no.{}".format(12)
            ),
            train_folder="World",
            valid_folder="UK",
            test_folder="Politics,Society",
        ),
        # # cross-genre
        GuardianAuthorshipConfig(
            name="cross_genre_{}".format(1),
            version=datasets.Version(
                "{}.0.0".format(13), description="The Original DS with the cross-genre scenario no.{}".format(1)
            ),
            train_folder="Books",
            valid_folder="Politics",
            test_folder="Society,UK,World",
        ),
        GuardianAuthorshipConfig(
            name="cross_genre_{}".format(2),
            version=datasets.Version(
                "{}.0.0".format(14), description="The Original DS with the cross-genre scenario no.{}".format(2)
            ),
            train_folder="Books",
            valid_folder="Society",
            test_folder="Politics,UK,World",
        ),
        GuardianAuthorshipConfig(
            name="cross_genre_{}".format(3),
            version=datasets.Version(
                "{}.0.0".format(15), description="The Original DS with the cross-genre scenario no.{}".format(3)
            ),
            train_folder="Books",
            valid_folder="UK",
            test_folder="Politics,Society,World",
        ),
        GuardianAuthorshipConfig(
            name="cross_genre_{}".format(4),
            version=datasets.Version(
                "{}.0.0".format(16), description="The Original DS with the cross-genre scenario no.{}".format(4)
            ),
            train_folder="Books",
            valid_folder="World",
            test_folder="Politics,Society,UK",
        ),
    ]

    def _info(self):
        # Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    # There are 13 authors in this dataset
                    "author": datasets.features.ClassLabel(
                        names=[
                            "catherinebennett",
                            "georgemonbiot",
                            "hugoyoung",
                            "jonathanfreedland",
                            "martinkettle",
                            "maryriddell",
                            "nickcohen",
                            "peterpreston",
                            "pollytoynbee",
                            "royhattersley",
                            "simonhoggart",
                            "willhutton",
                            "zoewilliams",
                        ]
                    ),
                    # There are book reviews, and articles on the following four topics
                    "topic": datasets.features.ClassLabel(names=["Politics", "Society", "UK", "World", "Books"]),
                    "article": datasets.Value("string"),
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
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)

        # This folder contains the orginal/2013 dataset
        data_dir = os.path.join(dl_dir, "Guardian", "Guardian_original")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"data_dir": data_dir, "samples_folders": self.config.train_folder, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"data_dir": data_dir, "samples_folders": self.config.test_folder, "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"data_dir": data_dir, "samples_folders": self.config.valid_folder, "split": "valid"},
            ),
        ]

    def _generate_examples(self, data_dir, samples_folders, split):
        """ Yields examples. """
        # Yields (key, example) tuples from the dataset

        # Training and validation are on 1 topic/genre, while testing is on multiple topics
        # We convert the sample folders into list (from string)
        if samples_folders.count(",") == 0:
            samples_folders = [samples_folders]
        else:
            samples_folders = samples_folders.split(",")

        # the dataset is structured as:
        # |-Topic1
        # |---author 1
        # |------- article-1
        # |------- article-2
        # |---author 2
        # |------- article-1
        # |------- article-2
        # |-Topic2
        # ...

        for topic in samples_folders:
            full_path = os.path.join(data_dir, topic)

            for author in os.listdir(full_path):

                list_articles = os.listdir(os.path.join(full_path, author))
                if len(list_articles) == 0:
                    # Some authors have no articles on certain topics
                    continue

                for id_, article in enumerate(list_articles):
                    path_2_author = os.path.join(full_path, author)
                    path_2_article = os.path.join(path_2_author, article)

                    with open(path_2_article, "r", encoding="utf8", errors="ignore") as f:
                        art = f.readlines()

                    # The whole article is stored as one line. We access the 1st element of the list
                    # to store it as string, not as a list
                    yield id_, {
                        "article": art[0],
                        "author": author,
                        "topic": topic,
                    }
