---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- unknown
multilinguality:
- monolingual
pretty_name: BlendedSkillTalk
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- conversational
task_ids:
- dialogue-generation
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
- **Paper:** [Can You Put it All Together: Evaluating Conversational Agents' Ability to Blend Skills](https://arxiv.org/abs/2004.08449v1)
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

### Data Instances

#### default

- **Size of downloaded dataset files:** 36.34 MB
- **Size of the generated dataset:** 14.38 MB
- **Total amount of disk used:** 50.71 MB

An example of 'train' looks as follows.
```
{
  'personas': ['my parents don t really speak english , but i speak italian and english.', 'i have three children.'],
  'additional_context': 'Backstreet Boys',
  'previous_utterance': ['Oh, I am a BIG fan of the Backstreet Boys!  Have you ever seen them performing live?', "No,I listen to their music a lot,  mainly the unbreakable which  is the Backstreet Boys' sixth studio album. "],
  'context': 'wizard_of_wikipedia',
  'free_messages': ['you are very knowledgeable, do you prefer nsync or bsb?', "haha kids of this days don't know them, i'm 46 and i still enjoying them, my kids only listen k-pop", "italian?haha that's strange, i only talk english and a little spanish "],
  'guided_messages': ["i don't have a preference, they are both great. All 3 of my kids get annoyed when I listen to them though.", 'Sometimes I sing their songs in Italian, that really annoys them lol.', 'My parents barely speak English, so I was taught both.  By the way, what is k-pop?'],
  'suggestions': {'convai2': ["i don't have a preference , both are pretty . do you have any hobbies ?", "do they the backstreet boys ? that's my favorite group .", 'are your kids interested in music ?'], 'empathetic_dialogues': ['I actually just discovered Imagine Dragons. I love them!', "Hahaha that just goes to show ya, age is just a umber!'", 'That would be hard! Do you now Spanish well?'], 'wizard_of_wikipedia': ['NSYNC Also had Lance Bass and Joey Fatone, sometimes called the Fat One.', 'Yes, there are a few K-Pop songs that I have heard good big in the USA. It is the most popular in South Korea and has Western elements of pop.', 'English, beleive it or not.']},
  'guided_chosen_suggestions': ['convai2', '', ''],
  'label_candidates': []}
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
- `guided_chosen_suggestions`: a `list` of `string` features.
- `label_candidates`: a `list` of `lists` of `string` features.

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