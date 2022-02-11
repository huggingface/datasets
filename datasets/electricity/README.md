---
annotations_creators: []
language_creators: []
languages: []
licenses: []
multilinguality: []
pretty_name: ElectricityLoadDiagrams20112014
size_categories:
- unknown
source_datasets: []
task_categories: []
task_ids: []
---

# Dataset Card for ElectricityLoadDiagrams20112014

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

- **Homepage:** [Electricity Load 2011-2014](https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014)
- **Paper:** [Modeling Long- and Short-Term Temporal Patterns with Deep Neural Networks
](https://dl.acm.org/doi/10.1145/3209978.3210006)
- **Point of Contact:** [Artur Trindade](mailto:artur.trindade@elergone.pt)

### Dataset Summary

This new dataset contains hourly kW electricity consumption time series of 370 Portuguese clients from 2011 to 2014.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

Data set has no missing values. Values are in kW of each 15 min and are resampled to hourly frequency. 
Each column represent one client. Some clients were created after 2011. In these cases consumption were considered zero. All time labels report to Portuguese hour. However all days present 96 measures (24*4). Every year in March time change day (which has only 23 hours) the values between 1:00 am and 2:00 am are zero for all points. Every year in October time change day (which has 25 hours) the values between 1:00 am and 2:00 am aggregate the consumption of two hours.


### Data Instances

A sample from the training set is provided below:

```python
{
  'start': '2012-01-01 00:00:00', 
  'target': [14.0, 18.0, 21.0, 20.0, 22.0, 20.0, 20.0, 20.0, 13.0, 11.0], # <= this target value is a concatenated sample
  'feat_static_cat': [0], 
  'item_id': '0'
}
```

We have two configurations `uci` and `lstnet`, which are specificed as follows. 

The time series are resampled to hourly frequency. We test on 7 rolling windows of prediction length of 24. 

The `uci` validation therefore ends 24*7 time steps before the end of each time series. The training split ends 24 time steps before the end of the validation split. 

For the `lsnet` configuration we split the training window to be 0.6 of the full time series and the validation is the 0.8-th time series and the last 0.2 time windows are used as the test set of 7 rolling windows of the 24 time steps. Finally, as in the LSTNet paper, we only consider time series that are active in the year 2012--2014, which leaves us with 320 time series.


### Data Fields

For this univariate regular time series we have:

- `start`: a `datetime` of the first entry of each time serie in the dataset
- `target`: an `array[float32]` of the actual target values
- `feat_static_cat`: an `array[uint64]` which contains a categorical identifier of each time series in the dataset
- `item_id`: a string identifier of each time series in a dataset for reference

Given the `freq` and the `start` datetime, we can assign a datetime to each entry in the target array.


### Data Splits

#### UCI configuration

```
DatasetDict({
    train: Dataset({
        features: ['start', 'target', 'feat_static_cat', 'item_id'],
        num_rows: 370
    })
    test: Dataset({
        features: ['start', 'target', 'feat_static_cat', 'item_id'],
        num_rows: 2590
    })
    validation: Dataset({
        features: ['start', 'target', 'feat_static_cat', 'item_id'],
        num_rows: 370
    })
})
```

### LSTNet configuration


```python
DatasetDict({
    train: Dataset({
        features: ['start', 'target', 'feat_static_cat', 'item_id'],
        num_rows: 320
    })
    test: Dataset({
        features: ['start', 'target', 'feat_static_cat', 'item_id'],
        num_rows: 2240
    })
    validation: Dataset({
        features: ['start', 'target', 'feat_static_cat', 'item_id'],
        num_rows: 320
    })
})
```

## Dataset Creation

The Electricity Load Diagrams 2011–2014 Dataset was developed by Artur Trindade and shared in UCI Machine Learning Repository. This dataset covers the electricity load of 370 substations in Portugal from the start of 2011 to the end of 2014 with a sampling period of 15 min. We will resample this to hourly time series.

### Curation Rationale

Research and development of load forecasting methods. In particular short-term electricity forecasting.

### Source Data

This dataset covers the electricity load of 370 sub-stations in Portugal from the start of 2011 to the end of 2014 with a sampling period of 15 min.

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

### UCI Metadata:

```json
{
    "freq": "1H",
    "prediction_length": 24,
    "feat_static_cat": [
        {
            "name": "feat_static_cat",
            "cardinality": "370"
        }
    ]
}
```

### LSTNet Metadata:

```json
{
    "freq": "1H",
    "prediction_length": 24,
    "feat_static_cat": [
        {
            "name": "feat_static_cat",
            "cardinality": "320"
        }
    ]
}
```

### Notes

- Data set has no missing values.
- Values are in kW of each 15 min rescaled to hourly. To convert values in kWh values must be divided by 4.
- All time labels report to Portuguese hour, however all days present 96 measures (24*4). 
- Every year in March time change day (which has only 23 hours) the values between 1:00 am and 2:00 am are zero for all points. 
- Every year in October time change day (which has 25 hours) the values between 1:00 am and 2:00 am aggregate the consumption of two hours.

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@kashif](https://github.com/kashif) for adding this dataset.
