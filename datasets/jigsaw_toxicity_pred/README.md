---
annotations_creators:
- crowdsourced
language_creators:
- other
languages:
- en
licenses:
- cc0-1.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
paperswithcode_id: null
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [Jigsaw Comment Toxicity Classification Kaggle Competition](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data)
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Discussing things you care about can be difficult. The threat of abuse and harassment online means that many people stop expressing themselves and give up on seeking different opinions. Platforms struggle to effectively facilitate conversations, leading many communities to limit or completely shut down user comments. This dataset consists of a large number of Wikipedia comments which have been labeled by human raters for toxic behavior. 

### Supported Tasks and Leaderboards

The dataset support multi-label classification

### Languages

The comments are in English

## Dataset Structure

### Data Instances

A data point consists of a comment followed by multiple labels that can be associated with it.
{'id': '02141412314',
 'comment_text': 'Sample comment text',
 'toxic': 0,
 'severe_toxic': 0,
 'obscene': 0,
 'threat': 0,
 'insult': 0,
 'identity_hate': 1,
}

### Data Fields

- `id`: id of the comment
- `comment_text`: the text of the comment
- `toxic`: value of 0(non-toxic) or 1(toxic) classifying the comment
- `severe_toxic`: value of 0(non-severe_toxic) or 1(severe_toxic) classifying the comment
- `obscene`: value of 0(non-obscene) or 1(obscene) classifying the comment
- `threat`: value of 0(non-threat) or 1(threat) classifying the comment
- `insult`: value of 0(non-insult) or 1(insult) classifying the comment
- `identity_hate`: value of 0(non-identity_hate) or 1(identity_hate) classifying the comment

### Data Splits

The data is split into a training and testing set.

## Dataset Creation

### Curation Rationale

The dataset was created to help in efforts to identify and curb instances of toxicity online.

### Source Data

#### Initial Data Collection and Normalization

The dataset is a collection of Wikipedia comments.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

If words that are associated with swearing, insults or profanity are present in a comment, it is likely that it will be classified as toxic, regardless of the tone or the intent of the author e.g. humorous/self-deprecating. This could present some biases towards already vulnerable minority groups.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

The "Toxic Comment Classification" dataset is released under [CC0], with the underlying comment text being governed by Wikipedia\'s [CC-SA-3.0].

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@Tigrex161](https://github.com/Tigrex161) for adding this dataset.