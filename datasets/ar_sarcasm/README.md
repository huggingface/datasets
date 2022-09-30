---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- ar
license:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-semeval_2017
- extended|other-astd
task_categories:
- text-classification
task_ids:
- sentiment-classification
- text-classification-other-sarcasm-detection
paperswithcode_id: null
pretty_name: ArSarcasm
---

# Dataset Card for ArSarcasm

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

- **Repository:** [GitHub](https://github.com/iabufarha/ArSarcasm)
- **Paper:** https://www.aclweb.org/anthology/2020.osact-1.5/

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

You can get more information about an Arabic sarcasm tasks and leaderboard
[here](https://sites.google.com/view/ar-sarcasm-sentiment-detection/).

### Languages

Arabic (multiple dialects)

## Dataset Structure

### Data Instances

```javascript
{'dialect': 1, 'original_sentiment': 0, 'sarcasm': 0, 'sentiment': 0, 'source': 'semeval', 'tweet': 'نصيحه ما عمرك اتنزل لعبة سوبر ماريو مش زي ما كنّا متوقعين الله يرحم ايامات السيقا والفاميلي #SuperMarioRun'}
```

### Data Fields

- tweet: the original tweet text
- sarcasm: 0 for non-sarcastic, 1 for sarcastic
- sentiment: 0 for negative, 1 for neutral, 2 for positive
- original_sentiment: 0 for negative, 1 for neutral, 2 for positive
- source: the original source of tweet: SemEval or ASTD
- dialect: 0 for Egypt, 1 for Gulf, 2 for Levant, 3 for Magreb, 4 for Modern Standard Arabic (MSA)

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

```
@inproceedings{abu-farha-magdy-2020-arabic,
    title = "From {A}rabic Sentiment Analysis to Sarcasm Detection: The {A}r{S}arcasm Dataset",
    author = "Abu Farha, Ibrahim  and Magdy, Walid",
    booktitle = "Proceedings of the 4th Workshop on Open-Source Arabic Corpora and Processing Tools, with a Shared Task on Offensive Language Detection",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resource Association",
    url = "https://www.aclweb.org/anthology/2020.osact-1.5",
    pages = "32--39",
    language = "English",
    ISBN = "979-10-95546-51-1",
}
```

### Contributions

Thanks to [@mapmeld](https://github.com/mapmeld) for adding this dataset.
