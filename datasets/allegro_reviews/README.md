---
annotations_creators:
- found
language_creators:
- found
languages:
- pl
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-scoring
task_ids:
- sentiment-scoring
---

# Dataset Card for [Dataset Name]

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:**
https://klejbenchmark.com/
- **Repository:**
https://github.com/allegro/klejbenchmark-allegroreviews
- **Paper:**
KLEJ: Comprehensive Benchmark for Polish Language Understanding (Rybak, Piotr and Mroczkowski, Robert and Tracz, Janusz and Gawlik, Ireneusz)
- **Leaderboard:**
https://klejbenchmark.com/leaderboard/
- **Point of Contact:**
klejbenchmark@allegro.pl

### Dataset Summary

Allegro Reviews is a sentiment analysis dataset, consisting of 11,588 product reviews written in Polish and extracted from Allegro.pl - a popular e-commerce marketplace. Each review contains at least 50 words and has a rating on a scale from one (negative review) to five (positive review).

We recommend using the provided train/dev/test split. The ratings for the test set reviews are kept hidden. You can evaluate your model using the online evaluation tool available on klejbenchmark.com.

### Supported Tasks and Leaderboards

Product reviews sentiment analysis.
https://klejbenchmark.com/leaderboard/

### Languages

Polish

## Dataset Structure

### Data Instances

Two tsv files (train, dev) with two columns (text, rating) and one (test) with just one (text). 

### Data Fields

- text: a product review of at least 50 words
- rating: product rating of a scale of one (negative review) to five (positive review)

### Data Splits

Data is splitted in train/dev/test split.

## Dataset Creation

### Curation Rationale

This dataset is one of nine evaluation tasks to improve polish language processing.

### Source Data

#### Initial Data Collection and Normalization

The Allegro Reviews is a set of product reviews from a popular e-commerce marketplace (Allegro.pl).

#### Who are the source language producers?

Customers of an e-commerce marketplace.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Allegro Machine Learning Research team klejbenchmark@allegro.pl

### Licensing Information

Dataset licensed under CC BY-SA 4.0

### Citation Information

@inproceedings{rybak-etal-2020-klej,
    title = "{KLEJ}: Comprehensive Benchmark for Polish Language Understanding",
    author = "Rybak, Piotr and Mroczkowski, Robert and Tracz, Janusz and Gawlik, Ireneusz",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.111",
    pages = "1191--1201",
}
