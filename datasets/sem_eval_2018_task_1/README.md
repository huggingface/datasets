---
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- en
- ar
- es
license:
- unknown
multilinguality:
- multilingual
pretty_name: 'SemEval-2018 Task 1: Affect in Tweets'
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
- text-classification-other-emotion-classification
---

# Dataset Card for SemEval-2018 Task 1: Affect in Tweets

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** https://competitions.codalab.org/competitions/17751
- **Repository:**
- **Paper:** http://saifmohammad.com/WebDocs/semeval2018-task1.pdf
- **Leaderboard:**
- **Point of Contact:** https://www.saifmohammad.com/

### Dataset Summary

Tasks: We present an array of tasks where systems have to automatically determine the intensity of emotions (E) and intensity of sentiment (aka valence V) of the tweeters from their tweets. (The term tweeter refers to the person who has posted the tweet.) We also include a multi-label emotion classification task for tweets. For each task, we provide separate training and test datasets for English, Arabic, and Spanish tweets. The individual tasks are described below:

1. EI-reg (an emotion intensity regression task): Given a tweet and an emotion E, determine the  intensity of E that best represents the mental state of the tweeter—a real-valued score between 0 (least E) and 1 (most E).
Separate datasets are provided for anger, fear, joy, and sadness.

2. EI-oc (an emotion intensity ordinal classification task): Given a tweet and an emotion E, classify the tweet into one of four ordinal classes of intensity of E that best represents the mental state of the tweeter.
Separate datasets are provided for anger, fear, joy, and sadness.

3. V-reg (a sentiment intensity regression task): Given a tweet, determine the intensity of sentiment or valence (V) that best represents the mental state of the tweeter—a real-valued score between 0 (most negative) and 1 (most positive).

4. V-oc (a sentiment analysis, ordinal classification, task): Given a tweet, classify it into one of seven ordinal classes, corresponding to various levels of positive and negative sentiment intensity, that best represents the mental state of the tweeter.

5. E-c (an emotion classification task): Given a tweet, classify it as 'neutral or no emotion' or as one, or more, of eleven given emotions that best represent the mental state of the tweeter.
Here, E refers to emotion, EI refers to emotion intensity, V refers to valence or sentiment intensity, reg refers to regression, oc refers to ordinal classification, c refers to classification. 

Together, these tasks encompass various emotion and sentiment analysis tasks. You are free to participate in any number of tasks and on any of the datasets.

**Currently only the subtask 5 (E-c) is available on the Hugging Face Dataset Hub.**

### Supported Tasks and Leaderboards

### Languages

English, Arabic and Spanish

## Dataset Structure

### Data Instances

An example from the `subtask5.english` config is:

```
{'ID': '2017-En-21441',
 'Tweet': "“Worry is a down payment on a problem you may never have'. \xa0Joyce Meyer.  #motivation #leadership #worry",
 'anger': False,
 'anticipation': True,
 'disgust': False,
 'fear': False,
 'joy': False,
 'love': False,
 'optimism': True,
 'pessimism': False,
 'sadness': False,
 'surprise': False,
 'trust': True}
 ```

### Data Fields

For any config of the subtask 5:
- ID: string id of the tweet
- Tweet: text content of the tweet as a string
- anger: boolean, True if anger represents the mental state of the tweeter
- anticipation: boolean, True if anticipation represents the mental state of the tweeter
- disgust: boolean, True if disgust represents the mental state of the tweeter
- fear: boolean, True if fear represents the mental state of the tweeter
- joy: boolean, True if joy represents the mental state of the tweeter
- love: boolean, True if love represents the mental state of the tweeter
- optimism: boolean, True if optimism represents the mental state of the tweeter
- pessimism: boolean, True if pessimism represents the mental state of the tweeter
- sadness: boolean, True if sadness represents the mental state of the tweeter
- surprise: boolean, True if surprise represents the mental state of the tweeter
- trust: boolean, True if trust represents the mental state of the tweeter

Note that the test set has no labels, and therefore all labels are set to False.

### Data Splits

|         | train | validation |  test |
|---------|------:|-----------:|------:|
| English | 6,838 |        886 | 3,259 |
| Arabic  | 2,278 |        585 | 1,518 |
| Spanish | 3,561 |        679 | 2,854 |

## Dataset Creation

### Curation Rationale

### Source Data

Tweets

#### Initial Data Collection and Normalization

#### Who are the source language producers?

Twitter users.

### Annotations

#### Annotation process

We presented one tweet at a time to the annotators
and asked which of the following options best de-
scribed the emotional state of the tweeter:
– anger (also includes annoyance, rage)
– anticipation (also includes interest, vigilance)
– disgust (also includes disinterest, dislike, loathing)
– fear (also includes apprehension, anxiety, terror)
– joy (also includes serenity, ecstasy)
– love (also includes affection)
– optimism (also includes hopefulness, confidence)
– pessimism (also includes cynicism, no confidence)
– sadness (also includes pensiveness, grief)
– surprise (also includes distraction, amazement)
– trust (also includes acceptance, liking, admiration)
– neutral or no emotion
Example tweets were provided in advance with ex-
amples of suitable responses.
On the Figure Eight task settings, we specified
that we needed annotations from seven people for
each tweet. However, because of the way the gold
tweets were set up, they were annotated by more
than seven people. The median number of anno-
tations was still seven. In total, 303 people anno-
tated between 10 and 4,670 tweets each. A total of
174,356 responses were obtained.

Mohammad, S., Bravo-Marquez, F., Salameh, M., & Kiritchenko, S. (2018). SemEval-2018 task 1: Affect in tweets. Proceedings of the 12th International Workshop on Semantic Evaluation, 1–17. https://doi.org/10.18653/v1/S18-1001

#### Who are the annotators?

Crowdworkers on Figure Eight.

### Personal and Sensitive Information

## Considerations for Using the Data

### Social Impact of Dataset

### Discussion of Biases

### Other Known Limitations

## Additional Information

### Dataset Curators

Saif M. Mohammad, Felipe Bravo-Marquez, Mohammad Salameh and Svetlana Kiritchenko

### Licensing Information

See the official [Terms and Conditions](https://competitions.codalab.org/competitions/17751#learn_the_details-terms_and_conditions)

### Citation Information

@InProceedings{SemEval2018Task1,
 author = {Mohammad, Saif M. and Bravo-Marquez, Felipe and Salameh, Mohammad and Kiritchenko, Svetlana},
 title = {SemEval-2018 {T}ask 1: {A}ffect in Tweets},
 booktitle = {Proceedings of International Workshop on Semantic Evaluation (SemEval-2018)},
 address = {New Orleans, LA, USA},
 year = {2018}} 

### Contributions

Thanks to [@maxpel](https://github.com/maxpel) for adding this dataset.
