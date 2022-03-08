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
    references: Ground truth (correct) target values.
    predictions: Estimated target values.
Returns:
    mae : mean absolute error.
Examples:

    >>> mae_metric = datasets.load_metric("mae")
    >>> results = mae_metric.compute(references=[3, -0.5, 2, 7], predictions=[2.5, 0.0, 2, 8])
    >>> print(results)
    {'mae': 0.5}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Mae(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("float"),
                    "references": datasets.Value("float"),
                }
            ),
            reference_urls=[
                "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html"
            ],
        )

    def _compute(self, predictions, references, sample_weight=None, multioutput="uniform_average"):

        mae_score = mean_absolute_error(references, predictions, sample_weight=sample_weight, multioutput=multioutput)

        return {"mae": mae_score}
