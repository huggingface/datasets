---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- unknown
licenses:
- unknown
multilinguality:
- monolingual
pretty_name: Monash Time Series Forecasting Repository
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

# Dataset Card for Monash Time Series Forecasting Repository

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

- **Homepage:** [Monash Time Series Forecasting Repository](https://forecastingdata.org/)
- **Paper:** [Monash Time Series Forecasting Archive](https://openreview.net/pdf?id=wEc1mgAjU-)
- **Leaderboard:** [Baseline Results](https://forecastingdata.org/#results)
- **Point of Contact:** [Rakshitha Godahewa](mailto:rakshitha.godahewa@monash.edu)

### Dataset Summary

The first comprehensive time series forecasting repository containing datasets of related time series to facilitate the evaluation of global forecasting models. All datasets are intended to use only for research purpose. Our repository contains 30 datasets including both publicly available time series datasets (in different formats) and datasets curated by us. Many datasets have different versions based on the frequency and the inclusion of missing values, making the total number of dataset variations to 58. Furthermore, it includes both real-world and competition time series datasets covering varied domains.

### Supported Tasks and Leaderboards

- `univariate-time-series-forecasting`: The time series forecasting tasks involves learning the future `target` values of time series in a dataset for the `prediction_length` time steps. The performance of the forecast models can then be validated via the ground truth in the `validation` split and tested via the `test` split.


### Languages

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

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

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode)

### Citation Information

```tex
@InProceedings{godahewa2021monash,
    author = "Godahewa, Rakshitha and Bergmeir, Christoph and Webb, Geoffrey I. and Hyndman, Rob J. and Montero-Manso, Pablo",
    title = "Monash Time Series Forecasting Archive",
    booktitle = "Neural Information Processing Systems Track on Datasets and Benchmarks",
    year = "2021",
    note = "forthcoming"
}
```

### Contributions

Thanks to [@kashif](https://github.com/kashif) for adding this dataset.
