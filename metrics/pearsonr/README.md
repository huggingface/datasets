# Metric Card for Pearson Correlation Coefficient (pearsonr)


## Metric Description

Pearson correlation coefficient and p-value for testing non-correlation.
The Pearson correlation coefficient measures the linear relationship between two datasets. The calculation of the p-value relies on the assumption that each dataset is normally distributed. Like other correlation coefficients, this one varies between -1 and +1 with 0 implying no correlation. Correlations of -1 or +1 imply an exact linear relationship. Positive correlations imply that as x increases, so does y. Negative correlations imply that as x increases, y decreases.
The p-value roughly indicates the probability of an uncorrelated system producing datasets that have a Pearson correlation at least as extreme as the one computed from these datasets.


## How to Use

This metric takes a list of predictions and a list of references as input

```python
>>> pearsonr_metric = datasets.load_metric("pearsonr")
>>> results = pearsonr_metric.compute(predictions=[10, 9, 2.5, 6, 4], references=[1, 2, 3, 4, 5])
>>> print(round(results['pearsonr']), 2)
['-0.74']
```


### Inputs
- **predictions** (`list` of `int`): Predicted class labels, as returned by a model.
- **references** (`list` of `int`): Ground truth labels.
- **return_pvalue** (`boolean`): If `True`, returns the p-value, along with the correlation coefficient. If `False`, returns only the correlation coefficient. Defaults to `False`.


### Output Values
- **pearsonr**(`float`): Pearson correlation coefficient. Minimum possible value is -1. Maximum possible value is 1. Values of 1 and -1 indicate exact linear positive and negative relationships, respectively. A value of 0 implies no correlation.
- **p-value**(`float`): P-value, which roughly indicates the probability of an The p-value roughly indicates the probability of an uncorrelated system producing datasets that have a Pearson correlation at least as extreme as the one computed from these datasets. Minimum possible value is 0. Maximum possible value is 1. Higher values indicate higher probabilities.

Like other correlation coefficients, this one varies between -1 and +1 with 0 implying no correlation. Correlations of -1 or +1 imply an exact linear relationship. Positive correlations imply that as x increases, so does y. Negative correlations imply that as x increases, y decreases.

Output Example(s):
```python
{'pearsonr': -0.7}
```
```python
{'p-value': 0.15}
```

#### Values from Popular Papers

### Examples

Example 1-A simple example using only predictions and references.
```python
>>> pearsonr_metric = datasets.load_metric("pearsonr")
>>> results = pearsonr_metric.compute(predictions=[10, 9, 2.5, 6, 4], references=[1, 2, 3, 4, 5])
>>> print(round(results['pearsonr'], 2))
-0.74
```

Example 2-The same as Example 1, but that also returns the `p-value`.
```python
>>> pearsonr_metric = datasets.load_metric("pearsonr")
>>> results = pearsonr_metric.compute(predictions=[10, 9, 2.5, 6, 4], references=[1, 2, 3, 4, 5], return_pvalue=True)
>>> print(sorted(list(results.keys())))
['p-value', 'pearsonr']
>>> print(round(results['pearsonr'], 2))
-0.74
>>> print(round(results['p-value'], 2))
0.15
```


## Limitations and Bias

As stated above, the calculation of the p-value relies on the assumption that each data set is normally distributed. This is not always the case, so verifying the true distribution of datasets is recommended.


## Citation(s)
```bibtex
@article{2020SciPy-NMeth,
author  = {Virtanen, Pauli and Gommers, Ralf and Oliphant, Travis E. and
      Haberland, Matt and Reddy, Tyler and Cournapeau, David and
      Burovski, Evgeni and Peterson, Pearu and Weckesser, Warren and
      Bright, Jonathan and {van der Walt}, St{\'e}fan J. and
      Brett, Matthew and Wilson, Joshua and Millman, K. Jarrod and
      Mayorov, Nikolay and Nelson, Andrew R. J. and Jones, Eric and
      Kern, Robert and Larson, Eric and Carey, C J and
      Polat, {\.I}lhan and Feng, Yu and Moore, Eric W. and
      {VanderPlas}, Jake and Laxalde, Denis and Perktold, Josef and
      Cimrman, Robert and Henriksen, Ian and Quintero, E. A. and
      Harris, Charles R. and Archibald, Anne M. and
      Ribeiro, Ant{\^o}nio H. and Pedregosa, Fabian and
      {van Mulbregt}, Paul and {SciPy 1.0 Contributors}},
title   = {{{SciPy} 1.0: Fundamental Algorithms for Scientific
      Computing in Python}},
journal = {Nature Methods},
year    = {2020},
volume  = {17},
pages   = {261--272},
adsurl  = {https://rdcu.be/b08Wh},
doi = {10.1038/s41592-019-0686-2},
}
```


## Further References
