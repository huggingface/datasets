# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors.
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
""" SQuAD metric. """

import nlp

from .evaluate import evaluate


_CITATION = """\
@inproceedings{Rajpurkar2016SQuAD10,
  title={SQuAD: 100, 000+ Questions for Machine Comprehension of Text},
  author={Pranav Rajpurkar and Jian Zhang and Konstantin Lopyrev and Percy Liang},
  booktitle={EMNLP},
  year={2016}
}
"""

_DESCRIPTION = """
This metric wrap the official scoring script for version 1 of the Stanford Question Answering Dataset (SQuAD).

Stanford Question Answering Dataset (SQuAD) is a reading comprehension dataset, consisting of questions posed by
crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span,
from the corresponding reading passage, or the question might be unanswerable.
"""

_KWARGS_DESCRIPTION = """
Computes SQuAD scores (F1 and EM).
Args:
    predictions: List of question-answers dictionaries with the following key-values:
        - 'id': id of the question-answer pair as given in the references (see below)
        - 'prediction_text': the text of the answer
    references: List of question-answers dictionaries with the following key-values:
        - 'id': id of the question-answer pair (see above),
        - 'answers': a Dict {'text': list of possible texts for the answer, as a list of strings}
Returns:
    'exact_match': Exact match (the normalized answer exactly match the gold answer)
    'f1': The F-score of predicted tokens versus the gold answer
"""


class Squad(nlp.Metric):
    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=nlp.Features(
                {
                    "predictions": {"id": nlp.Value("string"), "prediction_text": nlp.Value("string")},
                    "references": {
                        "id": nlp.Value("string"),
                        "answers": nlp.features.Sequence(
                            {
                                "text": nlp.Value("string"),
                                "answer_start": nlp.Value("int32"),
                            }
                        ),
                    },
                }
            ),
            codebase_urls=["https://rajpurkar.github.io/SQuAD-explorer/"],
            reference_urls=["https://rajpurkar.github.io/SQuAD-explorer/"],
        )

    def _compute(self, predictions, references):
        pred_dict = {prediction["id"]: prediction["prediction_text"] for prediction in predictions}
        dataset = [
            {
                "paragraphs": [
                    {
                        "qas": [
                            {
                                "answers": [{"text": answer_text} for answer_text in ref["answers"]["text"]],
                                "id": ref["id"],
                            }
                            for ref in references
                        ]
                    }
                ]
            }
        ]
        score = evaluate(dataset=dataset, predictions=pred_dict)
        return score
