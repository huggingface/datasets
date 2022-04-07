---
pretty_name: DBRD
annotations_creators:
- found
language_creators:
- found
languages:
- nl
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- sequence-modeling
- text-classification
task_ids:
- language-modeling
- sentiment-classification
paperswithcode_id: dbrd
---

# Dataset Card Creation Guide

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

- **Homepage:** [Dutch Book Review Dataset (DBRD) homepage](https://benjaminvdb.github.io/DBRD)
- **Repository:** https://github.com/benjaminvdb/DBRD
- **Paper:** [The merits of Universal Language Model Fine-tuning for Small Datasets - a case with Dutch book reviews](https://arxiv.org/abs/1910.00896)
- **Leaderboard:** 
- **Point of Contact:** [Benjamin van der Burgh](mailto:benjaminvdb@gmail.com)

### Dataset Summary

The DBRD (pronounced *dee-bird*) dataset contains over 110k book reviews of which 22k have associated binary sentiment polarity labels. It is intended as a benchmark for sentiment classification in Dutch and was created due to a lack of annotated datasets in Dutch that are suitable for this task.

### Supported Tasks and Leaderboards

- `sequence-modeling`: The dataset can be used to train a model for sequence modeling, more specifically language modeling.
- `text-classification`: The dataset can be used to train a model for text classification, more specifically sentiment classification, using the provided positive/negative sentiment polarity labels.

### Languages

Non-Dutch reviews were filtered out using [langdetect](https://github.com/Mimino666/langdetect), and all reviews should therefore be in Dutch (nl). They are written by reviewers on [Hebban](https://www.hebban.nl), a Dutch website for book reviews.

## Dataset Structure

### Data Instances

The dataset contains three subsets: train, test, and unsupervised. The `train` and `test` sets contain labels, while the `unsupervised` set doesn't (the label value is -1 for each instance in `unsupervised`). Here's an example of a positive review, indicated with a label value of `1`. 

```
{
  'label': 1,
  'text': 'Super om te lezen hoe haar leven is vergaan.\nBijzonder dat ze zo openhartig is geweest.'
}
```

### Data Fields

- `label`: either 0 (negative) or 1 (positive) in the supervised sets `train` and `test`. These are always -1 for the unsupervised set.
- `text`: book review as a utf-8 encoded string. 

### Data Splits

The `train` and `test` sets were constructed by extracting all non-neutral reviews because we want to assign either a positive or negative polarity label to each instance. Furthermore, the positive (pos) and negative (neg) labels were balanced in both train and test sets. The remainder was added to the unsupervised set.

|                            | Train  | Test  | Unsupervised |
| -----                      | ------ | ----- | -----------  |
| # No. texts                | 20028  | 2224  | 96264        |
| % of total                 | 16.9%  | 1.9%  | 81.2%        |

## Dataset Creation

### Curation Rationale

This dataset was created due to a lack of annotated Dutch text that is suitable for sentiment classification. Non-Dutch texts were therefore removed, but other than that, no curation was done.

### Source Data

The book reviews were taken from [Hebban](https://www.hebban.nl), a Dutch platform for book reviews.

#### Initial Data Collection and Normalization

The source code of the scraper and preprocessing process can be found in the [DBRD GitHub repository](https://github.com/benjaminvdb/DBRD).

#### Who are the source language producers?

The reviews are written by users of [Hebban](https://www.hebban.nl) and are of varying quality. Some are short, others long, and many contain spelling mistakes and other errors. 

### Annotations

Each book review was accompanied by a 1 to 5-star rating. The annotations are produced by mapping the user-provided ratings to either a positive or negative label. 1 and 2-star ratings are given the negative label `0` and 4 and 5-star ratings the positive label `1`. Reviews with a rating of 3 stars are considered neutral and left out of the `train`/`test` sets and added to the unsupervised set.

#### Annotation process

Users of [Hebban](https://www.hebban.nl) were unaware that their reviews would be used in the creation of this dataset.

#### Who are the annotators?

The annotators are the [Hebban](https://www.hebban.nl) users who wrote the book reviews associated with the annotation. Anyone can register on [Hebban](https://www.hebban.nl) and it's impossible to know the demographics of this group. 

### Personal and Sensitive Information

The book reviews and ratings are publicly available on [Hebban](https://www.hebban.nl) and no personal or otherwise sensitive information is contained in this dataset.

## Considerations for Using the Data

### Social Impact of Dataset

While predicting sentiment of book reviews in itself is not that interesting, the value of this dataset lies in its usage for benchmarking models. The dataset contains some challenges that are common to outings on the internet, such as spelling mistakes and other errors. It is therefore very useful for validating models for their real-world performance. These datasets are abundant for English but are harder to find for Dutch, making them a valuable resource for ML tasks in this language.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Reviews on [Hebban](https://www.hebban.nl) are usually written in Dutch, but some have been written in English and possibly in other languages. While we've done our best to filter out non-Dutch texts, it's hard to do this without errors. For example, some reviews are in multiple languages, and these might slip through. Also be aware that some commercial outings can appear in the text, making them different from other reviews and influencing your models. While this doesn't pose a major issue in most cases, we just wanted to mention it briefly.

## Additional Information

### Dataset Curators

This dataset was created by [Benjamin van der Burgh](mailto:benjaminvdb@gmail.com), who was working at [Leiden Institute of Advanced Computer Science (LIACS)](https://liacs.leidenuniv.nl/) at the time.

### Licensing Information

The dataset is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### Citation Information

Please use the following citation when making use of this dataset in your work.

```
@article{DBLP:journals/corr/abs-1910-00896,
  author    = {Benjamin van der Burgh and
               Suzan Verberne},
  title     = {The merits of Universal Language Model Fine-tuning for Small Datasets
               - a case with Dutch book reviews},
  journal   = {CoRR},
  volume    = {abs/1910.00896},
  year      = {2019},
  url       = {http://arxiv.org/abs/1910.00896},
  archivePrefix = {arXiv},
  eprint    = {1910.00896},
  timestamp = {Fri, 04 Oct 2019 12:28:06 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1910-00896.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

### Contributions

Thanks to [@benjaminvdb](https://github.com/benjaminvdb) for adding this dataset.