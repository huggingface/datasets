---
annotations_creators:
- machine-generated
language_creators:
- other
languages:
- te
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
- text-classification
task_ids:
- language-modeling
- multi-class-classification
- topic-classification
paperswithcode_id: null
---

# Dataset Card for [Dataset Name]

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

- **Homepage: https://www.kaggle.com/sudalairajkumar/telugu-nlp?select=telugu_news
- **Repository: https://github.com/AnushaMotamarri/Telugu-Newspaper-Article-Dataset


### Dataset Summary

This dataset contains Telugu language news articles along with respective topic 
labels (business, editorial, entertainment, nation, sport) extracted from the daily Andhra Jyoti. 
This dataset could be used to build Classification and Language Models.

### Supported Tasks and Leaderboards

Multiclass classification, Topic Classification, Language Model

### Languages

TE - Telugu, India

## Dataset Structure


### Data Instances

Two CSV files (train, test) with five columns (sno, date, heading, body, topic).

### Data Fields

- sno: id
- date: publish date of the news article
- heading: article heading/title
- body: article body/content
- topic: one of the following topics (business, editorial, entertainment, nation, sport)

### Data Splits

Train and Test

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

- https://www.kaggle.com/sudalairajkumar/telugu-nlp?select=telugu_news
- https://github.com/AnushaMotamarri/Telugu-Newspaper-Article-Dataset

#### Initial Data Collection and Normalization

The source data is scraped articles from archives of Telugu newspaper website Andhra Jyoti. 
A set of queries were created and the corresponding ground truth answers were retrieved by a combination of BM25 and tf-idf.

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

Sudalai Rajkumar, Anusha Motamarri

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@oostopitre](https://github.com/oostopitre) for adding this dataset.