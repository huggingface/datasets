---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- Microsoft Research Data License Agreement
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
paperswithcode_id: metalwoz
---

# Dataset Card for MetaLWOz

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

- **Repository:** [MetaLWOz Project Website](https://www.microsoft.com/en-us/research/project/metalwoz/)
- **Paper:** [Fast Domain Adaptation for Goal-Oriented Dialogue Using a Hybrid Generative-Retrieval Transformer](https://ieeexplore.ieee.org/abstract/document/9053599), and [Hybrid Generative-Retrieval Transformers for Dialogue Domain Adaptation](https://arxiv.org/pdf/2003.01680.pdf)
- **Point of Contact:** [Hannes Schulz](https://www.microsoft.com/en-us/research/people/haschulz/)

### Dataset Summary

MetaLWOz: A Dataset of Multi-Domain Dialogues for the Fast Adaptation of Conversation Models. 
We introduce the Meta-Learning Wizard of Oz (MetaLWOz) dialogue dataset for developing fast adaptation methods for 
conversation models. This data can be used to train task-oriented dialogue models, specifically to develop methods to 
quickly simulate user responses with a small amount of data. Such fast-adaptation models fall into the research areas 
of transfer learning and meta learning. The dataset consists of 37,884 crowdsourced dialogues recorded between two 
human users in a Wizard of Oz setup, in which one was instructed to behave like a bot, and the other a true human 
user. The users are assigned a task belonging to a particular domain, for example booking a reservation at a 
particular restaurant, and work together to complete the task. Our dataset spans 47 domains having 227 tasks total. 
Dialogues are a minimum of 10 turns long.

### Supported Tasks and Leaderboards

This dataset supports a range of task.
- **Generative dialogue modeling** or `dialogue-modeling`: This data can be used to train task-oriented dialogue
 models, specifically to develop methods to quickly simulate user responses with a small amount of data. Such fast
-adaptation models fall into the research areas of transfer learning and meta learning. The text of the dialogues
  can be used to train a sequence model on the utterances. 
  Example of sample input/output is given in section [Data Instances](#data-instances)
 
  

### Languages

The text in the dataset is in English (`en`).

## Dataset Structure

### Data Instances

A data instance is a full multi-turn dialogue between two crowd-workers, one had the role of being a `bot`, and the other one was the `user`. Both were
given a `domain` and a `task`. Each turn has a single utterance, e.g.:
```
Domain: Ski
User Task: You want to know if there are good ski hills an
hour’s drive from your current location.
Bot Task: Tell the user that there are no ski hills in their
immediate location.
Bot: Hello how may I help you?
User: Is there any good ski hills an hour’s drive from my
current location?
Bot: I’m sorry to inform you that there are no ski hills in your
immediate location
User: Can you help me find the nearest?
Bot: Absolutely! It looks like you’re about 3 hours away from
Bear Mountain. That seems to be the closest.
User: Hmm.. sounds good
Bot: Alright! I can help you get your lift tickets now!When
will you be going?
User: Awesome! please get me a ticket for 10pax
Bot: You’ve got it. Anything else I can help you with?
User: None. Thanks again!
Bot: No problem!
```
Example of input/output for this dialog:
```
Input: dialog history = Hello how may I help you?; Is there
any good ski hills an hour’s drive from my current location?;
I’m sorry to inform you that there are no ski hills in your
immediate location
Output: user response = Can you help me find the nearest?
```

### Data Fields

Each dialogue instance has the following fields:
- `id`: a unique ID identifying the dialog. 
- `user_id`: a unique ID identifying the user. 
- `bot_id`: a unique ID identifying the bot.
- `domain`: a unique ID identifying the domain. Provides a mapping to tasks dataset.
- `task_id`: a unique ID identifying the task. Provides a mapping to tasks dataset.
- `turns`: the sequence of utterances alternating between `bot` and `user`, starting with a prompt from `bot`.
  
Each task instance has following fields:
- `task_id`: a unique ID identifying the task. 
- `domain`: a unique ID identifying the domain. 
- `bot_prompt`: The task specification for bot. 
- `bot_role`: The domain oriented role of bot. 
- `user_prompt`: The task specification for user. 
- `user_role`: The domain oriented role of user. 



### Data Splits

The dataset is split into a `train` and `test` split with the following sizes:

|                           | Training MetaLWOz     |  Evaluation MetaLWOz  | Combined |
| -----                     | ------                | -----                 | ----     |
| Total Domains             | 47                    | 4                     | 51       |
| Total Tasks               | 226                   | 14                    | 240      |
| Total Dialogs             | 37884                 | 2319                  | 40203    |

Below are the various statistics of the dataset:
 
| Statistic                     | Mean     |  Minimum   | Maximum   |
| -----                         | ------   | -----      | ----      |
| Number of tasks per domain    | 4.8      | 3          | 11        |
| Number of dialogs per domain  | 806.0    | 288        | 1990      |
| Number of dialogs per task    | 167.6    | 32         | 285       |
| Number of turns per dialog    | 11.4     | 10         | 46        |


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
The dataset v1 version is created by team of researchers from Microsoft Research (Montreal, Canada)

### Licensing Information

The dataset is released under [Microsoft Research Data License Agreement](https://msropendata-web-api.azurewebsites.net/licenses/2f933be3-284d-500b-7ea3-2aa2fd0f1bb2/view) 

### Citation Information

You can cite the following for the various versions of MetaLWOz:

Version 1.0
```
@InProceedings{shalyminov2020fast,
author = {Shalyminov, Igor and Sordoni, Alessandro and Atkinson, Adam and Schulz, Hannes},
title = {Fast Domain Adaptation For Goal-Oriented Dialogue Using A Hybrid Generative-Retrieval Transformer},
booktitle = {2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
year = {2020},
month = {April},
url = {https://www.microsoft.com/en-us/research/publication/fast-domain-adaptation-for-goal-oriented-dialogue-using-a
-hybrid-generative-retrieval-transformer/},
}
```

### Contributions

Thanks to [@pacman100](https://github.com/pacman100) for adding this dataset.