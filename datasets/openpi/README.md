---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- named-entity-recognition
task_ids:
- structure-prediction
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** "https://allenai.org/data/openpi"
- **Repository:** https://github.com/allenai/openpi-dataset
- **Paper:** https://www.aclweb.org/anthology/2020.emnlp-main.520.pdf
- **Leaderboard:** Coming Soon
- **Point of Contact:** {nikett, keisukes, bhavanad, peterc, michalg, kyler}@allenai.org, 
{dheeraj, hovy}@cs.cmu.edu

### Dataset Summary

OpenPI Dataset for Tracking Entities in Open Domain Procedural Text

### Supported Tasks and Leaderboards

Entity Tracking, Question Answering

### Languages

English

## Dataset Structure
  "id": WikiHow Question ID,
  "question": String with question,
  "answers": [List of Strings with answers for the same WikiHow ID]
  "question_metadata": Other metadata of the question such as
  {
    "url": URL to the WikiHow question, suffixed with step number,
    "step_id": Which step it is in the multi step question (4 - 7 steps),
    "context": Context if any *before* the question,
    "future_context": Context if any *after* the question,
    "query": Query for the answer,
    "topic": One among the 6-7 topics/categories used ranging from Health, Food, Home, Hobbies etc.
  }
  "answers_metadata": Other metadata for the answers such as 
  {
    "answer": Single sentence with instructions and expected status of entity before and after
    "entity": Entity identified in the answer
    "before": Status of the entity *before* the answer
    "after": Status of the entity *after* the answer
    "attr": Identified attributes/status for the answer
    "modality": With or without image
  }

### Data Instances
{
  "id": "www.wikihow.com/Flip-Someone-over-Your-Shoulder||1",
  "question": " Be in a fighting position with this person. Now, what happens?"
}
{
  "id": "www.wikihow.com/Flip-Someone-over-Your-Shoulder||1",
  "question_metadata": {
    "url": "www.wikihow.com/Flip-Someone-over-Your-Shoulder",
    "step_id": "1",
    "context": "",
    "query": "Be in a fighting position with this person.",
    "future_context": "Turn around, stepping away from them, pulling them towards you (this throws off their balance), and grab their arm. Roll them off of your hip. Once they are on the ground make sure they slap the floor as they hit to prevent friction.",
    "topic": "Sports and Fitness"
  }
}
{
  "id": "www.wikihow.com/Flip-Someone-over-Your-Shoulder||1",
  "answers": [
    "position of fists was open before and closed afterwards",
    "position of fighter was alone before and facing an opponent afterwards",
    "energy of body was calm before and tense afterwards",
    "position of arms was down before and up afterwards",
    "flexibility of knees was locked before and bent afterwards",
    "location of body was elsewhere before and on the mat afterwards",
    "placement of hands was kept to self before and now placed on other person afterwards",
    "energy of muscles was relaxed before and tight afterwards",
    "position of a normal position was taken before and now changed to a fighting position afterwards"
  ]
}
{
  "id": "www.wikihow.com/Flip-Someone-over-Your-Shoulder||1",
  "answers_metadata": [
    {
      "answer": "position of a normal position was taken before and now changed to a fighting position afterwards",
      "entity": "a normal position",
      "before": "taken",
      "after": "now changed to fighting position",
      "attr": "position",
      "modality": "with_image"
    },
    {
      "answer": "placement of hands was kept to self before and now placed on other person afterwards",
      "entity": "hands",
      "before": "kept to self",
      "after": "now placed on person",
      "attr": "placement",
      "modality": "with_image"
    },
    {
      "answer": "energy of body was calm before and tense afterwards",
      "entity": "body",
      "before": "calm",
      "after": "tense",
      "attr": "energy",
      "modality": "without_image"
    },
    {
      "answer": "energy of muscles was relaxed before and tight afterwards",
      "entity": "muscles",
      "before": "relaxed",
      "after": "tight",
      "attr": "energy",
      "modality": "without_image"
    },
    {
      "answer": "position of arms was down before and up afterwards",
      "entity": "arms",
      "before": "down",
      "after": "up",
      "attr": "position",
      "modality": "without_image"
    },
    {
      "answer": "position of fists was open before and closed afterwards",
      "entity": "fists",
      "before": "open",
      "after": "closed",
      "attr": "position",
      "modality": "without_image"
    },
    {
      "answer": "behavior of breathing was normal before, and controlled afterwards.",
      "entity": "breathing",
      "before": "normal",
      "after": "controlled",
      "attr": "behavior",
      "modality": "without_image"
    },
    {
      "answer": "position of chin was up before, and down afterwards.",
      "entity": "chin",
      "before": "up",
      "after": "down",
      "attr": "position",
      "modality": "without_image"
    },
    {
      "answer": "flexibility of knees was locked before and bent afterwards",
      "entity": "knees",
      "before": "locked",
      "after": "bent",
      "attr": "flexibility",
      "modality": "without_image"
    },
    {
      "answer": "location of body was elsewhere before and on the mat afterwards",
      "entity": "body",
      "before": "elsewhere",
      "after": "on mat",
      "attr": "location",
      "modality": "without_image"
    },
    {
      "answer": "position of fighter was alone before and facing an opponent afterwards",
      "entity": "fighter",
      "before": "alone",
      "after": "facing opponent",
      "attr": "position",
      "modality": "without_image"
    }
  ]
}

### Data Fields

- `id`: ID of the WikiHow question, suffixed with step number for multi-step questions
- `answers`: List of answers to the WikiHow question
- `question`: Single string question
- `question_metadata`: {
  - `url`: URL to the original WikiHow question
  - `step_id`: Which step in the multi-step question (4 - 7 steps are used)
  - `context`: Context before the question
  - `query`: Query sentence for the answer
  - `future_context`: Context after the question
  - `topic`: Which topic/category is the question classified under
}
 - `answers_metadata`: {
    - `answer`: Single sentence answer,
    - `entity`: Entity identified in the answer,
    - `before`: Status of entity before the answer,
    - `after`: Status of entity after the answer,
    - `attr`: Attribute/Status identified,
    - `modality`: With or without image
 }

### Data Splits

|                            | Train  | Valid  | Test  |
| -----                      | ------ | -----  | ----  |
| Questions                  | 3216   | 560    | 274   |
| Answers                    | 3216   | 560    | 274   |

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

Crowdsourced through Mechanical Turk with and without images

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

MIT License

### Citation Information

@inproceedings{tandon-etal-2020-dataset,
    title = "A Dataset for Tracking Entities in Open Domain Procedural Text",
    author = "Tandon, Niket  and
      Sakaguchi, Keisuke  and
      Dalvi, Bhavana  and
      Rajagopal, Dheeraj  and
      Clark, Peter  and
      Guerquin, Michal  and
      Richardson, Kyle  and
      Hovy, Eduard",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.520",
    doi = "10.18653/v1/2020.emnlp-main.520",
    pages = "6408--6417"
}
