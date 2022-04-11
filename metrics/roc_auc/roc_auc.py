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
Use Cases:
    - **binary**
    - **multiclass**
    - **multilabel**
"""

_KWARGS_DESCRIPTION = """
Args:
    references (array-like of shape (n_samples,) or (n_samples, n_classes)): Ground truth labels. Expects
        different input based on use case:
        - binary: expects a list, with one entry for each sample
        - multiclass: expects a list, with one entry for each sample
        - multilabel: expects a list[list], with one sub-list for each sample, and one entry per class
                        in each of the sub-lists
    prediction_scores (array-like of shape (n_samples,) or (n_samples, n_classes)): Ground truth labels.
        Expects different input based on use case:
        - binary: expects a list, with one entry for each sample
        - multiclass: expects a list, with one entry for each sample
        - multilabel: expects a list[list], with one sub-list for each sample, and one entry per class
                        in each of the sub-lists
    average (`str`): Type of average, and is ignored in the binary use case. Defaults to 'macro'. Options are:
        - 'micro': Calculates metrics globally by considering each lement of the label indicator
                    matrix as a label. Does not work with the multiclass use case.
        - 'macro': Calculate metrics for each label, and find their unweighted mean.  This does
                    not take label imbalance into account.
        - 'weighted': Calculate metrics for each label, and find their average, weighted by support (i.e.
                    the number of true instances for each label).
        - 'samples': Calculate metrics for each instance, and find their average. Does not work with the
                    multiclass use case.
        - None:  No average is calculated, and scores for each class are returned.
    sample_weight (array-like of shape (n_samples,)): Sample weights. Defaults to None.
    max_fpr (`float`): If not None, the standardized partial AUC over the range [0, max_fpr] is returned.
        Must be larger than 0 and less than or equal to 1. Defaults to None. Note: For the multiclass use
        case, max_fpr should be either `None` or `1.0` as ROC AUC partial computation is not currently
        supported for multiclass.
    multi_class (`str`): Only used for multiclass targets, where it is required. Determines the type of
        configuration to use. Options are:
        - 'ovr': Stands for One-vs-rest. Computes the AUC of each class against the rest [3]_ [4]_. This
            treats the multiclass case in the same way as the multilabel case. Sensitive to class imbalance
            even when `average == 'macro'`, because class imbalance affects the composition of each of the
            'rest' groupings.
        - 'ovo': Stands for One-vs-one. Computes the average AUC of all possible pairwise combinations of
            classes [5]_. Insensitive to class imbalance when `average == 'macro'`.
    labels (array-like of shape (n_classes,)): Only used for multiclass targets. List of labels that index the classes in 
        `prediction_scores`. If `None`, the numerical or lexicographical order of the labels in 
        `prediction_scores` is used. Defaults to `None`.
        
Returns:
    roc_auc (`float` or array-like of shape (n_classes,)): Returns array if `average='None'`
Examples:
    Example 1:
        >>> roc_auc_score = datasets.load_metric("roc_auc")
        >>> refs = [1, 0, 1, 1, 0, 0]
        >>> pred_scores = [0.5, 0.2, 0.99, 0.3, 0.1, 0.7]
        >>> results = roc_auc_score.compute(references=refs, prediction_scores=pred_scores)
        >>> print(round(results['roc_auc']))
        0.78
"""

_CITATION = """\

"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class ROCAUC(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features( #if self.config_name == "multilabel" {
                {
                    "prediction_scores": datasets.Sequence(datasets.Value("float")),
                    "references": datasets.Value("int32"),
                }
                if self.config_name == "multilabel"
                # elif self.config_name == "multiclass" {
                else {
                    "references": datasets.Sequence(datasets.Value("int32")),
                    "prediction_scores": datasets.Sequence(datasets.Value("float")),
                }
                if self.config_name == "multiclass"
                else {
                    "references": datasets.Value("int32"),
                    "prediction_scores": datasets.Value("float"),
                }
            ),
            reference_urls=["https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html"],
        )

    def _compute(self, references, prediction_scores, average='macro', sample_weight=None, max_fpr=None, multi_class='raise', labels=None):
        return {
            "roc_auc": roc_auc_score(references, prediction_scores, average=average, sample_weight=sample_weight, max_fpr=max_fpr, multi_class=multi_class, labels=labels)
        }
