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
"""Accuracy metric for the Mathematics Aptitude Test of Heuristics (MATH) dataset."""

import math_equivalence  # From: git+https://github.com/hendrycks/math.git

import datasets


_CITATION = """\
@article{hendrycksmath2021,
  title={Measuring Mathematical Problem Solving With the MATH Dataset},
  author={Dan Hendrycks
    and Collin Burns
    and Saurav Kadavath
    and Akul Arora
    and Steven Basart
    and Eric Tang
    and Dawn Song
    and Jacob Steinhardt},
  journal={arXiv preprint arXiv:2103.03874},
  year={2021}
}
"""


_DESCRIPTION = """\
This metric is used to assess performance on the Mathematics Aptitude Test of Heuristics (MATH) dataset.
It first canonicalizes the inputs (e.g., converting "1/2" to "\\frac{1}{2}") and then computes accuracy.
"""


_KWARGS_DESCRIPTION = r"""
Calculates accuracy after canonicalizing inputs.

Args:
    predictions: list of predictions to score. Each prediction
        is a string that contains natural language and LaTex.
    references: list of reference for each prediction. Each
        reference is a string that contains natural language
        and LaTex.
Returns:
    accuracy: accuracy after canonicalizing inputs
        (e.g., converting "1/2" to "\\frac{1}{2}")

Examples:
    >>> metric = datasets.load_metric("competition_math")
    >>> results = metric.compute(references=["\\frac{1}{2}"], predictions=["1/2"])
    >>> print(results)
    {'accuracy': 1.0}
"""


@datasets.utils.file_utils.add_end_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class CompetitionMathMetric(datasets.Metric):
    """Accuracy metric for the MATH dataset."""

    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string"),
                    "references": datasets.Value("string"),
                }
            ),
            # Homepage of the metric for documentation
            homepage="https://github.com/hendrycks/math",
            # Additional links to the codebase or references
            codebase_urls=["https://github.com/hendrycks/math"],
        )

    def _compute(self, predictions, references):
        """Returns the scores"""
        n_correct = 0.0
        for i, j in zip(predictions, references):
            n_correct += 1.0 if math_equivalence.is_equiv(i, j) else 0.0
        accuracy = n_correct / len(predictions)
        return {
            "accuracy": accuracy,
        }
