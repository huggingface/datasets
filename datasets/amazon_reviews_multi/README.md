---
annotations_creators:
- found
language_creators:
- found
languages:
  all_languages:
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
licenses: []
multilinguality:
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

The dataset contains reviews in English, Japanese, German, French, Chinese and Spanish

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

Each language configuration comes with it's own `train`, `validation`, and `test` splits. Each `all_languages` split
is simply a concatenation of the corresponding split across all languages.

## Additional Information

### Dataset Curators

Published by Phillip Keung, Yichao Lu, György Szarvas, and Noah A. Smith. Managed by Amazon.

### Licensing Information

By accessing the Multilingual Amazon Reviews Corpus (“Reviews Corpus”), you agree that the Reviews Corpus is an Amazon Service subject to the Amazon.com Conditions of Use and you agree to be bound by them, with the following additional conditions:

In addition to the license rights granted under the Conditions of Use, Amazon or its content providers grant you a limited, non-exclusive, non-transferable, non-sublicensable, revocable license to access and use the Reviews Corpus for purposes of academic research. You may not resell, republish, or make any commercial use of the Reviews Corpus or its contents, including use of the Reviews Corpus for commercial research, such as research related to a funding or consultancy contract, internship, or other relationship in which the results are provided for a fee or delivered to a for-profit organization. You may not (a) link or associate content in the Reviews Corpus with any personal information (including Amazon customer accounts), or (b) attempt to determine the identity of the author of any content in the Reviews Corpus. If you violate any of the foregoing conditions, your license to access and use the Reviews Corpus will automatically terminate without prejudice to any of the other rights or remedies Amazon may have.

This license language is also available at https://docs.opendata.aws/amazon-reviews-ml/license.txt

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
