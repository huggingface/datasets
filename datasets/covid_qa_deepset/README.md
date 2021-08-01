---
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
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- closed-domain-qa
- extractive-qa
paperswithcode_id: null
---


# Dataset Card for COVID-QA

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

- **Repository:** https://github.com/deepset-ai/COVID-QA
- **Paper:** https://openreview.net/forum?id=JENSKEEzsoU
- **Point of Contact:** [deepset AI](https://github.com/deepset-ai)

### Dataset Summary

COVID-QA is a Question Answering dataset consisting of 2,019 question/answer pairs annotated by volunteer biomedical experts on scientific articles related to COVID-19.
A total of 147 scientific articles from the CORD-19 dataset were annotated by 15 experts.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

**What do the instances that comprise the dataset represent?**
Each represents a question, a context (document passage from the CORD19 dataset) and an answer.

**How many instances are there in total?**
2019 instances

**What data does each instance consist of?**
Each instance is a question, a set of answers, and an id associated with each answer.

[More Information Needed]

### Data Fields

The data was annotated in SQuAD style fashion, where each row contains:

* **question**: Query question
* **context**: Context text to obtain the answer from
* **document_id** The document ID of the context text
* **answer**: Dictionary containing the answer string and the start index

### Data Splits

**data/COVID-QA.json**: 2,019 question/answer pairs annotated by volunteer biomedical experts on scientific articles related to COVID-19.

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The inital data collected comes from 147 scientific articles from the CORD-19 dataset. Question and answers were then
annotated afterwards.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

While annotators were volunteers, they were required to have at least a Master’s degree in biomedical sciences.
The annotation team was led by a medical doctor (G.A.R.) who vetted the volunteer’s credentials and
manually verified each question/answer pair produced. We used an existing, web-based annotation tool that had been
created by deepset and is available at their Neural Search framework [haystack](https://github.com/deepset-ai/haystack).

#### Who are the annotators?

The annotators are 15 volunteer biomedical experts on scientific articles related to COVID-19.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

The dataset aims to help build question answering models serving clinical and scientific researchers, public health authorities, and frontline workers.
These QA systems can help them find answers and patterns in research papers by locating relevant answers to common questions from scientific articles.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

## Additional Information

The listed authors in the homepage are maintaining/supporting the dataset.

### Dataset Curators

[More Information Needed]

### Licensing Information

The Proto_qa dataset is licensed under the [Apache License 2.0](https://github.com/deepset-ai/COVID-QA/blob/master/LICENSE)

### Citation Information

```
@inproceedings{moller2020covid,
  title={COVID-QA: A Question Answering Dataset for COVID-19},
  author={M{\"o}ller, Timo and Reina, Anthony and Jayakumar, Raghavan and Pietsch, Malte},
  booktitle={Proceedings of the 1st Workshop on NLP for COVID-19 at ACL 2020},
  year={2020}
}
```

### Contributions

Thanks to [@olinguyen](https://github.com/olinguyen) for adding this dataset.