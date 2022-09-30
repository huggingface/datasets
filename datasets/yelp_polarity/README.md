---
language:
- en
paperswithcode_id: null
pretty_name: YelpPolarity
train-eval-index:
- config: plain_text
  task: text-classification
  task_id: binary_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    text: text
    label: target
  metrics:
    - type: accuracy
      name: Accuracy
    - type: f1
      name: F1 binary
      args:
        average: binary
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

# Dataset Card for "yelp_polarity"

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

- **Homepage:** [https://course.fast.ai/datasets](https://course.fast.ai/datasets)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 158.67 MB
- **Size of the generated dataset:** 421.28 MB
- **Total amount of disk used:** 579.95 MB

### Dataset Summary

Large Yelp Review Dataset.
This is a dataset for binary sentiment classification. We provide a set of 560,000 highly polar yelp reviews for training, and 38,000 for testing.
ORIGIN
The Yelp reviews dataset consists of reviews from Yelp. It is extracted
from the Yelp Dataset Challenge 2015 data. For more information, please
refer to http://www.yelp.com/dataset_challenge

The Yelp reviews polarity dataset is constructed by
Xiang Zhang (xiang.zhang@nyu.edu) from the above dataset.
It is first used as a text classification benchmark in the following paper:
Xiang Zhang, Junbo Zhao, Yann LeCun. Character-level Convolutional Networks
for Text Classification. Advances in Neural Information Processing Systems 28
(NIPS 2015).

DESCRIPTION

The Yelp reviews polarity dataset is constructed by considering stars 1 and 2
negative, and 3 and 4 positive. For each polarity 280,000 training samples and
19,000 testing samples are take randomly. In total there are 560,000 trainig
samples and 38,000 testing samples. Negative polarity is class 1,
and positive class 2.

The files train.csv and test.csv contain all the training samples as
comma-sparated values. There are 2 columns in them, corresponding to class
index (1 and 2) and review text. The review texts are escaped using double
quotes ("), and any internal double quote is escaped by 2 double quotes ("").
New lines are escaped by a backslash followed with an "n" character,
that is "
".

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### plain_text

- **Size of downloaded dataset files:** 158.67 MB
- **Size of the generated dataset:** 421.28 MB
- **Total amount of disk used:** 579.95 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "label": 0,
    "text": "\"Unfortunately, the frustration of being Dr. Goldberg's patient is a repeat of the experience I've had with so many other doctor..."
}
```

### Data Fields

The data fields are the same among all splits.

#### plain_text
- `text`: a `string` feature.
- `label`: a classification label, with possible values including `1` (0), `2` (1).

### Data Splits

|   name   |train |test |
|----------|-----:|----:|
|plain_text|560000|38000|

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
@article{zhangCharacterlevelConvolutionalNetworks2015,
  archivePrefix = {arXiv},
  eprinttype = {arxiv},
  eprint = {1509.01626},
  primaryClass = {cs},
  title = {Character-Level {{Convolutional Networks}} for {{Text Classification}}},
  abstract = {This article offers an empirical exploration on the use of character-level convolutional networks (ConvNets) for text classification. We constructed several large-scale datasets to show that character-level convolutional networks could achieve state-of-the-art or competitive results. Comparisons are offered against traditional models such as bag of words, n-grams and their TFIDF variants, and deep learning models such as word-based ConvNets and recurrent neural networks.},
  journal = {arXiv:1509.01626 [cs]},
  author = {Zhang, Xiang and Zhao, Junbo and LeCun, Yann},
  month = sep,
  year = {2015},
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf), [@julien-c](https://github.com/julien-c) for adding this dataset.
