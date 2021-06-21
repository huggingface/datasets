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
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- dialogue-modeling
paperswithcode_id: null
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

- **Homepage:** [Taskmaster](https://research.google/tools/datasets/taskmaster-1/)
- **Repository:** [GitHub](https://github.com/google-research-datasets/Taskmaster/tree/master/TM-3-2020)
- **Paper:** [Taskmaster-1: Toward a Realistic and Diverse Dialog Dataset](https://arxiv.org/abs/1909.05358)
- **Leaderboard:** N/A
- **Point of Contact:** [Taskmaster Googlegroup](taskmaster-datasets@googlegroups.com)

### Dataset Summary

Taskmaster is dataset for goal oriented conversations. The Taskmaster-3 dataset consists of 23,757 movie ticketing dialogs.
By "movie ticketing" we mean conversations where the customer's goal is to purchase tickets after deciding
on theater, time, movie name, number of tickets, and date, or opt out of the transaction. This collection
was created using the "self-dialog" method. This means a single, crowd-sourced worker is
paid to create a conversation writing turns for both speakers, i.e. the customer and the ticketing agent.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is in English language.

## Dataset Structure

### Data Instances

A typical example looks like this

```
{
    "conversation_id": "dlg-ddee80da-9ffa-4773-9ce7-f73f727cb79c",
    "instructions": "SCENARIO: Pretend you’re *using a digital assistant to purchase tickets for a movie currently showing in theaters*.  ...",
    "scenario": "4 exchanges with 1 error and predefined variables",
    "utterances": [
        {
            "apis": [],
            "index": 0,
            "segments": [
                {
                    "annotations": [
                        {
                            "name": "num.tickets"
                        }
                    ],
                    "end_index": 21,
                    "start_index": 20,
                    "text": "2"
                },
                {
                    "annotations": [
                        {
                            "name": "name.movie"
                        }
                    ],
                    "end_index": 42,
                    "start_index": 37,
                    "text": "Mulan"
                }
            ],
            "speaker": "user",
            "text": "I would like to buy 2 tickets to see Mulan."
        },
        {
            "index": 6,
            "segments": [],
            "speaker": "user",
            "text": "Yes.",
            "apis": [
                {
                    "args": [
                        {
                            "arg_name": "name.movie",
                            "arg_value": "Mulan"
                        },
                        {
                            "arg_name": "name.theater",
                            "arg_value": "Mountain AMC 16"
                        }
                    ],
                    "index": 6,
                    "name": "book_tickets",
                    "response": [
                        {
                            "response_name": "status",
                            "response_value": "success"
                        }
                    ]
                }
            ]
        }
    ],
    "vertical": "Movie Tickets"
}
```

### Data Fields

Each conversation in the data file has the following structure:

- `conversation_id`: A universally unique identifier with the prefix 'dlg-'. The ID has no meaning.
- `utterances`: A list of utterances that make up the conversation.
- `instructions`: Instructions for the crowdsourced worker used in creating the conversation.
- `vertical`: In this dataset the vertical for all dialogs is "Movie Tickets".
- `scenario`: This is the title of the instructions for each dialog.

Each utterance has the following fields:

- `index`: A 0-based index indicating the order of the utterances in the conversation.
- `speaker`: Either USER or ASSISTANT, indicating which role generated this utterance.
- `text`: The raw text of the utterance. In case of self dialogs (one_person_dialogs), this is written by the crowdsourced worker. In case of the WOz dialogs, 'ASSISTANT' turns are written and 'USER' turns are transcribed from the spoken recordings of crowdsourced workers.
- `segments`: A list of various text spans with semantic annotations.
- `apis`: An array of API invocations made during the utterance.

Each API has the following structure:

- `name`: The name of the API invoked (e.g. find_movies).
- `index`: The index of the parent utterance.
- `args`: A `list` of `dict` with keys `arg_name` and `arg_value` which represent the name of the argument and the value for the argument respectively. 
- `response`: A `list` of `dict`s with keys `response_name` and `response_value` which represent the name of the response and the value for the response respectively. 

Each segment has the following fields:

- `start_index`: The position of the start of the annotation in the utterance text.
- `end_index`: The position of the end of the annotation in the utterance text.
- `text`: The raw text that has been annotated.
- `annotations`: A list of annotation details for this segment.

Each annotation has a single field:

- `name`: The annotation name.



### Data Splits

There are no deafults splits for all the config. The below table lists the number of examples in each config.

|                   | Train  |
|-------------------|--------|
| n_instances       | 23757  |


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