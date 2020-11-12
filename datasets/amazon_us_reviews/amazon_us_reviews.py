# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

"""Amazon Customer Reviews Dataset --- US REVIEWS DATASET."""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_CITATION = """\
"""

_DESCRIPTION = """\
Amazon Customer Reviews (a.k.a. Product Reviews) is one of Amazons iconic products. In a period of over two decades since the first review in 1995, millions of Amazon customers have contributed over a hundred million reviews to express opinions and describe their experiences regarding products on the Amazon.com website. This makes Amazon Customer Reviews a rich source of information for academic researchers in the fields of Natural Language Processing (NLP), Information Retrieval (IR), and Machine Learning (ML), amongst others. Accordingly, we are releasing this data to further research in multiple disciplines related to understanding customer product experiences. Specifically, this dataset was constructed to represent a sample of customer evaluations and opinions, variation in the perception of a product across geographical regions, and promotional intent or bias in reviews.

Over 130+ million customer reviews are available to researchers as part of this release. The data is available in TSV files in the amazon-reviews-pds S3 bucket in AWS US East Region. Each line in the data files corresponds to an individual review (tab delimited, with no quote and escape characters).

Each Dataset contains the following columns:

- marketplace: 2 letter country code of the marketplace where the review was written.
- customer_id: Random identifier that can be used to aggregate reviews written by a single author.
- review_id: The unique ID of the review.
- product_id: The unique Product ID the review pertains to. In the multilingual dataset the reviews for the same product in different countries can be grouped by the same product_id.
- product_parent: Random identifier that can be used to aggregate reviews for the same product.
- product_title: Title of the product.
- product_category: Broad product category that can be used to group reviews (also used to group the dataset into coherent parts).
- star_rating: The 1-5 star rating of the review.
- helpful_votes: Number of helpful votes.
- total_votes: Number of total votes the review received.
- vine: Review was written as part of the Vine program.
- verified_purchase: The review is on a verified purchase.
- review_headline: The title of the review.
- review_body: The review text.
- review_date: The date the review was written.
"""

_DATA_OPTIONS = [
    "Wireless_v1_00",
    "Watches_v1_00",
    "Video_Games_v1_00",
    "Video_DVD_v1_00",
    "Video_v1_00",
    "Toys_v1_00",
    "Tools_v1_00",
    "Sports_v1_00",
    "Software_v1_00",
    "Shoes_v1_00",
    "Pet_Products_v1_00",
    "Personal_Care_Appliances_v1_00",
    "PC_v1_00",
    "Outdoors_v1_00",
    "Office_Products_v1_00",
    "Musical_Instruments_v1_00",
    "Music_v1_00",
    "Mobile_Electronics_v1_00",
    "Mobile_Apps_v1_00",
    "Major_Appliances_v1_00",
    "Luggage_v1_00",
    "Lawn_and_Garden_v1_00",
    "Kitchen_v1_00",
    "Jewelry_v1_00",
    "Home_Improvement_v1_00",
    "Home_Entertainment_v1_00",
    "Home_v1_00",
    "Health_Personal_Care_v1_00",
    "Grocery_v1_00",
    "Gift_Card_v1_00",
    "Furniture_v1_00",
    "Electronics_v1_00",
    "Digital_Video_Games_v1_00",
    "Digital_Video_Download_v1_00",
    "Digital_Software_v1_00",
    "Digital_Music_Purchase_v1_00",
    "Digital_Ebook_Purchase_v1_00",
    "Camera_v1_00",
    "Books_v1_00",
    "Beauty_v1_00",
    "Baby_v1_00",
    "Automotive_v1_00",
    "Apparel_v1_00",
    "Digital_Ebook_Purchase_v1_01",
    "Books_v1_01",
    "Books_v1_02",
]

_DL_URLS = {
    name: "https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_" + name + ".tsv.gz"
    for name in _DATA_OPTIONS
}


class AmazonUSReviewsConfig(datasets.BuilderConfig):
    """BuilderConfig for AmazonUSReviews."""

    def __init__(self, **kwargs):
        """Constructs a AmazonUSReviewsConfig.
        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(AmazonUSReviewsConfig, self).__init__(version=datasets.Version("0.1.0", ""), **kwargs),


class AmazonUSReviews(datasets.GeneratorBasedBuilder):
    """AmazonUSReviews dataset."""

    BUILDER_CONFIGS = [
        AmazonUSReviewsConfig(  # pylint: disable=g-complex-comprehension
            name=config_name,
            description=(
                f"A dataset consisting of reviews of Amazon {config_name} products in US marketplace. Each product "
                "has its own version as specified with it."
            ),
        )
        for config_name in _DATA_OPTIONS
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "marketplace": datasets.Value("string"),
                    "customer_id": datasets.Value("string"),
                    "review_id": datasets.Value("string"),
                    "product_id": datasets.Value("string"),
                    "product_parent": datasets.Value("string"),
                    "product_title": datasets.Value("string"),
                    "product_category": datasets.Value("string"),
                    "star_rating": datasets.Value("int32"),
                    "helpful_votes": datasets.Value("int32"),
                    "total_votes": datasets.Value("int32"),
                    "vine": datasets.features.ClassLabel(names=["N", "Y"]),
                    "verified_purchase": datasets.features.ClassLabel(names=["N", "Y"]),
                    "review_headline": datasets.Value("string"),
                    "review_body": datasets.Value("string"),
                    "review_date": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://s3.amazonaws.com/amazon-reviews-pds/readme.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        url = _DL_URLS[self.config.name]
        path = dl_manager.download_and_extract(url)

        # There is no predefined train/val/test split for this dataset.
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"file_path": path}),
        ]

    def _generate_examples(self, file_path):
        """Generate features given the directory path.

        Args:
            file_path: path where the tsv file is stored
        Yields:
            The features.
        """

        with open(file_path, "r", encoding="utf-8") as tsvfile:
            # Need to disable quoting - as dataset contains invalid double quotes.
            reader = csv.DictReader(tsvfile, dialect="excel-tab", quoting=csv.QUOTE_NONE)
            for i, row in enumerate(reader):
                yield i, row
