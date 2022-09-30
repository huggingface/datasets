---
annotations_creators:
- expert-generated
language:
- en
language_creators:
- expert-generated
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: Modified Winograd Schema Challenge (MWSC)
size_categories:
- n<1K
source_datasets:
- extended|winograd_wsc
task_categories:
- multiple-choice
task_ids:
- multiple-choice-coreference-resolution
paperswithcode_id: null
---

# Dataset Card for The modified Winograd Schema Challenge (MWSC)

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

- **Homepage:** [http://decanlp.com](http://decanlp.com)
- **Repository:** https://github.com/salesforce/decaNLP
- **Paper:** [The Natural Language Decathlon: Multitask Learning as Question Answering](https://arxiv.org/abs/1806.08730)
- **Point of Contact:** [Bryan McCann](mailto:bmccann@salesforce.com), [Nitish Shirish Keskar](mailto:nkeskar@salesforce.com)
- **Size of downloaded dataset files:** 0.02 MB
- **Size of the generated dataset:** 0.04 MB
- **Total amount of disk used:** 0.06 MB

### Dataset Summary

Examples taken from the Winograd Schema Challenge modified to ensure that answers are a single word from the context.
This Modified Winograd Schema Challenge (MWSC) ensures that scores are neither inflated nor deflated by oddities in phrasing.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 0.02 MB
- **Size of the generated dataset:** 0.04 MB
- **Total amount of disk used:** 0.06 MB

An example looks as follows:
```
{
    "sentence": "The city councilmen refused the demonstrators a permit because they feared violence.",
    "question": "Who feared violence?",
    "options": [ "councilmen", "demonstrators" ],
    "answer": "councilmen"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `sentence`: a `string` feature.
- `question`: a `string` feature.
- `options`: a `list` of `string` features.
- `answer`: a `string` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|   80|        82| 100|

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

Our code for running decaNLP has been open sourced under BSD-3-Clause. 

We chose to restrict decaNLP to datasets that were free and publicly accessible for research, but you should check their individual terms if you deviate from this use case.

From the [Winograd Schema Challenge](https://cs.nyu.edu/~davise/papers/WinogradSchemas/WS.html):
> Both versions of the collections are licenced under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

### Citation Information

If you use this in your work, please cite:
```
@article{McCann2018decaNLP,
  title={The Natural Language Decathlon: Multitask Learning as Question Answering},
  author={Bryan McCann and Nitish Shirish Keskar and Caiming Xiong and Richard Socher},
  journal={arXiv preprint arXiv:1806.08730},
  year={2018}
}
```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@ghomasHudson](https://github.com/ghomasHudson), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
