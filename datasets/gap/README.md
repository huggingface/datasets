---
annotations_creators:
- crowdsourced
language:
- en
language_creators:
- found
license:
- unknown
multilinguality:
- monolingual
pretty_name: GAP Benchmark Suite
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- coreference-resolution
paperswithcode_id: gap
dataset_info:
  features:
  - name: ID
    dtype: string
  - name: Text
    dtype: string
  - name: Pronoun
    dtype: string
  - name: Pronoun-offset
    dtype: int32
  - name: A
    dtype: string
  - name: A-offset
    dtype: int32
  - name: A-coref
    dtype: bool
  - name: B
    dtype: string
  - name: B-offset
    dtype: int32
  - name: B-coref
    dtype: bool
  - name: URL
    dtype: string
  splits:
  - name: test
    num_bytes: 1090462
    num_examples: 2000
  - name: train
    num_bytes: 1095623
    num_examples: 2000
  - name: validation
    num_bytes: 248329
    num_examples: 454
  download_size: 2401971
  dataset_size: 2434414
---

# Dataset Card for "gap"

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

- **Homepage:** [https://github.com/google-research-datasets/gap-coreference](https://github.com/google-research-datasets/gap-coreference)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [Mind the GAP: A Balanced Corpus of Gendered Ambiguous Pronouns](https://arxiv.org/abs/1810.05201)
- **Point of Contact:** [gap-coreference@google.com](mailto:gap-coreference@google.com)
- **Size of downloaded dataset files:** 2.29 MB
- **Size of the generated dataset:** 2.32 MB
- **Total amount of disk used:** 4.61 MB

### Dataset Summary

GAP is a gender-balanced dataset containing 8,908 coreference-labeled pairs of
(ambiguous pronoun, antecedent name), sampled from Wikipedia and released by
Google AI Language for the evaluation of coreference resolution in practical
applications.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 2.29 MB
- **Size of the generated dataset:** 2.32 MB
- **Total amount of disk used:** 4.61 MB

An example of 'validation' looks as follows.
```
{
    "A": "aliquam ultrices sagittis",
    "A-coref": false,
    "A-offset": 208,
    "B": "elementum curabitur vitae",
    "B-coref": false,
    "B-offset": 435,
    "ID": "validation-1",
    "Pronoun": "condimentum mattis pellentesque",
    "Pronoun-offset": 948,
    "Text": "Lorem ipsum dolor",
    "URL": "sem fringilla ut"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `ID`: a `string` feature.
- `Text`: a `string` feature.
- `Pronoun`: a `string` feature.
- `Pronoun-offset`: a `int32` feature.
- `A`: a `string` feature.
- `A-offset`: a `int32` feature.
- `A-coref`: a `bool` feature.
- `B`: a `string` feature.
- `B-offset`: a `int32` feature.
- `B-coref`: a `bool` feature.
- `URL`: a `string` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default| 2000|       454|2000|

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
@article{webster-etal-2018-mind,
    title = "Mind the {GAP}: A Balanced Corpus of Gendered Ambiguous Pronouns",
    author = "Webster, Kellie  and
      Recasens, Marta  and
      Axelrod, Vera  and
      Baldridge, Jason",
    journal = "Transactions of the Association for Computational Linguistics",
    volume = "6",
    year = "2018",
    address = "Cambridge, MA",
    publisher = "MIT Press",
    url = "https://aclanthology.org/Q18-1042",
    doi = "10.1162/tacl_a_00240",
    pages = "605--617",
}
```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@otakumesi](https://github.com/otakumesi), [@lewtun](https://github.com/lewtun) for adding this dataset.