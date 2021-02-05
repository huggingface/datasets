---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- structure-prediction-other-acronym-identification
---

# Dataset Card Creation Guide

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://sites.google.com/view/sdu-aaai21/shared-task
- **Repository:** https://github.com/amirveyseh/AAAI-21-SDU-shared-task-1-AI
- **Paper:** https://arxiv.org/pdf/2010.14678v1.pdf
- **Leaderboard:** https://competitions.codalab.org/competitions/26609
- **Point of Contact:** [More Information Needed]

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

A sample training set is provided below

```
{'id': 'TR-0',
 'labels': [4, 4, 4, 4, 0, 2, 2, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4],
 'tokens': ['What',
  'is',
  'here',
  'called',
  'controlled',
  'natural',
  'language',
  '(',
  'CNL',
  ')',
  'has',
  'traditionally',
  'been',
  'given',
  'many',
  'different',
  'names',
  '.']}
```

Please note that in test set sentence only id, tokens are available. labels can be ignored for test set.
Labels in the test set are all `O`

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.