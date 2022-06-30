---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-story-completion
paperswithcode_id: null
pretty_name: Story Cloze Test
---

# Dataset Card for "story_cloze"

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

- **Homepage:** [https://cs.rochester.edu/nlp/rocstories/](https://cs.rochester.edu/nlp/rocstories/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [Lsdsem 2017 shared task: The story cloze test](https://aclanthology.org/W17-0906.pdf)
- **Point of Contact:** [Nasrin Mostafazadeh](nasrinm@cs.rochester.edu)
- **Size of downloaded dataset files:** 2.03 MB
- **Size of the generated dataset:** 2.03 MB
- **Total amount of disk used:** 2.05 MB

### Dataset Summary

Story Cloze Test' is a new commonsense reasoning framework for evaluating story understanding, 
story generation, and script learning.This test requires a system to choose the correct ending 
to a four-sentence story.

### Supported Tasks and Leaderboards

commonsense reasoning

### Languages

English

## Dataset Structure

### Data Instances

- **Size of downloaded dataset files:** 2.03 MB
- **Size of the generated dataset:** 2.03 MB
- **Total amount of disk used:** 2.05 MB

An example of 'train' looks as follows.
```
{'answer_right_ending': 1,
 'input_sentence_1': 'Rick grew up in a troubled household.',
 'input_sentence_2': 'He never found good support in family, and turned to gangs.',
 'input_sentence_3': "It wasn't long before Rick got shot in a robbery.",
 'input_sentence_4': 'The incident caused him to turn a new leaf.',
 'sentence_quiz1': 'He is happy now.',
 'sentence_quiz2': 'He joined a gang.',
 'story_id': '138d5bfb-05cc-41e3-bf2c-fa85ebad14e2'}
```

### Data Fields

The data fields are the same among all splits.

- `input_sentence_1`: The first statement in the story.
- `input_sentence_2`: The second statement in the story.
- `input_sentence_3`: The third statement in the story.
- `input_sentence_4`: The forth statement in the story.
- `sentence_quiz1`: first possible continuation of the story. 
- `sentence_quiz2`: second possible continuation of the story. 
- `answer_right_ending`: correct possible ending; either 1 or 2. 
- `story_id`: story id. 

### Data Splits

| name  |validation |test|
|-------|-----:|---:|
|2016|1871|1871|
|2018|1571|-|

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
@inproceedings{mostafazadeh2017lsdsem,
  title={Lsdsem 2017 shared task: The story cloze test},
  author={Mostafazadeh, Nasrin and Roth, Michael and Louis, Annie and Chambers, Nathanael and Allen, James},
  booktitle={Proceedings of the 2nd Workshop on Linking Models of Lexical, Sentential and Discourse-level Semantics},
  pages={46--51},
  year={2017}
}

```


### Contributions

Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai).