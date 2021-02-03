---
---

# Dataset Card for "wiki_dpr"

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

- **Homepage:** [https://github.com/facebookresearch/DPR](https://github.com/facebookresearch/DPR)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 406068.98 MB
- **Size of the generated dataset:** 448718.73 MB
- **Total amount of disk used:** 932739.13 MB

### [Dataset Summary](#dataset-summary)

This is the wikipedia split used to evaluate the Dense Passage Retrieval (DPR) model.
It contains 21M passages from wikipedia along with their DPR embeddings.
The wikipedia articles were split into multiple, disjoint text blocks of 100 words as passages.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### psgs_w100.multiset.compressed

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 145204.14 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "embeddings": "[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1....",
    "id": "0",
    "text": "his is the text of a dummy passag",
    "title": "Title of the article"
}
```

#### psgs_w100.multiset.exact

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 178700.81 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "embeddings": "[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1....",
    "id": "0",
    "text": "his is the text of a dummy passag",
    "title": "Title of the article"
}
```

#### psgs_w100.multiset.no_index

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 142464.62 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "embeddings": "[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1....",
    "id": "0",
    "text": "his is the text of a dummy passag",
    "title": "Title of the article"
}
```

#### psgs_w100.nq.compressed

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 145204.14 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "embeddings": "[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1....",
    "id": "0",
    "text": "his is the text of a dummy passag",
    "title": "Title of the article"
}
```

#### psgs_w100.nq.exact

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 178700.81 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "embeddings": "[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1....",
    "id": "0",
    "text": "his is the text of a dummy passag",
    "title": "Title of the article"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### psgs_w100.multiset.compressed
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

#### psgs_w100.multiset.exact
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

#### psgs_w100.multiset.no_index
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

#### psgs_w100.nq.compressed
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

#### psgs_w100.nq.exact
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

### [Data Splits Sample Size](#data-splits-sample-size)

|            name             | train  |
|-----------------------------|-------:|
|psgs_w100.multiset.compressed|21015300|
|psgs_w100.multiset.exact     |21015300|
|psgs_w100.multiset.no_index  |21015300|
|psgs_w100.nq.compressed      |21015300|
|psgs_w100.nq.exact           |21015300|

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

@misc{karpukhin2020dense,
    title={Dense Passage Retrieval for Open-Domain Question Answering},
    author={Vladimir Karpukhin and Barlas Oğuz and Sewon Min and Patrick Lewis and Ledell Wu and Sergey Edunov and Danqi Chen and Wen-tau Yih},
    year={2020},
    eprint={2004.04906},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@lhoestq](https://github.com/lhoestq) for adding this dataset.