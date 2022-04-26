# Metric Card for F1


## Metric Description

The F1 score is the harmonic mean of the precision and recall. It can be computed with the equation:
F1 = 2 * (precision * recall) / (precision + recall)


## How to Use

At minimum, this metric requires predictions and references as input

```python
>>> f1_metric = datasets.load_metric("f1")
>>> results = f1_metric.compute(predictions=[0, 1], references=[0, 1])
>>> print(results)
["{'f1': 1.0}"]
```


### Inputs
- **predictions** (`list` of `int`): Predicted labels.
- **references** (`list` of `int`): Ground truth labels.
- **labels** (`list` of `int`): The set of labels to include when `average` is not set to `'binary'`, and the order of the labels if `average` is `None`. Labels present in the data can be excluded, for example to calculate a multiclass average ignoring a majority negative class. Labels not present in the data will result in 0 components in a macro average. For multilabel targets, labels are column indices. By default, all labels in `predictions` and `references` are used in sorted order. Defaults to None.
- **pos_label** (`int`): The class to be considered the positive class, in the case where `average` is set to `binary`. Defaults to 1.
- **average** (`string`): This parameter is required for multiclass/multilabel targets. If set to `None`, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data. Defaults to `'binary'`.
    - 'binary': Only report results for the class specified by `pos_label`. This is applicable only if the classes found in `predictions` and `references` are binary.
    - 'micro': Calculate metrics globally by counting the total true positives, false negatives and false positives.
    - 'macro': Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
    - 'weighted': Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). This alters `'macro'` to account for label imbalance. This option can result in an F-score that is not between precision and recall.
    - 'samples': Calculate metrics for each instance, and find their average (only meaningful for multilabel classification).
- **sample_weight** (`list` of `float`): Sample weights Defaults to None.


### Output Values
- **f1**(`float` or `array` of `float`): F1 score or list of f1 scores, depending on the value passed to `average`. Minimum possible value is 0. Maximum possible value is 1. Higher f1 scores are better.

Output Example(s):
```python
{'f1': 0.26666666666666666}
```
```python
{'f1': array([0.8, 0.0, 0.0])}
```

This metric outputs a dictionary, with either a single f1 score, of type `float`, or an array of f1 scores, with entries of type `float`.


#### Values from Popular Papers




### Examples

Example 1-A simple binary example
```python
>>> f1_metric = datasets.load_metric("f1")
>>> results = f1_metric.compute(references=[0, 1, 0, 1, 0], predictions=[0, 0, 1, 1, 0])
>>> print(results)
{'f1': 0.5}
```

Example 2-The same simple binary example as in Example 1, but with `pos_label` set to `0`.
```python
>>> f1_metric = datasets.load_metric("f1")
>>> results = f1_metric.compute(references=[0, 1, 0, 1, 0], predictions=[0, 0, 1, 1, 0], pos_label=0)
>>> print(round(results['f1'], 2))
0.67
```

Example 3-The same simple binary example as in Example 1, but with `sample_weight` included.
```python
>>> f1_metric = datasets.load_metric("f1")
>>> results = f1_metric.compute(references=[0, 1, 0, 1, 0], predictions=[0, 0, 1, 1, 0], sample_weight=[0.9, 0.5, 3.9, 1.2, 0.3])
>>> print(round(results['f1'], 2))
0.35
```

Example 4-A multiclass example, with different values for the `average` input.
```python
>>> predictions = [0, 2, 1, 0, 0, 1]
>>> references = [0, 1, 2, 0, 1, 2]
>>> results = f1_metric.compute(predictions=predictions, references=references, average="macro")
>>> print(round(results['f1'], 2))
0.27
>>> results = f1_metric.compute(predictions=predictions, references=references, average="micro")
>>> print(round(results['f1'], 2))
0.33
>>> results = f1_metric.compute(predictions=predictions, references=references, average="weighted")
>>> print(round(results['f1'], 2))
0.27
>>> results = f1_metric.compute(predictions=predictions, references=references, average=None)
>>> print(results)
{'f1': array([0.8, 0. , 0. ])}
```


## Limitations and Bias



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