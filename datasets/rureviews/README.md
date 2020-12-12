---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- ru
licenses:
- unknown
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

# Dataset Card for [Dataset Name]

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

- **Homepage: [Link](https://ieeexplore.ieee.org/document/8807792)
- **Repository: [Link](https://github.com/sismetanin/rureviews)
- **Paper: [Link](https://ieeexplore.ieee.org/document/8807792)
- **Leaderboard:
- **Point of Contact: [Darshan Gandhi](darshangandhi1151@gmail.com)

### Dataset Summary

The training dataset was collected from reviews on top-ranked goods form the major e-commerce site in Russian, where user-ranked scores were used as class labels on a 5-point scale. Since the same words in different product categories may have different sentiment polarity, it was decided to collect reviews only from one category, namely "Women’s Clothes and Accessories" category. It helped to get the collected dataset to consists of 821k automatically labelled reviews.

According to the obtained data, in some cases, it is complex task to correctly evaluate reviews with the same texts. For example, the review text “Fine” (translation from Russian into English) has 42.45% reviews with a score of “5”, 36% reviews with a score of “4”, 29.25% reviews with a score of “3”, and 0.94% reviews with a score of “2”. It is clear that such contradictions in the training dataset tend to affect the classification score. Therefore, we decided to mark these reviews with the class labels, which are the most common for these texts in the collected dataset. Moreover, sometimes it is also difficult to distinguish reviews with the close score values, e.g. reviews with score “1” and “2” or with score “4” and “5”. To overcome this issue, we transformed 5-point scale to 3-point scale by combining reviews with “1” and “2” into one “negative” class and reviews with “3” and “5” scores into another one “positive” class. Thus, the 5-star rating scale collapsed into 3 classes: negative, neutral, and positive reviews.


### Supported Tasks and Leaderboards

Since the data were collected from the top-ranked goods with high average rating, the amount of positive reviews considerably exceeded the amount of neutral and negative reviews. At the same time, we have no information about real-life class distribution for reviews, that is why we decided to use an undersampling technique to deal with imbalanced data. For each class 30k of reviews were randomly selected to make balanced dataset.

### Languages

The dataset is based on Women’s Clothes and Accessories Reviews in Russian Language 

## Dataset Structure

### Data Instances

{reviews_sentiment : 'качество плохое пошив ужасный (горловина наперекос) Фото не соответствует Ткань ужасная рисунок блеклый маленький рукав не такой УЖАС!!!!! не стоит за такие деньги г.......	negative'}

### Data Fields

* reviews_sentiment : review of the user for women's clothes and accessories 

### Data Splits

The train data size is : 90000

## Dataset Creation

### Curation Rationale

The dataset was built to understand about the sentiments of the users who shop primarily Women's Shopping and Accessory in Russia

### Source Data

#### Initial Data Collection and Normalization

[Link](https://ieeexplore.ieee.org/document/8807792)

#### Who are the source language producers?

Crowdsourced

### Annotations

#### Annotation process

This repository contains an automatically collected dataset for sentiment analysis of product reviews in Russian, which were created within the paper "Sentiment Analysis of Product Reviews in Russian using Convolutional Neural Networks". 

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

The ideology of this dataset provides an approach for sentiment analysis of product reviews in Russian. This would help to understand more about what are the sentiments of users when they shop especially for clothers and accessories category by women. 

### Discussion of Biases

The reviews are only pertaining to Women’s Clothes and Accessories Category and also in Russian language and hence it is difficult for everyone to make use of 

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Sergey Smetanin, Mikhail Komarov

### Licensing Information

[Lisensce](https://github.com/sismetanin/rureviews/blob/master/LICENSE)

### Citation Information

@INPROCEEDINGS{Smetanin-SA-2019,
  author={Sergey Smetanin and Michail Komarov},
  booktitle={2019 IEEE 21st Conference on Business Informatics (CBI)},
  title={Sentiment Analysis of Product Reviews in Russian using Convolutional Neural Networks},
  year={2019},
  volume={01},
  number={},
  pages={482-486},
  doi={10.1109/CBI.2019.00062},
  ISSN={2378-1963},
  month={July}
}
