---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- yo
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- topic-classification
paperswithcode_id: null
---

# Dataset Card for Yoruba BBC News Topic Classification dataset (yoruba_bbc_topics)

## Table of Contents
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

- **Homepage:** -
- **Repository:** https://github.com/uds-lsv/transfer-distant-transformer-african
- **Paper:** https://www.aclweb.org/anthology/2020.emnlp-main.204/
- **Leaderboard:** -
- **Point of Contact:** Michael A. Hedderich and David Adelani 
{mhedderich, didelani} (at) lsv.uni-saarland.de

### Dataset Summary

A news headline topic classification dataset, similar to AG-news, for Yorùbá. The news headlines were collected from [BBC Yoruba](https://www.bbc.com/yoruba).

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Yorùbá (ISO 639-1: yo)

## Dataset Structure

### Data Instances

An instance consists of a news title sentence and the corresponding topic label as well as publishing information (date and website id).

### Data Fields

- `news_title`: A news title.
- `label`: The label describing the topic of the news title. Can be one of the following classes: africa, entertainment, health, nigeria, politics, sport or world.
- `date`: The publication date (in Yorùbá).
- `bbc_url_id`: The identifier of the article in the BBC URL.

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

[More Information Needed]

### Citation Information

[More Information Needed]


### Contributions

Thanks to [@michael-aloys](https://github.com/michael-aloys) for adding this dataset.