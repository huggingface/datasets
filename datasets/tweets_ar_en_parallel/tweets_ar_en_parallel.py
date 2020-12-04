"""Bilingual Corpus of Arabic-English Parallel Tweets"""

from __future__ import absolute_import, division, print_function

import os

import pandas as pd

import datasets


_CITATION = """\
@inproceedings{Mubarak2020bilingualtweets,
title={Constructing a Bilingual Corpus of Parallel Tweets},
author={Mubarak, Hamdy and Hassan, Sabit and Abdelali, Ahmed},
booktitle={Proceedings of 13th Workshop on Building and Using Comparable Corpora (BUCC)},
address={Marseille, France},
year={2020}
}
"""

_DESCRIPTION = """\
    Twitter users often post parallel tweets—tweets that contain the same content but are
    written in different languages. Parallel tweets can be an important resource for developing
    machine translation (MT) systems among other natural language processing (NLP) tasks. This
    resource is a result of a generic method for collecting parallel tweets. Using the method,
    we compiled a bilingual corpus of English-Arabic parallel tweets and a list of Twitter accounts
    who post English-Arabic tweets regularly. Additionally, we annotate a subset of Twitter accounts
    with their countries of origin and topic of interest, which provides insights about the population
    who post parallel tweets.
"""

_URL = "https://alt.qcri.org/resources/bilingual_corpus_of_parallel_tweets"

_DATA_URL = "https://alt.qcri.org/wp-content/uploads/2020/08/Bilingual-Corpus-of-Arabic-English-Parallel-Tweets.zip"


class ParallelTweetsConfig(datasets.BuilderConfig):
    """BuilderConfig for Arabic-English Parallel Tweets"""

    def __init__(self, description, data_url, citation, url, **kwrags):
        """
        Args:
            description: `string`, brief description of the dataset
            data_url: `dictionary`, dict with url for each split of data.
            citation: `string`, citation for the dataset.
            url: `string`, url for information about the dataset.
            **kwrags: keyword arguments frowarded to super
        """
        super(ParallelTweetsConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwrags)
        self.description = description
        self.data_url = data_url
        self.citation = citation
        self.url = url


class TweetsArEnParallel(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        ParallelTweetsConfig(name=name, description=_DESCRIPTION, data_url=_DATA_URL, citation=_CITATION, url=_URL)
        for name in ["parallelTweets", "accountList", "countryTopicAnnotation"]
    ]
    BUILDER_CONFIG_CLASS = ParallelTweetsConfig

    def _info(self):
        features = {}
        if self.config.name == "parallelTweets":
            features["ArabicTweetID"] = datasets.Value("int64")
            features["EnglishTweetID"] = datasets.Value("int64")
        if self.config.name == "accountList":
            features["account"] = datasets.Value("string")
        if self.config.name == "countryTopicAnnotation":
            features["account"] = datasets.Value("string")
            countries = ["QA", "BH", "AE", "OM", "SA", "PL", "JO", "IQ", "Other", "EG", "KW", "SY"]
            features["country"] = datasets.features.ClassLabel(names=countries)
            topics = [
                "Gov",
                "Culture",
                "Education",
                "Sports",
                "Travel",
                "Events",
                "Business",
                "Science",
                "Politics",
                "Health",
                "Governoment",
                "Media",
            ]
            features["topic"] = datasets.features.ClassLabel(names=topics)
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(self.config.data_url)
        dl_dir = os.path.join(dl_dir, "ArEnParallelTweets")
        if self.config.name == "parallelTweets":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "parallelTweets.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if self.config.name == "accountList":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "accountList.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]
        if self.config.name == "countryTopicAnnotation":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "countryTopicAnnotation.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

    def _generate_examples(self, **args):
        filename = args["datafile"]
        if self.config.name == "parallelTweets":
            df = pd.read_csv(filename)
            for id_, row in df.iterrows():
                yield id_, {"ArabicTweetID": row["ArabicTweetID"], "EnglishTweetID": row["EnglishTweetID"]}

        if self.config.name == "accountList":
            df = pd.read_csv(filename, names=["account"])
            for id_, row in df.iterrows():
                yield id_, {
                    "account": row["account"],
                }

        if self.config.name == "countryTopicAnnotation":
            df = pd.read_csv(filename)
            for id_, row in df.iterrows():
                yield id_, {"account": row["Account"], "country": row["Country"], "topic": row["Topic"]}
