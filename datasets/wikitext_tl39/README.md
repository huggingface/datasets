---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- fil
- tl
licenses:
- gpl-3.0
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: wikitext-tl-39
---

# Dataset Card for WikiText-TL-39

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

- **Homepage:** [Filipino Text Benchmarks](https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks)
- **Repository: **
- **Paper:** [Evaluating language model finetuning techniques for low-resource languages](https://arxiv.org/abs/1907.00409)
- **Leaderboard:**
- **Point of Contact:** Jan Christian Blaise Cruz (jan_christian_cruz@dlsu.edu.ph)

### Dataset Summary

Large scale, unlabeled text dataset with 39 Million tokens in the training set. Inspired by the original WikiText Long Term Dependency dataset (Merity et al., 2016). TL means "Tagalog." Published in Cruz & Cheng (2019).

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Filipino/Tagalog

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- `text` (`str`)

The dataset is in plaintext and only has one field ("text") as it is compiled for language modeling.

### Data Splits

Split | Documents | Tokens
------|-----------|-------
Train | 120,975   | 39M
Valid | 25,919    | 8M
Test  | 25,921    | 8M

Please see the paper for more details on the dataset splits

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

Tagalog Wikipedia

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

Thanks to [@jcblaisecruz02](https://github.com/jcblaisecruz02) for adding this dataset.