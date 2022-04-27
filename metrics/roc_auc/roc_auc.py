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
"""Accuracy metric."""

from sklearn.metrics import roc_auc_score

import datasets


_DESCRIPTION = """
This metric computes the area under the curve (AUC) for the Receiver Operating Characteristic Curve (ROC). The return values represent how well the model used is predicting the correct classes, based on the input data. A score of `0.5` means that the model is predicting exactly at chance, i.e. the model's predictions are correct at the same rate as if the predictions were being decided by the flip of a fair coin or the roll of a fair die. A score above `0.5` indicates that the model is doing better than chance, while a score below `0.5` indicates that the model is doing worse than chance.

This metric has three separate use cases:
    - binary: The case in which there are only two different label classes, and each example gets only one label. This is the default implementation.
    - multiclass: The case in which there can be more than two different label classes, but each example still gets only one label.
    - multilabel: The case in which there can be more than two different label classes, and each example can have more than one label.
"""

_KWARGS_DESCRIPTION = """
Args:
- references (array-like of shape (n_samples,) or (n_samples, n_classes)): Ground truth labels. Expects different input based on use case:
    - binary: expects an array-like of shape (n_samples,)
    - multiclass: expects an array-like of shape (n_samples,)
    - multilabel: expects an array-like of shape (n_samples, n_classes)
- prediction_scores (array-like of shape (n_samples,) or (n_samples, n_classes)): Ground truth labels. Expects different inputs based on use case:
    - binary: expects an array-like of shape (n_samples,)
    - multiclass: expects an array-like of shape (n_samples,)
    - multilabel: expects an array-like of shape (n_samples, n_classes)
- average (`str`): Type of average, and is ignored in the binary use case. Defaults to 'macro'. Options are:
    - `'micro'`: Calculates metrics globally by considering each element of the label indicator matrix as a label. Only works with the multilabel use case.
    - `'macro'`: Calculate metrics for each label, and find their unweighted mean.  This does not take label imbalance into account.
    - `'weighted'`: Calculate metrics for each label, and find their average, weighted by support (i.e. the number of true instances for each label).
    - `'samples'`: Calculate metrics for each instance, and find their average. Only works with the multilabel use case.
    - `None`:  No average is calculated, and scores for each class are returned. Only works with the multilabels use case.
- sample_weight (array-like of shape (n_samples,)): Sample weights. Defaults to None.
- max_fpr (`float`): If not None, the standardized partial AUC over the range [0, `max_fpr`] is returned. Must be greater than `0` and less than or equal to `1`. Defaults to `None`. Note: For the multiclass use case, `max_fpr` should be either `None` or `1.0` as ROC AUC partial computation is not currently supported for `multiclass`.
- multi_class (`str`): Only used for multiclass targets, where it is required. Determines the type of configuration to use. Options are:
    - `'ovr'`: Stands for One-vs-rest. Computes the AUC of each class against the rest. This treats the multiclass case in the same way as the multilabel case. Sensitive to class imbalance even when `average == 'macro'`, because class imbalance affects the composition of each of the 'rest' groupings.
    - `'ovo'`: Stands for One-vs-one. Computes the average AUC of all possible pairwise combinations of classes. Insensitive to class imbalance when `average == 'macro'`.
- labels (array-like of shape (n_classes,)): Only used for multiclass targets. List of labels that index the classes in
    `prediction_scores`. If `None`, the numerical or lexicographical order of the labels in
    `prediction_scores` is used. Defaults to `None`.
Returns:
    roc_auc (`float` or array-like of shape (n_classes,)): Returns array if in multilabel use case and `average='None'`. Otherwise, returns `float`.
Examples:
    Example 1:
        >>> roc_auc_score = datasets.load_metric("roc_auc")
        >>> refs = [1, 0, 1, 1, 0, 0]
        >>> pred_scores = [0.5, 0.2, 0.99, 0.3, 0.1, 0.7]
        >>> results = roc_auc_score.compute(references=refs, prediction_scores=pred_scores)
        >>> print(round(results['roc_auc'], 2))
        0.78

    Example 2:
        >>> roc_auc_score = datasets.load_metric("roc_auc", "multiclass")
        >>> refs = [1, 0, 1, 2, 2, 0]
        >>> pred_scores = [[0.3, 0.5, 0.2],
        ...                 [0.7, 0.2, 0.1],
        ...                 [0.005, 0.99, 0.005],
        ...                 [0.2, 0.3, 0.5],
        ...                 [0.1, 0.1, 0.8],
        ...                 [0.1, 0.7, 0.2]]
        >>> results = roc_auc_score.compute(references=refs, prediction_scores=pred_scores, multi_class='ovr')
        >>> print(round(results['roc_auc'], 2))
        0.85

    Example 3:
        >>> roc_auc_score = datasets.load_metric("roc_auc", "multilabel")
        >>> refs = [[1, 1, 0],
        ...         [1, 1, 0],
        ...         [0, 1, 0],
        ...         [0, 0, 1],
        ...         [0, 1, 1],
        ...         [1, 0, 1]]
        >>> pred_scores = [[0.3, 0.5, 0.2],
        ...                 [0.7, 0.2, 0.1],
        ...                 [0.005, 0.99, 0.005],
        ...                 [0.2, 0.3, 0.5],
        ...                 [0.1, 0.1, 0.8],
        ...                 [0.1, 0.7, 0.2]]
        >>> results = roc_auc_score.compute(references=refs, prediction_scores=pred_scores, average=None)
        >>> print([round(res, 2) for res in results['roc_auc']])
        [0.83, 0.38, 0.94]
"""

_CITATION = """\
@article{doi:10.1177/0272989X8900900307,
author = {Donna Katzman McClish},
title ={Analyzing a Portion of the ROC Curve},
journal = {Medical Decision Making},
volume = {9},
number = {3},
pages = {190-195},
year = {1989},
doi = {10.1177/0272989X8900900307},
    note ={PMID: 2668680},
URL = {https://doi.org/10.1177/0272989X8900900307},
eprint = {https://doi.org/10.1177/0272989X8900900307}
}


@article{10.1023/A:1010920819831,
author = {Hand, David J. and Till, Robert J.},
title = {A Simple Generalisation of the Area Under the ROC Curve for Multiple Class Classification Problems},
year = {2001},
issue_date = {November 2001},
publisher = {Kluwer Academic Publishers},
address = {USA},
volume = {45},
number = {2},
issn = {0885-6125},
url = {https://doi.org/10.1023/A:1010920819831},
doi = {10.1023/A:1010920819831},
journal = {Mach. Learn.},
month = {oct},
pages = {171–186},
numpages = {16},
keywords = {Gini index, AUC, error rate, ROC curve, receiver operating characteristic}
}


@article{scikit-learn,
title={Scikit-learn: Machine Learning in {P}ython},
author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V. and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P. and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.},
journal={Journal of Machine Learning Research},
volume={12},
pages={2825--2830},
year={2011}
}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class ROCAUC(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "prediction_scores": datasets.Sequence(datasets.Value("float")),
                    "references": datasets.Value("int32"),
                }
                if self.config_name == "multiclass"
                else {
                    "references": datasets.Sequence(datasets.Value("int32")),
                    "prediction_scores": datasets.Sequence(datasets.Value("float")),
                }
                if self.config_name == "multilabel"
                else {
                    "references": datasets.Value("int32"),
                    "prediction_scores": datasets.Value("float"),
                }
            ),
            reference_urls=["https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html"],
        )

    def _compute(
        self,
        references,
        prediction_scores,
        average="macro",
        sample_weight=None,
        max_fpr=None,
        multi_class="raise",
        labels=None,
    ):
        return {
            "roc_auc": roc_auc_score(
                references,
                prediction_scores,
                average=average,
                sample_weight=sample_weight,
                max_fpr=max_fpr,
                multi_class=multi_class,
                labels=labels,
            )
        }
