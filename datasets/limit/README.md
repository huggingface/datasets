---
annotations_creators:
- crowdsourced
language_creators:
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
- extended|net-activities-captions
- original
task_categories:
- structure-prediction
- text-classification
task_ids:
- multi-class-classification
- named-entity-recognition
paperswithcode_id: limit
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

- **Homepage:** -
- **Repository:** [github](https://github.com/ilmgut/limit_dataset)
- **Paper:** [LiMiT: The Literal Motion in Text Dataset](https://www.aclweb.org/anthology/2020.findings-emnlp.88/)
- **Leaderboard:** N/A
- **Point of Contact:** [More Information Needed]

### Dataset Summary

Motion recognition is one of the basic cognitive capabilities of many life forms, yet identifying
motion of physical entities in natural language have not been explored extensively and empirically.
Literal-Motion-in-Text (LiMiT) dataset, is a large human-annotated collection of English text sentences
describing physical occurrence of motion, with annotated physical entities in motion.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English (`en`).

## Dataset Structure

### Data Instances

Example of one instance in the dataset

```
{
	"id": 0,
	"motion": "yes",
	"motion_entities": [
		{
			"entity": "little boy",
			"start_index": 2
		},
		{
			"entity": "ball",
			"start_index": 30
		}
	],
	"sentence": " A little boy holding a yellow ball walks by."
}
```

### Data Fields

- `id`: intger index of the example
- `motion`:  indicates whether the sentence is literal motion i.e. describes the movement of a physical entity or not
- `motion_entities`: A `list` of `dicts` with following keys
    - `entity`: the extracted entity in motion 
    - `start_index`: index in the sentence for the first char of the entity text

### Data Splits

The dataset is split into a `train`, and `test` split with the following sizes:

|                            | Tain   | Valid |
| -----                      | ------ | ----- |
| Number of examples         | 23559  | 1000  |

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

[More Information Needed]

### Citation Information

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
    abstract = "Motion recognition is one of the basic cognitive capabilities of many life forms, yet identifying motion of physical entities in natural language have not been explored extensively and empirically. We present the Literal-Motion-in-Text (LiMiT) dataset, a large human-annotated collection of English text sentences describing physical occurrence of motion, with annotated physical entities in motion. We describe the annotation process for the dataset, analyze its scale and diversity, and report results of several baseline models. We also present future research directions and applications of the LiMiT dataset and share it publicly as a new resource for the research community.",
}
```

### Contributions

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.