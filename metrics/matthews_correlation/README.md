# Metric Card for Matthews Correlation Coefficient

## Metric Description
The Matthews correlation coefficient is used in machine learning as a
measure of the quality of binary and multiclass classifications. It takes
into account true and false positives and negatives and is generally
regarded as a balanced measure which can be used even if the classes are of
very different sizes. The MCC is in essence a correlation coefficient value
between -1 and +1. A coefficient of +1 represents a perfect prediction, 0
an average random prediction and -1 an inverse prediction.  The statistic
is also known as the phi coefficient. [source: Wikipedia]

## How to Use
At minimum, this metric requires a list of predictions and a list of references:
```python
>>> matthews_metric = datasets.load_metric("matthews_correlation")
>>> results = matthews_metric.compute(references=[0, 1], predictions=[0, 1])
>>> print(results)
{'matthews_correlation': 1.0}
```

### Inputs
- **`predictions`** (`list` of `int`s): Predicted class labels.
- **`references`** (`list` of `int`s): Ground truth labels.
- **`sample_weight`** (`list` of `int`s, `float`s, or `bool`s): Sample weights. Defaults to `None`.

### Output Values
- **`matthews_correlation`** (`float`): Matthews correlation coefficient.

The metric output takes the following form:
```python
{'matthews_correlation': 0.54}
```

This metric can be any value from -1 to +1, inclusive.

#### Values from Popular Papers


### Examples
A basic example with only predictions and references as inputs:
```python
>>> matthews_metric = datasets.load_metric("matthews_correlation")
>>> results = matthews_metric.compute(references=[1, 3, 2, 0, 3, 2],
...                                     predictions=[1, 2, 2, 0, 3, 3])
>>> print(results)
{'matthews_correlation': 0.5384615384615384}
```

The same example as above, but also including sample weights:
```python
>>> matthews_metric = datasets.load_metric("matthews_correlation")
>>> results = matthews_metric.compute(references=[1, 3, 2, 0, 3, 2],
...                                     predictions=[1, 2, 2, 0, 3, 3],
...                                     sample_weight=[0.5, 3, 1, 1, 1, 2])
>>> print(results)
{'matthews_correlation': 0.09782608695652174}
```

The same example as above, with sample weights that cause a negative correlation:
```python
>>> matthews_metric = datasets.load_metric("matthews_correlation")
>>> results = matthews_metric.compute(references=[1, 3, 2, 0, 3, 2],
...                                     predictions=[1, 2, 2, 0, 3, 3],
...                                     sample_weight=[0.5, 1, 0, 0, 0, 1])
>>> print(results)
{'matthews_correlation': -0.25}
```

## Limitations and Bias
*Note any limitations or biases that the metric has.*


## Citation
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

- This Hugging Face implementation uses [this scikit-learn implementation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.matthews_corrcoef.html)