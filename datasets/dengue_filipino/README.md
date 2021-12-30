---
annotations_creators:
- crowdsourced
- machine-generated
language_creators:
- crowdsourced
languages:
- tl
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
paperswithcode_id: dengue
---

# Dataset Card for Dengue Dataset in Filipino

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

- **Homepage: [Dengue Dataset in Filipino homepage](https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks)**
- **Repository: [Dengue Dataset in Filipino repository](https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks)**
- **Paper: [IEEE paper](https://ieeexplore.ieee.org/document/8459963)**
- **Leaderboard:**
- **Point of Contact: [Jan Christian Cruz](mailto:jan_christian_cruz@dlsu.edu.ph)**

### Dataset Summary

Benchmark dataset for low-resource multiclass classification, with 4,015 training, 500 testing, and 500 validation examples, each labeled as part of five classes. Each sample can be a part of multiple classes. Collected as tweets.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is primarily in Filipino, with the addition of some English words commonly used in Filipino vernacular.

## Dataset Structure

### Data Instances

Sample data:
```
{
  "text": "Tapos ang dami pang lamok.",
  "absent": "0",
  "dengue": "0",
  "health": "0",
  "mosquito": "1",
  "sick": "0"
}
```

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

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

[Jan Christian Cruz](mailto:jan_christian_cruz@dlsu.edu.ph)

### Licensing Information

[More Information Needed]

### Citation Information

  @INPROCEEDINGS{8459963,
    author={E. D. {Livelo} and C. {Cheng}},
    booktitle={2018 IEEE International Conference on Agents (ICA)},
    title={Intelligent Dengue Infoveillance Using Gated Recurrent Neural Learning and Cross-Label Frequencies},
    year={2018},
    volume={},
    number={},
    pages={2-7},
    doi={10.1109/AGENTS.2018.8459963}}
  }

### Contributions

Thanks to [@anaerobeth](https://github.com/anaerobeth) for adding this dataset.