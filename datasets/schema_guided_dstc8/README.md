---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
- machine-generated
languages:
- en
licenses:
- cc-by-sa-4.0
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

# Dataset Card for The Schema-Guided Dialogue Dataset

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

- **Repository:** [Github repository for The Schema-Guided Dialogue Dataset](https://github.com/google-research-datasets/dstc8-schema-guided-dialogue)
- **Paper:** [Towards Scalable Multi-Domain Conversational Agents: The Schema-Guided Dialogue Dataset](https://arxiv.org/abs/1909.05855)
- **Point of Contact:** [abhirast@google.com](abhirast@google.com)

### Dataset Summary

The Schema-Guided Dialogue dataset (SGD) was developed for the Dialogue State Tracking task of the Eights Dialogue Systems Technology Challenge (dstc8).
The SGD dataset consists of over 18k annotated multi-domain, task-oriented conversations between a human and a virtual assistant. These conversations involve interactions with services and APIs spanning 17 domains, ranging from banks and events to media, calendar, travel, and weather. For most of these domains, the SGD dataset contains multiple different APIs, many of which have overlapping functionalities but different interfaces, which reflects common real-world scenarios.

### Supported Tasks and Leaderboards

This dataset is designed to serve as an effective test-bed for intent prediction, slot filling, state tracking (i.e., estimating the user's goal) and language generation, among other tasks for large-scale virtual assistants:
- **Generative dialogue modeling** or `dialogue-modeling`: the text of the dialogues can be used to train a sequence model on the utterances. Performance on this task is typically evaluated with delexicalized-[BLEU](https://huggingface.co/metrics/bleu), inform rate and request success.
- **Intent state tracking**, a `multi-class-classification` task: predict the belief state of the user side of the conversation, performance is measured by [F1](https://huggingface.co/metrics/f1).
- **Action prediction**, a `parsing` task: parse an utterance into the corresponding dialog acts for the system to use. [F1](https://huggingface.co/metrics/f1) is typically reported.

### Languages

The text in the dataset is in English (`en`).

## Dataset Structure

### Data Instances

- `dialogues` configuration (default): Each dialogue is represented as a sequence of turns, each containing a user or system utterance. The annotations for each turn are grouped into frames, where each frame corresponds to a single service. The annotations for user turns include the active intent, the dialogue state and slot spans for the different slots values mentioned in the turn. For system turns, we have the system actions representing the semantics of the system utterance. Each system action is represented using a dialogue act with optional parameters.
- `schema` configuration: In addition to the dialogues, for each service used in the dataset, a normalized representation of the interface exposed is provided as the schema. The schema contains details like the name of the service, the list of tasks supported by the service (intents) and the attributes of the entities used by the service (slots). The schema also contains natural language descriptions of the service, intents and slots which can be used for developing models which can condition their predictions on the schema.

### Data Fields

Each dialog instance has the following fields:
- `dialogue_id`: A unique identifier for a dialogue.
- `services`: A list of services present in the dialogue.
- `turns`: A list of annotated system or user utterances. Each turn consists of the following fields:
  - `speaker`: The speaker for the turn. Either `USER` or `SYSTEM`.
  - `utterance`: A string containing the natural language utterance.
  - `frames`: A list of frames, each frame containing annotations for a single service and consists of the following fields:
    - `service`: The name of the service corresponding to the frame. The slots and intents used in the following fields are taken from the schema of this service.
    - `slots`: A list of slot spans in the utterance, only provided for non-categorical slots. Each slot span contains the following fields:
      - `slot`: The name of the slot.
      - `start`: The index of the starting character in the utterance corresponding to the slot value.
      - `exclusive_end`: The index of the character just after the last character corresponding to the slot value in the utterance.
    - `actions`: A list of actions corresponding to the system. Each action has the following fields:
      - `act`: The type of action.
      - `slot`: (optional) A slot argument for some of the actions.
      - `values`: (optional) A list of values assigned to the slot. If the values list is non-empty, then the slot must be present.
      - `canonical_values`: (optional) The values in their canonicalized form as used by the service. It is a list of strings of the same length as values.
    - `service_call`: (system turns only, optional) The request sent to the service. It consists of the following fields:
      - `method`: The name of the intent or function of the service or API being executed.
      - `parameters`: A pair of lists of the same lengths: `parameter_slot_name` contains slot names and `parameter_canonical_value` contains the corresponding values in their canonicalized form.
    - `service_results`: (system turns only, optional) A list of entities containing the results obtained from the service. It is only available for turns in which a service call is made. Each entity is represented as a pair of lists of the same length: `service_slot_name` contains slot names and `service_canonical_value` contains the corresponding canonical values.
    - `state`: (user turns only) The dialogue state corresponding to the service. It consists of the following fields:
      - `active_intent`: The intent corresponding to the service of the frame which is currently being fulfilled by the system. It takes the value "NONE" if none of the intents are active.
      - `requested_slots`: A list of slots requested by the user in the current turn.
      - `slot_values`: A pair of lists of the same lengths: `slot_name` contains slot names and `slot_value_list` contains the corresponding lists of strings. For categorical slots, this list contains a single value assigned to the slot. For non-categorical slots, all the values in this list are spoken variations of each other and are equivalent (e.g, "6 pm", "six in the evening", "evening at 6" etc.).


### Data Splits

The dataset is split into a `train`, `validation`, and `test` split with the following sizes:

|                            | Tain   | Valid | Test  |
| -----                      | ------ | ----- | ----- |
| Number of dialogues        | 16142  | 2482  | 4201  |
| Number of turns            | 48426  | 7446  | 12603 |


## Dataset Creation

### Curation Rationale

The data was collected by first using a dialogue simulator to generate dialogue outlines first and then paraphrasing them to obtain natural utterances. Using a dialogue simulator ensures the coverage of a large variety of dialogue flows by filtering out similar flows in the simulation phase to create a diverse dataset, and dialogues can be generated with their annotation, as opposed to a Wizard-of-Oz setup which is prone to manual annotation errors.

### Source Data

#### Initial Data Collection and Normalization

The dialogue outlines are first generated by a simulator. The dialogue simulator interacts with the services to generate dialogue outlines. It consists of two
agents playing the roles of the user and the system, interacting with each other using a finite set of actions specified through dialogue acts over a probabilistic automaton designed to capture varied dialogue trajectories. It is worth noting that the simulation automaton does not include any domain-specific constraints: all domain-specific constraints are encoded in the schema and scenario.

The dialogue paraphrasing framework then converts the outlines generated by the simulator into a natural conversation. Users may refer to the slot values in the dialogue acts in various different ways during the conversation, e.g., “los angeles” may be referred to as “LA” or “LAX”. To introduce these natural variations in the slot values, different slot values are replaced with a randomly selected variation while being kept consistent across user turns in a dialogue. The actions are then converted to pseudo-natural language utterances using a set of manually defined action-to-text templates, and the resulting utterances for the different actions in a turn are concatenated together.

Finally, the dialogue transformed by these steps is sent to the crowd workers to be reformulated into more natural language. One crowd worker is tasked with paraphrasing all utterances of a dialogue to ensure naturalness and coherence. The crowd workers are asked to exactly repeat the slot values in their paraphrases so that the span indices for the slots can be recovered via string matching.

#### Who are the source language producers?

The language structure is machine-generated, and the language realizations are produced by crowd workers. The dataset paper does not provide demographic information for the crowd workers.

### Annotations

#### Annotation process

The annotations are automatically obtained during the initial sampling process and by string matching after reformulation.

#### Who are the annotators?

[N/A]

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

The dataset was created by a team of researchers working at Google Mountain View.

### Licensing Information

The dataset is released under CC BY-SA 4.0 license.

### Citation Information

For the DSCT8 task, please cite:
```
@article{corr/abs-2002-01359,
  author    = {Abhinav Rastogi and
               Xiaoxue Zang and
               Srinivas Sunkara and
               Raghav Gupta and
               Pranav Khaitan},
  title     = {Schema-Guided Dialogue State Tracking Task at {DSTC8}},
  journal   = {CoRR},
  volume    = {abs/2002.01359},
  year      = {2020},
  url       = {https://arxiv.org/abs/2002.01359},
  archivePrefix = {arXiv},
  eprint    = {2002.01359}
}
```

For the initial release paper please cite:
```
@inproceedings{aaai/RastogiZSGK20,
  author    = {Abhinav Rastogi and
               Xiaoxue Zang and
               Srinivas Sunkara and
               Raghav Gupta and
               Pranav Khaitan},
  title     = {Towards Scalable Multi-Domain Conversational Agents: The Schema-Guided
               Dialogue Dataset},
  booktitle = {The Thirty-Fourth {AAAI} Conference on Artificial Intelligence, {AAAI}
               2020, The Thirty-Second Innovative Applications of Artificial Intelligence
               Conference, {IAAI} 2020, The Tenth {AAAI} Symposium on Educational
               Advances in Artificial Intelligence, {EAAI} 2020, New York, NY, USA,
               February 7-12, 2020},
  pages     = {8689--8696},
  publisher = {{AAAI} Press},
  year      = {2020},
  url       = {https://aaai.org/ojs/index.php/AAAI/article/view/6394}
}
```
