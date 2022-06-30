---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- cc0-1.0
multilinguality:
- monolingual
pretty_name: Jigsaw Unintended Bias in Toxicity Classification
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-scoring
- text-classification-other-toxicity-prediction
---

# Dataset Card for Jigsaw Unintended Bias in Toxicity Classification

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

- **Homepage:** https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification
- **Repository:**
- **Paper:**
- **Leaderboard:** https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/leaderboard
- **Point of Contact:**

### Dataset Summary

The Jigsaw Unintended Bias in Toxicity Classification dataset comes from the eponymous Kaggle competition.

Please see the original [data](https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data)
 description for more information.

### Supported Tasks and Leaderboards

The main target for this dataset is toxicity prediction. Several toxicity subtypes are also available, so the dataset 
can be used for multi-attribute prediction.

See the original [leaderboard](https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/leaderboard)
for reference.

### Languages

English

## Dataset Structure

### Data Instances

A data point consists of an id, a comment, the main target, the other toxicity subtypes as well as identity attributes.

For instance, here's the first train example.
```
{
    "article_id": 2006,
    "asian": NaN,
    "atheist": NaN,
    "bisexual": NaN,
    "black": NaN,
    "buddhist": NaN,
    "christian": NaN,
    "comment_text": "This is so cool. It's like, 'would you want your mother to read this??' Really great idea, well done!",
    "created_date": "2015-09-29 10:50:41.987077+00",
    "disagree": 0,
    "female": NaN,
    "funny": 0,
    "heterosexual": NaN,
    "hindu": NaN,
    "homosexual_gay_or_lesbian": NaN,
    "identity_annotator_count": 0,
    "identity_attack": 0.0,
    "insult": 0.0,
    "intellectual_or_learning_disability": NaN,
    "jewish": NaN,
    "latino": NaN,
    "likes": 0,
    "male": NaN,
    "muslim": NaN,
    "obscene": 0.0,
    "other_disability": NaN,
    "other_gender": NaN,
    "other_race_or_ethnicity": NaN,
    "other_religion": NaN,
    "other_sexual_orientation": NaN,
    "parent_id": NaN,
    "physical_disability": NaN,
    "psychiatric_or_mental_illness": NaN,
    "publication_id": 2,
    "rating": 0,
    "sad": 0,
    "severe_toxicity": 0.0,
    "sexual_explicit": 0.0,
    "target": 0.0,
    "threat": 0.0,
    "toxicity_annotator_count": 4,
    "transgender": NaN,
    "white": NaN,
    "wow": 0
}
```

### Data Fields

- `id`: id of the comment
- `target`: value between 0(non-toxic) and 1(toxic) classifying the comment
- `comment_text`: the text of the comment
- `severe_toxicity`: value between 0(non-severe_toxic) and 1(severe_toxic) classifying the comment
- `obscene`: value between 0(non-obscene) and 1(obscene) classifying the comment
- `identity_attack`: value between 0(non-identity_hate) or 1(identity_hate) classifying the comment
- `insult`: value between 0(non-insult) or 1(insult) classifying the comment
- `threat`: value between 0(non-threat) and 1(threat) classifying the comment
- For a subset of rows, columns containing whether the comment mentions the entities (they may contain NaNs): 
  - `male`
  - `female`
  - `transgender`
  - `other_gender`
  - `heterosexual`
  - `homosexual_gay_or_lesbian`
  - `bisexual`
  - `other_sexual_orientation`
  - `christian`
  - `jewish`
  - `muslim`
  - `hindu`
  - `buddhist`
  - `atheist`
  - `other_religion`
  - `black`
  - `white`
  - `asian`
  - `latino`
  - `other_race_or_ethnicity`
  - `physical_disability`
  - `intellectual_or_learning_disability`
  - `psychiatric_or_mental_illness`
  - `other_disability`
- Other metadata related to the source of the comment, such as creation date, publication id, number of likes,
number of annotators, etc:
  - `created_date`
  - `publication_id`
  - `parent_id`
  - `article_id`
  - `rating`
  - `funny`
  - `wow`
  - `sad`
  - `likes`
  - `disagree`
  - `sexual_explicit`
  - `identity_annotator_count`
  - `toxicity_annotator_count`

### Data Splits

There are four splits:
- train: The train dataset as released during the competition. Contains labels and identity information for a 
subset of rows.
- test: The train dataset as released during the competition. Does not contain labels nor identity information.
- test_private_expanded: The private leaderboard test set, including toxicity labels and subgroups. The competition target was a binarized version of the toxicity column, which can be easily reconstructed using a >=0.5 threshold.
- test_public_expanded: The public leaderboard test set, including toxicity labels and subgroups. The competition target was a binarized version of the toxicity column, which can be easily reconstructed using a >=0.5 threshold.

## Dataset Creation

### Curation Rationale

The dataset was created to help in efforts to identify and curb instances of toxicity online.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

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

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

This dataset is released under CC0, as is the underlying comment text.

### Citation Information

No citation is available for this dataset, though you may link to the [kaggle](https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification) competition

### Contributions

Thanks to [@iwontbecreative](https://github.com/iwontbecreative) for adding this dataset.
