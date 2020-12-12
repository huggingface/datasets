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

# Lint as: python3
"""RuReviews: An Automatically Annotated Sentiment Analysis Dataset for Product Reviews in Russian"""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_DESCRIPTION = """\
The training dataset was collected from reviews on top-ranked goods form the major e-commerce site in Russian, where user-ranked scores were used as class labels on a 5-point scale. Since the same words in different product categories may have different sentiment polarity, it was decided to collect reviews only from one category, namely "Women’s Clothes and Accessories" category. It helped to get the collected dataset to consists of 821k automatically labelled reviews.

According to the obtained data, in some cases, it is complex task to correctly evaluate reviews with the same texts. For example, the review text “Fine” (translation from Russian into English) has 42.45% reviews with a score of “5”, 36% reviews with a score of “4”, 29.25% reviews with a score of “3”, and 0.94% reviews with a score of “2”. It is clear that such contradictions in the training dataset tend to affect the classification score. Therefore, we decided to mark these reviews with the class labels, which are the most common for these texts in the collected dataset. Moreover, sometimes it is also difficult to distinguish reviews with the close score values, e.g. reviews with score “1” and “2” or with score “4” and “5”. To overcome this issue, we transformed 5-point scale to 3-point scale by combining reviews with “1” and “2” into one “negative” class and reviews with “3” and “5” scores into another one “positive” class. Thus, the 5-star rating scale collapsed into 3 classes: negative, neutral, and positive reviews.

Since the data were collected from the top-ranked goods with high average rating, the amount of positive reviews considerably exceeded the amount of neutral and negative reviews. At the same time, we have no information about real-life class distribution for reviews, that is why we decided to use an undersampling technique to deal with imbalanced data. For each class 30k of reviews were randomly selected to make balanced dataset.
"""

_CITATION = """\
@INPROCEEDINGS{Smetanin-SA-2019,
  author={Sergey Smetanin and Michail Komarov},
  booktitle={2019 IEEE 21st Conference on Business Informatics (CBI)},
  title={Sentiment Analysis of Product Reviews in Russian using Convolutional Neural Networks},
  year={2019},
  volume={01},
  number={},
  pages={482-486},
  doi={10.1109/CBI.2019.00062},
  ISSN={2378-1963},
  month={July}
}
"""


_TRAIN_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/sismetanin/rureviews/master/women-clothing-accessories.3-class.balanced.csv"
)


class AppReviews(datasets.GeneratorBasedBuilder):
    """RuReviews: An Automatically Annotated Sentiment Analysis Dataset for Product Reviews in Russian"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "review_sentiment": datasets.Value("string"),
                }
            ),
            homepage="https://ieeexplore.ieee.org/document/8807792",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Distaster Response Messages examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader, None)
            for id_, row in enumerate(csv_reader):
                (row) = row

                yield id_, {
                    "review_sentiment": (str(row)),
                }
