---
paperswithcode_id: null
pretty_name: StyleChangeDetection
---

# Dataset Card for "style_change_detection"

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

- **Homepage:** [https://pan.webis.de/clef20/pan20-web/style-change-detection.html](https://pan.webis.de/clef20/pan20-web/style-change-detection.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 197.60 MB
- **Total amount of disk used:** 197.60 MB

### Dataset Summary

The goal of the style change detection task is to identify text positions within a given multi-author document at which the author switches. Detecting these positions is a crucial part of the authorship identification process, and for multi-author document analysis in general.

Access to the dataset needs to be requested from zenodo.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### narrow

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 58.12 MB
- **Total amount of disk used:** 58.12 MB

An example of 'validation' looks as follows.
```
{
    "authors": 2,
    "changes": [false, false, true, false],
    "id": "2",
    "multi-author": true,
    "site": "exampleSite",
    "structure": ["A1", "A2"],
    "text": "This is text from example problem 2.\n"
}
```

#### wide

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 139.48 MB
- **Total amount of disk used:** 139.48 MB

An example of 'train' looks as follows.
```
{
    "authors": 2,
    "changes": [false, false, true, false],
    "id": "2",
    "multi-author": true,
    "site": "exampleSite",
    "structure": ["A1", "A2"],
    "text": "This is text from example problem 2.\n"
}
```

### Data Fields

The data fields are the same among all splits.

#### narrow
- `id`: a `string` feature.
- `text`: a `string` feature.
- `authors`: a `int32` feature.
- `structure`: a `list` of `string` features.
- `site`: a `string` feature.
- `multi-author`: a `bool` feature.
- `changes`: a `list` of `bool` features.

#### wide
- `id`: a `string` feature.
- `text`: a `string` feature.
- `authors`: a `int32` feature.
- `structure`: a `list` of `string` features.
- `site`: a `string` feature.
- `multi-author`: a `bool` feature.
- `changes`: a `list` of `bool` features.

### Data Splits

| name |train|validation|
|------|----:|---------:|
|narrow| 3418|      1713|
|wide  | 8030|      4019|

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
@inproceedings{bevendorff2020shared,
  title={Shared Tasks on Authorship Analysis at PAN 2020},
  author={Bevendorff, Janek and Ghanem, Bilal and Giachanou, Anastasia and Kestemont, Mike and Manjavacas, Enrique and Potthast, Martin and Rangel, Francisco and Rosso, Paolo and Specht, G{"u}nther and Stamatatos, Efstathios and others},
  booktitle={European Conference on Information Retrieval},
  pages={508--516},
  year={2020},
  organization={Springer}
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@ghomasHudson](https://github.com/ghomasHudson), [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
