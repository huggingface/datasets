---
annotations_creators:
- found
language_creators:
- found
languages:
  all_languages:
  - de
  - en
  - es
  - fr
  - ja
  - zh
  de:
  - de
  en:
  - en
  es:
  - es
  fr:
  - fr
  ja:
  - ja
  zh:
  - zh
licenses: 
  - other-amazon-license
multilinguality:
  all_languages:
  - multilingual
  de:
  - monolingual
  en:
  - monolingual
  es:
  - monolingual
  fr:
  - monolingual
  ja:
  - monolingual
  zh:
  - monolingual
size_categories:
  all_languages:
  - n>1M
  de:
  - 100K<n<1M
  en:
  - 100K<n<1M
  es:
  - 100K<n<1M
  fr:
  - 100K<n<1M
  ja:
  - 100K<n<1M
  zh:
  - 100K<n<1M
source_datasets:
- original
task_categories:
- conditional-text-generation
- sequence-modeling
- text-classification
- text-scoring
task_ids:
- language-modeling
- sentiment-classification
- sentiment-scoring
- summarization
- topic-classification
---

# Dataset Card for The Multilingual Amazon Reviews Corpus

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

- **Webpage:** https://registry.opendata.aws/amazon-reviews-ml/
- **Paper:** https://arxiv.org/abs/2010.02573
- **Point of Contact:** multilingual-reviews-dataset@amazon.com

### Dataset Summary

We provide an Amazon product reviews dataset for multilingual text classification. The dataset contains reviews in English, Japanese, German, French, Chinese and Spanish, collected between November 1, 2015 and November 1, 2019. Each record in the dataset contains the review text, the review title, the star rating, an anonymized reviewer ID, an anonymized product ID and the coarse-grained product category (e.g. ‘books’, ‘appliances’, etc.) The corpus is balanced across stars, so each star rating constitutes 20% of the reviews in each language.

For each language, there are 200,000, 5,000 and 5,000 reviews in the training, development and test sets respectively. The maximum number of reviews per reviewer is 20 and the maximum number of reviews per product is 20. All reviews are truncated after 2,000 characters, and all reviews are at least 20 characters long.

Note that the language of a review does not necessarily match the language of its marketplace (e.g. reviews from amazon.de are primarily written in German, but could also be written in English, etc.). For this reason, we applied a language detection algorithm based on the work in Bojanowski et al. (2017) to determine the language of the review text and we removed reviews that were not written in the expected language.

### Languages

The dataset contains reviews in English, Japanese, German, French, Chinese and Spanish.

## Dataset Structure

### Data Instances

Each data instance corresponds to a review. The original JSON for an instance looks like so (German example):

```json
{
    "review_id":"de_0784695",
    "product_id":"product_de_0572654",
    "reviewer_id":"reviewer_de_0645436",
    "stars":"1",
    "review_body":"Leider, leider nach einmal waschen ausgeblichen . Es sieht super h\u00fcbsch aus , nur leider stinkt es ganz schrecklich und ein Waschgang in der Maschine ist notwendig ! Nach einem mal waschen sah es aus als w\u00e4re es 10 Jahre alt und hatte 1000 e von Waschg\u00e4ngen hinter sich :( echt schade !",
    "review_title":"Leider nicht zu empfehlen",
    "language":"de",
    "product_category":"home"
}
```

### Data Fields

- `review_id`: A string identifier of the review.
- `product_id`: A string identifier of the product being reviewed.
- `reviewer_id`: A string identifier of the reviewer.
- `stars`: An int between 1-5 indicating the number of stars.
- `review_body`: The text body of the review.
- `review_title`: The text title of the review.
- `language`: The string identifier of the review language.
- `product_category`: String representation of the product's category.

### Data Splits

Each language configuration comes with it's own `train`, `validation`, and `test` splits. The `all_languages` split
is simply a concatenation of the corresponding split across all languages. That is, the `train` split for
`all_languages` is a concatenation of the `train` splits for each of the languages and likewise for `validation` and
`test`.

## Dataset Creation

### Curation Rationale

The dataset is motivated by the desire to advance sentiment analysis and text classification in other (non-English)
languages.

### Source Data

#### Initial Data Collection and Normalization

The authors gathered the reviews from the marketplaces in the US, Japan, Germany, France, Spain, and China for the
English, Japanese, German, French, Spanish, and Chinese languages, respectively. They then ensured the correct
language by applying a language detection algorithm, only retaining those of the target language. In a random sample
of the resulting reviews, the authors observed a small percentage of target languages that were incorrectly filtered
out and a very few mismatched languages that were incorrectly retained.

#### Who are the source language producers?

The original text comes from Amazon customers reviewing products on the marketplace across a variety of product
categories.

### Annotations

#### Annotation process

Each of the fields included are submitted by the user with the review or otherwise associated with the review. No
manual or machine-driven annotation was necessary.

#### Who are the annotators?

N/A

### Personal and Sensitive Information

Amazon Reviews are submitted by users with the knowledge and attention of being public. The reviewer ID's included in
this dataset are quasi-anonymized, meaning that they are disassociated from the original user profiles. However,
these fields would likely be easy to deannoymize given the public and identifying nature of free-form text responses.

## Considerations for Using the Data

### Social Impact of Dataset

This dataset is part of an effort to encourage text classification research in languages other than English. Such
work increases the accessibility of natural language technology to more regions and cultures. Unfortunately, each of
the languages included here is relatively high resource and well studied.

### Discussion of Biases

The data included here are from unverified consumers. Some percentage of these reviews may be fake or contain
misleading or offensive language. 
### Other Known Limitations

The dataset is constructed so that the distribution of star ratings is balanced. This feature has some advantages for
purposes of classification, but some types of language may be over or underrepresented relative to the original
distribution of reviews to acheive this balance.

[More Information Needed]

## Additional Information

### Dataset Curators

Published by Phillip Keung, Yichao Lu, György Szarvas, and Noah A. Smith. Managed by Amazon.

### Licensing Information

Amazon has licensed this dataset under its own agreement, to be found at the dataset webpage here:
https://docs.opendata.aws/amazon-reviews-ml/license.txt

### Citation Information

Please cite the following paper (arXiv) if you found this dataset useful:

Phillip Keung, Yichao Lu, György Szarvas and Noah A. Smith. “The Multilingual Amazon Reviews Corpus.” In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, 2020.

```
@inproceedings{marc_reviews,
    title={The Multilingual Amazon Reviews Corpus},
    author={Keung, Phillip and Lu, Yichao and Szarvas, György and Smith, Noah A.},
    booktitle={Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing},
    year={2020}
}
```
