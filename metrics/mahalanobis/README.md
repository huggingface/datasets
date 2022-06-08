# Metric Card for Mahalanobis Distance

## Metric Description
Mahalonobis distance is the distance between a point and a distribution (as opposed to the distance between two points), making it the multivariate equivalent of the Euclidean distance.

It is often used in multivariate anomaly detection, classification on highly imbalanced datasets and one-class classification. 

## How to Use
At minimum, this metric requires two `list`s of datapoints: 

```python
>>> mahalanobis_metric = datasets.load_metric("mahalanobis")
>>> results = mahalanobis_metric.compute(reference_distribution=[[0, 1], [1, 0]], X=[[0, 1]])
```

### Inputs
- `X` (`list`): data points to be compared with the `reference_distribution`.
- `reference_distribution` (`list`): data points from the reference distribution that we want to compare to.
                    
### Output Values
`mahalanobis` (`array`): the Mahalonobis distance for each data point in `X`.

```python
>>> print(results)
{'mahalanobis': array([0.5])}
```

#### Values from Popular Papers
*N/A*

### Example

```python
>>> mahalanobis_metric = datasets.load_metric("mahalanobis")
>>> results = mahalanobis_metric.compute(reference_distribution=[[0, 1], [1, 0]], X=[[0, 1]])
>>> print(results)
{'mahalanobis': array([0.5])}
```

## Limitations and Bias

The Mahalanobis distance is only able to capture linear relationships between the variables, which means it cannot capture all types of outliers. Mahalanobis distance also fails to faithfully represent data that is highly skewed or multimodal.

## Citation
```bibtex
@inproceedings{mahalanobis1936generalized,
  title={On the generalized distance in statistics},
  author={Mahalanobis, Prasanta Chandra},
  year={1936},
  organization={National Institute of Science of India}
}
```

```bibtex
@article{de2000mahalanobis,
  title={The Mahalanobis distance},
  author={De Maesschalck, Roy and Jouan-Rimbaud, Delphine and Massart, D{\'e}sir{\'e} L},
  journal={Chemometrics and intelligent laboratory systems},
  volume={50},
  number={1},
  pages={1--18},
  year={2000},
  publisher={Elsevier}
}
```

## Further References
-[Wikipedia -- Mahalanobis Distance](https://en.wikipedia.org/wiki/Mahalanobis_distance)

-[Machine Learning Plus -- Mahalanobis Distance](https://www.machinelearningplus.com/statistics/mahalanobis-distance/)
