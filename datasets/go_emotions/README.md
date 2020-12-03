---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
  raw:
  - 100K<n<1M
  simplified:
  - 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
- multi-label-classification
- text-classification-other-emotion
---

# Dataset Card for GoEmotions

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

- **Homepage:** https://github.com/google-research/google-research/tree/master/goemotions
- **Repository:** https://github.com/google-research/google-research/tree/master/goemotions
- **Paper:** https://arxiv.org/abs/2005.00547
- **Leaderboard:**
- **Point of Contact:** [Dora Demszky](https://nlp.stanford.edu/~ddemszky/index.html)

### Dataset Summary

The GoEmotions dataset contains 58k carefully curated Reddit comments labeled for 27 emotion categories or Neutral.
The raw data is included as well as the smaller, simplified version of the dataset with predefined train/val/test
splits.

### Supported Tasks and Leaderboards

This dataset is intended for multi-class, multi-label emotion classification.

### Languages

The data is in English.

## Dataset Structure

### Data Instances

Each instance is a reddit comment with a corresponding ID and one or more emotion annotations (or neutral).

### Data Fields

The simplified configuration includes:
- `text`: the reddit comment
- `labels`: the emotion annotations
- `comment_id`: unique identifier of the comment (can be used to look up the entry in the raw dataset)

In addition to the above, the raw data includes:
* `author`: The Reddit username of the comment's author.
* `subreddit`: The subreddit that the comment belongs to.
* `link_id`: The link id of the comment.
* `parent_id`: The parent id of the comment.
* `created_utc`: The timestamp of the comment.
* `rater_id`: The unique id of the annotator.
* `example_very_unclear`: Whether the annotator marked the example as being very unclear or difficult to label (in this
case they did not choose any emotion labels).

In the raw data, labels are listed as their own columns with binary 0/1 entries rather than a list of ids as in the
simplified data.

### Data Splits

The simplified data includes a set of train/val/test splits with 43,410, 5426, and 5427 examples respectively.

## Dataset Creation

### Curation Rationale

From the paper abstract:

> Understanding emotion expressed in language has a wide range of applications, from building empathetic chatbots to
detecting harmful online behavior. Advancement in this area can be improved using large-scale datasets with a
fine-grained typology, adaptable to multiple downstream tasks.

### Source Data

#### Initial Data Collection and Normalization

Data was collected from Reddit comments via a variety of automated methods discussed in 3.1 of the paper.

#### Who are the source language producers?

English-speaking Reddit users.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

Annotations were produced by 3 English-speaking crowdworkers in India.

### Personal and Sensitive Information

This dataset includes the original usernames of the Reddit users who posted each comment. Although Reddit usernames
are typically disasociated from personal real-world identities, this is not always the case. It may therefore be
possible to discover the identities of the individuals who created this content in some cases.

## Considerations for Using the Data

### Social Impact of Dataset

Emotion detection is a worthwhile problem which can potentially lead to improvements such as better human/computer
interaction. However, emotion detection algorithms (particularly in computer vision) have been abused in some cases
to make erroneous inferences in human monitoring and assessment applications such as hiring decisions, insurance
pricing, and student attentiveness (see
[this article](https://www.unite.ai/ai-now-institute-warns-about-misuse-of-emotion-detection-software-and-other-ethical-issues/)).

### Discussion of Biases

From the authors' github page:

> Potential biases in the data include: Inherent biases in Reddit and user base biases, the offensive/vulgar word lists used for data filtering, inherent or unconscious bias in assessment of offensive identity labels, annotators were all native English speakers from India. All these likely affect labelling, precision, and recall for a trained model. Anyone using this dataset should be aware of these limitations of the dataset.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Researchers at Amazon Alexa, Google Research, and Stanford. See the [author list](https://arxiv.org/abs/2005.00547).

### Licensing Information

The GitHub repository which houses this dataset has an
[Apache License 2.0](https://github.com/google-research/google-research/blob/master/LICENSE).

### Citation Information

@inproceedings{demszky2020goemotions,
 author = {Demszky, Dorottya and Movshovitz-Attias, Dana and Ko, Jeongwoo and Cowen, Alan and Nemade, Gaurav and Ravi, Sujith},
 booktitle = {58th Annual Meeting of the Association for Computational Linguistics (ACL)},
 title = {{GoEmotions: A Dataset of Fine-Grained Emotions}},
 year = {2020}
}
