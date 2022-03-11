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

import re
import time

import numpy as np

import datasets


_DESCRIPTION = """
Returns the rate at which the input predicted strings exactly match their references, ignoring characters in the chars_to_ignore string
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions: Predicted labels, as returned by a model.
    references: Ground truth labels.
    regexes_to_ignore: List, defaults to None. Regex expressions of characters to
        ignore when calculating the exact matches. Note: the regexes are applied after
        capitalization is normalized.
    ignore_capitalization: Boolean, defaults to False. If true, turns everything
        to lowercase so that capitalization differences are ignored.
Returns:
    exact_match: Dictionary containing exact_match rate. Possible values are between 0.0 and 100.0, inclusive.
Examples:
    >>> exact_match = datasets.load_metric("exact_match")
    >>> refs = ["the cat", "theater", "YELLING"]
    >>> preds = ["cat?", "theater", "yelling"]
    >>> results = exact_match.compute(references=refs, predictions=preds)
    >>> round(results["exact_match"], 1)
    33.3

    >>> exact_match = datasets.load_metric("exact_match")
    >>> refs = ["the cat", "theater", "YELLING"]
    >>> preds = ["cat?", "theater", "yelling"]
    >>> results = exact_match.compute(references=refs, predictions=preds, regexes_to_ignore=["the ", r"\?"])
    >>> round(results["exact_match"], 1)
    66.7


    >>> exact_match = datasets.load_metric("exact_match")
    >>> refs = ["the cat", "theater", "YELLING"]
    >>> preds = ["cat?", "theater", "yelling"]
    >>> results = exact_match.compute(references=refs, predictions=preds, regexes_to_ignore=["the ", r"\?"], ignore_capitalization=True)
    >>> round(results["exact_match"], 1)
    100.0
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

    def _compute(self, predictions, references, regexes_to_ignore=None, ignore_capitalization=False):

        if regexes_to_ignore is not None:
            for s in regexes_to_ignore:
                if ignore_capitalization:
                    predictions = np.array(list(map(lambda x: re.sub(s, "", x.lower()), predictions)))
                    references = np.array(list(map(lambda x: re.sub(s, "", x.lower()), references)))
                else:
                    predictions = np.array(list(map(lambda x: re.sub(s, "", x), predictions)))
                    references = np.array(list(map(lambda x: re.sub(s, "", x), references)))
        else:
            predictions = np.asarray(predictions)
            references = np.asarray(references)

        score_list = predictions == references

        return {"exact_match": np.mean(score_list) * 100}
