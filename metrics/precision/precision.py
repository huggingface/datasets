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
"""Precision metric."""

from sklearn.metrics import precision_score

import datasets


_DESCRIPTION = """
Precision is the fraction of correctly labeled positive examples out of all of the examples that were labeled as positive. It is computed via the equation:
Precision = TP / (TP + FP)
where TP is the True positives (i.e. the examples correctly labeled as positive) and FP is the False positive examples (i.e. the examples incorrectly labeled as positive).
"""


_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted class labels.
    references (`list` of `int`): Actual class labels.
    labels (`list` of `int`): The set of labels to include when `average` is not set to `'binary'`. If `average` is `None`, it should be the label order. Labels present in the data can be excluded, for example to calculate a multiclass average ignoring a majority negative class. Labels not present in the data will result in 0 components in a macro average. For multilabel targets, labels are column indices. By default, all labels in `predictions` and `references` are used in sorted order. Defaults to None.
    pos_label (`int`): The class to be considered the positive class, in the case where `average` is set to `binary`. Defaults to 1.
    average (`string`): This parameter is required for multiclass/multilabel targets. If set to `None`, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data. Defaults to `'binary'`.

        - 'binary': Only report results for the class specified by `pos_label`. This is applicable only if the classes found in `predictions` and `references` are binary.
        - 'micro': Calculate metrics globally by counting the total true positives, false negatives and false positives.
        - 'macro': Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
        - 'weighted': Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). This alters `'macro'` to account for label imbalance. This option can result in an F-score that is not between precision and recall.
        - 'samples': Calculate metrics for each instance, and find their average (only meaningful for multilabel classification).
    sample_weight (`list` of `float`): Sample weights Defaults to None.
    zero_division (`int` or `string`): Sets the value to return when there is a zero division. Defaults to 'warn'.

        - 0: Returns 0 when there is a zero division.
        - 1: Returns 1 when there is a zero division.
        - 'warn': Raises warnings and then returns 0 when there is a zero division.

Returns:
    precision (`float` or `array` of `float`): Precision score or list of precision scores, depending on the value passed to `average`. Minimum possible value is 0. Maximum possible value is 1. Higher values indicate that fewer negative examples were incorrectly labeled as positive, which means that, generally, higher scores are better.

Examples:

    Example 1-A simple binary example
        >>> precision_metric = datasets.load_metric("precision")
        >>> results = precision_metric.compute(references=[0, 1, 0, 1, 0], predictions=[0, 0, 1, 1, 0])
        >>> print(results)
        {'precision': 0.5}

    Example 2-The same simple binary example as in Example 1, but with `pos_label` set to `0`.
        >>> precision_metric = datasets.load_metric("precision")
        >>> results = precision_metric.compute(references=[0, 1, 0, 1, 0], predictions=[0, 0, 1, 1, 0], pos_label=0)
        >>> print(round(results['precision'], 2))
        0.67

    Example 3-The same simple binary example as in Example 1, but with `sample_weight` included.
        >>> precision_metric = datasets.load_metric("precision")
        >>> results = precision_metric.compute(references=[0, 1, 0, 1, 0], predictions=[0, 0, 1, 1, 0], sample_weight=[0.9, 0.5, 3.9, 1.2, 0.3])
        >>> print(results)
        {'precision': 0.23529411764705882}

    Example 4-A multiclass example, with different values for the `average` input.
        >>> predictions = [0, 2, 1, 0, 0, 1]
        >>> references = [0, 1, 2, 0, 1, 2]
        >>> results = precision_metric.compute(predictions=predictions, references=references, average='macro')
        >>> print(results)
        {'precision': 0.2222222222222222}
        >>> results = precision_metric.compute(predictions=predictions, references=references, average='micro')
        >>> print(results)
        {'precision': 0.3333333333333333}
        >>> results = precision_metric.compute(predictions=predictions, references=references, average='weighted')
        >>> print(results)
        {'precision': 0.2222222222222222}
        >>> results = precision_metric.compute(predictions=predictions, references=references, average=None)
        >>> print([round(res, 2) for res in results['precision']])
        [0.67, 0.0, 0.0]
"""


_CITATION = """
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
class Precision(datasets.Metric):
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
            reference_urls=["https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html"],
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
        score = precision_score(
            references,
            predictions,
            labels=labels,
            pos_label=pos_label,
            average=average,
            sample_weight=sample_weight,
            zero_division=zero_division,
        )
        return {"precision": float(score) if score.size == 1 else score}
