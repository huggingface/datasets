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
Returns the rate at which the input predicted strings exactly match their references, ignoring characters in the chars_to_ignore string
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions: Predicted labels, as returned by a model.
    references: Ground truth labels.
    chars_to_ignore: String of characters to ignore when calculating the exact matches.
Returns:
    exact_match: Exact match rate. Possible values are between 0 and 1, inclusive.
Examples:

    >>> exact_match = datasets.load_metric("exact_match")
    >>> refs = ["happy birthday!", "welcome..."]
    >>> preds = ["happy birthday", "elcome"]
    >>> results = exact_match.compute(references=refs, predictions=preds)
    >>> print(results)
    {'exact_match': 0.0}
    >>> results = exact_match.compute(references=refs, predictions=preds, chars_to_ignore="!")
    >>> print(results)
    {'exact_match': 0.5}
    >>> results = exact_match.compute(references=refs, predictions=preds, chars_to_ignore="!.w")
    >>> print(results)
    {'exact_match': 1.0}
"""

_CITATION = """
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
        score_list = np.zeros(len(predictions))

        if chars_to_ignore is not None:
            translate_dict = chars_to_ignore.maketrans('', '', chars_to_ignore)
            predictions = np.char.translate(predictions, translate_dict)
            references = np.char.translate(references, translate_dict)
        else:
            predictions = np.asarray(predictions)
            references = np.asarray(references)

        score_list = predictions == references

        return {"exact_match": np.mean(score_list)}
