---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- ar
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
---

# Dataset Card for WikiQAar

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
  - [Discussion of Social Impact and Biases](#discussion-of-social-impact-and-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [WikiQaAr](https://github.com/qcri/WikiQAar)
- **Repository:** [WikiQaAr](https://github.com/qcri/WikiQAar)
- **Paper:** 
- **Point of Contact:** [Ines Abbes
](abbes.ines@yahoo.com)

### Dataset Summary

Arabic Version of WikiQA by automatic automatic machine translators 
and crowdsourced the selection of the best one to be incorporated into the corpus

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

Each data point contains the question and whether the answer is a valid or not.  

### Data Fields

- `question_id`: the question id.
- `question`: the question text.
- `document_id`: the wikipedia document id.
- `answer_id` : the answer id.
- `answer` : a candidate answer to the question. 
- `label` : 1 if the `answer` is correct or 0 otherwise. 

### Data Splits

The dataset is not split. 

|           | Tain   | Dev   | Test  |
|---------- | ------ | ------| ------|
|Data split | 70,264 | 20,632| 10,387|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

Translation of WikiQA. 

#### Who are the source language producers?

Translation of WikiQA.   

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Discussion of Social Impact and Biases

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

Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai) for adding this dataset.