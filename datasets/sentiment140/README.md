---
language:
- en
paperswithcode_id: sentiment140
pretty_name: Sentiment140
train-eval-index:
- config: sentiment140
  task: text-classification
  task_id: multi_class_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    text: text
    sentiment: target
  metrics:
    - type: accuracy
      name: Accuracy
    - type: f1
      name: F1 macro
      args:
        average: macro
    - type: f1
      name: F1 micro
      args:
        average: micro
    - type: f1
      name: F1 weighted
      args:
        average: weighted
    - type: precision
      name: Precision macro
      args:
        average: macro
    - type: precision
      name: Precision micro
      args:
        average: micro
    - type: precision
      name: Precision weighted
      args:
        average: weighted
    - type: recall
      name: Recall macro
      args:
        average: macro
    - type: recall
      name: Recall micro
      args:
        average: micro
    - type: recall
      name: Recall weighted
      args:
        average: weighted
---

# Dataset Card for "sentiment140"

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

- **Homepage:** [http://help.sentiment140.com/home](http://help.sentiment140.com/home)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 77.59 MB
- **Size of the generated dataset:** 215.36 MB
- **Total amount of disk used:** 292.95 MB

### Dataset Summary

Sentiment140 consists of Twitter messages with emoticons, which are used as noisy labels for
sentiment classification. For more detailed information please refer to the paper.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### sentiment140

- **Size of downloaded dataset files:** 77.59 MB
- **Size of the generated dataset:** 215.36 MB
- **Total amount of disk used:** 292.95 MB

An example of 'train' looks as follows.
```
{
    "date": "23-04-2010",
    "query": "NO_QUERY",
    "sentiment": 3,
    "text": "train message",
    "user": "train user"
}
```

### Data Fields

The data fields are the same among all splits.

#### sentiment140
- `text`: a `string` feature.
- `date`: a `string` feature.
- `user`: a `string` feature.
- `sentiment`: a `int32` feature.
- `query`: a `string` feature.

### Data Splits

|    name    | train |test|
|------------|------:|---:|
|sentiment140|1600000| 498|

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
@article{go2009twitter,
  title={Twitter sentiment classification using distant supervision},
  author={Go, Alec and Bhayani, Richa and Huang, Lei},
  journal={CS224N project report, Stanford},
  volume={1},
  number={12},
  pages={2009},
  year={2009}
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
