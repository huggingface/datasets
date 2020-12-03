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
"""Arabic Book Reviews."""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_DESCRIPTION = """\
This dataset contains over 63,000 book reviews in Arabic.\
It is the largest sentiment analysis dataset for Arabic to-date.\
The book reviews were harvested from the website Goodreads during the month or March 2013.\
Each book review comes with the goodreads review id, the user id, the book id, the rating (1 to 5) and the text of the review.
"""

_CITATION = """\
@inproceedings{aly2013labr,
  title={Labr: A large scale arabic book reviews dataset},
  author={Aly, Mohamed and Atiya, Amir},
  booktitle={Proceedings of the 51st Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)},
  pages={494--498},
  year={2013}
}
"""

_URL = "https://raw.githubusercontent.com/mohamedadaly/LABR/master/data/"
_URLS = {
    "train": _URL + "5class-balanced-train.txt",
    "test": _URL + "5class-balanced-test.txt",
    "reviews": _URL + "reviews.tsv",
}


class LabrConfig(datasets.BuilderConfig):
    """BuilderConfig for Labr."""

    def __init__(self, **kwargs):
        """BuilderConfig for Labr.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(LabrConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class Labr(datasets.GeneratorBasedBuilder):
    """Labr dataset."""

    BUILDER_CONFIGS = [
        LabrConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "1",
                            "2",
                            "3",
                            "4",
                            "5",
                        ]
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/mohamedadaly/LABR",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URLS)
        self.reviews_path = data_dir["reviews"]
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"directory": data_dir["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"directory": data_dir["test"]}),
        ]

    def _generate_examples(self, directory):
        """Generate examples."""
        # For labeled examples, extract the label from the path.
        reviews = []
        with open(self.reviews_path, encoding="utf-8") as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            for line in tsvreader:
                reviews.append(line)

        with open(directory, encoding="utf-8") as f:
            for id_, record in enumerate(f.read().splitlines()):
                rating, _, _, _, review_text = reviews[int(record)]
                yield str(id_), {"text": review_text, "label": rating}
