---
annotations_creators:
- no-annotation
language_creators:
- other
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets: []
task_categories:
- text-scoring
task_ids:
- semantic-similarity-scoring
- text-scoring-other-humor-detection
---

# Dataset Card for Jokes English Dataset

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
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

## Dataset Description

- **Repository:**https://github.com/taivop/joke-dataset

### Dataset Summary

A dataset of 200k English plaintext Jokes scraped from three sources: Reddit, Stupidstuff and Wocka.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

For config 'reddit':
- `title`: a `string` feature.
- `body`: a `string` feature.
- `id`: a `string` feature.
- `score`: a `int32` feature.

For config 'stupidstuf':
- `category`: a `string` feature.
- `body`: a `string` feature.
- `id`: a `int32` feature.
- `rating`: a `float32` feature.

For config 'wocka':
- `title`: a `string` feature.
- `body`: a `string` feature.
- `category`: a `string` feature.
- `id`: a `int32` feature.

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
