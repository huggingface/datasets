---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
- machine-generated
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
- structure-prediction
- text-classification
task_ids:
- dialogue-modeling
- multi-class-classification
- parsing
---

# Dataset Card for MultiWOZ

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

- **Repository:** [MultiWOZ 2.2 github repository](https://github.com/budzianowski/multiwoz/tree/master/data/MultiWOZ_2.2)
- **Paper:** [MultiWOZ v2](https://arxiv.org/abs/1810.00278), and [MultiWOZ v2.2](https://www.aclweb.org/anthology/2020.nlp4convai-1.13.pdf)
- **Point of Contact:** [Paweł Budzianowski](pfb30@cam.ac.uk)

### Dataset Summary

Multi-Domain Wizard-of-Oz dataset (MultiWOZ), a fully-labeled collection of human-human written conversations spanning over multiple domains and topics.
MultiWOZ 2.1 (Eric et al., 2019) identified and fixed many erroneous annotations and user utterances in the original version, resulting in an
improved version of the dataset. MultiWOZ 2.2 is a yet another improved version of this dataset, which identifies and fixes dialogue state annotation errors
across 17.3% of the utterances on top of MultiWOZ 2.1 and redefines the ontology by disallowing vocabularies of slots with a large number of possible values
(e.g., restaurant name, time of booking) and introducing standardized slot span annotations for these slots.

### Supported Tasks and Leaderboards

This dataset supports a range of task.
- **Generative dialogue modeling** or `dialogue-modeling`: the text of the dialogues can be used to train a sequence model on the utterances. Performance on this task is typically evaluated with delexicalized-[BLEU](https://huggingface.co/metrics/bleu), inform rate and request success.
- **Intent state tracking**, a `multi-class-classification` task: predict the belief state of the user side of the conversation, performance is measured by [F1](https://huggingface.co/metrics/f1).
- **Dialog act prediction**, a `parsing` task: parse an utterance into the corresponding dialog acts for the system to use. [F1](https://huggingface.co/metrics/f1) is typically reported.

### Languages

The text in the dataset is in English (`en`).

## Dataset Structure

### Data Instances

A data instance is a full multi-turn dialogue between a `USER` and a `SYSTEM`. Each turn has a single utterance, e.g.:
```
['What fun places can I visit in the East?',
 'We have five spots which include boating, museums and entertainment. Any preferences that you have?']
```
The utterances of the `USER` are also annotated with frames denoting their intent and believe state:
```
[{'service': ['attraction'],
  'slots': [{'copy_from': [],
    'copy_from_value': [],
    'exclusive_end': [],
    'slot': [],
    'start': [],
    'value': []}],
  'state': [{'active_intent': 'find_attraction',
    'requested_slots': [],
    'slots_values': {'slots_values_list': [['east']],
     'slots_values_name': ['attraction-area']}}]},
 {'service': [], 'slots': [], 'state': []}]
```
Finally, each of the utterances is annotated with dialog acts which provide a structured representation of what the `USER` or `SYSTEM` is inquiring or giving information about.
```
[{'dialog_act': {'act_slots': [{'slot_name': ['east'],
     'slot_value': ['area']}],
   'act_type': ['Attraction-Inform']},
  'span_info': {'act_slot_name': ['area'],
   'act_slot_value': ['east'],
   'act_type': ['Attraction-Inform'],
   'span_end': [39],
   'span_start': [35]}},
 {'dialog_act': {'act_slots': [{'slot_name': ['none'], 'slot_value': ['none']},
    {'slot_name': ['boating', 'museums', 'entertainment', 'five'],
     'slot_value': ['type', 'type', 'type', 'choice']}],
   'act_type': ['Attraction-Select', 'Attraction-Inform']},
  'span_info': {'act_slot_name': ['type', 'type', 'type', 'choice'],
   'act_slot_value': ['boating', 'museums', 'entertainment', 'five'],
   'act_type': ['Attraction-Inform',
    'Attraction-Inform',
    'Attraction-Inform',
    'Attraction-Inform'],
   'span_end': [40, 49, 67, 12],
   'span_start': [33, 42, 54, 8]}}]
```

### Data Fields

Each dialogue instance has the following fields:
- `dialogue_id`: a unique ID identifying the dialog. The MUL and PMUL names refer to strictly multi domain dialogues (at least 2 main domains are involved) while the SNG, SSNG and WOZ names refer to single domain dialogues with potentially sub-domains like booking.
- `services`: a list of services mentioned in the dialog, such as `train` or `hospitals`.
- `turns`: the sequence of utterances with their annotations, including:
  - `turn_id`: a turn identifier, unique per dialog.
  - `speaker`: either the `USER` or `SYSTEM`.
  - `utterance`: the text of the utterance.
  - `dialogue_acts`: The structured parse of the utterance into dialog acts in the system's grammar
    - `act_type`: Such as e.g. `Attraction-Inform` to seek or provide information about an `attraction`
    - `act_slots`: provide more details about the action
    - `span_info`: maps these `act_slots` to the `utterance` text.
  - `frames`: only for `USER` utterances, track the user's belief state, i.e. a structured representation of what they are trying to achieve in the fialog. This decomposes into:
    - `service`: the service they are interested in
    - `state`: their belief state including their `active_intent` and further information expressed in `requested_slots`
    - `slots`: a mapping of the `requested_slots` to where they are mentioned in the text. It takes one of two forms, detailed next:
The first type are span annotations that identify the location where slot values have been mentioned in the utterances for non-categorical slots. These span annotations are represented as follows:
```
{
  "slots": [
    {
      "slot": String of slot name.
      "start": Int denoting the index of the starting character in the utterance corresponding to the slot value.
      "exclusive_end": Int denoting the index of the character just after the last character corresponding to the slot value in the utterance. In python, utterance[start:exclusive_end] gives the slot value.
      "value": String of value. It equals to utterance[start:exclusive_end], where utterance is the current utterance in string.
    }
  ]
}
```
There are also some non-categorical slots whose values are carried over from another slot in the dialogue state. Their values don"t explicitly appear in the utterances. For example, a user utterance can be "I also need a taxi from the restaurant to the hotel.", in which the state values of "taxi-departure" and "taxi-destination" are respectively carried over from that of "restaurant-name" and "hotel-name". For these slots, instead of annotating them as spans, a "copy from" annotation identifies the slot it copies the value from. This annotation is formatted as follows,
```
{
  "slots": [
    {
      "slot": Slot name string.
      "copy_from": The slot to copy from.
      "value": A list of slot values being . It corresponds to the state values of the "copy_from" slot.
    }
  ]
}
```

### Data Splits

The dataset is split into a `train`, `validation`, and `test` split with the following sizes:

|                            | Tain   | Valid | Test |
| -----                      | ------ | ----- | ---- |
| Number of dialogues        | 8438   | 1000  | 1000 |
| Number of turns            | 42190  | 5000  | 5000 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

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

The initial dataset (Versions 1.0 and 2.0) was created by a team of researchers from the [Cambridge Dialogue Systems Group](https://mi.eng.cam.ac.uk/research/dialogue/corpora/). Version 2.1 was developed on top of v2.0 by a team from Amazon, and v2.2 was developed by a team of Google researchers.

### Licensing Information

The dataset is released under the Apache License 2.0.

### Citation Information

You can cite the following for the various versions of MultiWOZ:

Version 1.0
```
@inproceedings{ramadan2018large,
  title={Large-Scale Multi-Domain Belief Tracking with Knowledge Sharing},
  author={Ramadan, Osman and Budzianowski, Pawe{\l} and Gasic, Milica},
  booktitle={Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics},
  volume={2},
  pages={432--437},
  year={2018}
}
```

Version 2.0
```
@inproceedings{budzianowski2018large,
    Author = {Budzianowski, Pawe{\l} and Wen, Tsung-Hsien and Tseng, Bo-Hsiang  and Casanueva, I{\~n}igo and Ultes Stefan and Ramadan Osman and Ga{\v{s}}i\'c, Milica},
    title={MultiWOZ - A Large-Scale Multi-Domain Wizard-of-Oz Dataset for Task-Oriented Dialogue Modelling},
    booktitle={Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
    year={2018}
}
```

Version 2.1
```
@article{eric2019multiwoz,
  title={MultiWOZ 2.1: Multi-Domain Dialogue State Corrections and State Tracking Baselines},
  author={Eric, Mihail and Goel, Rahul and Paul, Shachi and Sethi, Abhishek and Agarwal, Sanchit and Gao, Shuyag and Hakkani-Tur, Dilek},
  journal={arXiv preprint arXiv:1907.01669},
  year={2019}
}
```

Version 2.2
```
@inproceedings{zang2020multiwoz,
  title={MultiWOZ 2.2: A Dialogue Dataset with Additional Annotation Corrections and State Tracking Baselines},
  author={Zang, Xiaoxue and Rastogi, Abhinav and Sunkara, Srinivas and Gupta, Raghav and Zhang, Jianguo and Chen, Jindong},
  booktitle={Proceedings of the 2nd Workshop on Natural Language Processing for Conversational AI, ACL 2020},
  pages={109--117},
  year={2020}
}
```
