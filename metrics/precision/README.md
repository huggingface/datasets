# Metric Card for Precision


## Metric Description

Precision is the fraction of correctly labeled positive examples out of all of the examples that were labeled as positive. It is computed via the equation:
Precision = TP / (TP + FP)
where TP is the True positives (i.e. the examples correctly labeled as positive) and FP is the False positive examples (i.e. the examples incorrectly labeled as positive).


## How to Use

At minimum, precision takes as input a list of predicted labels, `predictions`, and a list of output labels, `references`.

```python
>>> precision_metric = datasets.load_metric("precision")
>>> results = precision_metric.compute(references=[0, 1], predictions=[0, 1])
>>> print(results)
{'precision': 1.0}
```


### Inputs
- **predictions** (`list` of `int`): Predicted class labels.
- **references** (`list` of `int`): Actual class labels.
- **labels** (`list` of `int`): The set of labels to include when `average` is not set to `'binary'`. If `average` is `None`, it should be the label order. Labels present in the data can be excluded, for example to calculate a multiclass average ignoring a majority negative class. Labels not present in the data will result in 0 components in a macro average. For multilabel targets, labels are column indices. By default, all labels in `predictions` and `references` are used in sorted order. Defaults to None.
- **pos_label** (`int`): The class to be considered the positive class, in the case where `average` is set to `binary`. Defaults to 1.
- **average** (`string`): This parameter is required for multiclass/multilabel targets. If set to `None`, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data. Defaults to `'binary'`.
    - 'binary': Only report results for the class specified by `pos_label`. This is applicable only if the classes found in `predictions` and `references` are binary.
    - 'micro': Calculate metrics globally by counting the total true positives, false negatives and false positives.
    - 'macro': Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
    - 'weighted': Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). This alters `'macro'` to account for label imbalance. This option can result in an F-score that is not between precision and recall.
    - 'samples': Calculate metrics for each instance, and find their average (only meaningful for multilabel classification).
- **sample_weight** (`list` of `float`): Sample weights Defaults to None.
- **zero_division** (): Sets the value to return when there is a zero division. Defaults to .
    - 0: Returns 0 when there is a zero division.
    - 1: Returns 1 when there is a zero division.
    - 'warn': Raises warnings and then returns 0 when there is a zero division.


### Output Values
- **precision**(`float` or `array` of `float`): Precision score or list of precision scores, depending on the value passed to `average`. Minimum possible value is 0. Maximum possible value is 1. Higher values indicate that fewer negative examples were incorrectly labeled as positive, which means that, generally, higher scores are better.

Output Example(s):
```python
{'precision': 0.2222222222222222}
```
```python
{'precision': array([0.66666667, 0.0, 0.0])}
```




#### Values from Popular Papers


### Examples

Example 1-A simple binary example
```python
>>> precision_metric = datasets.load_metric("precision")
>>> results = precision_metric.compute(references=[0, 1, 0, 1, 0], predictions=[0, 0, 1, 1, 0])
>>> print(results)
{'precision': 0.5}
```

Example 2-The same simple binary example as in Example 1, but with `pos_label` set to `0`.
```python
>>> precision_metric = datasets.load_metric("precision")
>>> results = precision_metric.compute(references=[0, 1, 0, 1, 0], predictions=[0, 0, 1, 1, 0], pos_label=0)
>>> print(round(results['precision'], 2))
0.67
```

Example 3-The same simple binary example as in Example 1, but with `sample_weight` included.
```python
>>> precision_metric = datasets.load_metric("precision")
>>> results = precision_metric.compute(references=[0, 1, 0, 1, 0], predictions=[0, 0, 1, 1, 0], sample_weight=[0.9, 0.5, 3.9, 1.2, 0.3])
>>> print(results)
{'precision': 0.23529411764705882}
```

Example 4-A multiclass example, with different values for the `average` input.
```python
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
```


## Limitations and Bias

[Precision](https://huggingface.co/metrics/precision) and [recall](https://huggingface.co/metrics/recall) are complementary and can be used to measure different aspects of model performance -- using both of them (or an averaged measure like [F1 score](https://huggingface.co/metrics/F1) to better represent different aspects of performance. See [Wikipedia](https://en.wikipedia.org/wiki/Precision_and_recall) for more information.

## Citation(s)
```bibtex
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
```


## Further References
- [Wikipedia -- Precision and recall](https://en.wikipedia.org/wiki/Precision_and_recall)
