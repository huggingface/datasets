---
annotations_creators:
- crowdsourced
language_creators:
- expert-generated
languages:
- en
- tw
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
- n<1K
source_datasets: []
task_categories:
- text-scoring
task_ids:
- semantic-similarity-scoring
---

# Dataset Card for Yorùbá Wordsim-353

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

- **Homepage:** -https://www.aclweb.org/anthology/2020.lrec-1.335/
- **Repository:** https://github.com/ajesujoba/YorubaTwi-Embedding
- **Paper:** https://www.aclweb.org/anthology/2020.lrec-1.335/
- **Leaderboard:** -
- **Point of Contact:** [Kwabena Amponsah-Kaakyire](mailto:s8kwampo@stud.uni-saarland.de)

### Dataset Summary

A translation of the word pair similarity dataset wordsim-353 to Twi. However, only 274 (out of 353) pairs of words were translated

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Twi (ISO 639-1: tw)

## Dataset Structure

### Data Instances

An instance consists of a pair of words as well as their similarity. The dataset contains both the original English words (from wordsim-353) as well as their translation to Twi.

### Data Fields

- `twi1`: the first word of the pair; translation to Twi
- `twi2`: the second word of the pair; translation to Twi
- `similarity`: similarity rating according to the English dataset

### Data Splits

Only the test data is available

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
