---
---

# Dataset Card for "openbookqa"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://allenai.org/data/open-book-qa](https://allenai.org/data/open-book-qa)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 2.76 MB
- **Size of the generated dataset:** 2.75 MB
- **Total amount of disk used:** 5.51 MB

### [Dataset Summary](#dataset-summary)

OpenBookQA aims to promote research in advanced question-answering, probing a deeper understanding of both the topic
(with salient facts summarized as an open book, also provided with the dataset) and the language it is expressed in. In
particular, it contains questions that require multi-step reasoning, use of additional common and commonsense knowledge,
and rich text comprehension.
OpenBookQA is a new kind of question-answering dataset modeled after open book exams for assessing human understanding of
a subject.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### additional

- **Size of downloaded dataset files:** 1.38 MB
- **Size of the generated dataset:** 1.38 MB
- **Total amount of disk used:** 2.75 MB

An example of 'train' looks as follows.
```

```

#### main

- **Size of downloaded dataset files:** 1.38 MB
- **Size of the generated dataset:** 1.38 MB
- **Total amount of disk used:** 2.75 MB

An example of 'validation' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### additional
- `id`: a `string` feature.
- `question_stem`: a `string` feature.
- `choices`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `label`: a `string` feature.
- `answerKey`: a `string` feature.

#### main
- `id`: a `string` feature.
- `question_stem`: a `string` feature.
- `choices`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `label`: a `string` feature.
- `answerKey`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|   name   |train|validation|test|
|----------|----:|---------:|---:|
|additional| 4957|       500| 500|
|main      | 4957|       500| 500|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

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