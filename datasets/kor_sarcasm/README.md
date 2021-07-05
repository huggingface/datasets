---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- ko
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-sarcasm-detection
paperswithcode_id: null
---

# Dataset Card for Korean Sarcasm Detection

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

- **Homepage: [Korean Sarcasm Detection](https://github.com/SpellOnYou/korean-sarcasm)**
- **Repository: [Korean Sarcasm Detection](https://github.com/SpellOnYou/korean-sarcasm)**
- **Point of Contact: [Dionne Kim](jiwon.kim.096@gmail.com)**

### Dataset Summary

The Korean Sarcasm Dataset was created to detect sarcasm in text, which can significantly alter the original meaning of a sentence. 9319 tweets were collected from Twitter and labeled for `sarcasm` or `not_sarcasm`. These tweets were gathered by querying for: `역설, 아무말, 운수좋은날, 笑, 뭐래 아닙니다, 그럴리없다, 어그로, irony sarcastic, and sarcasm`. The dataset was pre-processed by removing the keyword hashtag, urls and mentions of the user to maintain anonymity. 

### Supported Tasks and Leaderboards

* `sarcasm_detection`: The dataset can be used to train a model to detect sarcastic tweets. A [BERT](https://huggingface.co/bert-base-uncased) model can be presented with a tweet in Korean and be asked to determine whether it is sarcastic or not.

### Languages

The text in the dataset is in Korean and the associated is BCP-47 code is `ko-KR`.	

## Dataset Structure

### Data Instances

An example data instance contains a Korean tweet and a label whether it is sarcastic or not. `1` maps to sarcasm and `0` maps to no sarcasm.

```
{
  "tokens": "[ 수도권 노선 아이템 ] 17 . 신분당선의 #딸기 : 그의 이미지 컬러 혹은 머리 색에서 유래한 아이템이다 . #메트로라이프"
  "label": 	0
}
```

### Data Fields

* `tokens`: contains the text of the tweet
* `label`: determines whether the text is sarcastic (`1`: sarcasm, `0`: no sarcasm)

### Data Splits

The data is split into a training set comrpised of 9018 tweets and a test set of 301 tweets.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The dataset was created by gathering HTML data from Twitter. Queries for hashtags that include sarcasm and variants of it were used to return tweets. It was preprocessed by removing the keyword hashtag, urls and mentions of the user to preserve anonymity. 

#### Who are the source language producers?

The source language producers are Korean Twitter users.

### Annotations

#### Annotation process

Tweets were labeled `1` for sarcasm and `0` for no sarcasm.

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

Mentions of the user in a tweet were removed to keep them anonymous.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

This dataset was curated by Dionne Kim.

### Licensing Information

This dataset is licensed under the MIT License.

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@stevhliu](https://github.com/stevhliu) for adding this dataset.