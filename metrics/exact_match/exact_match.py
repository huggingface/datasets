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
"""Exact Match metric."""

import numpy as np

import datasets


_DESCRIPTION = """
TO DO!
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions: Predicted labels, as returned by a model.
    references: Ground truth labels.
Returns:
    exact_match: Exact match score.
Examples:

    >>> exact_match = datasets.load_metric("exact_match")
    >>> results = exact_match.compute(references=["happy birthday!", "welcome"], predictions=["happy birthday!", "welcome"])
    >>> print(results)
    {'exact_match': 1.0}
"""

_CITATION = """
TO DO!
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class ExactMatch(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Value("string", id="sequence"),
                }
            ),
            reference_urls=[""],
        )

    def _compute(self, predictions, references, chars_to_ignore=None):
        assert len(predictions) == len(references)

        score_list = np.zeros(len(predictions))

        if chars_to_ignore is not None:
            translate_dict = chars_to_ignore.maketrans('', '', chars_to_ignore)

            for i in range(len(predictions)):
                if predictions[i].translate(translate_dict) == references[i].translate(translate_dict):
                    score_list[i] = 1

        else:
            for i in range(len(predictions)):
                if predictions[i] == references[i]:
                    score_list[i] = 1


        return {"exact_match": np.mean(score_list)}
