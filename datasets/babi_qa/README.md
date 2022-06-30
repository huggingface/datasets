---
pretty_name: BabiQa
annotations_creators:
- machine-generated
language_creators:
- machine-generated
language:
- en
license:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- question-answering-other-chained-qa
paperswithcode_id: babi-1
configs:
- en-10k-qa1
- en-10k-qa10
- en-10k-qa11
- en-10k-qa12
- en-10k-qa13
- en-10k-qa14
- en-10k-qa15
- en-10k-qa16
- en-10k-qa17
- en-10k-qa18
- en-10k-qa19
- en-10k-qa2
- en-10k-qa20
- en-10k-qa3
- en-10k-qa4
- en-10k-qa5
- en-10k-qa6
- en-10k-qa7
- en-10k-qa8
- en-10k-qa9
- en-qa1
- en-qa10
- en-qa11
- en-qa12
- en-qa13
- en-qa14
- en-qa15
- en-qa16
- en-qa17
- en-qa18
- en-qa19
- en-qa2
- en-qa20
- en-qa3
- en-qa4
- en-qa5
- en-qa6
- en-qa7
- en-qa8
- en-qa9
- en-valid-10k-qa1
- en-valid-10k-qa10
- en-valid-10k-qa11
- en-valid-10k-qa12
- en-valid-10k-qa13
- en-valid-10k-qa14
- en-valid-10k-qa15
- en-valid-10k-qa16
- en-valid-10k-qa17
- en-valid-10k-qa18
- en-valid-10k-qa19
- en-valid-10k-qa2
- en-valid-10k-qa20
- en-valid-10k-qa3
- en-valid-10k-qa4
- en-valid-10k-qa5
- en-valid-10k-qa6
- en-valid-10k-qa7
- en-valid-10k-qa8
- en-valid-10k-qa9
- en-valid-qa1
- en-valid-qa10
- en-valid-qa11
- en-valid-qa12
- en-valid-qa13
- en-valid-qa14
- en-valid-qa15
- en-valid-qa16
- en-valid-qa17
- en-valid-qa18
- en-valid-qa19
- en-valid-qa2
- en-valid-qa20
- en-valid-qa3
- en-valid-qa4
- en-valid-qa5
- en-valid-qa6
- en-valid-qa7
- en-valid-qa8
- en-valid-qa9
- hn-10k-qa1
- hn-10k-qa10
- hn-10k-qa11
- hn-10k-qa12
- hn-10k-qa13
- hn-10k-qa14
- hn-10k-qa15
- hn-10k-qa16
- hn-10k-qa17
- hn-10k-qa18
- hn-10k-qa19
- hn-10k-qa2
- hn-10k-qa20
- hn-10k-qa3
- hn-10k-qa4
- hn-10k-qa5
- hn-10k-qa6
- hn-10k-qa7
- hn-10k-qa8
- hn-10k-qa9
- hn-qa1
- hn-qa10
- hn-qa11
- hn-qa12
- hn-qa13
- hn-qa14
- hn-qa15
- hn-qa16
- hn-qa17
- hn-qa18
- hn-qa19
- hn-qa2
- hn-qa20
- hn-qa3
- hn-qa4
- hn-qa5
- hn-qa6
- hn-qa7
- hn-qa8
- hn-qa9
- shuffled-10k-qa1
- shuffled-10k-qa10
- shuffled-10k-qa11
- shuffled-10k-qa12
- shuffled-10k-qa13
- shuffled-10k-qa14
- shuffled-10k-qa15
- shuffled-10k-qa16
- shuffled-10k-qa17
- shuffled-10k-qa18
- shuffled-10k-qa19
- shuffled-10k-qa2
- shuffled-10k-qa20
- shuffled-10k-qa3
- shuffled-10k-qa4
- shuffled-10k-qa5
- shuffled-10k-qa6
- shuffled-10k-qa7
- shuffled-10k-qa8
- shuffled-10k-qa9
- shuffled-qa1
- shuffled-qa10
- shuffled-qa11
- shuffled-qa12
- shuffled-qa13
- shuffled-qa14
- shuffled-qa15
- shuffled-qa16
- shuffled-qa17
- shuffled-qa18
- shuffled-qa19
- shuffled-qa2
- shuffled-qa20
- shuffled-qa3
- shuffled-qa4
- shuffled-qa5
- shuffled-qa6
- shuffled-qa7
- shuffled-qa8
- shuffled-qa9
---


# Dataset Card for bAbi QA

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

- **Homepage:**[The bAbI project](https://research.fb.com/downloads/babi/)
- **Repository:**
- **Paper:** [arXiv Paper](https://arxiv.org/pdf/1502.05698.pdf)
- **Leaderboard:**
- **Point of Contact:** 
### Dataset Summary

The (20) QA bAbI tasks are a set of proxy tasks that evaluate reading comprehension via question answering. Our tasks measure understanding in several ways: whether a system is able to answer questions via chaining facts, simple induction, deduction and many more. The tasks are designed to be prerequisites for any system that aims to be capable of conversing with a human. The aim is to classify these tasks into skill sets,so that researchers can identify (and then rectify) the failings of their systems.

### Supported Tasks and Leaderboards

The dataset supports a set of 20 proxy story-based question answering tasks for various "types" in English and Hindi. The tasks are:

|task_no|task_name|
|----|------------|
|qa1 |single-supporting-fact|
|qa2 |two-supporting-facts|
|qa3 |three-supporting-facts|
|qa4 |two-arg-relations|
|qa5 |three-arg-relations|
|qa6 |yes-no-questions|
|qa7 |counting|
|qa8 |lists-sets|
|qa9 |simple-negation|
|qa10| indefinite-knowledge|
|qa11| basic-coreference|
|qa12| conjunction|
|qa13| compound-coreference|
|qa14| time-reasoning|
|qa15| basic-deduction|
|qa16| basic-induction|
|qa17| positional-reasoning|
|qa18| size-reasoning|
|qa19| path-finding|
|qa20| agents-motivations|


The "types" are are:

- `en`
   - the tasks in English, readable by humans.

- `hn`
   - the tasks in Hindi, readable by humans.
- `shuffled` 
   - the same tasks with shuffled letters so they are not readable by humans, and for existing parsers and taggers cannot be used in a straight-forward fashion to leverage extra resources-- in this case the learner is more forced to rely on the given training data. This mimics a learner being first presented a language and having to learn from scratch.
- `en-10k`, `shuffled-10k` and `hn-10k`  
   - the same tasks in the three formats, but with 10,000 training examples, rather than 1000 training examples.
- `en-valid` and `en-valid-10k`
   - are the same as `en` and `en10k` except the train sets have been conveniently split into train and valid portions (90% and 10% split).

To get a particular dataset, use `load_dataset('babi_qa',type=f'{type}',task_no=f'{task_no}')` where `type` is one of the types, and `task_no` is one of the task numbers. For example, `load_dataset('babi_qa', type='en', task_no='qa1')`.
### Languages



## Dataset Structure

### Data Instances
An instance from the `en-qa1` config's `train` split:

```
{'story': {'answer': ['', '', 'bathroom', '', '', 'hallway', '', '', 'hallway', '', '', 'office', '', '', 'bathroom'], 'id': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'], 'supporting_ids': [[], [], ['1'], [], [], ['4'], [], [], ['4'], [], [], ['11'], [], [], ['8']], 'text': ['Mary moved to the bathroom.', 'John went to the hallway.', 'Where is Mary?', 'Daniel went back to the hallway.', 'Sandra moved to the garden.', 'Where is Daniel?', 'John moved to the office.', 'Sandra journeyed to the bathroom.', 'Where is Daniel?', 'Mary moved to the hallway.', 'Daniel travelled to the office.', 'Where is Daniel?', 'John went back to the garden.', 'John moved to the bedroom.', 'Where is Sandra?'], 'type': [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]}}
```

### Data Fields

- `story`: a dictionary feature containing:
  - `id`: a `string` feature, which denotes the line number in the example.
  - `type`: a classification label, with possible values including `context`, `question`, denoting whether the text is context or a question.
  - `text`: a `string` feature the text present, whether it is a question or context.
  - `supporting_ids`: a `list` of `string` features containing the line numbers of the lines in the example which support the answer.
  - `answer`: a `string` feature containing the answer to the question, or an empty string if the `type`s is not `question`.

### Data Splits

The splits and corresponding sizes are:

|                   |   train |   test |   validation |
|-------------------|---------|--------|--------------|
| en-qa1            |     200 |    200 |          -   |
| en-qa2            |     200 |    200 |          -   |
| en-qa3            |     200 |    200 |          -   |
| en-qa4            |    1000 |   1000 |          -   |
| en-qa5            |     200 |    200 |          -   |
| en-qa6            |     200 |    200 |          -   |
| en-qa7            |     200 |    200 |          -   |
| en-qa8            |     200 |    200 |          -   |
| en-qa9            |     200 |    200 |          -   |
| en-qa10           |     200 |    200 |          -   |
| en-qa11           |     200 |    200 |          -   |
| en-qa12           |     200 |    200 |          -   |
| en-qa13           |     200 |    200 |          -   |
| en-qa14           |     200 |    200 |          -   |
| en-qa15           |     250 |    250 |          -   |
| en-qa16           |    1000 |   1000 |          -   |
| en-qa17           |     125 |    125 |          -   |
| en-qa18           |     198 |    199 |          -   |
| en-qa19           |    1000 |   1000 |          -   |
| en-qa20           |      94 |     93 |          -   |
| en-10k-qa1        |    2000 |    200 |          -   |
| en-10k-qa2        |    2000 |    200 |          -   |
| en-10k-qa3        |    2000 |    200 |          -   |
| en-10k-qa4        |   10000 |   1000 |          -   |
| en-10k-qa5        |    2000 |    200 |          -   |
| en-10k-qa6        |    2000 |    200 |          -   |
| en-10k-qa7        |    2000 |    200 |          -   |
| en-10k-qa8        |    2000 |    200 |          -   |
| en-10k-qa9        |    2000 |    200 |          -   |
| en-10k-qa10       |    2000 |    200 |          -   |
| en-10k-qa11       |    2000 |    200 |          -   |
| en-10k-qa12       |    2000 |    200 |          -   |
| en-10k-qa13       |    2000 |    200 |          -   |
| en-10k-qa14       |    2000 |    200 |          -   |
| en-10k-qa15       |    2500 |    250 |          -   |
| en-10k-qa16       |   10000 |   1000 |          -   |
| en-10k-qa17       |    1250 |    125 |          -   |
| en-10k-qa18       |    1978 |    199 |          -   |
| en-10k-qa19       |   10000 |   1000 |          -   |
| en-10k-qa20       |     933 |     93 |          -   |
| en-valid-qa1      |     180 |    200 |           20 |
| en-valid-qa2      |     180 |    200 |           20 |
| en-valid-qa3      |     180 |    200 |           20 |
| en-valid-qa4      |     900 |   1000 |          100 |
| en-valid-qa5      |     180 |    200 |           20 |
| en-valid-qa6      |     180 |    200 |           20 |
| en-valid-qa7      |     180 |    200 |           20 |
| en-valid-qa8      |     180 |    200 |           20 |
| en-valid-qa9      |     180 |    200 |           20 |
| en-valid-qa10     |     180 |    200 |           20 |
| en-valid-qa11     |     180 |    200 |           20 |
| en-valid-qa12     |     180 |    200 |           20 |
| en-valid-qa13     |     180 |    200 |           20 |
| en-valid-qa14     |     180 |    200 |           20 |
| en-valid-qa15     |     225 |    250 |           25 |
| en-valid-qa16     |     900 |   1000 |          100 |
| en-valid-qa17     |     113 |    125 |           12 |
| en-valid-qa18     |     179 |    199 |           19 |
| en-valid-qa19     |     900 |   1000 |          100 |
| en-valid-qa20     |      85 |     93 |            9 |
| en-valid-10k-qa1  |    1800 |    200 |          200 |
| en-valid-10k-qa2  |    1800 |    200 |          200 |
| en-valid-10k-qa3  |    1800 |    200 |          200 |
| en-valid-10k-qa4  |    9000 |   1000 |         1000 |
| en-valid-10k-qa5  |    1800 |    200 |          200 |
| en-valid-10k-qa6  |    1800 |    200 |          200 |
| en-valid-10k-qa7  |    1800 |    200 |          200 |
| en-valid-10k-qa8  |    1800 |    200 |          200 |
| en-valid-10k-qa9  |    1800 |    200 |          200 |
| en-valid-10k-qa10 |    1800 |    200 |          200 |
| en-valid-10k-qa11 |    1800 |    200 |          200 |
| en-valid-10k-qa12 |    1800 |    200 |          200 |
| en-valid-10k-qa13 |    1800 |    200 |          200 |
| en-valid-10k-qa14 |    1800 |    200 |          200 |
| en-valid-10k-qa15 |    2250 |    250 |          250 |
| en-valid-10k-qa16 |    9000 |   1000 |         1000 |
| en-valid-10k-qa17 |    1125 |    125 |          125 |
| en-valid-10k-qa18 |    1781 |    199 |          197 |
| en-valid-10k-qa19 |    9000 |   1000 |         1000 |
| en-valid-10k-qa20 |     840 |     93 |           93 |
| hn-qa1            |     200 |    200 |          -   |
| hn-qa2            |     200 |    200 |          -   |
| hn-qa3            |     167 |    167 |          -   |
| hn-qa4            |    1000 |   1000 |          -   |
| hn-qa5            |     200 |    200 |          -   |
| hn-qa6            |     200 |    200 |          -   |
| hn-qa7            |     200 |    200 |          -   |
| hn-qa8            |     200 |    200 |          -   |
| hn-qa9            |     200 |    200 |          -   |
| hn-qa10           |     200 |    200 |          -   |
| hn-qa11           |     200 |    200 |          -   |
| hn-qa12           |     200 |    200 |          -   |
| hn-qa13           |     125 |    125 |          -   |
| hn-qa14           |     200 |    200 |          -   |
| hn-qa15           |     250 |    250 |          -   |
| hn-qa16           |    1000 |   1000 |          -   |
| hn-qa17           |     125 |    125 |          -   |
| hn-qa18           |     198 |    198 |          -   |
| hn-qa19           |    1000 |   1000 |          -   |
| hn-qa20           |      93 |     94 |          -   |
| hn-10k-qa1        |    2000 |    200 |          -   |
| hn-10k-qa2        |    2000 |    200 |          -   |
| hn-10k-qa3        |    1667 |    167 |          -   |
| hn-10k-qa4        |   10000 |   1000 |          -   |
| hn-10k-qa5        |    2000 |    200 |          -   |
| hn-10k-qa6        |    2000 |    200 |          -   |
| hn-10k-qa7        |    2000 |    200 |          -   |
| hn-10k-qa8        |    2000 |    200 |          -   |
| hn-10k-qa9        |    2000 |    200 |          -   |
| hn-10k-qa10       |    2000 |    200 |          -   |
| hn-10k-qa11       |    2000 |    200 |          -   |
| hn-10k-qa12       |    2000 |    200 |          -   |
| hn-10k-qa13       |    1250 |    125 |          -   |
| hn-10k-qa14       |    2000 |    200 |          -   |
| hn-10k-qa15       |    2500 |    250 |          -   |
| hn-10k-qa16       |   10000 |   1000 |          -   |
| hn-10k-qa17       |    1250 |    125 |          -   |
| hn-10k-qa18       |    1977 |    198 |          -   |
| hn-10k-qa19       |   10000 |   1000 |          -   |
| hn-10k-qa20       |     934 |     94 |          -   |
| shuffled-qa1      |     200 |    200 |          -   |
| shuffled-qa2      |     200 |    200 |          -   |
| shuffled-qa3      |     200 |    200 |          -   |
| shuffled-qa4      |    1000 |   1000 |          -   |
| shuffled-qa5      |     200 |    200 |          -   |
| shuffled-qa6      |     200 |    200 |          -   |
| shuffled-qa7      |     200 |    200 |          -   |
| shuffled-qa8      |     200 |    200 |          -   |
| shuffled-qa9      |     200 |    200 |          -   |
| shuffled-qa10     |     200 |    200 |          -   |
| shuffled-qa11     |     200 |    200 |          -   |
| shuffled-qa12     |     200 |    200 |          -   |
| shuffled-qa13     |     200 |    200 |          -   |
| shuffled-qa14     |     200 |    200 |          -   |
| shuffled-qa15     |     250 |    250 |          -   |
| shuffled-qa16     |    1000 |   1000 |          -   |
| shuffled-qa17     |     125 |    125 |          -   |
| shuffled-qa18     |     198 |    199 |          -   |
| shuffled-qa19     |    1000 |   1000 |          -   |
| shuffled-qa20     |      94 |     93 |          -   |
| shuffled-10k-qa1  |    2000 |    200 |          -   |
| shuffled-10k-qa2  |    2000 |    200 |          -   |
| shuffled-10k-qa3  |    2000 |    200 |          -   |
| shuffled-10k-qa4  |   10000 |   1000 |          -   |
| shuffled-10k-qa5  |    2000 |    200 |          -   |
| shuffled-10k-qa6  |    2000 |    200 |          -   |
| shuffled-10k-qa7  |    2000 |    200 |          -   |
| shuffled-10k-qa8  |    2000 |    200 |          -   |
| shuffled-10k-qa9  |    2000 |    200 |          -   |
| shuffled-10k-qa10 |    2000 |    200 |          -   |
| shuffled-10k-qa11 |    2000 |    200 |          -   |
| shuffled-10k-qa12 |    2000 |    200 |          -   |
| shuffled-10k-qa13 |    2000 |    200 |          -   |
| shuffled-10k-qa14 |    2000 |    200 |          -   |
| shuffled-10k-qa15 |    2500 |    250 |          -   |
| shuffled-10k-qa16 |   10000 |   1000 |          -   |
| shuffled-10k-qa17 |    1250 |    125 |          -   |
| shuffled-10k-qa18 |    1978 |    199 |          -   |
| shuffled-10k-qa19 |   10000 |   1000 |          -   |
| shuffled-10k-qa20 |     933 |     93 |          -   |


## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Code to generate tasks is available on [github](https://github.com/facebook/bAbI-tasks)

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

Jesse Dodge and Andreea Gane and Xiang Zhang and Antoine Bordes and Sumit Chopra and Alexander Miller and Arthur Szlam and Jason Weston, at Facebook Research.

### Licensing Information

```
Creative Commons Attribution 3.0 License
```

### Citation Information

```
@misc{dodge2016evaluating,
      title={Evaluating Prerequisite Qualities for Learning End-to-End Dialog Systems}, 
      author={Jesse Dodge and Andreea Gane and Xiang Zhang and Antoine Bordes and Sumit Chopra and Alexander Miller and Arthur Szlam and Jason Weston},
      year={2016},
      eprint={1511.06931},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```


### Contributions

Thanks to [@gchhablani](https://github.com/gchhablani) for adding this dataset.
