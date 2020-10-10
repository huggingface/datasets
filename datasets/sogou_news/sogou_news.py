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
"""Sogou News"""

from __future__ import absolute_import, division, print_function

import csv
import ctypes
import os

import datasets


csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))


_CITATION = """\
@misc{zhang2015characterlevel,
    title={Character-level Convolutional Networks for Text Classification},
    author={Xiang Zhang and Junbo Zhao and Yann LeCun},
    year={2015},
    eprint={1509.01626},
    archivePrefix={arXiv},
    primaryClass={cs.LG}
}
"""

_DESCRIPTION = """\
The Sogou News dataset is a mixture of 2,909,551 news articles from the SogouCA and SogouCS news corpora, in 5 categories.
The number of training samples selected for each class is 90,000 and testing 12,000. Note that the Chinese characters have been converted to Pinyin.
classification labels of the news are determined by their domain names in the URL. For example, the news with
URL http://sports.sohu.com is categorized as a sport class.
"""

_DATA_URL = "https://s3.amazonaws.com/fast-ai-nlp/sogou_news_csv.tgz"


class Sogou_News(datasets.GeneratorBasedBuilder):
    """Sogou News dataset"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=["sports", "finance", "entertainment", "automobile", "technology"]
                    ),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="",  # didn't find a real homepage
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": os.path.join(dl_dir, "sogou_news_csv", "test.csv")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_dir, "sogou_news_csv", "train.csv")}
            ),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        with open(filepath, encoding="utf-8") as csv_file:
            data = csv.reader(csv_file)
            for id_, row in enumerate(data):
                yield id_, {"title": row[1], "content": row[2], "label": int(row[0]) - 1}
