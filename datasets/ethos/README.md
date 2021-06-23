---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- found, other
languages:
- en
licenses:
- agpl-3.0-or-later
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
  binary:
  - sentiment-classification
  - text-classification-other-Hate Speech Detection
  multilabel:
  - multi-label-classification
  - sentiment-classification
  - text-classification-other-Hate Speech Detection
paperswithcode_id: ethos
---

# Dataset Card for Ethos

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

- **Homepage:** [ETHOS Hate Speech Dataset](https://github.com/intelligence-csd-auth-gr/Ethos-Hate-Speech-Dataset)
- **Repository:**[ETHOS Hate Speech Dataset](https://github.com/intelligence-csd-auth-gr/Ethos-Hate-Speech-Dataset)
- **Paper:**[ETHOS: an Online Hate Speech Detection Dataset](https://arxiv.org/abs/2006.08328)

### Dataset Summary

ETHOS: onlinE haTe speecH detectiOn dataSet. This repository contains a dataset for hate speech detection on social media platforms, called Ethos. There are two variations of the dataset:
- **Ethos_Dataset_Binary**: contains 998 comments in the dataset alongside with a label about hate speech *presence* or *absence*. 565 of them do not contain hate speech, while the rest of them, 433, contain. 
- **Ethos_Dataset_Multi_Label** which contains 8 labels for the 433 comments with hate speech content. These labels are *violence* (if it incites (1) or not (0) violence), *directed_vs_general* (if it is directed to a person (1) or a group (0)), and 6 labels about the category of hate speech like, *gender*, *race*, *national_origin*, *disability*, *religion* and *sexual_orientation*.

***Ethos /ˈiːθɒs/*** 
is a Greek word meaning “character” that is used to describe the guiding beliefs or ideals that characterize a community, nation, or ideology. The Greeks also used this word to refer to the power of music to influence emotions, behaviors, and even morals.

### Supported Tasks and Leaderboards

[More Information Needed]
- `text-classification-other-Hate Speech Detection`, `sentiment-classification`,`multi-label-classification`: The dataset can be used to train a model for hate speech detection. Moreover, it can be used as a benchmark dataset for multi label classification algorithms.

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

A typical data point in the binary version comprises a comment, with a `text` containing the  text and a `label` describing if a comment contains hate speech content (1 - hate-speech) or not (0 - non-hate-speech). In the multilabel version more labels like *violence* (if it incites (1) or not (0) violence), *directed_vs_general* (if it is directed to a person (1) or a group (0)), and 6 labels about the category of hate speech like, *gender*, *race*, *national_origin*, *disability*, *religion* and *sexual_orientation* are appearing.

An example from the binary version, which is offensive, but it does not contain hate speech content:
```
{'text': 'What the fuck stupid people !!!',
 'label': '0'
}
```

An example from the multi-label version, which contains hate speech content towards women (gender):
```
{'text': 'You should know women's sports are a joke',
 `violence`: 0,
 `directed_vs_generalized`: 0,
 `gender`: 1,
 `race`: 0,
 `national_origin`: 0,
 `disability`: 0,
 `religion`: 0,
 `sexual_orientation`: 0
}
```


### Data Fields

Ethos Binary:
- `text`: a `string` feature containing the text of the comment.
- `label`: a classification label, with possible values including `no_hate_speech`, `hate_speech`.

Ethis Multilabel:
- `text`: a `string` feature containing the text of the comment.
- `violence`: a classification label, with possible values including `not_violent`, `violent`.
- `directed_vs_generalized`: a classification label, with possible values including `generalized`, `directed`.
- `gender`: a classification label, with possible values including `false`, `true`.
- `race`: a classification label, with possible values including `false`, `true`.
- `national_origin`: a classification label, with possible values including `false`, `true`.
- `disability`: a classification label, with possible values including `false`, `true`.
- `religion`: a classification label, with possible values including `false`, `true`.
- `sexual_orientation`: a classification label, with possible values including `false`, `true`.

### Data Splits

The data is split into binary and multilabel. Multilabel is a subset of the binary version.

|                             | Instances   | Labels |
| -----                       | ------ | ----- |
| binary | 998 |  1 |
| multilabel       | 433 |  8 |

## Dataset Creation

### Curation Rationale

The dataset was build by gathering online comments in Youtube videos and reddit comments, from videos and subreddits which may attract hate speech content. 

### Source Data

#### Initial Data Collection and Normalization

The initial data we used are from the hatebusters platform: [Original data used](https://intelligence.csd.auth.gr/topics/hate-speech-detection/), but they were not included in this dataset

#### Who are the source language producers?

The language producers are users of reddit and Youtube. More informations can be found in this paper: [ETHOS: an Online Hate Speech Detection Dataset](https://arxiv.org/abs/2006.08328)

### Annotations

#### Annotation process

The annotation process is detailed in the third section of this paper: [ETHOS: an Online Hate Speech Detection Dataset](https://arxiv.org/abs/2006.08328)

#### Who are the annotators?

Originally anotated by Ioannis Mollas and validated through the Figure8 platform (APEN).

### Personal and Sensitive Information

No personal and sensitive information included in the dataset.

## Considerations for Using the Data

### Social Impact of Dataset

This dataset will help on the evolution of the automated hate speech detection tools. Those tools have great impact on preventing social issues.

### Discussion of Biases

This dataset tries to be unbiased towards its classes and labels.

### Other Known Limitations

The dataset is relatively small and should be used combined with larger datasets.

## Additional Information

### Dataset Curators

The dataset was initially created by [Intelligent Systems Lab](https://intelligence.csd.auth.gr).

### Licensing Information

The licensing status of the datasets is [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/).

### Citation Information
```
@misc{mollas2020ethos,
      title={ETHOS: an Online Hate Speech Detection Dataset}, 
      author={Ioannis Mollas and Zoe Chrysopoulou and Stamatis Karlos and Grigorios Tsoumakas},
      year={2020},
      eprint={2006.08328},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

### Contributions

Thanks to [@iamollas](https://github.com/iamollas) for adding this dataset.