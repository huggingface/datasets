---
---

# Dataset Card for "wikipedia"

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

- **Homepage:** [https://dumps.wikimedia.org](https://dumps.wikimedia.org)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 30739.25 MB
- **Size of the generated dataset:** 35376.35 MB
- **Total amount of disk used:** 66115.60 MB

### [Dataset Summary](#dataset-summary)

Wikipedia dataset containing cleaned articles of all languages.
The datasets are built from the Wikipedia dump
(https://dumps.wikimedia.org/) with one split per language. Each example
contains the content of one full Wikipedia article with cleaning to strip
markdown and unwanted sections (references, etc.).

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### 20200501.de

- **Size of downloaded dataset files:** 5531.82 MB
- **Size of the generated dataset:** 7716.79 MB
- **Total amount of disk used:** 13248.61 MB

An example of 'train' looks as follows.
```

```

#### 20200501.en

- **Size of downloaded dataset files:** 17396.28 MB
- **Size of the generated dataset:** 17481.07 MB
- **Total amount of disk used:** 34877.35 MB

An example of 'train' looks as follows.
```

```

#### 20200501.fr

- **Size of downloaded dataset files:** 4653.55 MB
- **Size of the generated dataset:** 6182.24 MB
- **Total amount of disk used:** 10835.79 MB

An example of 'train' looks as follows.
```

```

#### 20200501.frr

- **Size of downloaded dataset files:** 9.05 MB
- **Size of the generated dataset:** 5.88 MB
- **Total amount of disk used:** 14.93 MB

An example of 'train' looks as follows.
```

```

#### 20200501.it

- **Size of downloaded dataset files:** 2970.57 MB
- **Size of the generated dataset:** 3809.89 MB
- **Total amount of disk used:** 6780.46 MB

An example of 'train' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### 20200501.de
- `title`: a `string` feature.
- `text`: a `string` feature.

#### 20200501.en
- `title`: a `string` feature.
- `text`: a `string` feature.

#### 20200501.fr
- `title`: a `string` feature.
- `text`: a `string` feature.

#### 20200501.frr
- `title`: a `string` feature.
- `text`: a `string` feature.

#### 20200501.it
- `title`: a `string` feature.
- `text`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|    name    | train |
|------------|------:|
|20200501.de |3140341|
|20200501.en |6078422|
|20200501.fr |2210508|
|20200501.frr|  11803|
|20200501.it |1931197|

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
@ONLINE {wikidump,
    author = "Wikimedia Foundation",
    title  = "Wikimedia Downloads",
    url    = "https://dumps.wikimedia.org"
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.