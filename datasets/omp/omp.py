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
"""The “One Million Posts” corpus is an annotated data set consisting of
user comments posted to an Austrian newspaper website (in German language)."""


from pathlib import Path

import pandas as pd

import datasets


_CITATION = """\
@InProceedings{Schabus2017,
  Author    = {Dietmar Schabus and Marcin Skowron and Martin Trapp},
  Title     = {One Million Posts: A Data Set of German Online Discussions},
  Booktitle = {Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR)},
  Pages     = {1241--1244},
  Year      = {2017},
  Address   = {Tokyo, Japan},
  Doi       = {10.1145/3077136.3080711},
  Month     = aug
}
"""

_DESCRIPTION = """\
The “One Million Posts” corpus is an annotated data set consisting of
user comments posted to an Austrian newspaper website (in German language).

DER STANDARD is an Austrian daily broadsheet newspaper. On the newspaper’s website,
there is a discussion section below each news article where readers engage in
online discussions. The data set contains a selection of user posts from the
12 month time span from 2015-06-01 to 2016-05-31. There are 11,773 labeled and
1,000,000 unlabeled posts in the data set. The labeled posts were annotated by
professional forum moderators employed by the newspaper.

The data set contains the following data for each post:

* Post ID
* Article ID
* Headline (max. 250 characters)
* Main Body (max. 750 characters)
* User ID (the user names used by the website have been re-mapped to new numeric IDs)
* Time stamp
* Parent post (replies give rise to tree-like discussion thread structures)
* Status (online or deleted by a moderator)
* Number of positive votes by other community members
* Number of negative votes by other community members

For each article, the data set contains the following data:

* Article ID
* Publishing date
* Topic Path (e.g.: Newsroom / Sports / Motorsports / Formula 1)
* Title
* Body

Detailed descriptions of the post selection and annotation procedures are given in the paper.

## Annotated Categories

Potentially undesirable content:

* Sentiment (negative/neutral/positive)
    An important goal is to detect changes in the prevalent sentiment in a discussion, e.g.,
    the location within the fora and the point in time where a turn from positive/neutral
    sentiment to negative sentiment takes place.
* Off-Topic (yes/no)
    Posts which digress too far from the topic of the corresponding article.
* Inappropriate (yes/no)
    Swearwords, suggestive and obscene language, insults, threats etc.
* Discriminating (yes/no)
    Racist, sexist, misogynistic, homophobic, antisemitic and other misanthropic content.

Neutral content that requires a reaction:

* Feedback (yes/no)
    Sometimes users ask questions or give feedback to the author of the article or the
    newspaper in general, which may require a reply/reaction.

Potentially desirable content:

* Personal Stories (yes/no)
    In certain fora, users are encouraged to share their personal stories, experiences,
    anecdotes etc. regarding the respective topic.
* Arguments Used (yes/no)
    It is desirable for users to back their statements with rational argumentation,
    reasoning and sources.
"""

_HOMEPAGE = "https://ofai.github.io/million-post-corpus/"

_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License"

_URLs = {
    "posts_labeled": "https://github.com/aseifert/million-post-corpus/raw/master/data/posts_labeled.csv.xz",
    "posts_unlabeled": "https://github.com/aseifert/million-post-corpus/raw/master/data/posts_unlabeled.csv.xz",
    "articles": "https://github.com/aseifert/million-post-corpus/raw/master/data/articles.csv.xz",
}


class Omp(datasets.GeneratorBasedBuilder):
    """The “One Million Posts” corpus is an annotated data set consisting of user comments
    posted to an Austrian newspaper website (in German language). Annotated categories include:
    sentiment (negative/neutral/positive), off-topic (yes/no), inappropriate (yes/no),
    discriminating (yes/no), feedback (yes/no), personal story (yes/no), arguments used (yes/no)."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="posts_labeled",
            version=VERSION,
            description="This part of the dataset includes labeled posts (11,773 annotated posts)",
        ),
        datasets.BuilderConfig(
            name="posts_unlabeled",
            version=VERSION,
            description="This part of the dataset includes unlabeled posts (1,000,000)",
        ),
        datasets.BuilderConfig(
            name="articles",
            version=VERSION,
            description="This part of the dataset includes the articles that the comments were posted to (~12k)",
        ),
    ]

    DEFAULT_CONFIG_NAME = (
        "posts_labeled"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        if self.config.name == "posts_labeled":
            features = datasets.Features(
                {
                    "ID_Post": datasets.Value("string"),
                    "ID_Parent_Post": datasets.Value("string"),
                    "ID_Article": datasets.Value("string"),
                    "ID_User": datasets.Value("string"),
                    "CreatedAt": datasets.Value("string"),
                    "Status": datasets.Value("string"),
                    "Headline": datasets.Value("string"),
                    "Body": datasets.Value("string"),
                    "PositiveVotes": datasets.Value("int32"),
                    "NegativeVotes": datasets.Value("int32"),
                    "Category": datasets.features.ClassLabel(
                        names=[
                            "ArgumentsUsed",
                            "Discriminating",
                            "Inappropriate",
                            "OffTopic",
                            "PersonalStories",
                            "PossiblyFeedback",
                            "SentimentNegative",
                            "SentimentNeutral",
                            "SentimentPositive",
                        ]
                    ),
                    "Value": datasets.Value("int32"),
                    "Fold": datasets.Value("int32"),
                }
            )
        elif self.config.name == "posts_unlabeled":
            features = datasets.Features(
                {
                    "ID_Post": datasets.Value("string"),
                    "ID_Parent_Post": datasets.Value("string"),
                    "ID_Article": datasets.Value("string"),
                    "ID_User": datasets.Value("string"),
                    "CreatedAt": datasets.Value("string"),
                    "Status": datasets.Value("string"),
                    "Headline": datasets.Value("string"),
                    "Body": datasets.Value("string"),
                    "PositiveVotes": datasets.Value("int32"),
                    "NegativeVotes": datasets.Value("int32"),
                }
            )
        elif self.config.name == "articles":
            features = datasets.Features(
                {
                    "ID_Article": datasets.Value("string"),
                    "Path": datasets.Value("string"),
                    "publishingDate": datasets.Value("string"),
                    "Title": datasets.Value("string"),
                    "Body": datasets.Value("string"),
                }
            )
        else:
            assert False

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

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URLs[self.config.name]
        data_path = Path(dl_manager.download_and_extract(my_urls))
        if data_path.is_dir():
            if self.config.name == "posts_labeled":
                fname = "posts_labeled.csv.gz"
            elif self.config.name == "posts_unlabeled":
                fname = "posts_unlabeled.csv.gz"
            elif self.config.name == "articles":
                fname = "articles.csv.gz"
            else:
                assert False
            data_path = data_path / fname

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": str(data_path), "split": "train"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        if self.config.name in ["posts_labeled", "posts_unlabeled"]:
            dtype = {"ID_Post": str, "ID_Parent_Post": str, "ID_Article": str, "ID_User": str}
        elif self.config.name == "articles":
            dtype = {"ID_Article": str, "Path": str, "publishingDate": str, "ID_User": str}
        data = pd.read_csv(filepath, compression=None, dtype=dtype).fillna("")
        for id_, row in data.iterrows():
            yield id_, row.to_dict()
