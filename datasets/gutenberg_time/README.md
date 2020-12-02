---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
---

# Dataset Card for the Gutenberg Time dataset

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

- **[Repository](https://github.com/allenkim/what-time-is-it)**
- **[Paper](https://arxiv.org/abs/2011.04124)**

### Dataset Summary

A clean data resource containing all explicit time references in a dataset of 52,183 novels whose full text is available via Project Gutenberg.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Time-of-the-day classification from excerpts.

## Dataset Structure

### Data Instances

```
{
    "guten_id": 28999,
    "hour_reference": 12,
    "time_phrase": "midday",
    "is_ambiguous": False,
    "time_pos_start": 133,
    "time_pos_end": 134,
    "tok_context": "Sorrows and trials she had had in plenty in her life , but these the sweetness of her nature had transformed , so that from being things difficult to bear , she had built up with them her own character . Sorrow had increased her own power of sympathy ; out of trials she had learnt patience ; and failure and the gradual sinking of one she had loved into the bottomless slough of evil habit had but left her with an added dower of pity and tolerance . So the past had no sting left , and if iron had ever entered into her soul it now but served to make it strong . She was still young , too ; it was not near sunset with her yet , nor even midday , and the future that , humanly speaking , she counted to be hers was almost dazzling in its brightness . For love had dawned for her again , and no uncertain love , wrapped in the mists of memory , but one that had ripened through liking and friendship and intimacy into the authentic glory . He was in England , too ; she was going back to him . And before very long she would never go away from him again ."
}
```

### Data Fields

```
    guten_id - Gutenberg ID number
    hour_reference - hour from 0 to 23
    time_phrase - the phrase corresponding to the referenced hour
    is_ambiguous - boolean whether it is clear whether time is AM or PM
    time_pos_start - token position where time_phrase begins
    time_pos_end - token position where time_phrase ends (exclusive)
    tok_context - context in which time_phrase appears as space-separated tokens
```

### Data Splits

No data splits.

## Dataset Creation

### Curation Rationale

The flow of time is an indispensable guide for our actions, and provides a framework in which to see a logical progression of events. Just as in real life,the clock provides the background against which literary works play out: when characters wake, eat,and act. In most works of fiction, the events of the story take place during recognizable time periods over the course of the day. Recognizing a story’s flow through time is essential to understanding the text.In this paper, we try to capture the flow of time through novels by attempting to recognize what time of day each event in the story takes place at.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Novel authors.

### Annotations

#### Annotation process

Manually annotated.

#### Who are the annotators?

Two of the authors.

### Personal and Sensitive Information

No Personal or sensitive information.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Allen Kim, Charuta Pethe and Steven Skiena, Stony Brook University

### Licensing Information

[More Information Needed]

### Citation Information

```
@misc{kim2020time,
      title={What time is it? Temporal Analysis of Novels}, 
      author={Allen Kim and Charuta Pethe and Steven Skiena},
      year={2020},
      eprint={2011.04124},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```