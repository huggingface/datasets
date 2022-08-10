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
"""COVID-QA: A Question Answering Dataset for COVID-19."""


import json

import datasets
from datasets.tasks import QuestionAnsweringExtractive


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{moller2020covid,
  title={COVID-QA: A Question Answering Dataset for COVID-19},
  author={M{\"o}ller, Timo and Reina, Anthony and Jayakumar, Raghavan and Pietsch, Malte},
  booktitle={Proceedings of the 1st Workshop on NLP for COVID-19 at ACL 2020},
  year={2020}
}
"""

# You can copy an official description
_DESCRIPTION = """\
COVID-QA is a Question Answering dataset consisting of 2,019 question/answer pairs annotated by volunteer biomedical \
experts on scientific articles related to COVID-19.
"""

_HOMEPAGE = "https://github.com/deepset-ai/COVID-QA"

_LICENSE = "Apache License 2.0"

_URL = "https://raw.githubusercontent.com/deepset-ai/COVID-QA/master/data/question-answering/"
_URLs = {"covid_qa_deepset": _URL + "COVID-QA.json"}


class CovidQADeepset(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="covid_qa_deepset", version=VERSION, description="COVID-QA deepset"),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "document_id": datasets.Value("int32"),
                "context": datasets.Value("string"),
                "question": datasets.Value("string"),
                "is_impossible": datasets.Value("bool"),
                "id": datasets.Value("int32"),
                "answers": datasets.features.Sequence(
                    {
                        "text": datasets.Value("string"),
                        "answer_start": datasets.Value("int32"),
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
            task_templates=[
                QuestionAnsweringExtractive(
                    question_column="question", context_column="context", answers_column="answers"
                )
            ],
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
            for article in covid_qa["data"]:
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    document_id = paragraph["document_id"]
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        is_impossible = qa["is_impossible"]
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "document_id": document_id,
                            "context": context,
                            "question": question,
                            "is_impossible": is_impossible,
                            "id": id_,
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
