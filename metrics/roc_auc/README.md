# Metric Card for RUC AOC


## Metric Description
This metric computes the area under the curve (AUC) for the Receiver Operating Characteristic Curve (ROC). The return values represent how well the model used is predicting the correct classes, based on the input data. A score of `0.5` means that the model is predicting exactly at chance, i.e. the model's predictions are correct at the same rate as if the predictions were being decided by the flip of a fair coin or the roll of a fair die. A score above `0.5` indicates that the model is doing better than chance, while a score below `0.5` indicates that the model is doing worse than chance.

This metric has three separate use cases:
    - **binary**: The case in which there are only two different label classes, and each example gets only one label. This is the default implementation.
    - **multiclass**: The case in which there can be more than two different label classes, but each example still gets only one label.
    - **multilabel**: The case in which there can be more than two different label classes, and each example can have more than one label.


## How to Use
At minimum, this metric requires references and prediction scores:
```python
>>> roc_auc_score = datasets.load_metric("roc_auc")
>>> refs = [1, 0, 1, 1, 0, 0]
>>> pred_scores = [0.5, 0.2, 0.99, 0.3, 0.1, 0.7]
>>> results = roc_auc_score.compute(references=refs, prediction_scores=pred_scores)
>>> print(round(results['roc_auc'], 2))
0.78
```

The default implementation of this metric is the **binary** implementation. If employing the **multiclass** or **multilabel** use cases, the keyword `"multiclass"` or `"multilabel"` must be specified when loading the metric:
- In the **multiclass** case, the metric is loaded with:
    ```python
    >>> roc_auc_score = datasets.load_metric("roc_auc", "multiclass")
    ```
- In the **multilabel** case, the metric is loaded with:
    ```python
    >>> roc_auc_score = datasets.load_metric("roc_auc", "multilabel")
    ```

See the [Examples Section Below](#examples_section) for more extensive examples.


### Inputs
- **`references`** (array-like of shape (n_samples,) or (n_samples, n_classes)): Ground truth labels. Expects different inputs based on use case:
    - binary: expects an array-like of shape (n_samples,)
    - multiclass: expects an array-like of shape (n_samples,)
    - multilabel: expects an array-like of shape (n_samples, n_classes)
- **`prediction_scores`** (array-like of shape (n_samples,) or (n_samples, n_classes)): Ground truth labels. Expects different inputs based on use case:
    - binary: expects an array-like of shape (n_samples,)
    - multiclass: expects an array-like of shape (n_samples,)
    - multilabel: expects an array-like of shape (n_samples, n_classes)
- **`average`** (`str`): Type of average, and is ignored in the binary use case. Defaults to `'macro'`. Options are:
    - `'micro'`: Calculates metrics globally by considering each element of the label indicator matrix as a label. Only works with the multilabel use case.
    - `'macro'`: Calculate metrics for each label, and find their unweighted mean.  This does not take label imbalance into account.
    - `'weighted'`: Calculate metrics for each label, and find their average, weighted by support (i.e. the number of true instances for each label).
    - `'samples'`: Calculate metrics for each instance, and find their average. Only works with the multilabel use case.
    - `None`:  No average is calculated, and scores for each class are returned. Only works with the multilabels use case.
- **`sample_weight`** (array-like of shape (n_samples,)): Sample weights. Defaults to None.
- **`max_fpr`** (`float`): If not None, the standardized partial AUC over the range [0, `max_fpr`] is returned. Must be greater than `0` and less than or equal to `1`. Defaults to `None`. Note: For the multiclass use case, `max_fpr` should be either `None` or `1.0` as ROC AUC partial computation is not currently supported for `multiclass`.
- **`multi_class`** (`str`): Only used for multiclass targets, in which case it is required. Determines the type of configuration to use. Options are:
    - `'ovr'`: Stands for One-vs-rest. Computes the AUC of each class against the rest. This treats the multiclass case in the same way as the multilabel case. Sensitive to class imbalance even when `average == 'macro'`, because class imbalance affects the composition of each of the 'rest' groupings.
    - `'ovo'`: Stands for One-vs-one. Computes the average AUC of all possible pairwise combinations of classes. Insensitive to class imbalance when `average == 'macro'`.
- **`labels`** (array-like of shape (n_classes,)): Only used for multiclass targets. List of labels that index the classes in `prediction_scores`. If `None`, the numerical or lexicographical order of the labels in `prediction_scores` is used. Defaults to `None`.

### Output Values
This metric returns a dict containing the `roc_auc` score. The score is a `float`, unless it is the multilabel case with `average=None`, in which case the score is a numpy `array` with entries of type `float`.

The output therefore generally takes the following format:
```python
{'roc_auc': 0.778}
```

In contrast, though, the output takes the following format in the multilabel case when `average=None`:
```python
{'roc_auc': array([0.83333333, 0.375, 0.94444444])}
```

ROC AUC scores can take on any value between `0` and `1`, inclusive.

#### Values from Popular Papers


### <a name="examples_section"></a>Examples
Example 1, the **binary** use case:
```python
>>> roc_auc_score = datasets.load_metric("roc_auc")
>>> refs = [1, 0, 1, 1, 0, 0]
>>> pred_scores = [0.5, 0.2, 0.99, 0.3, 0.1, 0.7]
>>> results = roc_auc_score.compute(references=refs, prediction_scores=pred_scores)
>>> print(round(results['roc_auc'], 2))
0.78
```

Example 2, the **multiclass** use case:
```python
>>> roc_auc_score = datasets.load_metric("roc_auc", "multiclass")
>>> refs = [1, 0, 1, 2, 2, 0]
>>> pred_scores = [[0.3, 0.5, 0.2],
...                 [0.7, 0.2, 0.1],
...                 [0.005, 0.99, 0.005],
...                 [0.2, 0.3, 0.5],
...                 [0.1, 0.1, 0.8],
...                 [0.1, 0.7, 0.2]]
>>> results = roc_auc_score.compute(references=refs,
...                                 prediction_scores=pred_scores,
...                                 multi_class='ovr')
>>> print(round(results['roc_auc'], 2))
0.85
```

Example 3, the **multilabel** use case:
```python
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
>>> results = roc_auc_score.compute(references=refs,
...                                 prediction_scores=pred_scores,
...                                 average=None)
>>> print([round(res, 2) for res in results['roc_auc'])
[0.83, 0.38, 0.94]
```


## Limitations and Bias


## Citation
```bibtex
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
```

```bibtex
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
```

```bibtex
@article{scikit-learn,
title={Scikit-learn: Machine Learning in {P}ython},
author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V. and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P. and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.},
journal={Journal of Machine Learning Research},
volume={12},
pages={2825--2830},
year={2011}
}
```

## Further References
This implementation is a wrapper around the [Scikit-learn implementation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html). Much of the documentation here was adapted from their existing documentation, as well.

The [Guide to ROC and AUC](https://youtu.be/iCZJfO-7C5Q) video from the channel Data Science Bits is also very informative.