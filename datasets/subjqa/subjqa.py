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


import ast
import os

import pandas as pd

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
                "domain": datasets.Value("string"),
                "nn_mod": datasets.Value("string"),
                "nn_asp": datasets.Value("string"),
                "query_mod": datasets.Value("string"),
                "query_asp": datasets.Value("string"),
                "q_reviews_id": datasets.Value("string"),
                "question_subj_level": datasets.Value("int64"),
                "ques_subj_score": datasets.Value("float"),
                "is_ques_subjective": datasets.Value("bool"),
                "review_id": datasets.Value("string"),
                "id": datasets.Value("string"),
                "title": datasets.Value("string"),
                "context": datasets.Value("string"),
                "question": datasets.Value("string"),
                "answers": datasets.features.Sequence(
                    {
                        "text": datasets.Value("string"),
                        "answer_start": datasets.Value("int32"),
                        "answer_subj_level": datasets.Value("int64"),
                        "ans_subj_score": datasets.Value("float"),
                        "is_ans_subjective": datasets.Value("bool"),
                    }
                ),
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
        df = pd.read_csv(filepath)
        squad_format = self._convert_to_squad(df)
        for example in squad_format["data"]:
            title = example.get("title", "").strip()
            for paragraph in example["paragraphs"]:
                context = paragraph["context"].strip()
                for qa in paragraph["qas"]:
                    question = qa["question"].strip()
                    question_meta = {k: v for k, v in qa.items() if k in self.question_meta_columns}
                    id_ = qa["id"]
                    answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                    answers = [answer["text"].strip() for answer in qa["answers"]]
                    answer_meta = pd.DataFrame(qa["answers"], columns=self.answer_meta_columns).to_dict("list")
                    yield id_, {
                        **{
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {
                                **{
                                    "answer_start": answer_starts,
                                    "text": answers,
                                },
                                **answer_meta,
                            },
                        },
                        **question_meta,
                    }

    def _create_paragraphs(self, df):
        "A helper function to convert a pandas.DataFrame of (question, context, answer) rows to SQuAD paragraphs."
        self.question_meta_columns = [
            "domain",
            "nn_mod",
            "nn_asp",
            "query_mod",
            "query_asp",
            "q_reviews_id",
            "question_subj_level",
            "ques_subj_score",
            "is_ques_subjective",
            "review_id",
        ]
        self.answer_meta_columns = ["answer_subj_level", "ans_subj_score", "is_ans_subjective"]
        id2review = dict(zip(df["review_id"], df["review"]))
        pars = []
        for review_id, review in id2review.items():
            qas = []
            review_df = df.query(f"review_id == '{review_id}'")
            id2question = dict(zip(review_df["q_review_id"], review_df["question"]))

            for k, v in id2question.items():
                d = df.query(f"q_review_id == '{k}'").to_dict(orient="list")
                answer_starts = [ast.literal_eval(a)[0] for a in d["human_ans_indices"]]
                answer_meta = {k: v[0] for k, v in d.items() if k in self.answer_meta_columns}
                question_meta = {k: v[0] for k, v in d.items() if k in self.question_meta_columns}
                # Only fill answerable questions
                if pd.unique(d["human_ans_spans"])[0] != "ANSWERNOTFOUND":
                    answers = [
                        {**{"text": text, "answer_start": answer_start}, **answer_meta}
                        for text, answer_start in zip(d["human_ans_spans"], answer_starts)
                        if text != "ANSWERNOTFOUND"
                    ]
                else:
                    answers = []
                qas.append({**{"question": v, "id": k, "answers": answers}, **question_meta})
            # Slice off ANSWERNOTFOUND from context
            pars.append({"qas": qas, "context": review[: -len(" ANSWERNOTFOUND")]})
        return pars

    def _convert_to_squad(self, df):
        "A helper function to convert a pandas.DataFrame of product-based QA dataset into SQuAD format"
        groups = (
            df.groupby("item_id")
            .apply(self._create_paragraphs)
            .to_frame(name="paragraphs")
            .reset_index()
            .rename(columns={"item_id": "title"})
        )
        squad_data = {}
        squad_data["data"] = groups.to_dict(orient="records")
        return squad_data
