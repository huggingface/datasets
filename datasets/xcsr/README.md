---
annotations_creators:
- other
language_creators:
- other
languages:
- en
- zh
- de
- es
- fr
- it
- jap
- nl
- pl
- pt
- ru
- ar
- vi
- hi
- sw
- ur
licenses: []
multilinguality:
- multilingual
pretty_name: X-CSR
size_categories:
- unknown
source_datasets:
- extended|codah
- extended|commonsense_qa
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
---

# Dataset Card for X-CSR

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

- **Homepage:** https://inklab.usc.edu//XCSR/
- **Repository:** https://github.com/INK-USC/XCSR
- **Paper:** https://arxiv.org/abs/2106.06937
- **Leaderboard:** https://inklab.usc.edu//XCSR/leaderboard
- **Point of Contact:** https://yuchenlin.xyz/

### Dataset Summary

To evaluate multi-lingual language models (ML-LMs) for commonsense reasoning in a cross-lingual zero-shot transfer setting (X-CSR), i.e., training in English and test in other languages, we create two benchmark datasets, namely X-CSQA and X-CODAH. Specifically, we automatically translate the original CSQA and CODAH datasets, which only have English versions, to 15 other languages, forming development and test sets for studying X-CSR. As our goal is to evaluate different ML-LMs in a unified evaluation protocol for X-CSR, we argue that such translated examples, although might contain noise, can serve as a starting benchmark for us to obtain meaningful analysis, before more human-translated datasets will be available in the future.


### Supported Tasks and Leaderboards

https://inklab.usc.edu//XCSR/leaderboard

### Languages

The total 16 languages for X-CSR: {en, zh, de, es, fr, it, jap, nl, pl, pt, ru, ar, vi, hi, sw, ur}.


## Dataset Structure

### Data Instances

An example of the X-CSQA dataset:
```
{
  "id": "be1920f7ba5454ad",  # an id shared by all languages
  "lang": "en", # one of the 16 language codes.
  "question": { 
    "stem": "What will happen to your knowledge with more learning?",   # question text
    "choices": [
      {"label": "A",  "text": "headaches" },
      {"label": "B",  "text": "bigger brain" },
      {"label": "C",  "text": "education" },
      {"label": "D",  "text": "growth" },
      {"label": "E",  "text": "knowing more" }
    ] },
  "answerKey": "D"    # hidden for test data.
}
```

An example of the X-CODAH dataset:
```
{
  "id": "b8eeef4a823fcd4b",   # an id shared by all languages
  "lang": "en", # one of the 16 language codes.
  "question_tag": "o",  # one of 6 question types
  "question": {
    "stem": " ", # always a blank as a dummy question
    "choices": [
      {"label": "A",
        "text": "Jennifer loves her school very much, she plans to drop every courses."},
      {"label": "B",
        "text": "Jennifer loves her school very much, she is never absent even when she's sick."},
      {"label": "C",
        "text": "Jennifer loves her school very much, she wants to get a part-time job."},
      {"label": "D",
        "text": "Jennifer loves her school very much, she quits school happily."}
    ]
  },
  "answerKey": "B"  # hidden for test data.
}
```

### Data Fields

  - id: an id shared by all languages
  - lang: one of the 16 language codes.
  - question_tag: one of 6 question types
  - stem: always a blank as a dummy question
  - choices: a list of answers, each answer has: 
    - label: a string answer identifier for each answer
    - text: the answer text

### Data Splits

[Needs More Information]

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

[Needs More Information]