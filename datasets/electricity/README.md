---
YAML tags:
- copy-paste the tags obtained with the online tagging app: https://huggingface.co/spaces/huggingface/datasets-tagging
---

# Dataset Card for [Dataset Name]

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
- **Point of Contact:** [Artur Trindade](artur.trindade@elergone.pt)

### Dataset Summary

This new dataset contains hourly kW electricity consumption time series of 370 Portuguese clients from 2011 to 2014.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

Data set has no missing values. Values are in kW of each 15 min and are resampled to hourly frequency. 
Each column represent one client. Some clients were created after 2011. In these cases consumption were considered zero.
All time labels report to Portuguese hour. However all days present 96 measures (24*4). Every year in March time change day (which has only 23 hours) the values between 1:00 am and 2:00 am are zero for all points. Every year in October time change day (which has 25 hours) the values between 1:00 am and 2:00 am aggregate the consumption of two hours.



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

### Data Fields

For this univariate regular time series we have:

- `start`: a `datetime` as string of the first entry of each time serie in the dataset
- `target`: an `array[float32]` of the actual target values

Given the `freq` and the `start` date, we can assign a datetime to each entry in the target array. Each time serie is also assigned a unique `feat_static_cat` integer id as well as an identifier `item_id`.


### Data Splits

```python
DatasetDict({
    train: Dataset({
        features: ['start', 'target', 'feat_static_cat', 'item_id'],
        num_rows: 321
    })
    test: Dataset({
        features: ['start', 'target', 'feat_static_cat', 'item_id'],
        num_rows: 2247
    })
    validation: Dataset({
        features: ['start', 'target', 'feat_static_cat', 'item_id'],
        num_rows: 321
    })
})
```

## Dataset Creation

### Curation Rationale

[More Information Needed]

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@github-username](https://github.com/<github-username>) for adding this dataset.
