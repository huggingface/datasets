---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- de
licenses:
- cc-by-nc-sa-4.0
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
---

# Dataset Card for One Million Posts Corpus

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://ofai.github.io/million-post-corpus/
- **Repository:** https://github.com/OFAI/million-post-corpus
- **Paper:** https://dl.acm.org/doi/10.1145/3077136.3080711
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The “One Million Posts” corpus is an annotated data set consisting of user comments posted to an Austrian newspaper website (in German language).

DER STANDARD is an Austrian daily broadsheet newspaper. On the newspaper’s website, there is a discussion section below each news article where readers engage in online discussions. The data set contains a selection of user posts from the 12 month time span from 2015-06-01 to 2016-05-31. There are 11,773 labeled and 1,000,000 unlabeled posts in the data set. The labeled posts were annotated by professional forum moderators employed by the newspaper.

The data set contains the following data for each post:

* Post ID
* Article ID
* Headline (max. 250 characters)
* Main Body (max. 750 characters)
* User ID (the user names used by the website have been re-mapped to new numeric IDs)
* Time stamp
* Parent post (replies give rise to tree-like discussion thread structures)
* Status (online or deleted by a moderator)
* Number of positive votes by other community members
* Number of negative votes by other community members

For each article, the data set contains the following data:

* Article ID
* Publishing date
* Topic Path (e.g.: Newsroom / Sports / Motorsports / Formula 1)
* Title
* Body

Detailed descriptions of the post selection and annotation procedures are given in the paper.

#### Annotated Categories

Potentially undesirable content:

* Sentiment (negative/neutral/positive)
    An important goal is to detect changes in the prevalent sentiment in a discussion, e.g., the location within the fora and the point in time where a turn from positive/neutral sentiment to negative sentiment takes place.
* Off-Topic (yes/no)
    Posts which digress too far from the topic of the corresponding article.
* Inappropriate (yes/no)
    Swearwords, suggestive and obscene language, insults, threats etc.
* Discriminating (yes/no)
    Racist, sexist, misogynistic, homophobic, antisemitic and other misanthropic content.

Neutral content that requires a reaction:

* Feedback (yes/no)
    Sometimes users ask questions or give feedback to the author of the article or the newspaper in general, which may require a reply/reaction.

Potentially desirable content:

* Personal Stories (yes/no)
    In certain fora, users are encouraged to share their personal stories, experiences, anecdotes etc. regarding the respective topic.
* Arguments Used (yes/no)
    It is desirable for users to back their statements with rational argumentation, reasoning and sources.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Austrian German

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

The data set contains the following data for each post:

* **ID_Post**: Post ID
* **ID_Parent_Post**: Parent post (replies give rise to tree-like discussion thread structures)
* **ID_Article**: Article ID
* **ID_User**: User ID (the user names used by the website have been re-mapped to new numeric IDs)
* **Headline**: Headline (max. 250 characters)
* **Body**: Main Body (max. 750 characters)
* **CreatedAt**: Time stamp
* **Status**: Status (online or deleted by a moderator)
* **PositiveVotes**: Number of positive votes by other community members
* **NegativeVotes**: Number of negative votes by other community members

Labeled posts also contain:

* **Category**: The category of the annotation, one of: ArgumentsUsed, Discriminating, Inappropriate, OffTopic, PersonalStories, PossiblyFeedback, SentimentNegative, SentimentNeutral, SentimentPositive
* **Value**: either 0 or 1, explicitly indicating whether or not the post has the specified category as a label (i.e. a category of `ArgumentsUsed` with value of `0` means that an annotator explicitly labeled that this post doesn't use arguments, as opposed to the mere absence of a positive label).
* **Fold**: a number between [0-9] from a 10-fold split by the authors

For each article, the data set contains the following data:

* **ID_Article**: Article ID
* **publishingDate**: Publishing date
* **Path**: Topic Path (e.g.: Newsroom / Sports / Motorsports / Formula 1)
* **Title**: Title
* **Body**: Body

### Data Splits

[More Information Needed]

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

This data set is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

### Citation Information

```
@InProceedings{Schabus2018,
  author    = {Dietmar Schabus and Marcin Skowron},
  title     = {Academic-Industrial Perspective on the Development and Deployment of a Moderation System for a Newspaper Website},
  booktitle = {Proceedings of the 11th International Conference on Language Resources and Evaluation (LREC)},
  year      = {2018},
  address   = {Miyazaki, Japan},
  month     = may,
  pages     = {1602-1605},
  abstract  = {This paper describes an approach and our experiences from the development, deployment and usability testing of a Natural Language Processing (NLP) and Information Retrieval system that supports the moderation of user comments on a large newspaper website. We highlight some of the differences between industry-oriented and academic research settings and their influence on the decisions made in the data collection and annotation processes, selection of document representation and machine learning methods. We report on classification results, where the problems to solve and the data to work with come from a commercial enterprise. In this context typical for NLP research, we discuss relevant industrial aspects. We believe that the challenges faced as well as the solutions proposed for addressing them can provide insights to others working in a similar setting.},
  url       = {http://www.lrec-conf.org/proceedings/lrec2018/summaries/8885.html},
}
```

### Contributions

Thanks to [@aseifert](https://github.com/aseifert) for adding this dataset.