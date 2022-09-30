---
annotations_creators:
- machine-generated
language_creators:
- machine-generated
language:
- en
license:
- unknown
multilinguality:
- monolingual
pretty_name: 'text2log'
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- translation
task_ids: []
---

# Dataset Card for text2log

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
- **Repository:** [GitHub](https://github.com/alevkov/text2log)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** https://github.com/alevkov

### Dataset Summary

The dataset contains 100,000 simple English sentences selected and filtered from `enTenTen15` and their translation into First Order Logic (FOL) using `ccg2lambda`.

### Supported Tasks and Leaderboards

'semantic-parsing': The data set is used to train models which can generate FOL statements from natural language text

### Languages

en-US

## Dataset Structure

### Data Instances

```
{
'clean':'All things that are new are good.',
'trans':'all x1.(_thing(x1) -> (_new(x1) -> _good(x1)))'
}
```

### Data Fields

- 'clean': a simple English sentence
- 'trans': the corresponding translation into Lambda Dependency-based Compositional Semantics 

### Data Splits

No predefined train/test split is given. The authors used a 80/20 split

## Dataset Creation

### Curation Rationale

The text2log data set is used to improve FOL statement generation from natural text

### Source Data

#### Initial Data Collection and Normalization

Short text samples selected from enTenTen15

#### Who are the source language producers?

See https://www.sketchengine.eu/ententen-english-corpus/

### Annotations

#### Annotation process

Machine generated using https://github.com/mynlp/ccg2lambda

#### Who are the annotators?

none

### Personal and Sensitive Information

The dataset does not contain personal or sensitive information.

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

None given

### Citation Information
```bibtex
@INPROCEEDINGS{9401852, 
author={Levkovskyi, Oleksii and Li, Wei},
booktitle={SoutheastCon 2021},
title={Generating Predicate Logic Expressions from Natural Language},
year={2021},
volume={},
number={},
pages={1-8},
doi={10.1109/SoutheastCon45413.2021.9401852}
}
```

### Contributions

Thanks to [@apergo-ai](https://github.com/apergo-ai) for adding this dataset.