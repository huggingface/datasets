# Metric Card for Recall


## Metric Description

Recall is the fraction of the positive examples that were correctly labeled by the model as positive. It can be computed with the equation:
Recall = TP / (TP + FN)
Where TP is the number of true positives and FN is the number of false negatives.


## How to Use

At minimum, this metric takes as input two `list`s, each containing `int`s: predictions and references.

```python
>>> recall_metric = datasets.load_metric('recall')
>>> results = recall_metric.compute(references=[0, 1], predictions=[0, 1])
>>> print(results)
["{'recall': 1.0}"]
```


### Inputs
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


### Output Values
- **recall**(`float`, or `array` of `float`, for multiclass targets): Either the general recall score, or the recall scores for individual classes, depending on the values input to `labels` and `average`. Minimum possible value is 0. Maximum possible value is 1. A higher recall means that more of the positive examples have been labeled correctly. Therefore, a higher recall is generally considered better.

Output Example(s):
```python
{'recall': 1.0}
```
```python
{'recall': array([1., 0., 0.])}
```

This metric outputs a dictionary with one entry, `'recall'`.


#### Values from Popular Papers


### Examples

Example 1-A simple example with some errors
```python
>>> recall_metric = datasets.load_metric('recall')
>>> results = recall_metric.compute(references=[0, 0, 1, 1, 1], predictions=[0, 1, 0, 1, 1])
>>> print(results)
{'recall': 0.6666666666666666}
```

Example 2-The same example as Example 1, but with `pos_label=0` instead of the default `pos_label=1`.
```python
>>> recall_metric = datasets.load_metric('recall')
>>> results = recall_metric.compute(references=[0, 0, 1, 1, 1], predictions=[0, 1, 0, 1, 1], pos_label=0)
>>> print(results)
{'recall': 0.5}
```

Example 3-The same example as Example 1, but with `sample_weight` included.
```python
>>> recall_metric = datasets.load_metric('recall')
>>> sample_weight = [0.9, 0.2, 0.9, 0.3, 0.8]
>>> results = recall_metric.compute(references=[0, 0, 1, 1, 1], predictions=[0, 1, 0, 1, 1], sample_weight=sample_weight)
>>> print(results)
{'recall': 0.55}
```

Example 4-A multiclass example, using different averages.
```python
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
```


## Limitations and Bias


## Citation(s)
```bibtex
@article{scikit-learn, title={Scikit-learn: Machine Learning in {P}ython}, author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V. and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P. and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.}, journal={Journal of Machine Learning Research}, volume={12}, pages={2825--2830}, year={2011}
```


## Further References
