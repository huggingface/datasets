---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
- machine-generated
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
- structure-prediction
task_ids:
- dialogue-modeling
- parsing
---

# Dataset Card for MultiWOZ

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

- **Repository:** [MultiWOZ 2.2 github repository](https://github.com/budzianowski/multiwoz/tree/master/data/MultiWOZ_2.2)
- **Paper:** [MultiWOZ v2](https://arxiv.org/abs/1810.00278), and [MultiWOZ v2.2](https://www.aclweb.org/anthology/2020.nlp4convai-1.13.pdf)
- **Point of Contact:** [Paweł Budzianowski](pfb30@cam.ac.uk)

### Dataset Summary

Multi-Domain Wizard-of-Oz dataset (MultiWOZ), a fully-labeled collection of human-human written conversations spanning over multiple domains and topics.
MultiWOZ 2.1 (Eric et al., 2019) identified and fixed many erroneous annotations and user utterances in the original version, resulting in an
improved version of the dataset. MultiWOZ 2.2 is a yet another improved version of this dataset, which identifies and fixes dialogue state annotation errors
across 17.3% of the utterances on top of MultiWOZ 2.1 and redefines the ontology by disallowing vocabularies of slots with a large number of possible values
(e.g., restaurant name, time of booking) and introducing standardized slot span annotations for these slots.

### Supported Tasks and Leaderboards

This dataset can be used for generative dialogue modeling and dialogue state tracking.

### Languages

The text in the dataset is in English (`en`).

## Dataset Structure

### Data Instances

A data instance is a full multi-turn dialogue between a `USER` and a `SYSTEM`.

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

[More Information Needed]

### Licensing Information

The dataset is released under the Apache License 2.0.

### Citation Information

You can cite the following for the various versions of MultiWOZ:

Version 1.0
```
@inproceedings{ramadan2018large,
  title={Large-Scale Multi-Domain Belief Tracking with Knowledge Sharing},
  author={Ramadan, Osman and Budzianowski, Pawe{\l} and Gasic, Milica},
  booktitle={Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics},
  volume={2},
  pages={432--437},
  year={2018}
}
```

Version 2.0
```
@inproceedings{budzianowski2018large,
    Author = {Budzianowski, Pawe{\l} and Wen, Tsung-Hsien and Tseng, Bo-Hsiang  and Casanueva, I{\~n}igo and Ultes Stefan and Ramadan Osman and Ga{\v{s}}i\'c, Milica},
    title={MultiWOZ - A Large-Scale Multi-Domain Wizard-of-Oz Dataset for Task-Oriented Dialogue Modelling},
    booktitle={Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
    year={2018}
}
```

Version 2.1
```
@article{eric2019multiwoz,
  title={MultiWOZ 2.1: Multi-Domain Dialogue State Corrections and State Tracking Baselines},
  author={Eric, Mihail and Goel, Rahul and Paul, Shachi and Sethi, Abhishek and Agarwal, Sanchit and Gao, Shuyag and Hakkani-Tur, Dilek},
  journal={arXiv preprint arXiv:1907.01669},
  year={2019}
}
```

Version 2.2
```
@inproceedings{zang2020multiwoz,
  title={MultiWOZ 2.2: A Dialogue Dataset with Additional Annotation Corrections and State Tracking Baselines},
  author={Zang, Xiaoxue and Rastogi, Abhinav and Sunkara, Srinivas and Gupta, Raghav and Zhang, Jianguo and Chen, Jindong},
  booktitle={Proceedings of the 2nd Workshop on Natural Language Processing for Conversational AI, ACL 2020},
  pages={109--117},
  year={2020}
}
```
