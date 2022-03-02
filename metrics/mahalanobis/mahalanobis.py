# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""Mahalanobis metric."""

import numpy as np

import datasets


_DESCRIPTION = """
Compute the Mahalanobis Distance

Mahalonobis distance is the distance between a point and a distribution.
And not between two distinct points. It is effectively a multivariate equivalent of the Euclidean distance.
It was introduced by Prof. P. C. Mahalanobis in 1936
and has been used in various statistical applications ever since
[source: https://www.machinelearningplus.com/statistics/mahalanobis-distance/]
"""

_CITATION = """\
@article{de2000mahalanobis,
  title={The mahalanobis distance},
  author={De Maesschalck, Roy and Jouan-Rimbaud, Delphine and Massart, D{\'e}sir{\'e} L},
  journal={Chemometrics and intelligent laboratory systems},
  volume={50},
  number={1},
  pages={1--18},
  year={2000},
  publisher={Elsevier}
}
"""

_KWARGS_DESCRIPTION = """
Args:
    X: List of datapoints to be compared with the `reference_distribution`.
    reference_distribution: List of datapoints from the reference distribution we want to compare to.
Returns:
    mahalanobis: The Mahalonobis distance for each datapoint in `X`.
Examples:

    >>> mahalanobis_metric = datasets.load_metric("mahalanobis")
    >>> results = mahalanobis_metric.compute(reference_distribution=[[0, 1], [1, 0]], X=[[0, 1]])
    >>> print(results)
    {'mahalanobis': array([0.5])}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Mahalanobis(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "X": datasets.Sequence(datasets.Value("float", id="sequence"), id="X"),
                }
            ),
        )

    def _compute(self, X, reference_distribution):

        # convert to numpy arrays
        X = np.array(X)
        reference_distribution = np.array(reference_distribution)

        # Assert that arrays are 2D
        if len(X.shape) != 2:
            raise ValueError("Expected `X` to be a 2D vector")
        if len(reference_distribution.shape) != 2:
            raise ValueError("Expected `reference_distribution` to be a 2D vector")
        if reference_distribution.shape[0] < 2:
            raise ValueError(
                "Expected `reference_distribution` to be a 2D vector with more than one element in the first dimension"
            )

        # Get mahalanobis distance for each prediction
        X_minus_mu = X - np.mean(reference_distribution)
        cov = np.cov(reference_distribution.T)
        try:
            inv_covmat = np.linalg.inv(cov)
        except np.linalg.LinAlgError:
            inv_covmat = np.linalg.pinv(cov)
        left_term = np.dot(X_minus_mu, inv_covmat)
        mahal_dist = np.dot(left_term, X_minus_mu.T).diagonal()

        return {"mahalanobis": mahal_dist}
