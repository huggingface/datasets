---
annotations_creators:
- expert-generated
language_creators:
- other
languages:
- pl
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-sentences entailment and relatedness
---

# Dataset Card for [Dataset Name]

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

- **Homepage:**
http://zil.ipipan.waw.pl/Scwad/CDSCorpus
- **Repository:**
- **Paper:**
@inproceedings{wroblewska2017polish,
title={Polish evaluation dataset for compositional distributional semantics models},
author={Wr{\'o}blewska, Alina and Krasnowska-Kiera{\'s}, Katarzyna},
booktitle={Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
pages={784--792},
year={2017}
}
- **Leaderboard:**
https://klejbenchmark.com/leaderboard/
- **Point of Contact:**
alina@ipipan.waw.pl 

### Dataset Summary

Polish CDSCorpus consists of 10K Polish sentence pairs which are human-annotated for semantic relatedness and entailment. The dataset may be used for the evaluation of compositional distributional semantics models of Polish. The dataset was presented at ACL 2017. Please refer to the Wróblewska and Krasnowska-Kieraś (2017) for a detailed description of the resource.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Polish

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- pair_ID: id of sentences pairs
- sentence_A: first sentence
- sentence_B: second sentence

for cdsc-e domain:
- entailment_judgment: either 'NEUTRAL', 'CONTRADICTION' or 'ENTAILMENT'

for cdsc-r domain:
- relatedness_score: float representing a reletedness


### Data Splits

Data is splitted in train/dev/test split.

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

CC BY-NC-SA 4.0

### Citation Information

[More Information Needed]
