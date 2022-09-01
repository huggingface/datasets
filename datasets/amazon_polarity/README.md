---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
pretty_name: Amazon Review Polarity
train-eval-index:
- config: amazon_polarity
  task: text-classification
  task_id: binary_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    content: text
    label: target
  metrics:
    - type: accuracy
      name: Accuracy
    - type: f1
      name: F1 macro
      args:
        average: macro
    - type: f1
      name: F1 micro
      args:
        average: micro  
    - type: f1
      name: F1 weighted
      args:
        average: weighted
    - type: precision
      name: Precision macro
      args:
        average: macro  
    - type: precision
      name: Precision micro
      args:
        average: micro  
    - type: precision
      name: Precision weighted
      args:
        average: weighted  
    - type: recall
      name: Recall macro
      args:
        average: macro  
    - type: recall
      name: Recall micro
      args:
        average: micro  
    - type: recall
      name: Recall weighted
      args:
        average: weighted
---

# Dataset Card for Amazon Review Polarity

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

- **Homepage:** https://registry.opendata.aws/
- **Repository:** https://github.com/zhangxiangxiao/Crepe
- **Paper:** https://arxiv.org/abs/1509.01626
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Xiang Zhang](mailto:xiang.zhang@nyu.edu)

### Dataset Summary

The Amazon reviews dataset consists of reviews from amazon.
The data span a period of 18 years, including ~35 million reviews up to March 2013.
Reviews include product and user information, ratings, and a plaintext review.

### Supported Tasks and Leaderboards

- `text-classification`, `sentiment-classification`: The dataset is mainly used for text classification: given the content and the title, predict the correct star rating. 

### Languages

Mainly English.

## Dataset Structure

### Data Instances

A typical data point, comprises of a title, a content and the corresponding label. 

An example from the AmazonPolarity test set looks as follows:

```
{
    'title':'Great CD',
    'content':"My lovely Pat has one of the GREAT voices of her generation. I have listened to this CD for YEARS and I still LOVE IT. When I'm in a good mood it makes me feel better. A bad mood just evaporates like sugar in the rain. This CD just oozes LIFE. Vocals are jusat STUUNNING and lyrics just kill. One of life's hidden gems. This is a desert isle CD in my book. Why she never made it big is just beyond me. Everytime I play this, no matter black, white, young, old, male, female EVERYBODY says one thing ""Who was that singing ?""",
    'label':1
}
```

### Data Fields

- 'title': a string containing the title of the review - escaped using double quotes (") and any internal double quote is escaped by 2 double quotes (""). New lines are escaped by a backslash followed with an "n" character, that is "\n".
- 'content': a string containing the body of the document - escaped using double quotes (") and any internal double quote is escaped by 2 double quotes (""). New lines are escaped by a backslash followed with an "n" character, that is "\n".
- 'label': either 1 (positive) or 0 (negative) rating.

### Data Splits

The Amazon reviews polarity dataset is constructed by taking review score 1 and 2 as negative, and 4 and 5 as positive. Samples of score 3 is ignored. Each class has 1,800,000 training samples and 200,000 testing samples.

## Dataset Creation

### Curation Rationale

The Amazon reviews polarity dataset is constructed by Xiang Zhang (xiang.zhang@nyu.edu). It is used as a text classification benchmark in the following paper: Xiang Zhang, Junbo Zhao, Yann LeCun. Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NIPS 2015).

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

Apache License 2.0

### Citation Information

McAuley, Julian, and Jure Leskovec. "Hidden factors and hidden topics: understanding rating dimensions with review text." In Proceedings of the 7th ACM conference on Recommender systems, pp. 165-172. 2013.

Xiang Zhang, Junbo Zhao, Yann LeCun. Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NIPS 2015)

### Contributions

Thanks to [@hfawaz](https://github.com/hfawaz) for adding this dataset.
