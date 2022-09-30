---
pretty_name: RottenTomatoes - MR Movie Review Data
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- unknown
multilinguality:
- monolingual
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: mr
size_categories:
- 1K<n<10K
source_datasets:
- original
train-eval-index:
- config: default
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
      name: F1
      args:
        average: binary
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

# Dataset Card for "rotten_tomatoes"

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

- **Homepage:** [http://www.cs.cornell.edu/people/pabo/movie-review-data/](http://www.cs.cornell.edu/people/pabo/movie-review-data/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [https://arxiv.org/abs/cs/0506075](https://arxiv.org/abs/cs/0506075)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.47 MB
- **Size of the generated dataset:** 1.28 MB
- **Total amount of disk used:** 1.75 MB

### Dataset Summary

Movie Review Dataset.
This is a dataset of containing 5,331 positive and 5,331 negative processed
sentences from Rotten Tomatoes movie reviews. This data was first used in Bo
Pang and Lillian Lee, ``Seeing stars: Exploiting class relationships for
sentiment categorization with respect to rating scales.'', Proceedings of the
ACL, 2005.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 0.47 MB
- **Size of the generated dataset:** 1.28 MB
- **Total amount of disk used:** 1.75 MB

An example of 'validation' looks as follows.
```
{
    "label": 1,
    "text": "Sometimes the days and nights just drag on -- it 's the morning that make me feel alive . And I have one thing to thank for that : pancakes . "
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `text`: a `string` feature.
- `label`: a classification label, with possible values including `neg` (0), `pos` (1).

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default| 8530|      1066|1066|

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
@InProceedings{Pang+Lee:05a,
  author =       {Bo Pang and Lillian Lee},
  title =        {Seeing stars: Exploiting class relationships for sentiment
                  categorization with respect to rating scales},
  booktitle =    {Proceedings of the ACL},
  year =         2005
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@jxmorris12](https://github.com/jxmorris12) for adding this dataset.
