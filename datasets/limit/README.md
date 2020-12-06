---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- crowdsourced
- found
languages:
- en
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-activitynet-captions
- original
task_categories:
- structure-prediction
- text-classification
task_ids:
- structure-prediction-other-motion-entity-recognition
- text-classification-other-literal-motion-classification
---

# Dataset Card for the Literal Motion in Text Dataset (LiMiT)

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

- **Homepage:**
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary
This is the Literal Motion in Text (LiMiT) dataset. It includes ~24K sentences 
that describe literal motion (~14K sentences) i.e., movement of a physical entity, 
as well as sentences that do not describe motion/contains other types of motion
(e.g., fictive motion). Senteces were extracted from electronic books categorized as fiction or novels, 
and a portion from the [ActivityNet Captions Dataset](https://cs.stanford.edu/people/ranjaykrishna/densevid/).

Sentences in the LiMiT dataset have two labels: 
1. Motion label: whether the sentence describes literal motion i.e. describes the movement of a physical entity or not
2. Motion entity: tokens in the sentence that belong to physical entities in motion. Motion entity labels include, for each entity, the index in the sentence for the first char of the entity tokens.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages
English.

## Dataset Structure

### Data Instances
Each instance comprise a sentence and information about entities in literal motion (if any). For example:
```python
{
  'motion': True, 
  'motion_entities': {
      'entity_start': [2, 30], 
      'text': ['little boy', 'ball']
  }, 
  'sentence': 'A little boy holding a yellow ball walks by.'
}
```

### Data Fields
- sentence: the text to process
- motion: whether sentence describes literal motion
- motion_entities: entities in literal motion (if any)
  - text: token(s) in sentence corresponding to the entities in literal motion
  - entity_start: index in sentence of initial character for each entity in literal motion

### Data Splits
This dataset contains 24559 instances in total.

Split | Motion | No Motion | Total 
--- | --- | --- | --- |
Train | 14660| 8899  | 23559 | 
Test | 686 | 314 | 1000 | 
Total | 15346 | 9213 | 24559 | 

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information
This resource is from [Manatos et al., 2020](https://www.aclweb.org/anthology/2020.findings-emnlp.88.pdf).
```
@inproceedings{manotas-etal-2020-limit,
    title = "{L}i{M}i{T}: The Literal Motion in Text Dataset",
    author = "Manotas, Irene  and
      Vo, Ngoc Phuoc An  and
      Sheinin, Vadim",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.findings-emnlp.88",
    doi = "10.18653/v1/2020.findings-emnlp.88",
    pages = "991--1000",
    }
```