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
""" Spearman correlation metric. """

import nlp
import numpy as np
import scipy.stats as stats

_CITATION = """\
"""

_DESCRIPTION = """
Spearman's rank correlation coefficient or Spearman's ρ, is a measure of rank
correlation (statistical dependence between the rankings of two variables).
It assesses how well the relationship between two variables can be described using
a monotonic function.

The Spearman correlation between two variables is equal to the Pearson correlation between the rank values of those two variables; while Pearson's correlation assesses linear relationships, Spearman's correlation assesses monotonic relationships (whether linear or not). If there are no repeated data values, a perfect Spearman correlation of +1 or −1 occurs when each of the variables is a perfect monotone function of the other.

Intuitively, the Spearman correlation between two variables will be high when observations have a similar (or identical for a correlation of 1) rank (i.e. relative position label of the observations within the variable: 1st, 2nd, 3rd, etc.) between the two variables, and low when observations have a dissimilar (or fully opposed for a correlation of −1) rank between the two variables.
"""

_KWARGS_DESCRIPTION = """
Computes Spearman's correlation.
Args:
    predictions: List of model probability over the distribution.
    references: List of samples (correct classes)
Returns:
    'correlation' : float or ndarray (2-D square)
        Spearman correlation matrix or correlation coefficient (if only 2
        variables are given as parameters. Correlation matrix is square with
        length equal to total number of variables (columns or rows) in ``a``
        and ``b`` combined.
    'pvalue' : float
        The two-sided p-value for a hypothesis test whose null hypothesis is
        that two sets of data are uncorrelated, has same dimension as rho.

"""

class Spearman(nlp.Metric):
    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            prediction_features=nlp.Value('int64'),
            reference_features=nlp.Value('int64'),
            codebase_urls=[],
            reference_urls=["https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient"],
            use_numpy=True,
        )

    def _compute(self, predictions: np.ndarray, references: np.ndarray):
        spearman_correlation = stats.spearmanr(
            predictions, references
        )
        return {'correlation': spearman_correlation[0],
                'pvalue': spearman_correlation[1]}
