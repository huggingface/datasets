---
annotations_creators:
- no-annotation
language_creators:
- Ibrahim Abu Farha
languages:
- ar
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
- text-classification-other-sarcasm-detection
---

# Dataset Card for ArSarcasm

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
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

## Dataset Description

### Dataset Summary

ArSarcasm is a new Arabic sarcasm detection dataset.
The dataset was created using previously available Arabic sentiment analysis
datasets ([SemEval 2017](https://www.aclweb.org/anthology/S17-2088.pdf)
and [ASTD](https://www.aclweb.org/anthology/D15-1299.pdf)) and adds sarcasm and
dialect labels to them.

The dataset contains 10,547 tweets, 1,682 (16%) of which are sarcastic.

For more details, please check the paper
[From Arabic Sentiment Analysis to Sarcasm Detection: The ArSarcasm Dataset](https://www.aclweb.org/anthology/2020.osact-1.5/)

### Supported Tasks and Leaderboards

https://sites.google.com/view/ar-sarcasm-sentiment-detection/

### Languages

Arabic (multiple dialects)

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- tweet: the original tweet text surrounded by quotes (").
- sarcasm: boolean the indicates whether a tweet is sarcastic or not.
- sentiment: the sentiment from the new annotation (positive, negative, neutral).
- original_sentiment: the sentiment in the original annotations (positive, negative, neutral).
- source: the original source of tweet SemEval or ASTD.
- dialect: the dialect used in the tweet, we used the 5 main regions in the Arab world

### Data Splits

The training set contains 8,437 tweets, while the test set contains 2,110 tweets.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The dataset was created using previously available Arabic sentiment analysis datasets (SemEval 2017 and ASTD) and adds sarcasm and dialect labels to them.

#### Who are the source language producers?

SemEval 2017 and ASTD

### Annotations

#### Annotation process

For the annotation process, we used Figure-Eight
crowdsourcing platform. Our main objective was to annotate the
data for sarcasm detection, but due to the challenges imposed by dialectal variations, we decided to add the annotation for dialects. We also include a new annotation for
sentiment labels in order to have a glimpse of the variability and subjectivity between different annotators. Thus, the
annotators were asked to provide three labels for each tweet
as the following:

- Sarcasm: sarcastic or non-sarcastic.
- Sentiment: positive, negative or neutral.
- Dialect: Egyptian, Gulf, Levantine, Maghrebi or Modern Standard Arabic (MSA).

#### Who are the annotators?

Figure-Eight crowdsourcing platform

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

- Ibrahim Abu-Farha
- Walid Magdy

### Licensing Information

MIT

### Citation Information

See https://www.aclweb.org/anthology/2020.osact-1.5/
