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
import string

import numpy as np

import datasets


_DESCRIPTION = """
Returns the rate at which the input predicted strings exactly match their references, ignoring any strings input as part of the regexes_to_ignore list.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions: List of predicted texts.
    references: List of reference texts.
    regexes_to_ignore: List, defaults to None. Regex expressions of characters to
        ignore when calculating the exact matches. Note: these regexes are removed
        from the input data before the changes based on the options below (e.g. ignore_case,
        ignore_punctuation, ignore_numbers) are applied.
    ignore_case: Boolean, defaults to False. If true, turns everything
        to lowercase so that capitalization differences are ignored.
    ignore_punctuation: Boolean, defaults to False. If true, removes all punctuation before
        comparing predictions and references.
    ignore_numbers: Boolean, defaults to False. If true, removes all punctuation before
        comparing predictions and references.
Returns:
    exact_match: Dictionary containing exact_match rate. Possible values are between 0.0 and 100.0, inclusive.
Examples:
    >>> exact_match = datasets.load_metric("exact_match")
    >>> refs = ["the cat", "theater", "YELLING", "agent007"]
    >>> preds = ["cat?", "theater", "yelling", "agent"]
    >>> results = exact_match.compute(references=refs, predictions=preds)
    >>> print(round(results["exact_match"], 1))
    25.0

    >>> exact_match = datasets.load_metric("exact_match")
    >>> refs = ["the cat", "theater", "YELLING", "agent007"]
    >>> preds = ["cat?", "theater", "yelling", "agent"]
    >>> results = exact_match.compute(references=refs, predictions=preds, regexes_to_ignore=["the ", "yell"], ignore_case=True, ignore_punctuation=True)
    >>> print(round(results["exact_match"], 1))
    50.0


    >>> exact_match = datasets.load_metric("exact_match")
    >>> refs = ["the cat", "theater", "YELLING", "agent007"]
    >>> preds = ["cat?", "theater", "yelling", "agent"]
    >>> results = exact_match.compute(references=refs, predictions=preds, regexes_to_ignore=["the ", "yell", "YELL"], ignore_case=True, ignore_punctuation=True)
    >>> print(round(results["exact_match"], 1))
    75.0

    >>> exact_match = datasets.load_metric("exact_match")
    >>> refs = ["the cat", "theater", "YELLING", "agent007"]
    >>> preds = ["cat?", "theater", "yelling", "agent"]
    >>> results = exact_match.compute(references=refs, predictions=preds, regexes_to_ignore=["the ", "yell", "YELL"], ignore_case=True, ignore_punctuation=True, ignore_numbers=True)
    >>> print(round(results["exact_match"], 1))
    100.0

    >>> exact_match = datasets.load_metric("exact_match")
    >>> refs = ["The cat sat on the mat.", "Theaters are great.", "It's like comparing oranges and apples."]
    >>> preds = ["The cat sat on the mat?", "Theaters are great.", "It's like comparing apples and oranges."]
    >>> results = exact_match.compute(references=refs, predictions=preds)
    >>> print(round(results["exact_match"], 1))
    33.3

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
            reference_urls=[],
        )

    def _compute(
        self,
        predictions,
        references,
        regexes_to_ignore=None,
        ignore_case=False,
        ignore_punctuation=False,
        ignore_numbers=False,
    ):

        if regexes_to_ignore is not None:
            for s in regexes_to_ignore:
                predictions = np.array([re.sub(s, "", x) for x in predictions])
                references = np.array([re.sub(s, "", x) for x in references])
        else:
            predictions = np.asarray(predictions)
            references = np.asarray(references)

        if ignore_case:
            predictions = np.char.lower(predictions)
            references = np.char.lower(references)

        if ignore_punctuation:
            repl_table = string.punctuation.maketrans("", "", string.punctuation)
            predictions = np.char.translate(predictions, table=repl_table)
            references = np.char.translate(references, table=repl_table)

        if ignore_numbers:
            repl_table = string.digits.maketrans("", "", string.digits)
            predictions = np.char.translate(predictions, table=repl_table)
            references = np.char.translate(references, table=repl_table)

        score_list = predictions == references

        return {"exact_match": np.mean(score_list) * 100}
