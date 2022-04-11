---
annotations_creators:
- crowdsourced
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
- sequence-modeling
task_ids:
- dialogue-modeling
paperswithcode_id: mutualfriends
pretty_name: MutualFriends
---

# Dataset Card for MutualFriends

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

- **Homepage:** [COCOA](https://stanfordnlp.github.io/cocoa/)
- **Repository:** [Github repository](https://github.com/stanfordnlp/cocoa)
- **Paper:** [Learning Symmetric Collaborative Dialogue Agents with Dynamic Knowledge Graph Embeddings (ACL 2017)](https://arxiv.org/abs/1704.07130)
- **Codalab**: [Codalab](https://worksheets.codalab.org/worksheets/0xc757f29f5c794e5eb7bfa8ca9c945573/)

### Dataset Summary

Our goal is to build systems that collaborate with people by exchanging information through natural language and reasoning over structured knowledge base. In the MutualFriend task, two agents, A and B, each have a private knowledge base, which contains a list of friends with multiple attributes (e.g., name, school, major, etc.). The agents must chat with each other to find their unique mutual friend.

### Supported Tasks and Leaderboards

We consider two agents, each with a private knowledge base of items, who must communicate their knowledge to achieve a common goal. Specifically, we designed the MutualFriends task (see the figure below). Each agent has a list of friends with attributes like school, major etc. They must chat with each other to find the unique mutual friend.

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

An example looks like this.

```
{
  'uuid': 'C_423324a5fff045d78bef75a6f295a3f4'

  'scenario_uuid': 'S_hvmRM4YNJd55ecT5',
  'scenario_alphas': [0.30000001192092896, 1.0, 1.0],
  'scenario_attributes': {
    'name': ['School', 'Company', 'Location Preference'],
    'unique': [False, False, False],
    'value_type': ['school', 'company', 'loc_pref']
  },
  'scenario_kbs': [
    [
      [['School', 'Company', 'Location Preference'], ['Longwood College', 'Alton Steel', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['Salisbury State University', 'Leonard Green & Partners', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['New Mexico Highlands University', 'Crazy Eddie', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['Rhodes College', "Tully's Coffee", 'indoor']],
      [['School', 'Company', 'Location Preference'], ['Sacred Heart University', 'AMR Corporation', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['Salisbury State University', 'Molycorp', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['New Mexico Highlands University', 'The Hartford Financial Services Group', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['Sacred Heart University', 'Molycorp', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['Babson College', 'The Hartford Financial Services Group', 'indoor']]
    ],
    [
      [['School', 'Company', 'Location Preference'], ['National Technological University', 'Molycorp', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['Fairmont State College', 'Leonard Green & Partners', 'outdoor']],
      [['School', 'Company', 'Location Preference'], ['Johnson C. Smith University', 'Data Resources Inc.', 'outdoor']],
      [['School', 'Company', 'Location Preference'], ['Salisbury State University', 'Molycorp', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['Fairmont State College', 'Molycorp', 'outdoor']],
      [['School', 'Company', 'Location Preference'], ['University of South Carolina - Aiken', 'Molycorp', 'indoor']],
      [['School', 'Company', 'Location Preference'], ['University of South Carolina - Aiken', 'STX', 'outdoor']],
      [['School', 'Company', 'Location Preference'], ['National Technological University', 'STX', 'outdoor']],
      [['School', 'Company', 'Location Preference'], ['Johnson C. Smith University', 'Rockstar Games', 'indoor']]
    ]
  ],

  'agents': {
    '0': 'human',
    '1': 'human'
  },

  'outcome_reward': 1,

  'events': {
    'actions': ['message', 'message', 'message', 'message', 'select', 'select'],
    'agents': [1, 1, 0, 0, 1, 0],
    'data_messages': ['Hello', 'Do you know anyone who works at Molycorp?', 'Hi. All of my friends like the indoors.', 'Ihave two friends that work at Molycorp. They went to Salisbury and Sacred Heart.', '', ''],
    'data_selects': {
      'attributes': [
        [], [], [], [], ['School', 'Company', 'Location Preference'], ['School', 'Company', 'Location Preference']
      ],
      'values': [
        [], [], [], [], ['Salisbury State University', 'Molycorp', 'indoor'], ['Salisbury State University', 'Molycorp', 'indoor']
      ]
    },
    'start_times': [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
    'times': [1480737280.0, 1480737280.0, 1480737280.0, 1480737280.0, 1480737280.0, 1480737280.0]
  },
}
```

### Data Fields

- `uuid`: example id.
- `scenario_uuid`: scenario id.
- `scenario_alphas`: scenario alphas.
- `scenario_attributes`: all the attributes considered in the scenario. The dictionaries are liniearized: to reconstruct the dictionary of attribute i-th, one should extract the i-th elements of `unique`, `value_type` and `name`.
  - `unique`: bool.
  - `value_type`: code/type of the attribute.
  - `name`: name of the attribute.
- `scenario_kbs`: descriptions of the persons present in the two users' databases. List of two (one for each user in the dialogue). `scenario_kbs[i]` is a list of persons. Each person is represented as two lists (one for attribute names and the other for attribute values). The j-th element of attribute names corresponds to the j-th element of attribute values (linearized dictionary).
- `agents`: the two users engaged in the dialogue.
- `outcome_reward`: reward of the present dialogue.
- `events`: dictionary describing the dialogue. The j-th element of each sub-element of the dictionary describes the turn along the axis of the sub-element.
  - `actions`: type of turn (either `message` or `select`).
  - `agents`: who is talking? Agent 1 or 0?
  - `data_messages`: the string exchanged if `action==message`. Otherwise, empty string.
  - `data_selects`: selection of the user if `action==select`. Otherwise, empty selection/dictionary.
  - `start_times`: always -1 in these data.
  - `times`: sending time.

### Data Splits

There are 8967 dialogues for training, 1083 for validation and 1107 for testing.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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
@inproceedings{he-etal-2017-learning,
    title = "Learning Symmetric Collaborative Dialogue Agents with Dynamic Knowledge Graph Embeddings",
    author = "He, He  and
      Balakrishnan, Anusha  and
      Eric, Mihail  and
      Liang, Percy",
    booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P17-1162",
    doi = "10.18653/v1/P17-1162",
    pages = "1766--1776",
    abstract = "We study a \textit{symmetric collaborative dialogue} setting in which two agents, each with private knowledge, must strategically communicate to achieve a common goal. The open-ended dialogue state in this setting poses new challenges for existing dialogue systems. We collected a dataset of 11K human-human dialogues, which exhibits interesting lexical, semantic, and strategic elements. To model both structured knowledge and unstructured language, we propose a neural model with dynamic knowledge graph embeddings that evolve as the dialogue progresses. Automatic and human evaluations show that our model is both more effective at achieving the goal and more human-like than baseline neural and rule-based models.",
}
```

### Contributions

Thanks to [@VictorSanh](https://github.com/VictorSanh) for adding this dataset.