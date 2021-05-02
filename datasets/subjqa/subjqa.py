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
"""SubjQA is a question answering dataset that focuses on subjective questions and answers.
The dataset consists of roughly 10,000 questions over reviews from 6 different domains: books, movies, grocery,
electronics, TripAdvisor (i.e. hotels), and restaurants."""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{bjerva20subjqa,
    title = "SubjQA: A Dataset for Subjectivity and Review Comprehension",
    author = "Bjerva, Johannes  and
      Bhutani, Nikita  and
      Golahn, Behzad  and
      Tan, Wang-Chiew  and
      Augenstein, Isabelle",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing",
    month = November,
    year = "2020",
    publisher = "Association for Computational Linguistics",
}
"""

_DESCRIPTION = """SubjQA is a question answering dataset that focuses on subjective questions and answers.
The dataset consists of roughly 10,000 questions over reviews from 6 different domains: books, movies, grocery,
electronics, TripAdvisor (i.e. hotels), and restaurants."""

_HOMEPAGE = ""

_LICENSE = ""

_URLs = {"default": "https://github.com/lewtun/SubjQA/archive/refs/heads/master.zip"}


class Subjqa(datasets.GeneratorBasedBuilder):
    """SubjQA is a question answering dataset that focuses on subjective questions and answers."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="books", version=VERSION, description="Amazon book reviews"),
        datasets.BuilderConfig(name="electronics", version=VERSION, description="Amazon electronics reviews"),
        datasets.BuilderConfig(name="grocery", version=VERSION, description="Amazon grocery reviews"),
        datasets.BuilderConfig(name="movies", version=VERSION, description="Amazon movie reviews"),
        datasets.BuilderConfig(name="restaurants", version=VERSION, description="Yelp restaurant reviews"),
        datasets.BuilderConfig(name="tripadvisor", version=VERSION, description="TripAdvisor hotel reviews"),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "item_id": datasets.Value("string"),
                "domain": datasets.Value("string"),
                "nn_mod": datasets.Value("string"),
                "nn_asp": datasets.Value("string"),
                "query_mod": datasets.Value("string"),
                "query_asp": datasets.Value("string"),
                "q_review_id": datasets.Value("string"),
                "q_reviews_id": datasets.Value("string"),
                "question": datasets.Value("string"),
                "question_subj_level": datasets.Value("int64"),
                "ques_subj_score": datasets.Value("float"),
                "is_ques_subjective": datasets.Value("bool"),
                "review_id": datasets.Value("string"),
                "review": datasets.Value("string"),
                "human_ans_spans": datasets.Value("string"),
                "human_ans_indices": datasets.Value("string"),
                "answer_subj_level": datasets.Value("int64"),
                "ans_subj_score": datasets.Value("float"),
                "is_ans_subjective": datasets.Value("bool"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URLs["default"])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, f"SubjQA-master/SubjQA/{self.config.name}/splits/train.csv")
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, f"SubjQA-master/SubjQA/{self.config.name}/splits/test.csv")
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, f"SubjQA-master/SubjQA/{self.config.name}/splits/dev.csv")
                },
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            column_names = next(csv_reader)
            for _id, row in enumerate(csv_reader):
                yield _id, {column_name: value for column_name, value in zip(column_names, row)}
