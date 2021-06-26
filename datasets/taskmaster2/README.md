---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- dialogue-modeling
paperswithcode_id: taskmaster-2
---

# Dataset Card Creation Guide

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

- **Homepage:** [Taskmaster-1](https://research.google/tools/datasets/taskmaster-1/)
- **Repository:** [GitHub](https://github.com/google-research-datasets/Taskmaster/tree/master/TM-2-2020)
- **Paper:** [Taskmaster-1: Toward a Realistic and Diverse Dialog Dataset](https://arxiv.org/abs/1909.05358)
- **Leaderboard:** N/A
- **Point of Contact:** [Taskmaster Googlegroup](taskmaster-datasets@googlegroups.com)

### Dataset Summary

Taskmaster is dataset for goal oriented conversations. The Taskmaster-2 dataset consists of 17,289 dialogs
in the seven domains which include restaurants, food ordering, movies, hotels, flights, music and sports. 
Unlike Taskmaster-1, which includes both written "self-dialogs" and spoken two-person dialogs,
Taskmaster-2 consists entirely of spoken two-person dialogs. In addition, while Taskmaster-1 is
almost exclusively task-based, Taskmaster-2 contains a good number of search- and recommendation-oriented dialogs.
All dialogs in this release were created using a Wizard of Oz (WOz) methodology in which crowdsourced
workers played the role of a 'user' and trained call center operators played the role of the 'assistant'.
In this way, users were led to believe they were interacting with an automated system that “spoke”
using text-to-speech (TTS) even though it was in fact a human behind the scenes.
As a result, users could express themselves however they chose in the context of an automated interface.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is in English language.

## Dataset Structure

### Data Instances

A typical example looks like this

```
{
    "conversation_id": "dlg-0047a087-6a3c-4f27-b0e6-268f53a2e013",
    "instruction_id": "flight-6",
    "utterances": [
        {
            "index": 0,
            "segments": [],
            "speaker": "USER",
            "text": "Hi, I'm looking for a flight. I need to visit a friend."
        },
        {
            "index": 1,
            "segments": [],
            "speaker": "ASSISTANT",
            "text": "Hello, how can I help you?"
        },
        {
            "index": 2,
            "segments": [],
            "speaker": "ASSISTANT",
            "text": "Sure, I can help you with that."
        },
        {
            "index": 3,
            "segments": [],
            "speaker": "ASSISTANT",
            "text": "On what dates?"
        },
        {
            "index": 4,
            "segments": [
                {
                    "annotations": [
                        {
                            "name": "flight_search.date.depart_origin"
                        }
                    ],
                    "end_index": 37,
                    "start_index": 27,
                    "text": "March 20th"
                },
                {
                    "annotations": [
                        {
                            "name": "flight_search.date.return"
                        }
                    ],
                    "end_index": 45,
                    "start_index": 41,
                    "text": "22nd"
                }
            ],
            "speaker": "USER",
            "text": "I'm looking to travel from March 20th to 22nd."
        }
    ]
}
```

### Data Fields

Each conversation in the data file has the following structure:

- `conversation_id`: A universally unique identifier with the prefix 'dlg-'. The ID has no meaning.
- `utterances`: A list of utterances that make up the conversation.
- `instruction_id`: A reference to the file(s) containing the user (and, if applicable, agent) instructions for this conversation.

Each utterance has the following fields:

- `index`: A 0-based index indicating the order of the utterances in the conversation.
- `speaker`: Either USER or ASSISTANT, indicating which role generated this utterance.
- `text`: The raw text of the utterance. In case of self dialogs (one_person_dialogs), this is written by the crowdsourced worker. In case of the WOz dialogs, 'ASSISTANT' turns are written and 'USER' turns are transcribed from the spoken recordings of crowdsourced workers.
- `segments`: A list of various text spans with semantic annotations.

Each segment has the following fields:

- `start_index`: The position of the start of the annotation in the utterance text.
- `end_index`: The position of the end of the annotation in the utterance text.
- `text`: The raw text that has been annotated.
- `annotations`: A list of annotation details for this segment.

Each annotation has a single field:

- `name`: The annotation name.



### Data Splits

There are no deafults splits for all the config. The below table lists the number of examples in each config.

| Config            | Train  |
|-------------------|--------|
| flights           | 2481   |
| food-orderings    | 1050   |
| hotels            | 2355   |
| movies            | 3047   |
| music             | 1602   |
| restaurant-search | 3276   |
| sports            | 3478   |


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

The dataset is licensed under `Creative Commons Attribution 4.0 License`

### Citation Information

[More Information Needed]
```
@inproceedings{48484,
title	= {Taskmaster-1: Toward a Realistic and Diverse Dialog Dataset},
author	= {Bill Byrne and Karthik Krishnamoorthi and Chinnadhurai Sankar and Arvind Neelakantan and Daniel Duckworth and Semih Yavuz and Ben Goodrich and Amit Dubey and Kyu-Young Kim and Andy Cedilnik},
year	= {2019}
}
```
### Contributions

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.