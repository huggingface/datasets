---
pretty_name: SciFact
language:
- en
paperswithcode_id: null
---

# Dataset Card for "scifact"

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

- **Homepage:** [https://scifact.apps.allenai.org/](https://scifact.apps.allenai.org/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 5.43 MB
- **Size of the generated dataset:** 7.88 MB
- **Total amount of disk used:** 13.32 MB

### Dataset Summary

SciFact, a dataset of 1.4K expert-written scientific claims paired with evidence-containing abstracts, and annotated with labels and rationales

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### claims

- **Size of downloaded dataset files:** 2.72 MB
- **Size of the generated dataset:** 0.25 MB
- **Total amount of disk used:** 2.97 MB

An example of 'validation' looks as follows.
```
{
    "cited_doc_ids": [14717500],
    "claim": "1,000 genomes project enables mapping of genetic sequence variation consisting of rare variants with larger penetrance effects than common variants.",
    "evidence_doc_id": "14717500",
    "evidence_label": "SUPPORT",
    "evidence_sentences": [2, 5],
    "id": 3
}
```

#### corpus

- **Size of downloaded dataset files:** 2.72 MB
- **Size of the generated dataset:** 7.63 MB
- **Total amount of disk used:** 10.35 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "abstract": "[\"Alterations of the architecture of cerebral white matter in the developing human brain can affect cortical development and res...",
    "doc_id": 4983,
    "structured": false,
    "title": "Microstructural development of human newborn cerebral white matter assessed in vivo by diffusion tensor magnetic resonance imaging."
}
```

### Data Fields

The data fields are the same among all splits.

#### claims
- `id`: a `int32` feature.
- `claim`: a `string` feature.
- `evidence_doc_id`: a `string` feature.
- `evidence_label`: a `string` feature.
- `evidence_sentences`: a `list` of `int32` features.
- `cited_doc_ids`: a `list` of `int32` features.

#### corpus
- `doc_id`: a `int32` feature.
- `title`: a `string` feature.
- `abstract`: a `list` of `string` features.
- `structured`: a `bool` feature.

### Data Splits

#### claims

|      |train|validation|test|
|------|----:|---------:|---:|
|claims| 1261|       450| 300|

#### corpus

|      |train|
|------|----:|
|corpus| 5183|

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
@inproceedings{scifact2020
  title={ Fact or Fiction: Verifying Scientific Claims},
  author={David,  Wadden and Kyle, Lo and Lucy Lu, Wang and Shanchuan, Lin and Madeleine van, Zuylen and Arman, Cohan and  Hannaneh, Hajishirzi},
  booktitle={2011 AAAI Spring Symposium Series},
  year={2020},
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@dwadden](https://github.com/dwadden), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham), [@lewtun](https://github.com/lewtun) for adding this dataset.