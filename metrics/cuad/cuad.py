# Copyright 2020 The HuggingFace Datasets Authors.
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
""" CUAD metric. """

import datasets

from .evaluate import evaluate


_CITATION = """\
@article{hendrycks2021cuad,
      title={CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review},
      author={Dan Hendrycks and Collin Burns and Anya Chen and Spencer Ball},
      journal={arXiv preprint arXiv:2103.06268},
      year={2021}
}
"""

_DESCRIPTION = """
This metric wrap the official scoring script for version 1 of the Contract
Understanding Atticus Dataset (CUAD).
Contract Understanding Atticus Dataset (CUAD) v1 is a corpus of more than 13,000 labels in 510
commercial legal contracts that have been manually labeled to identify 41 categories of important
clauses that lawyers look for when reviewing contracts in connection with corporate transactions.
"""

_KWARGS_DESCRIPTION = """
Computes CUAD scores (EM, F1, AUPR, Precision@80%Recall, and Precision@90%Recall).
Args:
    predictions: List of question-answers dictionaries with the following key-values:
        - 'id': id of the question-answer pair as given in the references (see below)
        - 'prediction_text': list of possible texts for the answer, as a list of strings
        depending on a threshold on the confidence probability of each prediction.
    references: List of question-answers dictionaries with the following key-values:
        - 'id': id of the question-answer pair (see above),
        - 'answers': a Dict in the CUAD dataset format
            {
                'text': list of possible texts for the answer, as a list of strings
                'answer_start': list of start positions for the answer, as a list of ints
            }
            Note that answer_start values are not taken into account to compute the metric.
Returns:
    'exact_match': Exact match (the normalized answer exactly match the gold answer)
    'f1': The F-score of predicted tokens versus the gold answer
    'aupr': Area Under the Precision-Recall curve
    'prec_at_80_recall': Precision at 80% recall
    'prec_at_90_recall': Precision at 90% recall
Examples:
    >>> predictions = [{'prediction_text': ['The seller:', 'The buyer/End-User: Shenzhen LOHAS Supply Chain Management Co., Ltd.'], 'id': 'LohaCompanyltd_20191209_F-1_EX-10.16_11917878_EX-10.16_Supply Agreement__Parties'}]
    >>> references = [{'answers': {'answer_start': [143, 49], 'text': ['The seller:', 'The buyer/End-User: Shenzhen LOHAS Supply Chain Management Co., Ltd.']}, 'id': 'LohaCompanyltd_20191209_F-1_EX-10.16_11917878_EX-10.16_Supply Agreement__Parties'}]
    >>> cuad_metric = datasets.load_metric("cuad")
    >>> results = cuad_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'exact_match': 100.0, 'f1': 100.0, 'aupr': 0.0, 'prec_at_80_recall': 1.0, 'prec_at_90_recall': 1.0}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class CUAD(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": {
                        "id": datasets.Value("string"),
                        "prediction_text": datasets.features.Sequence(datasets.Value("string")),
                    },
                    "references": {
                        "id": datasets.Value("string"),
                        "answers": datasets.features.Sequence(
                            {
                                "text": datasets.Value("string"),
                                "answer_start": datasets.Value("int32"),
                            }
                        ),
                    },
                }
            ),
            codebase_urls=["https://www.atticusprojectai.org/cuad"],
            reference_urls=["https://www.atticusprojectai.org/cuad"],
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
