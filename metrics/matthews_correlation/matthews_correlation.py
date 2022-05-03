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
"""Matthews Correlation metric."""

from sklearn.metrics import matthews_corrcoef

import datasets


_DESCRIPTION = """
Compute the Matthews correlation coefficient (MCC)

The Matthews correlation coefficient is used in machine learning as a
measure of the quality of binary and multiclass classifications. It takes
into account true and false positives and negatives and is generally
regarded as a balanced measure which can be used even if the classes are of
very different sizes. The MCC is in essence a correlation coefficient value
between -1 and +1. A coefficient of +1 represents a perfect prediction, 0
an average random prediction and -1 an inverse prediction.  The statistic
is also known as the phi coefficient. [source: Wikipedia]
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (list of int): Predicted labels, as returned by a model.
    references (list of int): Ground truth labels.
    sample_weight (list of int, float, or bool): Sample weights. Defaults to `None`.
Returns:
    matthews_correlation (dict containing float): Matthews correlation.
Examples:
    Example 1, a basic example with only predictions and references as inputs:
        >>> matthews_metric = datasets.load_metric("matthews_correlation")
        >>> results = matthews_metric.compute(references=[1, 3, 2, 0, 3, 2],
        ...                                     predictions=[1, 2, 2, 0, 3, 3])
        >>> print(round(results['matthews_correlation'], 2))
        0.54

    Example 2, the same example as above, but also including sample weights:
        >>> matthews_metric = datasets.load_metric("matthews_correlation")
        >>> results = matthews_metric.compute(references=[1, 3, 2, 0, 3, 2],
        ...                                     predictions=[1, 2, 2, 0, 3, 3],
        ...                                     sample_weight=[0.5, 3, 1, 1, 1, 2])
        >>> print(round(results['matthews_correlation'], 2))
        0.1

    Example 3, the same example as above, but with sample weights that cause a negative correlation:
        >>> matthews_metric = datasets.load_metric("matthews_correlation")
        >>> results = matthews_metric.compute(references=[1, 3, 2, 0, 3, 2],
        ...                                     predictions=[1, 2, 2, 0, 3, 3],
        ...                                     sample_weight=[0.5, 1, 0, 0, 0, 1])
        >>> print(round(results['matthews_correlation'], 2))
        -0.25
"""

_CITATION = """\
@article{scikit-learn,
  title={Scikit-learn: Machine Learning in {P}ython},
  author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V.
         and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P.
         and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and
         Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.},
  journal={Journal of Machine Learning Research},
  volume={12},
  pages={2825--2830},
  year={2011}
}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class MatthewsCorrelation(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("int32"),
                    "references": datasets.Value("int32"),
                }
            ),
            reference_urls=[
                "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.matthews_corrcoef.html"
            ],
        )

    def _compute(self, predictions, references, sample_weight=None):
        return {
            "matthews_correlation": float(matthews_corrcoef(references, predictions, sample_weight=sample_weight)),
        }
