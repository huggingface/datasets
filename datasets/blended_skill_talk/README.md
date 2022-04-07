---
pretty_name: BlendedSkillTalk
languages:
- en
paperswithcode_id: blended-skill-talk
---

# Dataset Card for "blended_skill_talk"

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

- **Homepage:** [https://parl.ai/projects/bst/](https://parl.ai/projects/bst/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 36.34 MB
- **Size of the generated dataset:** 14.38 MB
- **Total amount of disk used:** 50.71 MB

### Dataset Summary

A dataset of 7k conversations explicitly designed to exhibit multiple conversation modes: displaying personality, having empathy, and demonstrating knowledge.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### default

- **Size of downloaded dataset files:** 36.34 MB
- **Size of the generated dataset:** 14.38 MB
- **Total amount of disk used:** 50.71 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "additional_context": "Electrician",
    "context": "wizard_of_wikipedia",
    "free_messages": "[\"Which level are you at?\", \"Thats great! How long have you been doing this work? \", \"Sounds like it could be a dangerous job at...",
    "guided_messages": ["I received on-the-job training when i first started", "For a good number of years now.", "That it is,especially if you dont take the proper measures", "Thats true,especially in this economy", "Do you enjoy it?", "I feel you. Stretch along the halls"],
    "personas": ["i work as an electrician.", "i always sleep 8 hours a day."],
    "previous_utterance": ["That sounds dangerous. Is it worth doing such a dangerous job?", "Wekk it is okay is you are well trained.  There are three levels: Apprentice, journeyman and Master."],
    "suggestions": "{\"convai2\": [\"i'm a grandmaster . i think they rank bridge players like chess .\", \"since i can remember . i enjoy it a lot .\", \"..."
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `personas`: a `list` of `string` features.
- `additional_context`: a `string` feature.
- `previous_utterance`: a `list` of `string` features.
- `context`: a `string` feature.
- `free_messages`: a `list` of `string` features.
- `guided_messgaes`: a `list` of `string` features.
- `suggestions`: a dictionary feature containing:
  - `convai2`: a `string` feature.
  - `empathetic_dialogues`: a `string` feature.
  - `wizard_of_wikipedia`: a `string` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default| 4819|      1009| 980|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@misc{smith2020evaluating,
    title={Can You Put it All Together: Evaluating Conversational Agents' Ability to Blend Skills},
    author={Eric Michael Smith and Mary Williamson and Kurt Shuster and Jason Weston and Y-Lan Boureau},
    year={2020},
    eprint={2004.08449},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.