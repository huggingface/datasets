---
annotations_creators:
- crowdsourced
language_creators:
- expert-generated
languages:
- en
- yo
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-scoring
task_ids:
- semantic-similarity-scoring
paperswithcode_id: null
---

# Dataset Card for wordsim-353 in Yorùbá (yoruba_wordsim353)

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
- **Repository:** https://github.com/ajesujoba/YorubaTwi-Embedding
- **Paper:** https://www.aclweb.org/anthology/2020.lrec-1.335/
- **Leaderboard:** -
- **Point of Contact:** Jesujoba Alabi ( jesujobaoluwadara.alabi (at) dfki.de ) and David Adelani ( didelani (at) lsv.uni-saarland.de )

### Dataset Summary

A translation of the word pair similarity dataset wordsim-353 to Yorùbá.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Yorùbá (ISO 639-1: yo)

## Dataset Structure

### Data Instances

An instance consists of a pair of words as well as their similarity. The dataset contains both the original English words (from wordsim-353) as well as their translation to Yorùbá.

### Data Fields

- `english1`: the first word of the pair; the original English word
- `english2`: the second word of the pair; the original English word
- `yoruba1`: the first word of the pair; translation to Yorùbá
- `yoruba2`: the second word of the pair; translation to Yorùbá
- `similarity`: similarity rating according to the English dataset

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