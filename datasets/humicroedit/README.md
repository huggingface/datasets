---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
  subtask-1:
  - text-scoring
  subtask-2:
  - text-classification
task_ids:
  subtask-1:
  - text-scoring-other-funniness-score-prediction
  subtask-2:
  - text-classification-other-funnier-headline-identification
paperswithcode_id: humicroedit
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

- **Homepage:**[Humicroedit](https://www.cs.rochester.edu/u/nhossain/humicroedit.html)
- **Repository:**
- **Paper:**["President Vows to Cut Taxes Hair": Dataset and Analysis of Creative Text Editing for Humorous Headlines.](http://cs.rochester.edu/~nhossain/humicroedit-naacl-19.pdf)
- **Leaderboard:**
- **Point of Contact:**[nhossain@cs.rochester.edu]

### Dataset Summary

This is the task dataset for SemEval-2020 Task 7: Assessing Humor in Edited News Headlines.

### Supported Tasks and Leaderboards

[Task Description Page](https://competitions.codalab.org/competitions/20970)

- Regression Task: In this task, given the original and the edited headline, the participant is required to predict the mean funniness of the edited headline. Success on this task is typically measured by achieving a *low* Mean Square Error.
- Predict the funnier of the two edited headlines: Given the original headline and two edited versions, the participant has to predict which edited version is the funnier of the two. Success on this task is typically measured by achieving a *high* accuracy.

### Languages

English

## Dataset Structure

### Data Instances
For subtask-1, i.e Given the original and the edited headline, predict the mean funniness of the edited headline. 
```
{
  'id': 1183,
  'original': 'Kushner to visit <Mexico/> following latest trump tirades.',
  'edit': 'therapist',
  'grades': '33332',
  'meanGrade': 2.8
}
```
For subtask-2, i.e Given the original headline and two edited versions, predict which edited version is the funnier of the two.
```
{
  'id': 1183,
  'original1': 'Gene Cernan , Last <Astronaut/> on the Moon , Dies at 82',
  'edit1': 'Dancer',
  'grades1': '1113',
  'meanGrade1': 1.2, 
  'original2': 'Gene Cernan , Last Astronaut on the Moon , <Dies/> at 82',
  'edit2': 'impregnated',
  'grades2': '30001',
  'meanGrade2': 0.8, 
  'label': 1 
}
```

### Data Fields
For subtask-1
- `id`: Unique identifier of an edited headline.
- `original`: The headline with replaced word(s) identified with the </> tag.
- `edit`: The new word which replaces the word marked in </> tag in the original field.
- `grades`: 'grades' are the concatenation of all the grades by different annotators. 
- `mean` is the mean of all the judges scores.


For subtask-2
- `id`: Unique identifier of an edited headline.
- `original1`: The original headline with replaced word(s) identified with </> tag.
- `edit1`: The new word which replaces the word marked in </> tag in the `original1` field.
- `grades1`: The concatenation of all the grades annotated by different annotators for sentence1. 
- `meanGrade1` is the mean of all the judges scores for sentence1.
- `original2`: The original headline with replaced word(s) identified with </> tag.
- `edit2`: The new word which replaces the word marked in </> tag in the `original1` field.
- `grades2`: The concatenation of all the grades annotated by different annotators for the sentence2. 
- `meanGrade2` is the mean of all the judges scores for sentence2.
- `label` is 1 if sentence1 is more humourous than sentence2,
           2 if sentence 2 is more humorous than sentence1,
           0 if both the sentences are equally humorous

### Data Splits
|   Sub Task                 | Train   | Dev | Test  | Funlines|
| -----                      | ------ | ---- | ---- |-----|
| Subtask-1:Regression                 |  9652  |  2419 |  3024| 8248 |
| Subtask-2: Funnier headline prediction|   9381  |  2355 |  2960| 1958 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Crowd-sourced the data by gamifying it as on the website funlines.co. Players rate the headlines on a scale of 0-4. 
Players are scored based on their editing and rating, and they
are ranked on the game’s leaderboard page.

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

[More Information Needed]

### Citation Information
```
@article{hossain2019president,
  title={" President Vows to Cut< Taxes> Hair": Dataset and Analysis of Creative Text Editing for Humorous Headlines},
  author={Hossain, Nabil and Krumm, John and Gamon, Michael},
  journal={arXiv preprint arXiv:1906.00274},
  year={2019}
}```

### Contributions

Thanks to [@saradhix](https://github.com/saradhix) for adding this dataset.