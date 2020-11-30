---
annotations_creators:
- crowdsourced
language_creators:
- expert-generated
- found
languages:
- ar
- bn
- fi
- ja
- ko
- ru
- te
licenses:
- mit
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
- extended|tydiqa
task_categories:
- question-answering
task_ids:
- open-domain-qa
---

# Dataset Card for XOR QA

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

- **Homepage:** [XOR QA Homepage](https://nlp.cs.washington.edu/xorqa/)
- **Repository:** [XOR QA Repository](https://github.com/AkariAsai/XORQA)
- **Paper:** [XOR QA Paper](https://arxiv.org/abs/2010.11856)
- **Leaderboard:** [XOR QA Leaderboard](https://nlp.cs.washington.edu/xorqa/)
- **Point of Contact:** [Akari Asai](akari@cs.washington.edu)

### Dataset Summary

XOR-TyDi QA brings together for the first time information-seeking questions, open-retrieval QA, and multilingual QA to create a multilingual open-retrieval QA dataset that enables cross-lingual answer retrieval. It consists of questions written by information-seeking native speakers in 7 typologically diverse languages and answer annotations that are retrieved from multilingual document collections. 

### Supported Tasks and Leaderboards

There are three sub-tasks: XOR-Retrieve, XOR-EnglishSpan, and XOR-Full.

- `XOR-retrieve`: XOR-Retrieve is a cross-lingual retrieval task where a question is written in a target language (e.g., Japanese) and a system is required to retrieve English paragraphs that answer the question. The dataset can be used to train a model for cross-lingual retrieval. Success on this task is typically measured by R@5kt, R@2kt (the recall by computing the fraction of the questions for which the minimal answer is contained in the top 5,000 / 2,000 tokens selected). This task has an active leaderboard which can be found at [leaderboard url](https://nlp.cs.washington.edu/xorqa/)

- `XOR-English Span`: XOR-English Span is a cross-lingual retrieval task where a question is written in a target language (e.g., Japanese) and a system is required to output a short answer in English. The dataset can be used to train a model for cross-lingual retrieval. Success on this task is typically measured by F1, EM. This task has an active leaderboard which can be found at [leaderboard url](https://nlp.cs.washington.edu/xorqa/)

- `XOR-Full`: XOR-Full is a cross-lingual retrieval task where a question is written in the target language (e.g., Japanese) and a system is required to output a short answer in a target language. Success on this task is typically measured by F1, EM, BLEU This task has an active leaderboard which can be found at [leaderboard url](https://nlp.cs.washington.edu/xorqa/)
### Languages

The text in the dataset is available in 7 languages: Arabic `ar`, Bengali `bn`, Finnish `fi`, Japanese `ja`, Korean `ko`, Russian `ru`, Telugu `te`

## Dataset Structure

### Data Instances

A typical data point comprises a `question`, it's `answer` the `language` of the question text and the split to which it belongs.

```
{
    "id": "-3979399588609321314", 
    "question": "Сколько детей было у Наполео́на I Бонапа́рта?", 
    "answers": ["сын"], 
    "lang": "ru", 
    "split": "train"
}
```

### Data Fields

- `id`: An identifier for each example in the dataset
- `question`: Open domain question
- `answers`: The corresponding answer to the question posed
- `lang`: BCP-47 language tag
- `split`: identifier to differentiate train, validation and test splits

### Data Splits

The data is split into a training, validation and test set for each of the two configurations.

|                            | Tain   | Valid | Test |
| -----                      | ------ | ----- | ---- |
| XOR Retrieve               |   15250|   2113|  2501|
| XOR Full                   |   61360|   3179|  8177|

## Dataset Creation

### Curation Rationale

This task framework reflects well real-world scenarios where a QA system uses multilingual document collections and answers questions asked by users with diverse linguistic and cultural backgrounds. Despite the common assumption that we can find answers in the target language, web re- sources in non-English languages are largely lim- ited compared to English (information scarcity), or the contents are biased towards their own cul- tures (information asymmetry). To solve these issues, XOR-TYDI QA (Asai et al., 2020) provides a benchmark for developing a multilingual QA system that finds answers in multiple languages.

### Source Data

annotation pipeline consists of four steps: 1) collection of realistic questions that require cross-lingual ref- erences by annotating questions from TYDI QA without a same-language answer; 2) question translation from a target language to the pivot language of English where the missing informa- tion may exist; 3) answer span selection in the pivot language given a set of candidate documents; 4) answer verification and translation from the pivot language back to the original language.

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

The Dataset is created by extending TyDiQA dataset and translating the questions into other languages. The answers are obtained by crowdsourcing the questions to Mechanical Turk workders

### Annotations

#### Annotation process

The English questions from TyDiQA are translated into other languages. The languages are chosen based on the availability of wikipedia data and the availability of tranlators. 

#### Who are the annotators?

The translations are carried out using the professionla tranlation service (Gengo)[https://gengo.com] and the answers are annotated by MechanicalTurk workers

### Personal and Sensitive Information

The dataset is created from wikipedia content and the QA task requires preserving the named entities, there by all the Wikipedia Named Entities are preserved in the data. Not much information has been provided about masking sensitive information. 

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The people associated with the creation of the dataset are Akari Asai, Jungo Kasai, Jonathan H. Clark, Kenton Lee, Eunsol Choi, Hannaneh Hajishirzi

### Licensing Information

XOR-TyDi QA is distributed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode) license

### Citation Information

```
@article{xorqa,
    title   = {XOR QA: Cross-lingual Open-Retrieval Question Answering},
    author  = {Akari Asai and Jungo Kasai and Jonathan H. Clark and Kenton Lee and Eunsol Choi and Hannaneh Hajishirzi}
    year    = {2020}
}
```