---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
language:
- en-IN
- kn-IN
license:
- cc-by-4.0
multilinguality:
- multilingual
pretty_name: KanHope
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
- text-classification-other-Hope Speech Detection
---

# Dataset Card for KanHope

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

## Dataset Description

- **Homepage:** https://zenodo.org/record/4904729 
- **Repository:** [KanHope](https://github.com/adeepH/KanHope)
- **Paper:** [Hope speech detection in Under-resourced Kannada langauge](https://arxiv.org/abs/2108.04616)
- **Leaderboard:** [N/A]
- **Point of Contact:** [Adeep Hande](adeeph18c@iiitt.ac.in)

### Dataset Summary

KanHope dataset is a code-mixed Kannada-English dataset for hope speech detection. All texts are scraped from the comments section of YouTube. The dataset consists of 6,176 user-generated comments in code mixed Kannada scraped from YouTube and manually annotated as bearing hope speech or Not-hope speech. 

### Supported Tasks and Leaderboards

This task aims to detect Hope speech content of the code-mixed dataset of comments/posts in Dravidian Languages ( Kannada-English) collected from social media. The comment/post may contain more than one sentence, but the average sentence length of the corpora is 1. Each comment/post is annotated at the comment/post level. This dataset also has class imbalance problems depicting real-world scenarios.

### Languages

Code-mixed text in Dravidian languages (Kannada-English).


## Dataset Structure

### Data Instances

An example from the Kannada dataset looks as follows:

| text   | label |
| :------ | :----- |
| ���������  ��ͭ� heartly heltidini... plz avrigella namma nimmellara supprt beku          | 0 (Non_hope speech) |
| Next song gu kuda alru andre evaga yar comment  madidera alla alrru like madi share madi nam industry na next level ge togond hogaona.      | 1 (Hope Speech) |


### Data Fields

Kannada
- `text`: Kannada-English code mixed comment.
- `label`: integer from either of 0 or 1 that corresponds to these values: "Non_hope Speech", "Hope Speech"

### Data Splits

|         | train | validation | test |
|---------|------:|-----------:|-----:|
| Kannada |  4941 |        618 |  617 |

## Dataset Creation

### Curation Rationale

Numerous methods have been developed to monitor the spread of negativity in modern years by eliminating vulgar, offensive, and fierce comments from social media platforms. However, there are relatively lesser amounts of study that converges on embracing positivity, reinforcing supportive and reassuring content in online forums.

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

Youtube users

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

[Needs More Information]


### Citation Information
```
@misc{hande2021hope,
      title={Hope Speech detection in under-resourced Kannada language}, 
      author={Adeep Hande and Ruba Priyadharshini and Anbukkarasi Sampath and Kingston Pal Thamburaj and Prabakaran Chandran and Bharathi Raja Chakravarthi},
      year={2021},
      eprint={2108.04616},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@adeepH](https://github.com/adeepH) for adding this dataset.
