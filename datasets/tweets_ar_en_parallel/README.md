---
annotations_creators:
- expert-generated
- no-annotation
language_creators:
- found
languages:
- ar
- en
licenses:
- apache-2.0
multilinguality:
- translation
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-machine-translation
paperswithcode_id: bilingual-corpus-of-arabic-english-parallel
pretty_name: Bilingual Corpus of Arabic-English Parallel Tweets
---

# Dataset Card for Bilingual Corpus of Arabic-English Parallel Tweets

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

- **Homepage:** [Bilingual Corpus of Arabic-English Parallel Tweets](https://alt.qcri.org/resources/bilingual_corpus_of_parallel_tweets)
- **Repository:**
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/2020.bucc-1.3/)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Twitter users often post parallel tweets—tweets that contain the same content but are written in different languages. Parallel tweets can be an important resource for developing machine translation (MT) systems among other natural language processing (NLP) tasks. This resource is a result of a generic method for collecting parallel tweets. Using the method, we compiled a bilingual corpus of English-Arabic parallel tweets and a list of Twitter accounts who post English-Arabic tweets regularly. Additionally, we annotate a subset of Twitter accounts with their countries of origin and topic of interest, which provides insights about the population who post parallel tweets.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

parallelTweets:
```
{
  "ArabicTweetID": 981111245209243600,
  "EnglishTweetID": 981111450432401400
}
```

accountList:
```
{
  'account': 'HukoomiQatar'
}
```

countryTopicAnnotation:
```
{
  'account': 'HukoomiQatar',
  'country': 'QA',
  'topic': 'Gov'
}
```

### Data Fields

parallelTweets:
- `ArabicTweetID` (int)
- `EnglishTweetID` (int)

accountList:
- `account` (str)

countryTopicAnnotation:
- `account` (str)
- `country` (class label): One of:
  - "QA",
  - "BH",
  - "AE",
  - "OM",
  - "SA",
  - "PL",
  - "JO",
  - "IQ",
  - "Other",
  - "EG",
  - "KW",
  - "SY"
- `topic` (class label): One of:
  - "Gov",
  - "Culture",
  - "Education",
  - "Sports",
  - "Travel",
  - "Events",
  - "Business",
  - "Science",
  - "Politics",
  - "Health",
  - "Governoment",
  - "Media",

### Data Splits

All configuration have only one split: "test".

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

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

[More Information Needed]

### Licensing Information

It is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

### Citation Information

```
@inproceedings{Mubarak2020bilingualtweets,
  title={Constructing a Bilingual Corpus of Parallel Tweets},
  author={Mubarak, Hamdy and Hassan, Sabit and Abdelali, Ahmed},
  booktitle={Proceedings of 13th Workshop on Building and Using Comparable Corpora (BUCC)},
  address={Marseille, France},
  year={2020}
}
```

[More Information Needed]

### Contributions

Thanks to [@sumanthd17](https://github.com/sumanthd17) for adding this dataset.