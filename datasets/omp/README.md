---
pretty_name: One Million Posts
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
paperswithcode_id: one-million-posts-corpus
---

# Dataset Card for One Million Posts Corpus

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

An example from the `posts_labeled` config:
```json
{
  "ID_Post": "79",
  "ID_Parent_Post": "",
  "ID_Article": "1",
  "ID_User": "12071",
  "CreatedAt": "2015-06-01 08:58:32.363",
  "Status": "online",
  "Headline": "",
  "Body": "ich kann keinen hinweis finden, wo man sich hinwenden muss, sollte man als abonnent des standard, die zeitung nicht bekommt, ist dass bewusst so arrangiert?",
  "PositiveVotes": 0,
  "NegativeVotes": 0,
  "Category": 5,
  "Value": 1,
  "Fold": 1
}
```

An example from the `posts_unlabeled` config:
```json
{
  "ID_Post": "51",
  "ID_Parent_Post": "",
  "ID_Article": "1",
  "ID_User": "11125",
  "CreatedAt": "2011-05-15 08:37:11.313",
  "Status": "online",
  "Headline": "Ich würde es sehr begrüßen, wenn",
  "Body": "Antworten erst beim Erscheinen als e-Mail dem Poster zugestellt würden.\r\n\r\nEs gibt User, die ihre Kommentare sofort nach Mail-Eingang irgendwo hinposten. Dadurch wird \r\n1. vor allem für andere Unser die Lesbarkeit wesentlich beeinträchtigt,\r\n2. kann das Post verdreht wiedergegeben werden,\r\n3. man ist immer wieder gezwungen die Antwort richtig zu stellen.\r\n\r\nPrivatfehden von Usern sollten, wenn schon zugelassen, für alle User nachvollziehbar sein.\r\n\r\nDanke!",
  "PositiveVotes": 1,
  "NegativeVotes": 0
}
```

An example from the `articles` config:
```json
{
  "ID_Article": "41",
  "Path": "Newsroom/Wirtschaft/Wirtschaftpolitik/Energiemarkt",
  "publishingDate": "2015-06-01 12:39:35.00",
  "Title": "Öl- und Gas-Riesen fordern weltweite CO2-Preise",
  "Body": '<div class="section" id="content-main" itemprop="articleBody"><div class="copytext"><h2 itemprop="description">Brief von BP, Total, Shell, Statoil, BG Group und Eni unterzeichnet</h2><p>Paris/London/La Defense - Sechs große Öl- und Gaskonzerne haben mit Blick auf die Verhandlungen über einen neuen Welt-Klimavertrag ein globales Preissystem für CO2-Emissionen gefordert. Wenn der Ausstoß von CO2 Geld kostet, sei dies ein Anreiz für die Nutzung von Erdgas statt Kohle, mehr Energieeffizienz und Investitionen zur Vermeidung des Treibhausgases, heißt es in einem am Montag veröffentlichten Brief.</p>\n<p>Das Schreiben ist unterzeichnet von BP, Total, Shell, Statoil, BG Group und Eni. Die Unternehmen versicherten, sie seien bereit, ihren Teil zum Kampf gegen den <a href="/r1937/Klimawandel">Klimawandel</a> beizutragen. Dafür sei aber ein klarer und verlässlicher Politik-Rahmen nötig. (APA, 1.6.2015)</p> </div></div>'
}
```

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

Training split only.

|      name       | train |
|-----------------|------:|
| posts_labeled   |  40567|
| posts_unlabeled |1000000|
| articles        |  12087|

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