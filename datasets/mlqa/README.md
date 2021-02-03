---
---

# Dataset Card for "mlqa"

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

- **Homepage:** [https://github.com/facebookresearch/MLQA](https://github.com/facebookresearch/MLQA)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3958.58 MB
- **Size of the generated dataset:** 867.85 MB
- **Total amount of disk used:** 4826.43 MB

### [Dataset Summary](#dataset-summary)

    MLQA (MultiLingual Question Answering) is a benchmark dataset for evaluating cross-lingual question answering performance.
    MLQA consists of over 5K extractive QA instances (12K in English) in SQuAD format in seven languages - English, Arabic,
    German, Spanish, Hindi, Vietnamese and Simplified Chinese. MLQA is highly parallel, with QA instances parallel between
    4 different languages on average.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### mlqa-translate-test.ar

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 5.23 MB
- **Total amount of disk used:** 14.84 MB

An example of 'test' looks as follows.
```

```

#### mlqa-translate-test.de

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 3.70 MB
- **Total amount of disk used:** 13.31 MB

An example of 'test' looks as follows.
```

```

#### mlqa-translate-test.es

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 3.74 MB
- **Total amount of disk used:** 13.34 MB

An example of 'test' looks as follows.
```

```

#### mlqa-translate-test.hi

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 4.40 MB
- **Total amount of disk used:** 14.00 MB

An example of 'test' looks as follows.
```

```

#### mlqa-translate-test.vi

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 5.72 MB
- **Total amount of disk used:** 15.33 MB

An example of 'test' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### mlqa-translate-test.ar
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

#### mlqa-translate-test.de
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

#### mlqa-translate-test.es
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

#### mlqa-translate-test.hi
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

#### mlqa-translate-test.vi
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|         name         |test|
|----------------------|---:|
|mlqa-translate-test.ar|5335|
|mlqa-translate-test.de|4517|
|mlqa-translate-test.es|5253|
|mlqa-translate-test.hi|4918|
|mlqa-translate-test.vi|5495|

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
@article{lewis2019mlqa,
  title={MLQA: Evaluating Cross-lingual Extractive Question Answering},
  author={Lewis, Patrick and Oguz, Barlas and Rinott, Ruty and Riedel, Sebastian and Schwenk, Holger},
  journal={arXiv preprint arXiv:1910.07475},
  year={2019}
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@M-Salti](https://github.com/M-Salti), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham), [@lhoestq](https://github.com/lhoestq) for adding this dataset.