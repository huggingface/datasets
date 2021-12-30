---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- found
languages:
- bn
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
- text-classification-other-hate-speech-topic-classification
paperswithcode_id: bengali-hate-speech
---

# Dataset Card for Bengali Hate Speech Dataset

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

- **Homepage: [Bengali Hate Speech Dataset](https://github.com/rezacsedu/Bengali-Hate-Speech-Dataset)**
- **Repository: [Bengali Hate Speech Dataset](https://github.com/rezacsedu/Bengali-Hate-Speech-Dataset)**
- **Paper: [Classification Benchmarks for Under-resourced Bengali Language based on Multichannel Convolutional-LSTM Network](https://arxiv.org/abs/2004.07807)**
- **Point of Contact: [Md. Rezaul Karim](rezaul.karim.fit@gmail.com)**

### Dataset Summary

The Bengali Hate Speech Dataset is a Bengali-language dataset of news articles collected from various Bengali media sources and categorized based on the type of hate in the text. The dataset was created to provide greater support for under-resourced languages like Bengali on NLP tasks, and serves as a benchmark for multiple types of classification tasks. 

### Supported Tasks and Leaderboards

* `topic classification`: The dataset can be used to train a Multichannel Convolutional-LSTM for classifying different types of hate speech. The model performance can be measured by its F1 score.

### Languages

The text in the dataset is in Bengali and the associated BCP-47 code is `bn`.

## Dataset Structure

### Data Instances

A data instance takes the form of a news article and its associated label. 

🚨 Beware that the following example contains extremely offensive content! 

An example looks like this:

```
{"text": "রেন্ডিয়াকে পৃথীবির মানচিএ থেকে মুচে ফেলতে হবে",
 "label": "Geopolitical"}
```

### Data Fields

* `text`: the text of the Bengali news article
* `label`: one of `Geopolitical`, `Personal`, `Political`, `Religious`, or `Gender abusive` indicating the type of hate speech

### Data Splits

The dataset has 3418 examples. 

## Dataset Creation

### Curation Rationale

Under-resourced languages like Bengali lack supporting resources that languages like English have. This dataset was collected from multiple Bengali news sources to provide several classification benchmarks for hate speech detection, document classification and sentiment analysis. 

### Source Data

#### Initial Data Collection and Normalization

Bengali articles were collected from a Bengali Wikipedia dump, Bengali news articles, news dumps of TV channels, books, blogs, sports portal and social media. Emphasis was placed on Facebook pages and newspaper sources because they have about 50 million followers and is a common source of opinion and hate speech. The full dataset consists of 250 million articles and is currently being prepared. This is a subset of the full dataset.

#### Who are the source language producers?

The source language producers are Bengali authors and users who interact with these various forms of Bengali media.

### Annotations

#### Annotation process

The data was annotated by manually identifying freqently occurring terms in texts containing hate speech and references to specific entities. The authors also prepared normalized frequency vectors of 175 abusive terms that are commonly used to express hate in Bengali. A hate label is assigned if at least one of these terms exists in the text. Annotator's were provided with unbiased text only contents to make the decision. Non-hate statements were removed from the list and the category of hate was further divided into political, personal, gender abusive, geopolitical and religious. To reduce possible bias, each label was assigned based on a majority voting on the annotator's opinions and Cohen's Kappa was computed to measure inter-annotator agreement.

#### Who are the annotators?

Three native Bengali speakers and two linguists annotated the dataset which was then reviewed and validated by three experts (one South Asian linguist and two native speakers). 

### Personal and Sensitive Information

The dataset contains very sensitive and highly offensive comments in a religious, political and gendered context. Some of the comments are directed towards contemporary public figures like politicians, religious leaders, celebrities and athletes.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of the dataset is to improve hate speech detection in Bengali. The growth of social media has enabled people to express hate freely online and there has been a lot of focus on detecting hate speech for highly resourced languages like English. The use of hate speech is pervasive, like any other major language, which can have serious and deadly consequences. Failure to react to hate speech renders targeted minorities more vulnerable to attack and it can also create indifference towards their treatment from majority populations. 

### Discussion of Biases

The dataset was collected using a bootstrapping approach. An initial search was made for specific types of texts, articles and tweets containing common harassment directed at targeting characteristics. As a result, this dataset contains **extremely** offensive content that is disturbing. In addition, Facebook pages and newspaper sources were emphasized because they are well-known for having hate and harassment issues.

### Other Known Limitations

The dataset contains racist, sexist, homophobic and offensive comments. It is collected and annotated for research related purposes only.

## Additional Information

### Dataset Curators

The dataset was curated by Md. Rezaul Karim, Sumon Kanti Dey, Bharathi Raja Chakravarthi, John McCrae and Michael Cochez.

### Licensing Information

This dataset is licensed under the MIT License.

### Citation Information

```
@inproceedings{karim2020BengaliNLP,
    title={Classification Benchmarks for Under-resourced Bengali Language based on Multichannel Convolutional-LSTM Network},
    author={Karim, Md. Rezaul and Chakravarti, Bharathi Raja and P. McCrae, John and Cochez, Michael},
    booktitle={7th IEEE International Conference on Data Science and Advanced Analytics (IEEE DSAA,2020)},
    publisher={IEEE},
    year={2020}
}
```

### Contributions

Thanks to [@stevhliu](https://github.com/stevhliu) for adding this dataset.