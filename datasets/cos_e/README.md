---
---

# Dataset Card for "cos_e"

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

- **Homepage:** [https://github.com/salesforce/cos-e](https://github.com/salesforce/cos-e)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 10.33 MB
- **Size of the generated dataset:** 5.14 MB
- **Total amount of disk used:** 15.47 MB

### [Dataset Summary](#dataset-summary)

Common Sense Explanations (CoS-E) allows for training language models to
automatically generate explanations that can be used during training and
inference in a novel Commonsense Auto-Generated Explanation (CAGE) framework.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### v1.0

- **Size of downloaded dataset files:** 4.10 MB
- **Size of the generated dataset:** 2.23 MB
- **Total amount of disk used:** 6.33 MB

An example of 'train' looks as follows.
```
{
    "abstractive_explanation": "this is open-ended",
    "answer": "b",
    "choices": ["a", "b", "c"],
    "extractive_explanation": "this is selected train",
    "id": "42",
    "question": "question goes here."
}
```

#### v1.11

- **Size of downloaded dataset files:** 6.23 MB
- **Size of the generated dataset:** 2.91 MB
- **Total amount of disk used:** 9.14 MB

An example of 'train' looks as follows.
```
{
    "abstractive_explanation": "this is open-ended",
    "answer": "b",
    "choices": ["a", "b", "c"],
    "extractive_explanation": "this is selected train",
    "id": "42",
    "question": "question goes here."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### v1.0
- `id`: a `string` feature.
- `question`: a `string` feature.
- `choices`: a `list` of `string` features.
- `answer`: a `string` feature.
- `abstractive_explanation`: a `string` feature.
- `extractive_explanation`: a `string` feature.

#### v1.11
- `id`: a `string` feature.
- `question`: a `string` feature.
- `choices`: a `list` of `string` features.
- `answer`: a `string` feature.
- `abstractive_explanation`: a `string` feature.
- `extractive_explanation`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|name |train|validation|
|-----|----:|---------:|
|v1.0 | 7610|       950|
|v1.11| 9741|      1221|

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

@inproceedings{rajani2019explain,
     title = "Explain Yourself! Leveraging Language models for Commonsense Reasoning",
    author = "Rajani, Nazneen Fatema  and
      McCann, Bryan  and
      Xiong, Caiming  and
      Socher, Richard",
      year="2019",
    booktitle = "Proceedings of the 2019 Conference of the Association for Computational Linguistics (ACL2019)",
    url ="https://arxiv.org/abs/1906.02361"
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham), [@patrickvonplaten](https://github.com/patrickvonplaten), [@albertvillanova](https://github.com/albertvillanova), [@lhoestq](https://github.com/lhoestq) for adding this dataset.