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
"""Recall metric."""

from sklearn.metrics import recall_score

import datasets


_DESCRIPTION = """
Recall is the fraction of the positive examples that were correctly labeled by the model as positive. It can be computed with the equation:
Recall = TP / (TP + FN)
Where TP is the true positives and FN is the false negatives.
"""


_KWARGS_DESCRIPTION = """
Args:
- **predictions** (`list` of `int`): The predicted labels.
- **references** (`list` of `int`): The ground truth labels.
- **labels** (`list` of `int`): The set of labels to include when `average` is not set to `binary`, and their order when average is `None`. Labels present in the data can be excluded in this input, for example to calculate a multiclass average ignoring a majority negative class, while labels not present in the data will result in 0 components in a macro average. For multilabel targets, labels are column indices. By default, all labels in y_true and y_pred are used in sorted order. Defaults to None.
- **pos_label** (`int`): The class label to use as the 'positive class' when calculating the recall. Defaults to `1`.
- **average** (`string`): This parameter is required for multiclass/multilabel targets. If None, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data. Defaults to `'binary'`.
    - `'binary'`: Only report results for the class specified by `pos_label`. This is applicable only if the target labels and predictions are binary.
    - `'micro'`: Calculate metrics globally by counting the total true positives, false negatives, and false positives.
    - `'macro'`: Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
    - `'weighted'`: Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). This alters `'macro'` to account for label imbalance. Note that it can result in an F-score that is not between precision and recall.
    - `'samples'`: Calculate metrics for each instance, and find their average (only meaningful for multilabel classification).
- **sample_weight** (`list` of `float`): Sample weights Defaults to `None`.
- **zero_division** (): Sets the value to return when there is a zero division. Defaults to .
    - `'warn'`: If there is a zero division, the return value is `0`, but warnings are also raised.
    - `0`: If there is a zero division, the return value is `0`.
    - `1`: If there is a zero division, the return value is `1`.

Returns:
- **recall** (`float`, or `array` of `float`): Either the general recall score, or the recall scores for individual classes, depending on the values input to `labels` and `average`. Minimum possible value is 0. Maximum possible value is 1. A higher recall means that more of the positive examples have been labeled correctly. Therefore, a higher recall is generally considered better.

Examples:

    Example 1-A simple example with some errors
        >>> recall_metric = datasets.load_metric('recall')
        >>> results = recall_metric.compute(references=[0, 0, 1, 1, 1], predictions=[0, 1, 0, 1, 1])
        >>> print(results)
        {'recall': 0.6666666666666666}

    Example 2-The same example as Example 1, but with `pos_label=0` instead of the default `pos_label=1`.
        >>> recall_metric = datasets.load_metric('recall')
        >>> results = recall_metric.compute(references=[0, 0, 1, 1, 1], predictions=[0, 1, 0, 1, 1], pos_label=0)
        >>> print(results)
        {'recall': 0.5}

    Example 3-The same example as Example 1, but with `sample_weight` included.
        >>> recall_metric = datasets.load_metric('recall')
        >>> sample_weight = [0.9, 0.2, 0.9, 0.3, 0.8]
        >>> results = recall_metric.compute(references=[0, 0, 1, 1, 1], predictions=[0, 1, 0, 1, 1], sample_weight=sample_weight)
        >>> print(results)
        {'recall': 0.55}

    Example 4-A multiclass example, using different averages.
        >>> recall_metric = datasets.load_metric('recall')
        >>> predictions = [0, 2, 1, 0, 0, 1]
        >>> references = [0, 1, 2, 0, 1, 2]
        >>> results = recall_metric.compute(predictions=predictions, references=references, average='macro')
        >>> print(results)
        {'recall': 0.3333333333333333}
        >>> results = recall_metric.compute(predictions=predictions, references=references, average='micro')
        >>> print(results)
        {'recall': 0.3333333333333333}
        >>> results = recall_metric.compute(predictions=predictions, references=references, average='weighted')
        >>> print(results)
        {'recall': 0.3333333333333333}
        >>> results = recall_metric.compute(predictions=predictions, references=references, average=None)
        >>> print(results)
        {'recall': array([1., 0., 0.])}
"""


_CITATION = """
@article{scikit-learn, title={Scikit-learn: Machine Learning in {P}ython}, author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V. and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P. and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.}, journal={Journal of Machine Learning Research}, volume={12}, pages={2825--2830}, year={2011}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Recall(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Sequence(datasets.Value("int32")),
                    "references": datasets.Sequence(datasets.Value("int32")),
                }
                if self.config_name == "multilabel"
                else {
                    "predictions": datasets.Value("int32"),
                    "references": datasets.Value("int32"),
                }
            ),
            reference_urls=["https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html"],
        )

    def _compute(
        self,
        predictions,
        references,
        labels=None,
        pos_label=1,
        average="binary",
        sample_weight=None,
        zero_division="warn",
    ):
        score = recall_score(
            references,
            predictions,
            labels=labels,
            pos_label=pos_label,
            average=average,
            sample_weight=sample_weight,
            zero_division=zero_division,
        )
        return {"recall": float(score) if score.size == 1 else score}
