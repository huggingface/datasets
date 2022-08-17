---
annotations_creators:
- other
language:
- ru
language_creators:
- found
license:
- other
multilinguality:
- monolingual
pretty_name: Collection3
size_categories:
- 10K<n<100K
source_datasets: []
tags: []
task_categories:
- token-classification
task_ids:
- named-entity-recognition
---

# Dataset Card for Collection3

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

- **Homepage:** [Collection3 homepage](http://labinform.ru/pub/named_entities/index.htm)
- **Repository:** [Needs More Information]
- **Paper:** [Two-stage approach in Russian named entity recognition](https://ieeexplore.ieee.org/document/7584769)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

Collection3 is a Russian dataset for named entity recognition annotated with LOC (location), PER (person), and ORG (organization) tags. Dataset is based on collection [Persons-1000](http://ai-center.botik.ru/Airec/index.php/ru/collections/28-persons-1000) originally containing 1000 news documents labeled only with names of persons.

Additional labels were obtained using guidelines similar to MUC-7 with web-based tool [Brat](http://brat.nlplab.org/) for collaborative text annotation.

Currently dataset contains 26K annotated named entities (11K Persons, 7K Locations and 8K Organizations).

Conversion to the IOB2 format and splitting into train, validation and test sets obtained from [DeepPavlov](http://files.deeppavlov.ai/deeppavlov_data/collection3_v2.tar.gz).

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Russian

## Dataset Structure

### Data Instances

An example of 'train' looks as follows.

```
{
    "id": "851",
    "ner_tags": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 2, 0, 0, 0],
    "tokens": ['Главный', 'архитектор', 'программного', 'обеспечения', '(', 'ПО', ')', 'американского', 'высокотехнологичного', 'гиганта', 'Microsoft', 'Рэй', 'Оззи', 'покидает', 'компанию', '.']
}
```

### Data Fields

- id: a string feature.
- tokens: a list of string features.
- ner_tags: a list of classification labels (int). Full tagset with indices:
```
{'O': 0, 'B-PER': 1, 'I-PER': 2, 'B-ORG': 3, 'I-ORG': 4, 'B-LOC': 5, 'I-LOC': 6}
```

### Data Splits

|name|train|validation|test|
|---------|----:|---------:|---:|
|Collection3|9301|2153|1922|

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
```
@inproceedings{mozharova-loukachevitch-2016-two-stage-russian-ner,
  author={Mozharova, Valerie and Loukachevitch, Natalia},
  booktitle={2016 International FRUCT Conference on Intelligence, Social Media and Web (ISMW FRUCT)},
  title={Two-stage approach in Russian named entity recognition}, 
  year={2016},
  pages={1-6},
  doi={10.1109/FRUCT.2016.7584769}}
  ```