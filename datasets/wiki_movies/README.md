---
pretty_name: WikiMovies
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- closed-domain-qa
paperswithcode_id: wikimovies
---


# Dataset Card for WikiMovies

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

- **Homepage: [WikiMovies Homepage](https://research.fb.com/downloads/babi/)**
- **Repository:**
- **Paper: [Key-Value Memory Networks for Directly Reading Documents](https://arxiv.org/pdf/1606.03126.pdf)**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The WikiMovies dataset consists of roughly 100k (templated) questions over 75k entitiesbased on questions with answers in the open movie database (OMDb). It is the QA part of the Movie Dialog dataset.

### Supported Tasks and Leaderboards

- Question Answering

### Languages

The text in the dataset is written in English.

## Dataset Structure

### Data Instances

The raw data consists of question answer pairs separated by a tab. Here are 3 examples:
```buildoutcfg
1 what does Grégoire Colin appear in?	Before the Rain
1 Joe Thomas appears in which movies?	The Inbetweeners Movie, The Inbetweeners 2
1 what films did Michelle Trachtenberg star in?	Inspector Gadget, Black Christmas, Ice Princess, Harriet the Spy, The Scribbler
```
It is unclear what the `1` is for at the beginning of each line, but it has been removed in the `Dataset` object.

### Data Fields
Here is an example of the raw data ingested by `Datasets`:
```buildoutcfg
{
'answer': 'Before the Rain', 
'question': 'what does Grégoire Colin appear in?'
}
```
`answer`: a string containing the answer to a corresponding question.
`question`: a string containing the relevant question.

### Data Splits
The data is split into train, test, and dev sets. The split sizes are as follows:

| wiki-entities_qa_* | n examples|
| -----              | ----      |
| train.txt          | 96185     |
| dev.txt            | 10000     |
| test.txt           | 9952      | 

## Dataset Creation

### Curation Rationale

WikiMovies was built with the following goals in mind: (i) machine learning techniques should have ample training examples for learning; and (ii) one can analyze easily the performance of different representations of knowledge and break down the results by question type. The datasetcan be downloaded fromhttp://fb.ai/babi

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

Thanks to [@aclifton314](https://github.com/aclifton314) for adding this dataset.