---
annotations_creators:
- found
language_creators:
- found
languages:
- ig
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
paperswithcode_id: null
---

# Dataset Card for Igbo NER dataset

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

- **Homepage:** https://github.com/IgnatiusEzeani/IGBONLP/tree/master/ig_ner
- **Repository:** https://github.com/IgnatiusEzeani/IGBONLP/tree/master/ig_ner
- **Paper:** https://arxiv.org/abs/2004.00648

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

Here is an example from the dataset:
```
{'content_n': 'content_0', 'named_entity': 'Ike Ekweremmadụ', 'sentences': ['Ike Ekweremmadụ', "Ike ịda jụụ otụ nkeji banyere oke ogbugbu na-eme n'ala Naijiria agwụla Ekweremmadụ"]}
```

### Data Fields

- content_n : ID 
- named_entity : Name of the entity 
- sentences : List of sentences for the entity 

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

@misc{ezeani2020igboenglish,  
    title={Igbo-English Machine Translation: An Evaluation Benchmark},  
    author={Ignatius Ezeani and Paul Rayson and Ikechukwu Onyenwe and Chinedu Uchechukwu and Mark Hepple},  
    year={2020},  
    eprint={2004.00648},  
    archivePrefix={arXiv},  
    primaryClass={cs.CL}   
}

### Contributions

Thanks to [@purvimisal](https://github.com/purvimisal) for adding this dataset.