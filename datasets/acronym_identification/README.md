---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- structure-prediction-other-acronym-identification
paperswithcode_id: acronym-identification
---

# Dataset Card for Acronym Identification Dataset

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

- **Homepage:** https://sites.google.com/view/sdu-aaai21/shared-task
- **Repository:** https://github.com/amirveyseh/AAAI-21-SDU-shared-task-1-AI
- **Paper:** [What Does This Acronym Mean? Introducing a New Dataset for Acronym Identification and Disambiguation](https://arxiv.org/pdf/2010.14678v1.pdf)
- **Leaderboard:** https://competitions.codalab.org/competitions/26609
- **Point of Contact:** [More Information Needed]

### Dataset Summary

This dataset contains the training, validation, and test data for the **Shared Task 1: Acronym Identification** of the AAAI-21 Workshop on Scientific Document Understanding.

### Supported Tasks and Leaderboards

The dataset supports an `acronym-identification` task, where the aim is to predic which tokens in a pre-tokenized sentence correspond to acronyms. The dataset was released for a Shared Task which supported a [leaderboard](https://competitions.codalab.org/competitions/26609).

### Languages

The sentences in the dataset are in English (`en`).

## Dataset Structure

### Data Instances

A sample from the training set is provided below:

```
{'id': 'TR-0',
 'labels': [4, 4, 4, 4, 0, 2, 2, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4],
 'tokens': ['What',
  'is',
  'here',
  'called',
  'controlled',
  'natural',
  'language',
  '(',
  'CNL',
  ')',
  'has',
  'traditionally',
  'been',
  'given',
  'many',
  'different',
  'names',
  '.']}
```

Please note that in test set sentences only the `id` and `tokens` fields are available. `labels` can be ignored for test set. Labels in the test set are all `O`

### Data Fields

The data instances have the following fields:

- `id`: a `string` variable representing the example id, unique across the full dataset
- `tokens`: a list of `string` variables representing the word-tokenized sentence
- `labels`: a list of `categorical` variables with possible values `["B-long", "B-short", "I-long", "I-short", "O"]` corresponding to a BIO scheme. `-long` corresponds to the expanded acronym, such as *controlled natural language* here, and `-short` to the abbrviation, `CNL` here.

### Data Splits

The training, validation, and test set contain `14,006`, `1,717`, and `1750` sentences respectively.

## Dataset Creation

### Curation Rationale

> First, most of the existing datasets for acronym identification (AI) are either limited in their sizes or created using simple rule-based methods.
> This is unfortunate as rules are in general not able to capture all the diverse forms to express acronyms and their long forms in text.
> Second, most of the existing datasets are in the medical domain, ignoring the challenges in other scientific domains.
> In order to address these limitations this paper introduces two new datasets for Acronym Identification.
> Notably, our datasets are annotated by human to achieve high quality and have substantially larger numbers of examples than the existing AI datasets in the non-medical domain. 

### Source Data

#### Initial Data Collection and Normalization

> In order to prepare a corpus for acronym annotation, we collect a corpus of 6,786 English papers from arXiv.
> These papers consist of 2,031,592 sentences that would be used for data annotation for AI in this work.

The dataset paper does not report the exact tokenization method.

#### Who are the source language producers?

The language was comes from papers hosted on the online digital archive [arXiv](https://arxiv.org/). No more information is available on the selection process or identity of the writers.

### Annotations

#### Annotation process

> Each sentence for annotation needs to contain at least one word in which more than half of the characters in are capital letters (i.e., acronym candidates).
> Afterward, we search for a sub-sequence of words in which the concatenation of the first one, two or three characters of the words (in the order of the words in the sub-sequence could form an acronym candidate.
> We call the sub-sequence a long form candidate. If we cannot find any long form candidate, we remove the sentence.
> Using this process, we end up with 17,506 sentences to be annotated manually by the annotators from Amazon Mechanical Turk (MTurk).
> In particular, we create a HIT for each sentence and ask the workers to annotate the short forms and the long forms in the sentence.
> In case of disagreements, if two out of three workers agree on an annotation, we use majority voting to decide the correct annotation.
> Otherwise, a fourth annotator is hired to resolve the conflict

#### Who are the annotators?

Workers were recruited through Amazon MEchanical Turk and paid $0.05 per annotation. No further demographic information is provided.

### Personal and Sensitive Information

Papers published on arXiv are unlikely to contain much personal information, although some do include some poorly chosen examples revealing personal details, so the data should be used with care.

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

The dataset provided for this shared task is licensed under CC BY-NC-SA 4.0 international license.

### Citation Information

```
@inproceedings{Veyseh2020,
  author    = {Amir Pouran Ben Veyseh and
               Franck Dernoncourt and
               Quan Hung Tran and
               Thien Huu Nguyen},
  editor    = {Donia Scott and
               N{\'{u}}ria Bel and
               Chengqing Zong},
  title     = {What Does This Acronym Mean? Introducing a New Dataset for Acronym
               Identification and Disambiguation},
  booktitle = {Proceedings of the 28th International Conference on Computational
               Linguistics, {COLING} 2020, Barcelona, Spain (Online), December 8-13,
               2020},
  pages     = {3285--3301},
  publisher = {International Committee on Computational Linguistics},
  year      = {2020},
  url       = {https://doi.org/10.18653/v1/2020.coling-main.292},
  doi       = {10.18653/v1/2020.coling-main.292}
}
```

### Contributions

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.
