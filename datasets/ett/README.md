---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- unknown
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: Electricity Transformer Temperature
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- time-series-forecasting
task_ids:
- univariate-time-series-forecasting
- multivariate-time-series-forecasting
---

# Dataset Card for [Electricity Transformer Temperature](https://github.com/zhouhaoyi/ETDataset)

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [Electricity Transformer Dataset](https://github.com/zhouhaoyi/ETDataset)
- **Repository:** https://github.com/zhouhaoyi/ETDataset
- **Paper:** [Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting](https://arxiv.org/abs/2012.07436)
- **Point of Contact:** [Haoyi Zhou](mailto:zhouhy@act.buaa.edu.cn)

### Dataset Summary

The electric power distribution problem is the distribution of electricity to different areas depending on its sequential usage. But predicting the future demand of a specific area is difficult, as it varies with weekdays, holidays, seasons, weather, temperatures, etc. However, no existing method can perform a long-term prediction based on super long-term real-world data with high precision. Any false predictions may damage the electrical transformer. So currently, without an efficient method to predict future electric usage, managers have to make decisions based on the empirical number, which is much higher than the real-world demands. It causes unnecessary waste of electric and equipment depreciation. On the other hand, the oil temperatures can reflect the condition of the  Transformer. One of the most efficient strategies is to predict how the electrical transformers' oil temperature is safe and avoid unnecessary waste. As a result, to address this problem, the authors and Beijing Guowang Fuda Science & Technology Development Company have provided 2-years worth of data.

Specifically, the dataset combines short-term periodical patterns, long-term periodical patterns, long-term trends, and many irregular patterns. The dataset are obtained from  2 Electricity Transformers at 2 stations  and come in an `1H` (hourly) or `15T` (15-minute) frequency containing 2 year * 365 days * 24 hours * (4 for 15T) times = 17,520 (70,080 for 15T) data points.

The target time series is the  **O**il **T**emperature and the dataset comes with the following 6 covariates in the univariate setup:
* **H**igh **U**se**F**ul **L**oad 
* **H**igh **U**se**L**ess **L**oad
* **M**iddle **U**se**F**ul **L**oad 
* **M**iddle **U**se**L**ess **L**oad 
* **L**ow **U**se**F**ul **L**oad 
* **L**ow **U**se**L**ess **L**oad


### Dataset Usage

To load a particular variant of the dataset just specify its name e.g:

```python
load_dataset("ett", "m1", multivariate=False) # univariate 15-min frequency dataset from first transformer
```

or to specify a prediction length:

```python
load_dataset("ett", "h2", prediction_length=48) # multivariate dataset from second transformer with prediction length of 48 (hours)
```


### Supported Tasks and Leaderboards

The time series data is split into  train/val/test  set of 12/4/4 months respectively.  Given the prediction length (default: 1 day (24 hours or 24*4 15T)) we create rolling windows of this size for the val/test sets. 

#### `time-series-forecasting`

##### `univariate-time-series-forecasting`

The univariate time series forecasting tasks involves learning the future one dimensional `target` values of a time series in a dataset for some `prediction_length` time steps. The performance of the forecast models can then be validated via the ground truth in the `validation` split and tested via the `test` split. The covriates are stored in the `feat_dynamic_real` key of each time series.

##### `multivariate-time-series-forecasting`

The multivariate time series forecasting task involves learning the future vector of `target` values of a time series in a dataset for some `prediction_length` time steps. Similar to the univariate setting the performance of a multivariate model can be validated via the ground truth in the `validation` split and tested via the `test` split.


### Languages

## Dataset Structure

### Data Instances

A sample from the training set is provided below:

```python
{
  'start': datetime.datetime(2012, 1, 1, 0, 0),
  'target': [14.0, 18.0, 21.0, 20.0, 22.0, 20.0, ...],
  'feat_static_cat': [0], 
  'feat_dynamic_real': [[0.3, 0.4], [0.1, 0.6], ...],
  'item_id': 'OT'
}
```

### Data Fields

For the univariate regular time series each series has the following keys:

* `start`: a datetime of the first entry of each time series in the dataset
* `target`: an array[float32] of the actual target values
* `feat_static_cat`: an array[uint64] which contains a categorical identifier of each time series in the dataset
* `feat_dynamic_real`: optional array of covariate features
* `item_id`: a string identifier of each time series in a dataset for reference

For the multivariate time series the `target` is a vector of the multivariate dimension for each time point.

### Data Splits

The time series data is split into  train/val/test  set of 12/4/4 months respectively.

## Dataset Creation

### Curation Rationale

Develop time series methods  that can perform a long-term prediction based on super long-term real-world data with high precision.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

* [Haoyi Zhou](mailto:zhouhy@act.buaa.edu.cn)

### Licensing Information

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode)

### Citation Information

```tex
@inproceedings{haoyietal-informer-2021,
  author    = {Haoyi Zhou and
               Shanghang Zhang and
               Jieqi Peng and
               Shuai Zhang and
               Jianxin Li and
               Hui Xiong and
               Wancai Zhang},
  title     = {Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting},
  booktitle = {The Thirty-Fifth {AAAI} Conference on Artificial Intelligence, {AAAI} 2021, Virtual Conference},
  volume    = {35},
  number    = {12},
  pages     = {11106--11115},
  publisher = {{AAAI} Press},
  year      = {2021},
}
```

### Contributions

Thanks to [@kashif](https://github.com/kashif) for adding this dataset.
