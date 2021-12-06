---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- gpl-3.0
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
paperswithcode_id: null
pretty_name: Tweets Hate Speech Detection
---

# Dataset Card for Tweets Hate Speech Detection

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

- **Homepage:** [Home](https://github.com/sharmaroshan/Twitter-Sentiment-Analysis)
- **Repository:** [Repo](https://github.com/sharmaroshan/Twitter-Sentiment-Analysis/blob/master/train_tweet.csv)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** [Darshan Gandhi](darshangandhi1151@gmail.com)

### Dataset Summary

The objective of this task is to detect hate speech in tweets. For the sake of simplicity, we say a tweet contains hate speech if it has a racist or sexist sentiment associated with it. So, the task is to classify racist or sexist tweets from other tweets.

Formally, given a training sample of tweets and labels, where label ‘1’ denotes the tweet is racist/sexist and label ‘0’ denotes the tweet is not racist/sexist, your objective is to predict the labels on the given test dataset.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages
The tweets are primarily in English Language.

## Dataset Structure

### Data Instances

The dataset contains a label denoting is the tweet a hate speech or not

```
{'label': 0,  # not a hate speech
 'tweet': ' @user when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run'}
```


### Data Fields

* label : 1 - it is a hate speech, 0 - not a hate speech.
* tweet: content of the tweet as a string.

### Data Splits
 
The data contains training data with :31962 entries

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Crowdsourced from tweets of users 

#### Who are the source language producers?

Cwodsourced from twitter

### Annotations

#### Annotation process

The data has been precprocessed and a model has been trained to assign the relevant label to the tweet 

#### Who are the annotators?

The data has been provided by Roshan Sharma 

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

With the help of this dataset, one can understand more about the human sentiments and also analye the situations when a particular person intends to make use of   hatred/racist comments 

### Discussion of Biases

The data could be cleaned up further for additional purposes such as applying a better feature extraction techniques


[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Roshan Sharma 

### Licensing Information

[Information](https://github.com/sharmaroshan/Twitter-Sentiment-Analysis/blob/master/LICENSE)

### Citation Information

[Citation](https://github.com/sharmaroshan/Twitter-Sentiment-Analysis/blob/master/CONTRIBUTING.md)

### Contributions

Thanks to [@darshan-gandhi](https://github.com/darshan-gandhi) for adding this dataset.