---
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- en
license:
- other
multilinguality:
- monolingual
pretty_name: RiddleSense
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
---

# Dataset Card for RiddleSense

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

- **Homepage:** https://inklab.usc.edu/RiddleSense/
- **Repository:** https://github.com/INK-USC/RiddleSense/
- **Paper:** https://inklab.usc.edu/RiddleSense/riddlesense_acl21_paper.pdf
- **Leaderboard:** https://inklab.usc.edu/RiddleSense/#leaderboard
- **Point of Contact:** [Yuchen Lin](yuchen.lin@usc.edu)

### Dataset Summary

Answering such a riddle-style question is a challenging cognitive process, in that it requires 
complex commonsense reasoning abilities, an understanding of figurative language, and counterfactual reasoning 
skills, which are all important abilities for advanced natural language understanding (NLU). However, 
there is currently no dedicated datasets aiming to test these abilities. Herein, we present RiddleSense, 
a new multiple-choice question answering task, which comes with the first large dataset (5.7k examples) for answering 
riddle-style commonsense questions. We systematically evaluate a wide range of models over the challenge, 
and point out that there is a large gap between the best-supervised model and human performance  suggesting 
intriguing future research in the direction of higher-order commonsense reasoning and linguistic creativity towards 
building advanced NLU systems. 

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

English

## Dataset Structure

### Data Instances

An example of 'train' looks as follows.
```
{
    "answerKey": "E",
    "choices": {
        "label": ["A", "B", "C", "D", "E"],
        "text": ["throw", "bit", "gallow", "mouse", "hole"]
    },
    "question": "A man is incarcerated in prison, and as his punishment he has to carry a one tonne bag of sand backwards and forwards across a field the size of a football pitch.  What is the one thing he can put in it to make it lighter?"
}
```

### Data Fields

Data Fields
The data fields are the same among all splits.

default
- `answerKey`: a string feature.
- `question`: a string feature.
- `choices`: a dictionary feature containing:
  - `label`: a string feature.
  - `text`: a string feature.

### Data Splits

|name|	train|	validation|	test|
|---|---|---|---|
|default|	3510|	1021|	1184|

## Dataset Creation

### Curation Rationale

[Needs More Information]

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

Dataset provided for research purposes only. Please check dataset license for additional information.

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

The copyright of RiddleSense dataset is consistent with the terms of use of the fan websites and the intellectual property and privacy rights of the original sources. All of our riddles and answers are from fan websites that can be accessed freely. The website owners state that you may print and download material from the sites solely for non-commercial use provided that we agree not to change or delete any copyright or proprietary notices from the materials. The dataset users must agree that they will only use the dataset for research purposes before they can access the both the riddles and our annotations. We do not vouch for the potential bias or fairness issue that might exist within the riddles. You do not have the right to redistribute them. Again, you must not use this dataset for any commercial purposes. 

### Citation Information

```
@InProceedings{lin-etal-2021-riddlesense,
title={RiddleSense: Reasoning about Riddle Questions Featuring Linguistic Creativity and Commonsense Knowledge},
author={Lin, Bill Yuchen and Wu, Ziyi and Yang, Yichi and Lee, Dong-Ho and Ren, Xiang},
journal={Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL-IJCNLP 2021): Findings},
year={2021}
}
```

### Contributions

Thanks to [@ziyiwu9494](https://github.com/ziyiwu9494) for adding this dataset.
