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
paperswithcode_id: taskmaster-1
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
- **Repository:** [GitHub](https://github.com/google-research-datasets/Taskmaster/tree/master/TM-1-2019)
- **Paper:** [Taskmaster-1: Toward a Realistic and Diverse Dialog Dataset](https://arxiv.org/abs/1909.05358)
- **Leaderboard:** N/A
- **Point of Contact:** [Taskmaster Googlegroup](taskmaster-datasets@googlegroups.com)

### Dataset Summary

Taskmaster-1 is a  goal-oriented conversational dataset. It includes 13,215 task-based
dialogs comprising six domains. Two procedures were used to create this collection,
each with unique advantages. The first involves a two-person, spoken "Wizard of Oz" (WOz) approach
in which trained agents and crowdsourced workers interact to complete the task while the second is
"self-dialog" in which crowdsourced workers write the entire dialog themselves.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is in English language.

## Dataset Structure

### Data Instances

A typical example looks like this

```
{
    "conversation_id":"dlg-336c8165-068e-4b4b-803d-18ef0676f668",
    "instruction_id":"restaurant-table-2",
    "utterances":[
      {
        "index":0,
        "segments":[
          
        ],
        "speaker":"USER",
        "text":"Hi, I'm looking for a place that sells spicy wet hotdogs, can you think of any?"
      },
      {
        "index":1,
        "segments":[
          {
            "annotations":[
              {
                "name":"restaurant_reservation.name.restaurant.reject"
              }
            ],
            "end_index":37,
            "start_index":16,
            "text":"Spicy Wet Hotdogs LLC"
          }
        ],
        "speaker":"ASSISTANT",
        "text":"You might enjoy Spicy Wet Hotdogs LLC."
      },
      {
        "index":2,
        "segments":[
          
        ],
        "speaker":"USER",
        "text":"That sounds really good, can you make me a reservation?"
      },
      {
        "index":3,
        "segments":[
          
        ],
        "speaker":"ASSISTANT",
        "text":"Certainly, when would you like a reservation?"
      },
      {
        "index":4,
        "segments":[
          {
            "annotations":[
              {
                "name":"restaurant_reservation.num.guests"
              },
              {
                "name":"restaurant_reservation.num.guests"
              }
            ],
            "end_index":20,
            "start_index":18,
            "text":"50"
          }
        ],
        "speaker":"USER",
        "text":"I have a party of 50 who want a really sloppy dog on Saturday at noon."
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

- one_person_dialogs

The data in `one_person_dialogs` config is split into `train`, `dev` and `test` splits.

|                            | Tain   | Valid | Test  |
| -----                      | ------ | ----- | ----- |
| N. Instances               | 6168   | 770   | 770   |

- woz_dialogs

The data in `woz_dialogs` config has no default splits.

|                            | Tain   |
| -----                      | ------ |
| N. Instances               | 5507   |


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