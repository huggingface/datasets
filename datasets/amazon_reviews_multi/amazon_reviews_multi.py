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

"""The Multilingual Amazon Reviews Corpus"""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """\
@inproceedings{marc_reviews,
    title={The Multilingual Amazon Reviews Corpus},
    author={Keung, Phillip and Lu, Yichao and Szarvas, György and Smith, Noah A.},
    booktitle={Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing},
    year={2020}
}
"""

_LICENSE = """\
By accessing the Multilingual Amazon Reviews Corpus ("Reviews Corpus"), you agree that the Reviews Corpus is an Amazon Service subject to the Amazon.com Conditions of Use (https://www.amazon.com/gp/help/customer/display.html/ref=footer_cou?ie=UTF8&nodeId=508088) and you agree to be bound by them, with the following additional conditions:

In addition to the license rights granted under the Conditions of Use, Amazon or its content providers grant you a limited, non-exclusive, non-transferable, non-sublicensable, revocable license to access and use the Reviews Corpus for purposes of academic research. You may not resell, republish, or make any commercial use of the Reviews Corpus or its contents, including use of the Reviews Corpus for commercial research, such as research related to a funding or consultancy contract, internship, or other relationship in which the results are provided for a fee or delivered to a for-profit organization. You may not (a) link or associate content in the Reviews Corpus with any personal information (including Amazon customer accounts), or (b) attempt to determine the identity of the author of any content in the Reviews Corpus. If you violate any of the foregoing conditions, your license to access and use the Reviews Corpus will automatically terminate without prejudice to any of the other rights or remedies Amazon may have.
"""

_DESCRIPTION = """\
We provide an Amazon product reviews dataset for multilingual text classification. The dataset contains reviews in English, Japanese, German, French, Chinese and Spanish, collected between November 1, 2015 and November 1, 2019. Each record in the dataset contains the review text, the review title, the star rating, an anonymized reviewer ID, an anonymized product ID and the coarse-grained product category (e.g. ‘books’, ‘appliances’, etc.) The corpus is balanced across stars, so each star rating constitutes 20% of the reviews in each language.

For each language, there are 200,000, 5,000 and 5,000 reviews in the training, development and test sets respectively. The maximum number of reviews per reviewer is 20 and the maximum number of reviews per product is 20. All reviews are truncated after 2,000 characters, and all reviews are at least 20 characters long.

Note that the language of a review does not necessarily match the language of its marketplace (e.g. reviews from amazon.de are primarily written in German, but could also be written in English, etc.). For this reason, we applied a language detection algorithm based on the work in Bojanowski et al. (2017) to determine the language of the review text and we removed reviews that were not written in the expected language.
"""

_LANGUAGES = {
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "ja": "Japanese",
    "zh": "Chinese",
}
_ALL_LANGUAGES = "all_languages"
_VERSION = "1.0.0"
_HOMEPAGE_URL = "https://registry.opendata.aws/amazon-reviews-ml/"
_DOWNLOAD_URL = "https://amazon-reviews-ml.s3-us-west-2.amazonaws.com/json/{split}/dataset_{lang}_{split}.json"


class AmazonReviewsMultiConfig(datasets.BuilderConfig):
    """BuilderConfig for AmazonReviewsMultiConfig."""

    def __init__(self, languages=None, **kwargs):
        super(AmazonReviewsMultiConfig, self).__init__(version=datasets.Version(_VERSION, ""), **kwargs),
        self.languages = languages


class AmazonReviewsMulti(datasets.GeneratorBasedBuilder):
    """The Multilingual Amazon Reviews Corpus"""

    BUILDER_CONFIGS = [
        AmazonReviewsMultiConfig(
            name=_ALL_LANGUAGES,
            languages=_LANGUAGES,
            description="A collection of Amazon reviews specifically designed to aid research in multilingual text classification.",
        )
    ] + [
        AmazonReviewsMultiConfig(
            name=lang,
            languages=[lang],
            description=f"{_LANGUAGES[lang]} examples from a collection of Amazon reviews specifically designed to aid research in multilingual text classification",
        )
        for lang in _LANGUAGES
    ]
    BUILDER_CONFIG_CLASS = AmazonReviewsMultiConfig
    DEFAULT_CONFIG_NAME = _ALL_LANGUAGES

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "review_id": datasets.Value("string"),
                    "product_id": datasets.Value("string"),
                    "reviewer_id": datasets.Value("string"),
                    "stars": datasets.Value("int32"),
                    "review_body": datasets.Value("string"),
                    "review_title": datasets.Value("string"),
                    "language": datasets.Value("string"),
                    "product_category": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            license=_LICENSE,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_urls = [_DOWNLOAD_URL.format(split="train", lang=lang) for lang in self.config.languages]
        dev_urls = [_DOWNLOAD_URL.format(split="dev", lang=lang) for lang in self.config.languages]
        test_urls = [_DOWNLOAD_URL.format(split="test", lang=lang) for lang in self.config.languages]

        train_paths = dl_manager.download_and_extract(train_urls)
        dev_paths = dl_manager.download_and_extract(dev_urls)
        test_paths = dl_manager.download_and_extract(test_urls)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"file_paths": train_paths}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"file_paths": dev_paths}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"file_paths": test_paths}),
        ]

    def _generate_examples(self, file_paths):
        row_count = 0
        for file_path in file_paths:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    yield row_count, json.loads(line)
                    row_count += 1
