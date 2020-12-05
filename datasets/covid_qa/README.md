---
YAML tags:
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets: []
task_categories:
- question-answering
task_ids:
- closed-domain-qa
- extractive-qa
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

- **Repository:** https://github.com/deepset-ai/COVID-QA
- **Paper:** https://openreview.net/forum?id=JENSKEEzsoU
- **Point of Contact:** [deepset AI](https://github.com/deepset-ai)

### Dataset Summary

COVID-QA is a Question Answering dataset consisting of 2,019 question/answer pairs annotated by volunteer biomedical experts on scientific articles related to COVID-19.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English

## Dataset Structure

### Data Instances

**What do the instances that comprise the dataset represent?**
Each represents a survey question from Family Feud game and reported answer clusters

**How many instances are there in total?**
2019 instances

**What data does each instance consist of?**
Each instance is a question, a set of answers, and an id associated with each answer.

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

**data/COVID-QA.json**: 2,019 question/answer pairs annotated by volunteer biomedical experts on scientific articles related to COVID-19.

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

## Additional Information

The listed authors are maintaining/supporting the dataset. 


### Dataset Curators

[More Information Needed]

The Proto_qa dataset is licensed under 
the [Apache License 2.0](https://github.com/deepset-ai/COVID-QA/blob/master/LICENSE)

[More Information Needed]

### Citation Information

```
@inproceedings{moller2020covid,
  title={COVID-QA: A Question Answering Dataset for COVID-19},
  author={M{\"o}ller, Timo and Reina, Anthony and Jayakumar, Raghavan and Pietsch, Malte},
  booktitle={Proceedings of the 1st Workshop on NLP for COVID-19 at ACL 2020},
  year={2020}
}
```
