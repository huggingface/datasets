---
annotations_creators:
- expert-generated
extended:
- original
language_creators:
- expert-generated
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
- text-classification
task_ids:
- intent-classification
- multi-class-classification
---

# Dataset Card for BANKING77

## Table of Contents
- [Dataset Card for BANKING77](#dataset-card-for-dataset-name)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** [Github](https://github.com/PolyAI-LDN/task-specific-datasets)
- **Repository:** [Github](https://github.com/PolyAI-LDN/task-specific-datasets)
- **Paper:** [ArXiv](https://arxiv.org/abs/2003.04807)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Dataset composed of online banking queries annotated with their corresponding intents.

BANKING77 dataset provides a very fine-grained set of intents in a banking domain.
It comprises 13,083 customer service queries labeled with 77 intents. 
It focuses on fine-grained single-domain intent detection.

### Supported Tasks and Leaderboards

Intent classification, intent detection

### Languages

English

## Dataset Structure

### Data Instances

An example of 'train' looks as follows.
```
{
  'label': 0, # integer label corresponding to "card_arrival" intent
  'text': 'I am still waiting on my card?'
}
```

### Data Fields

- `text`: a string feature.
- `label`: One of classification labels (0-76) corresponding to unique intents.

### Data Splits

| Dataset statistics               |      |
| ---            |   --- |
| Train examples | 10 003 |
| Test examples | 3 080 |
| Number of intents | 77 |

## Dataset Creation

### Curation Rationale

[N/A]

### Source Data

#### Initial Data Collection and Normalization

[N/A]

#### Who are the source language producers?

[N/A]

### Annotations

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

[N/A]

## Considerations for Using the Data

### Social Impact of Dataset

[N/A]

### Discussion of Biases

[N/A]

### Other Known Limitations

[N/A]

## Additional Information

### Dataset Curators

[N/A]

### Licensing Information

Creative Commons Attribution 4.0 International

### Citation Information

```
@inproceedings{Casanueva2020,
    author      = {I{\~{n}}igo Casanueva and Tadas Temcinas and Daniela Gerz and Matthew Henderson and Ivan Vulic},
    title       = {Efficient Intent Detection with Dual Sentence Encoders},
    year        = {2020},
    month       = {mar},
    note        = {Data available at https://github.com/PolyAI-LDN/task-specific-datasets},
    url         = {https://arxiv.org/abs/2003.04807},
    booktitle   = {Proceedings of the 2nd Workshop on NLP for ConvAI - ACL 2020}
}
```

### Contributions

Thanks to [@dkajtoch](https://github.com/dkajtoch) for adding this dataset.
