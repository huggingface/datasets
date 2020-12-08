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
"""Inquisitive Question Generation for High Level Text Comprehension"""

from __future__ import absolute_import, division, print_function

import itertools
import os

import datasets


_CITATION = """\
@InProceedings{ko2020inquisitive,
  author    = {Ko, Wei-Jen and Chen, Te-Yuan and Huang, Yiyan and Durrett, Greg and Li, Junyi Jessy},
  title     = {Inquisitive Question Generation for High Level Text Comprehension},
  booktitle = {Proceedings of EMNLP},
  year      = {2020},
}
"""

_DESCRIPTION = """\
A dataset of about 20k questions that are elicited from readers as they naturally read through a document sentence by sentence. \
Compared to existing datasets, INQUISITIVE questions target more towards high-level (semantic and discourse) comprehension of text. \
Because these questions are generated while the readers are processing the information, the questions directly communicate gaps between \
the reader’s and writer’s knowledge about the events described in the text, and are not necessarily answered in the document itself. \
This type of question reflects a real-world scenario: if one has questions during reading, some of them are answered by the text later on, \
the rest are not, but any of them would help further the reader’s understanding at the particular point when they asked it. \
This resource could enable question generation models to simulate human-like curiosity and cognitive processing, which may open up a new realm of applications.
"""

_ARTICLES_URL = "https://github.com/wjko2/INQUISITIVE/raw/master/articles.tgz"
_QUESTIONS_URL = "https://github.com/wjko2/INQUISITIVE/raw/master/questions.txt"

ALL_ARTICLE_IDS = list(range(1, 1501))
DEV_ARTICLE_IDS = list(itertools.chain(range(1, 101), range(1051, 1101)))
TEST_ARTICLE_IDS = list(itertools.chain(range(101, 151), range(501, 551), range(1101, 1151)))
DEV_AND_TEST_IDS = DEV_ARTICLE_IDS + TEST_ARTICLE_IDS
TRAIN_ARTICLE_IDS = [id_ for id_ in ALL_ARTICLE_IDS if id_ not in DEV_AND_TEST_IDS]


class InquisitiveQgConfig(datasets.BuilderConfig):
    """BuilderConfig for INQUISITIVE."""

    def __init__(self, **kwrags):
        """BuilderConfig for INQUISITIVE.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(InquisitiveQgConfig, self).__init__(**kwrags)


class InquisitiveQg(datasets.GeneratorBasedBuilder):
    """Inquisitive Question Generation for High Level Text Comprehension"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        InquisitiveQgConfig(name="plain_text", version=datasets.Version("1.0.0", ""), description="plain_text"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "article_id": datasets.Value("int32"),
                    "article": datasets.Value("string"),
                    "sentence_id": datasets.Value("int32"),
                    "sentence": datasets.Value("string"),
                    "span": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "span_start_position": datasets.Value("int32"),
                    "span_end_position": datasets.Value("int32"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/wjko2/INQUISITIVE",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        questions_file = dl_manager.download(_QUESTIONS_URL)
        extracted_path = dl_manager.download_and_extract(_ARTICLES_URL)
        articles_dir = os.path.join(extracted_path, "article")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "articles_dir": articles_dir,
                    "questions_file": questions_file,
                    "article_ids": TRAIN_ARTICLE_IDS,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "articles_dir": articles_dir,
                    "questions_file": questions_file,
                    "article_ids": DEV_ARTICLE_IDS,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "articles_dir": articles_dir,
                    "questions_file": questions_file,
                    "article_ids": TEST_ARTICLE_IDS,
                },
            ),
        ]

    def _generate_examples(self, articles_dir, questions_file, article_ids):
        with open(questions_file, encoding="utf-8") as f:
            questions_counter = 0
            rows = f.readlines()
            for i, row in enumerate(rows):
                if i == 0:
                    continue  # skip header line
                row = row.strip()
                cols = row.split("\t")

                article_id = int(cols[0])
                if article_id not in article_ids:
                    continue

                # read the article file
                fname = str(article_id).rjust(4, "0") + ".txt"
                article_path = os.path.join(articles_dir, fname)
                with open(article_path, encoding="utf-8") as f:
                    article = f.read()

                id_ = str(questions_counter)
                example = {
                    "article_id": article_id,
                    "sentence_id": int(cols[1]),
                    "sentence": cols[2],
                    "span": cols[3],
                    "question": cols[4],
                    "span_start_position": cols[5],
                    "span_end_position": cols[6],
                    "id": id_,
                    "article": article,
                }
                yield id_, example
