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
"""CovidQA, a question answering dataset specifically designed for COVID-19."""


import json

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@article{tang2020rapidly,
  title={Rapidly Bootstrapping a Question Answering Dataset for COVID-19},
  author={Tang, Raphael and Nogueira, Rodrigo and Zhang, Edwin and Gupta, Nikhil and Cam, Phuong and Cho, Kyunghyun and Lin, Jimmy},
  journal={arXiv preprint arXiv:2004.11339},
  year={2020}
}
"""

_DESCRIPTION = """\
CovidQA is the beginnings of a question answering dataset specifically designed for COVID-19, built by hand from \
knowledge gathered from Kaggle's COVID-19 Open Research Dataset Challenge.
"""

_HOMEPAGE = "http://covidqa.ai"

_LICENSE = "Apache License 2.0"

_URL = "https://raw.githubusercontent.com/castorini/pygaggle/master/data/"
_URLs = {"covid_qa_castorini": _URL + "kaggle-lit-review-0.2.json"}


class CovidQaCastorini(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.2.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="covid_qa_castorini",
            version=VERSION,
            description="CovidQA, a question answering dataset specifically designed for COVID-19",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "category_name": datasets.Value("string"),
                "question_query": datasets.Value("string"),
                "keyword_query": datasets.Value("string"),
                "answers": datasets.features.Sequence(
                    {
                        "id": datasets.Value("string"),
                        "title": datasets.Value("string"),
                        "exact_answer": datasets.Value("string"),
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
        url = _URLs[self.config.name]
        downloaded_filepath = dl_manager.download_and_extract(url)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_filepath},
            ),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            covid_qa = json.load(f)
            for article_idx, article in enumerate(covid_qa["categories"]):
                category_name = article["name"]
                for paragraph_idx, paragraph in enumerate(article["sub_categories"]):
                    question_query = paragraph["nq_name"]
                    keyword_query = paragraph["kq_name"]

                    ids = [answer["id"] for answer in paragraph["answers"]]
                    titles = [answer["title"] for answer in paragraph["answers"]]
                    exact_answers = [answer["exact_answer"] for answer in paragraph["answers"]]

                    yield f"{article_idx}_{paragraph_idx}", {
                        "category_name": category_name,
                        "question_query": question_query,
                        "keyword_query": keyword_query,
                        "answers": {
                            "id": ids,
                            "title": titles,
                            "exact_answer": exact_answers,
                        },
                    }
