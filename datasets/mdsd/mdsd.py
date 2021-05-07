# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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

# Lint as: python3
import os
import datasets
import xml
from lxml import html
import xmltodict

_DESCRIPTION = """\
The Multi-Domain Sentiment Dataset contains product reviews taken from Amazon.com from 4 product types (domains): Kitchen, Books, DVDs, and Electronics. Each domain has several thousand reviews, but the exact number varies by domain. Reviews contain star ratings (1 to 5 stars) that can be converted into binary labels if needed. This page contains some descriptions about the data.
"""
_HOMEPAGE_URL = ""
_CITATION = None
_URL = "http://www.cs.jhu.edu/~mdredze/datasets/sentiment/domain_sentiment_data.tar.gz"
_MISSING_BOOKS_UNLABELED = (
    "http://www.cs.jhu.edu/~mdredze/datasets/sentiment/book.unlabeled.gz"
)
_VERSION = "1.0.0"
_DOMAINS = ["books", "dvd", "electronics", "kitchen_&_housewares"]
_ALL = "all"


class MDSDConfig(datasets.BuilderConfig):
    def __init__(self, *args, domains=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.domains = domains


class MDSD(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        MDSDatasetConfig(
            name=domain,
            domains=[domain],
            description=f"domain: {domain}.",
            version=datasets.Version(_VERSION),
        )
        for domain in _DOMAINS
    ] + [
        MDSDatasetConfig(
            name=_ALL,
            domains=_DOMAINS,
            description=f"All sources included: books, dvd, electronics, kitchen_&_housewares",
            version=datasets.Version(_VERSION),
        )
    ]
    BUILDER_CONFIG_CLASS = MDSDatasetConfig
    DEFAULT_CONFIG_NAME = _ALL

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "unique_id": datasets.Value("string"),
                    "asin": datasets.Value("string"),
                    "product_name": datasets.Value("string"),
                    "product_type": datasets.Value("string"),
                    "helpful": datasets.Value("string"),
                    "rating": datasets.Value("float32"),
                    "title": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "reviewer": datasets.Value("string"),
                    "reviewer_location": datasets.Value("string"),
                    "review_text": datasets.Value("string"),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_URL)
        unlabeled_books_path = dl_manager.download_and_extract(_MISSING_BOOKS_UNLABELED)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "datapath": os.path.join(path, "sorted_data_acl"),
                    "datatype": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "datapath": os.path.join(path, "sorted_data_acl"),
                    "unlabeled_books_path": unlabeled_books_path,
                    "datatype": "test",
                },
            ),
        ]

    def _generate_examples(self, datapath, datatype, unlabeled_books_path=None):
        for domain in self.config.domains:
            if datatype == "train":
                datapaths = [
                    os.path.join(datapath, domain, "positive.review"),
                    os.path.join(datapath, domain, "negative.review"),
                ]
            elif datatype == "test":
                if domain == "books":
                    datapaths = [unlabeled_books_path]
                else:
                    datapaths = [os.path.join(datapath, domain, "unlabeled.review")]
            else:
                raise Exception("Invalid datatype. Try one of: train, test")

            sentence_counter = 0

            for dp in datapaths:
                with open(dp, "r", encoding="utf-8") as f:
                    xml_string = f.read()

                reviews = html.fromstring(xml_string)
                for review in reviews:
                    try:
                        review = dict(xmltodict.parse(html.tostring(review))["review"])
                        review["rating"] = float(review["rating"])
                        review["id"] = sentence_counter
                        for k, v in review.items():
                            if v is None and k != "rating":
                                review[k] = ""
                        # there are 4 invalid formatted examples. we will ignore them
                        # these examples are only available in books unlabeled set
                        num_types = len(set([type(review[x]) for x in review]))
                        if num_types == 3:
                            sentence_counter += 1
                            yield sentence_counter, review
                    except xml.parsers.expat.ExpatError:
                        print("Ignoring example that could not be parsed properly.")
