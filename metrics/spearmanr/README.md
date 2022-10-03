# Metric Card for Spearman Correlation Coefficient Metric (spearmanr)


## Metric Description
The Spearman rank-order correlation coefficient is a measure of the
relationship between two datasets. Like other correlation coefficients,
this one varies between -1 and +1 with 0 implying no correlation.
Positive correlations imply that as data in dataset x increases, so 
does data in dataset y. Negative correlations imply that as x increases,
y decreases. Correlations of -1 or +1 imply an exact monotonic relationship.

Unlike the Pearson correlation, the Spearman correlation does not 
assume that both datasets are normally distributed. 

The p-value roughly indicates the probability of an uncorrelated system
producing datasets that have a Spearman correlation at least as extreme
as the one computed from these datasets. The p-values are not entirely
reliable but are probably reasonable for datasets larger than 500 or so.


## How to Use
At minimum, this metric only requires a `list` of predictions and a `list` of references:

```python
>>> spearmanr_metric = datasets.load_metric("spearmanr")
>>> results = spearmanr_metric.compute(references=[1, 2, 3, 4, 5], predictions=[10, 9, 2.5, 6, 4])
>>> print(results)
{'spearmanr': -0.7}
```

### Inputs
- **`predictions`** (`list` of `float`): Predicted labels, as returned by a model.
- **`references`** (`list` of `float`): Ground truth labels.
- **`return_pvalue`** (`bool`): If `True`, returns the p-value. If `False`, returns
                    only the spearmanr score. Defaults to `False`.

### Output Values
-  **`spearmanr`** (`float`): Spearman correlation coefficient.
- **`p-value`** (`float`): p-value. **Note**: is only returned
                        if `return_pvalue=True` is input.

If `return_pvalue=False`, the output is a `dict` with one value, as below:
```python
{'spearmanr': -0.7}
```

Otherwise, if `return_pvalue=True`, the output is a `dict` containing a the `spearmanr` value as well as the corresponding `pvalue`:
```python
{'spearmanr': -0.7, 'spearmanr_pvalue': 0.1881204043741873}
```

Spearman rank-order correlations can take on any value from `-1` to `1`, inclusive.

The p-values can take on any value from `0` to `1`, inclusive.

#### Values from Popular Papers


### Examples
A basic example:
```python
>>> spearmanr_metric = datasets.load_metric("spearmanr")
>>> results = spearmanr_metric.compute(references=[1, 2, 3, 4, 5], predictions=[10, 9, 2.5, 6, 4])
>>> print(results)
{'spearmanr': -0.7}
```

The same example, but that also returns the pvalue:
```python
>>> spearmanr_metric = datasets.load_metric("spearmanr")
>>> results = spearmanr_metric.compute(references=[1, 2, 3, 4, 5], predictions=[10, 9, 2.5, 6, 4], return_pvalue=True)
>>> print(results)
{'spearmanr': -0.7, 'spearmanr_pvalue': 0.1881204043741873
>>> print(results['spearmanr'])
-0.7
>>> print(results['spearmanr_pvalue'])
0.1881204043741873
```

## Limitations and Bias


## Citation
```bibtex
@book{kokoska2000crc,
  title={CRC standard probability and statistics tables and formulae},
  author={Kokoska, Stephen and Zwillinger, Daniel},
  year={2000},
  publisher={Crc Press}
}
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
  doi     = {10.1038/s41592-019-0686-2},
}
```

## Further References
*Add any useful further references.*
