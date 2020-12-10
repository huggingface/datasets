---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- gpl-3.0+
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- sequence-modeling
- text-retrieval
task_ids:
  all:
  - dialogue-modeling
  - utterance-retrieval
  happy:
  - dialogue-modeling
  - utterance-retrieval
  offmychest:
  - dialogue-modeling
  - utterance-retrieval
---

# Dataset Card for PEC

## Table of Contents
- [Dataset Card for PEC](#dataset-card-for-pec)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Repository:** [PEC repository](https://github.com/zhongpeixiang/PEC)
- **Paper:** [Towards Persona-Based Empathetic Conversational Models](https://www.aclweb.org/anthology/2020.emnlp-main.531/)
- **Point of Contact:** [Peixiang Zhong](mailto:zhongpeixiang@gmail.com)

### Dataset Summary

The PEC dataset is an English-language dataset of open-domain conversations gathered from two subreddits on Reddit, i.e., happy and offmychest. PEC has around 350K persona-based empathetic conversations. Each utterance is associated with a speaker, and each speaker has a persona of multiple persona sentences. The conversations in PEC are more empathetic than casual conversations. The conversations in the happy domain are mostly positive, whereas the conversations in the offmychest domain are mostly negative.

### Supported Tasks and Leaderboards

- `dialogue-modeling`, `utterance-retrieval`: this dataset can be used to train a generative or retrieval-based conversational model. 

### Languages

English

## Dataset Structure

### Data Instances

A typical data example comprises a list of context utterances, a list of context speakers, a response to the context, the response speaker and the persona of the response speaker. 

An example from PEC looks as follows:
```
{'context': ['found out this morning i got a job promotion ! ! !'],
 'context_speakers': ['HeWentToJared91'],
 'personas': [
  "i ca n't stand working in the ugli .",
  'i ’ve always liked my eyes except for the fact that they ca n’t shoot lasers',
  'i feel really bad about myself as a person right now , and i could really use a hand .',
  'i drank a coffee , and it just made me feel even more exhausted .',
  'i want a natsuki t shirt',
  "i 've dealt with depression in the past .",
  'i love red dead 2'],
 'response': "you look like a nice person ! we 're proud of you , and i bet you earned that promotion !",
 'response_speaker': 'tylock'}
```

### Data Fields

- `context`: a list of strings, each string denotes a context utterance. 
- `context_speakers`: a list of strings, each string denotes a speaker.
- `response`: a string denoting the response to the `context`.
- `response_speaker`: a string denoting the speaker of `response`.
- `personas`: a list of strings, each string denotes a persona sentence of `response_speaker`.

### Data Splits
The data is split into a training, validation and test set for each of the three domains. Note that the *all* domain is the concatenation of the *happy* and *offmychest* domains.

| domain     | Tain   | Valid | Test |
| -----      | ------ | ----- | ---- |
| happy      | 157195 | 19829 | 22730|
| offmychest | 123968 | 16004 | 15324|
| all        | 281163 | 35833 | 38054|

## Dataset Creation

### Curation Rationale

PEC was built to provide a testbed for machines to learn persona-based empathetic responding. In our empirical analysis, we found that different personas have different styles of empathetic responding. This dataset can also be used to investigate the link between persona and empathy in human conversations. According to our human assessment, the conversations on the happy and offmychest subreddits are significantly more empathetic than casual conversations. 

### Source Data

#### Initial Data Collection and Normalization

The data was obtained via the [pushshift API](https://pushshift.io/using-bigquery-with-reddit-data/) via Google BigQuery. 

#### Who are the source language producers?

The language producers are users of the [r/happy](https://www.reddit.com/r/happy/), and [r/offmychest](https://www.reddit.com/r/offmychest/) subreddits between 2012 and 2020. No further demographic information was available from the data source.

### Annotations

#### Annotation process

The dataset does not contain any additional annotations.

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

The dataset includes the speaker IDs of users on *happy* and *offmychest* subreddits.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help develop more personalised and empathetic conversational systems, which is an important milestone towards truly human-like conversational agents.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

A small portion of the dataset has the issues of sexism, hate, and harassment. The persona sentences are noisy.

## Additional Information

### Dataset Curators

The dataset was initially created by Peixiang Zhong, Chen Zhang, Hao Wang, Yong Liu, and Chunyan Miao, jointly done at Nanyang Technological University and Alibaba Group.

### Licensing Information

The licensing status of the dataset hinges on the legal status of the [Pushshift.io](https://files.pushshift.io/reddit/) data which is unclear.

### Citation Information
```
@inproceedings{zhong-etal-2020-towards,
    title = "Towards Persona-Based Empathetic Conversational Models",
    author = "Zhong, Peixiang  and
      Zhang, Chen  and
      Wang, Hao  and
      Liu, Yong  and
      Miao, Chunyan",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    year = "2020",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.531",
    pages = "6556--6566"
}
```