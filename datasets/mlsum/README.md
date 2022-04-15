---
annotations_creators:
- found
language_creators:
- found
languages:
- de
- es
- fr
- ru
- tr
licenses:
- other-research-only
multilinguality:
- multilingual
size_categories:
  de:
  - 100K<n<1M
  es:
  - 100K<n<1M
  fr:
  - 100K<n<1M
  ru:
  - 10K<n<100K
  tu:
  - 100K<n<1M
source_datasets:
- extended|cnn_dailymail
- original
task_categories:
- translation
- text-classification
task_ids:
- multi-class-classification
- multi-label-classification
- summarization
- topic-classification
paperswithcode_id: mlsum
pretty_name: MLSUM
---

# Dataset Card for MLSUM

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

- **Homepage:** []()
- **Repository:** https://github.com/recitalAI/MLSUM
- **Paper:** https://www.aclweb.org/anthology/2020.emnlp-main.647/
- **Point of Contact:** [email](thomas@recital.ai)
- **Size of downloaded dataset files:** 1748.64 MB
- **Size of the generated dataset:** 4635.42 MB
- **Total amount of disk used:** 6384.06 MB

### Dataset Summary

We present MLSUM, the first large-scale MultiLingual SUMmarization dataset.
Obtained from online newspapers, it contains 1.5M+ article/summary pairs in five different languages -- namely, French, German, Spanish, Russian, Turkish.
Together with English newspapers from the popular CNN/Daily mail dataset, the collected data form a large scale multilingual dataset which can enable new research directions for the text summarization community.
We report cross-lingual comparative analyses based on state-of-the-art systems.
These highlight existing biases which motivate the use of a multi-lingual dataset.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### de

- **Size of downloaded dataset files:** 330.52 MB
- **Size of the generated dataset:** 897.34 MB
- **Total amount of disk used:** 1227.86 MB

An example of 'validation' looks as follows.
```
{
    "date": "01/01/2001",
    "summary": "A text",
    "text": "This is a text",
    "title": "A sample",
    "topic": "football",
    "url": "https://www.google.com"
}
```

#### es

- **Size of downloaded dataset files:** 489.53 MB
- **Size of the generated dataset:** 1274.55 MB
- **Total amount of disk used:** 1764.09 MB

An example of 'validation' looks as follows.
```
{
    "date": "01/01/2001",
    "summary": "A text",
    "text": "This is a text",
    "title": "A sample",
    "topic": "football",
    "url": "https://www.google.com"
}
```

#### fr

- **Size of downloaded dataset files:** 591.27 MB
- **Size of the generated dataset:** 1537.36 MB
- **Total amount of disk used:** 2128.63 MB

An example of 'validation' looks as follows.
```
{
    "date": "01/01/2001",
    "summary": "A text",
    "text": "This is a text",
    "title": "A sample",
    "topic": "football",
    "url": "https://www.google.com"
}
```

#### ru

- **Size of downloaded dataset files:** 101.30 MB
- **Size of the generated dataset:** 263.38 MB
- **Total amount of disk used:** 364.68 MB

An example of 'train' looks as follows.
```
{
    "date": "01/01/2001",
    "summary": "A text",
    "text": "This is a text",
    "title": "A sample",
    "topic": "football",
    "url": "https://www.google.com"
}
```

#### tu

- **Size of downloaded dataset files:** 236.03 MB
- **Size of the generated dataset:** 662.79 MB
- **Total amount of disk used:** 898.82 MB

An example of 'train' looks as follows.
```
{
    "date": "01/01/2001",
    "summary": "A text",
    "text": "This is a text",
    "title": "A sample",
    "topic": "football",
    "url": "https://www.google.com"
}
```

### Data Fields

The data fields are the same among all splits.

#### de
- `text`: a `string` feature.
- `summary`: a `string` feature.
- `topic`: a `string` feature.
- `url`: a `string` feature.
- `title`: a `string` feature.
- `date`: a `string` feature.

#### es
- `text`: a `string` feature.
- `summary`: a `string` feature.
- `topic`: a `string` feature.
- `url`: a `string` feature.
- `title`: a `string` feature.
- `date`: a `string` feature.

#### fr
- `text`: a `string` feature.
- `summary`: a `string` feature.
- `topic`: a `string` feature.
- `url`: a `string` feature.
- `title`: a `string` feature.
- `date`: a `string` feature.

#### ru
- `text`: a `string` feature.
- `summary`: a `string` feature.
- `topic`: a `string` feature.
- `url`: a `string` feature.
- `title`: a `string` feature.
- `date`: a `string` feature.

#### tu
- `text`: a `string` feature.
- `summary`: a `string` feature.
- `topic`: a `string` feature.
- `url`: a `string` feature.
- `title`: a `string` feature.
- `date`: a `string` feature.

### Data Splits

|name|train |validation|test |
|----|-----:|---------:|----:|
|de  |220887|     11394|10701|
|es  |266367|     10358|13920|
|fr  |392902|     16059|15828|
|ru  | 25556|       750|  757|
|tu  |249277|     11565|12775|

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

Usage of dataset is restricted to non-commercial research purposes only. Copyright belongs to the original copyright holders. See https://github.com/recitalAI/MLSUM#mlsum

### Citation Information

```
@article{scialom2020mlsum,
  title={MLSUM: The Multilingual Summarization Corpus},
  author={Scialom, Thomas and Dray, Paul-Alexis and Lamprier, Sylvain and Piwowarski, Benjamin and Staiano, Jacopo},
  journal={arXiv preprint arXiv:2004.14900},
  year={2020}
}

```


### Contributions

Thanks to [@RachelKer](https://github.com/RachelKer), [@albertvillanova](https://github.com/albertvillanova), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
