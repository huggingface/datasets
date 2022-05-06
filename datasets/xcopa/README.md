---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- et
- ht
- id
- it
- qu
- sw
- ta
- th
- tr
- vi
- zh
licenses:
- cc-by-4.0
multilinguality:
- multilingual
pretty_name: XCOPA
size_categories:
- unknown
source_datasets:
- extended|copa
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
paperswithcode_id: xcopa
---

# Dataset Card for "xcopa"

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

- **Homepage:** [https://github.com/cambridgeltl/xcopa](https://github.com/cambridgeltl/xcopa)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3.89 MB
- **Size of the generated dataset:** 0.97 MB
- **Total amount of disk used:** 4.86 MB

### Dataset Summary

  XCOPA: A Multilingual Dataset for Causal Commonsense Reasoning
The Cross-lingual Choice of Plausible Alternatives dataset is a benchmark to evaluate the ability of machine learning models to transfer commonsense reasoning across
languages. The dataset is the translation and reannotation of the English COPA (Roemmele et al. 2011) and covers 11 languages from 11 families and several areas around
the globe. The dataset is challenging as it requires both the command of world knowledge and the ability to generalise to new languages. All the details about the
creation of XCOPA and the implementation of the baselines are available in the paper.

Xcopa language et

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

- et
- ht
- id
- it
- qu
- sw
- ta
- th
- tr
- vi
- zh

## Dataset Structure

### Data Instances

#### et

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.07 MB
- **Total amount of disk used:** 0.42 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

#### ht

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.07 MB
- **Total amount of disk used:** 0.42 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

#### id

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.07 MB
- **Total amount of disk used:** 0.43 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

#### it

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.08 MB
- **Total amount of disk used:** 0.43 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

#### qu

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.08 MB
- **Total amount of disk used:** 0.43 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

### Data Fields

The data fields are the same among all splits.

#### et
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

#### ht
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

#### id
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

#### it
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

#### qu
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

### Data Splits

|name|validation|test|
|----|---------:|---:|
|et  |       100| 500|
|ht  |       100| 500|
|id  |       100| 500|
|it  |       100| 500|
|qu  |       100| 500|

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

[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

### Citation Information

```
  @article{ponti2020xcopa,
  title={{XCOPA: A} Multilingual Dataset for Causal Commonsense Reasoning},
  author={Edoardo M. Ponti, Goran Glava{s}, Olga Majewska, Qianchu Liu, Ivan Vuli'{c} and Anna Korhonen},
  journal={arXiv preprint},
  year={2020},
  url={https://ducdauge.github.io/files/xcopa.pdf}
}

@inproceedings{roemmele2011choice,
  title={Choice of plausible alternatives: An evaluation of commonsense causal reasoning},
  author={Roemmele, Melissa and Bejan, Cosmin Adrian and Gordon, Andrew S},
  booktitle={2011 AAAI Spring Symposium Series},
  year={2011},
  url={https://people.ict.usc.edu/~gordon/publications/AAAI-SPRING11A.PDF},
}

```

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
