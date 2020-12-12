---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- 235 different languages
licenses:
- ODC Open Database License v1.0
multilinguality:
- 235 different languages
size_categories:
- 1000 lines of text for every language, so in total 235000 lines of text (as total 235 languages)
source_datasets:
- original
task_categories:
- language-identification
task_ids:
- language-identification
---

# Dataset Card for wili_2018

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** https://zenodo.org/record/841984
- **Repository:** [Needs More Information]
- **Paper:** https://arxiv.org/pdf/1801.07779
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** Thoma, Martin (Email: info@martin-thoma.de)

### Dataset Summary

WiLI-2018, the Wikipedia language identification benchmark dataset, contains 235000 paragraphs of 235 languages. The dataset is balanced and a train-test split is provided.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

235 Different Languages

## Dataset Structure

### Data Instances

* `x_train.txt`: 175000 lines of text. Each line belongs to one language.
* `y_train.txt`: 175000 lines. Each line denotes the language of the same line
                 in `x_train.txt`
* `x_test.txt`: See `x_train.txt`
* `y_test.txt`: See `y_train.txt`
* `urls.txt`: A list of permanent URLs to all pages used for paragraph extraction
* `labels.csv`: A header line plus one line per language
* `README.txt`: This file

### Data Fields

[Needs More Information]

### Data Splits

175000 lines of text each for train and test data.

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

The dataset was initially created by Thomas Martin

### Licensing Information

ODC Open Database License v1.0

### Citation Information

```
@dataset{thoma_martin_2018_841984,
  author       = {Thoma, Martin},
  title        = {{WiLI-2018 - Wikipedia Language Identification database}},
  month        = jan,
  year         = 2018,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.841984},
  url          = {https://doi.org/10.5281/zenodo.841984}
}
```