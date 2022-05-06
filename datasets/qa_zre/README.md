---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
pretty_name: QaZre
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- question-answering-other-zero-shot-relation-extraction
paperswithcode_id: null
---

# Dataset Card for QaZre

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

- **Homepage:** [http://nlp.cs.washington.edu/zeroshot](http://nlp.cs.washington.edu/zeroshot)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 492.15 MB
- **Size of the generated dataset:** 1989.22 MB
- **Total amount of disk used:** 2481.37 MB

### Dataset Summary

A dataset reducing relation extraction to simple reading comprehension questions

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 492.15 MB
- **Size of the generated dataset:** 1989.22 MB
- **Total amount of disk used:** 2481.37 MB

An example of 'validation' looks as follows.
```
{
    "answers": [],
    "context": "answer",
    "question": "What is XXX in this question?",
    "relation": "relation_name",
    "subject": "Some entity Here is a bit of context which will explain the question in some way"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `relation`: a `string` feature.
- `question`: a `string` feature.
- `subject`: a `string` feature.
- `context`: a `string` feature.
- `answers`: a `list` of `string` features.

### Data Splits

| name    |   train | validation |   test |
|---------|--------:|-----------:|-------:|
| default | 8400000 |       6000 | 120000 |

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

Unknown.

### Citation Information

```
@inproceedings{levy-etal-2017-zero,
    title = "Zero-Shot Relation Extraction via Reading Comprehension",
    author = "Levy, Omer  and
      Seo, Minjoon  and
      Choi, Eunsol  and
      Zettlemoyer, Luke",
    booktitle = "Proceedings of the 21st Conference on Computational Natural Language Learning ({C}o{NLL} 2017)",
    month = aug,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/K17-1034",
    doi = "10.18653/v1/K17-1034",
    pages = "333--342",
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@ghomasHudson](https://github.com/ghomasHudson), [@lewtun](https://github.com/lewtun) for adding this dataset.
