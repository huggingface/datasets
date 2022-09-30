# Copyright 2022 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""MAE - Mean Absolute Error Metric"""

from sklearn.metrics import mean_absolute_error

import datasets


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

_DESCRIPTION = """\
Mean Absolute Error (MAE) is the mean of the magnitude of difference between the predicted and actual
values.
"""


_KWARGS_DESCRIPTION = """
Args:
    predictions: array-like of shape (n_samples,) or (n_samples, n_outputs)
        Estimated target values.
    references: array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values.
    sample_weight: array-like of shape (n_samples,), default=None
        Sample weights.
    multioutput: {"raw_values", "uniform_average"} or array-like of shape (n_outputs,), default="uniform_average"
        Defines aggregating of multiple output values. Array-like value defines weights used to average errors.

                 "raw_values" : Returns a full set of errors in case of multioutput input.

                 "uniform_average" : Errors of all outputs are averaged with uniform weight.

Returns:
    mae : mean absolute error.
        If multioutput is "raw_values", then mean absolute error is returned for each output separately. If multioutput is "uniform_average" or an ndarray of weights, then the weighted average of all output errors is returned.
        MAE output is non-negative floating point. The best value is 0.0.
Examples:

    >>> mae_metric = datasets.load_metric("mae")
    >>> predictions = [2.5, 0.0, 2, 8]
    >>> references = [3, -0.5, 2, 7]
    >>> results = mae_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'mae': 0.5}

    If you're using multi-dimensional lists, then set the config as follows :

    >>> mae_metric = datasets.load_metric("mae", "multilist")
    >>> predictions = [[0.5, 1], [-1, 1], [7, -6]]
    >>> references = [[0, 2], [-1, 2], [8, -5]]
    >>> results = mae_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'mae': 0.75}
    >>> results = mae_metric.compute(predictions=predictions, references=references, multioutput='raw_values')
    >>> print(results)
    {'mae': array([0.5, 1. ])}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Mae(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(self._get_feature_types()),
            reference_urls=[
                "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html"
            ],
        )

    def _get_feature_types(self):
        if self.config_name == "multilist":
            return {
                "predictions": datasets.Sequence(datasets.Value("float")),
                "references": datasets.Sequence(datasets.Value("float")),
            }
        else:
            return {
                "predictions": datasets.Value("float"),
                "references": datasets.Value("float"),
            }

    def _compute(self, predictions, references, sample_weight=None, multioutput="uniform_average"):

        mae_score = mean_absolute_error(references, predictions, sample_weight=sample_weight, multioutput=multioutput)

        return {"mae": mae_score}
