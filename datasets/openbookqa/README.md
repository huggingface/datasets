---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- unknown
multilinguality:
- monolingual
pretty_name: OpenBookQA
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: openbookqa
---

# Dataset Card for OpenBookQA

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

- **Homepage:** [https://allenai.org/data/open-book-qa](https://allenai.org/data/open-book-qa)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 2.76 MB
- **Size of the generated dataset:** 2.75 MB
- **Total amount of disk used:** 5.51 MB

### Dataset Summary

OpenBookQA aims to promote research in advanced question-answering, probing a deeper understanding of both the topic
(with salient facts summarized as an open book, also provided with the dataset) and the language it is expressed in. In
particular, it contains questions that require multi-step reasoning, use of additional common and commonsense knowledge,
and rich text comprehension.
OpenBookQA is a new kind of question-answering dataset modeled after open book exams for assessing human understanding of
a subject.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### main

- **Size of downloaded dataset files:** 1.38 MB
- **Size of the generated dataset:** 1.38 MB
- **Total amount of disk used:** 2.75 MB

An example of 'train' looks as follows:
```
{'id': '7-980',
 'question_stem': 'The sun is responsible for',
 'choices': {'text': ['puppies learning new tricks',
   'children growing up and getting old',
   'flowers wilting in a vase',
   'plants sprouting, blooming and wilting'],
  'label': ['A', 'B', 'C', 'D']},
 'answerKey': 'D'}
```

#### additional

- **Size of downloaded dataset files:** 1.38 MB
- **Size of the generated dataset:** 1.38 MB
- **Total amount of disk used:** 2.75 MB

An example of 'train' looks as follows:
```
{'id': '7-980',
 'question_stem': 'The sun is responsible for',
 'choices': {'text': ['puppies learning new tricks',
   'children growing up and getting old',
   'flowers wilting in a vase',
   'plants sprouting, blooming and wilting'],
  'label': ['A', 'B', 'C', 'D']},
 'answerKey': 'D',
 'fact1': 'the sun is the source of energy for physical cycles on Earth',
 'humanScore': 1.0,
 'clarity': 2.0,
 'turkIdAnonymized': 'b356d338b7'}
```

### Data Fields

The data fields are the same among all splits.

#### main
- `id`: a `string` feature.
- `question_stem`: a `string` feature.
- `choices`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `label`: a `string` feature.
- `answerKey`: a `string` feature.

#### additional
- `id`: a `string` feature.
- `question_stem`: a `string` feature.
- `choices`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `label`: a `string` feature.
- `answerKey`: a `string` feature.
- `fact1` (`str`): oOriginating common knowledge core fact associated to the question.
- `humanScore` (`float`): Human accuracy score.
- `clarity` (`float`): Clarity score.
- `turkIdAnonymized` (`str`): Anonymized crowd-worker ID.

### Data Splits

| name       | train | validation | test |
|------------|------:|-----------:|-----:|
| main       |  4957 |        500 |  500 |
| additional |  4957 |        500 |  500 |

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@inproceedings{OpenBookQA2018,
 title={Can a Suit of Armor Conduct Electricity? A New Dataset for Open Book Question Answering},
 author={Todor Mihaylov and Peter Clark and Tushar Khot and Ashish Sabharwal},
 booktitle={EMNLP},
 year={2018}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun) for adding this dataset.
