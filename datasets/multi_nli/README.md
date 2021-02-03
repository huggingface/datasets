---
---

# Dataset Card for "multi_nli"

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

- **Homepage:** [https://www.nyu.edu/projects/bowman/multinli/](https://www.nyu.edu/projects/bowman/multinli/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 216.34 MB
- **Size of the generated dataset:** 73.39 MB
- **Total amount of disk used:** 289.74 MB

### [Dataset Summary](#dataset-summary)

The Multi-Genre Natural Language Inference (MultiNLI) corpus is a
crowd-sourced collection of 433k sentence pairs annotated with textual
entailment information. The corpus is modeled on the SNLI corpus, but differs in
that covers a range of genres of spoken and written text, and supports a
distinctive cross-genre generalization evaluation. The corpus served as the
basis for the shared task of the RepEval 2017 Workshop at EMNLP in Copenhagen.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### plain_text

- **Size of downloaded dataset files:** 216.34 MB
- **Size of the generated dataset:** 73.39 MB
- **Total amount of disk used:** 289.74 MB

An example of 'validation_matched' looks as follows.
```
{
    "hypothesis": "flammable",
    "label": 0,
    "premise": "inflammable"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### plain_text
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).

### [Data Splits Sample Size](#data-splits-sample-size)

|   name   |train |validation_matched|validation_mismatched|
|----------|-----:|-----------------:|--------------------:|
|plain_text|392702|              9815|                 9832|

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
@InProceedings{N18-1101,
  author = "Williams, Adina
            and Nangia, Nikita
            and Bowman, Samuel",
  title = "A Broad-Coverage Challenge Corpus for
           Sentence Understanding through Inference",
  booktitle = "Proceedings of the 2018 Conference of
               the North American Chapter of the
               Association for Computational Linguistics:
               Human Language Technologies, Volume 1 (Long
               Papers)",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  pages = "1112--1122",
  location = "New Orleans, Louisiana",
  url = "http://aclweb.org/anthology/N18-1101"
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.