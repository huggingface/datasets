---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- ja
licenses:
- cc-by-nd-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- fact-checking
paperswithcode_id: null
---

# Dataset Card for COVID-19 日本語Twitterデータセット (COVID-19 Japanese Twitter Dataset)

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

- **Homepage:** [COVID-19 日本語Twitterデータセット homepage](http://www.db.info.gifu-u.ac.jp/data/Data_5f02db873363f976fce930d1)
- **Repository:** [N/A]
- **Paper:** [N/A]
- **Leaderboard:** [N/A]
- **Point of Contact:** Check the homepage.

### Dataset Summary

53,640 Japanese tweets with annotation if a tweet is related to COVID-19 or not. The annotation is by majority decision by 5 - 10 crowd workers. Target tweets include "COVID" or "コロナ". The period of the tweets is from around January 2020 to around June 2020. The original tweets are not contained. Please use Twitter API to get them, for example.

### Supported Tasks and Leaderboards

Text-classification, Whether the tweet is related to COVID-19, and whether it is fact or opinion.

### Languages

The text can be gotten using the IDs in this dataset is Japanese, posted on Twitter.

## Dataset Structure

### Data Instances

CSV file with the 1st column is Twitter ID and the 2nd column is assessment option ID.

### Data Fields

- `tweet_id`: Twitter ID.
- `assessment_option_id`: The selection result. It has the following meanings:
  - 63: a general fact: generally published information, such as news.
  - 64: a personal fact: personal news. For example, a person heard that the next-door neighbor, XX, has infected COVID-19, which has not been in a news.
  - 65: an opinion/feeling
  - 66: difficult to determine if they are related to COVID-19 (it is definitely the tweet is not "67: unrelated", but 63, 64, 65 cannot be determined)
  - 67: unrelated
  - 68: it is a fact, but difficult to determine whether general facts, personal facts, or impressions (it may be irrelevant to COVID-19 since it is indistinguishable between 63 - 65 and 67).

### Data Splits

No articles have been published for this dataset, and it appears that the author of the dataset is willing to publish an article (it is not certain that the splitting information will be included). Therefore, at this time, information on data splits is not provided.

## Dataset Creation

### Curation Rationale

[More Information Needed] because the paper is not yet published.

### Source Data

#### Initial Data Collection and Normalization

53,640 Japanese tweets with annotation if a tweet is related to COVID-19 or not. Target tweets include "COVID" or "コロナ". The period of the tweets is from around January 2020 to around June 2020.

#### Who are the source language producers?

The language producers are users of Twitter.

### Annotations

#### Annotation process

The annotation is by majority decision by 5 - 10 crowd workers.

#### Who are the annotators?

Crowd workers.

### Personal and Sensitive Information

The author does not contain original tweets.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The dataset is hosted by Suzuki Laboratory, Gifu University, Japan.

### Licensing Information

CC-BY-ND 4.0

### Citation Information

A related paper has not yet published.
The author shows how to cite as「鈴木 優: COVID-19 日本語 Twitter データセット （ http://www.db.info.gifu-u.ac.jp/data/Data_5f02db873363f976fce930d1 ） 」.

### Contributions

Thanks to [@forest1988](https://github.com/forest1988) for adding this dataset.