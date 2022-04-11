---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-genia-v3.02
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
paperswithcode_id: null
pretty_name: BioNLP / JNLPBA Shared Task 2004
---

# Dataset Card for JNLPBA

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

- **Homepage:** http://www.geniaproject.org/shared-tasks/bionlp-jnlpba-shared-task-2004
- **Repository:** [Needs More Information]
- **Paper:** https://www.aclweb.org/anthology/W04-1213.pdf
- **Leaderboard:** https://paperswithcode.com/sota/named-entity-recognition-ner-on-jnlpba?p=biobert-a-pre-trained-biomedical-language
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The data came from the GENIA version 3.02 corpus (Kim et al., 2003). This was formed from a controlled search on MEDLINE using the MeSH terms human, blood cells and transcription factors. From this search 2,000 abstracts were selected and hand annotated according to a small taxonomy of 48 classes based on a chemical classification. Among the classes, 36 terminal classes were used to annotate the GENIA corpus.

### Supported Tasks and Leaderboards

NER

### Languages

English

## Dataset Structure

### Data Instances

{
  'id': '1',
  'tokens': ['IL-2', 'gene', 'expression', 'and', 'NF-kappa', 'B', 'activation', 'through', 'CD28', 'requires', 'reactive', 'oxygen', 'production', 'by', '5-lipoxygenase', '.'],
  'ner_tags': [1, 2, 0, 0, 9, 10, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0],
}

### Data Fields

- `id`: Sentence identifier.
- `tokens`: Array of tokens composing a sentence.
- `ner_tags`: Array of tags, where `0` indicates no bio-entity mentioned, `1` signals the first token of a bio-entity and `2` the subsequent bio-entity tokens.

### Data Splits

Train samples: 37094
Validation samples: 7714

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
@inproceedings{collier-kim-2004-introduction,
    title = "Introduction to the Bio-entity Recognition Task at {JNLPBA}",
    author = "Collier, Nigel  and
      Kim, Jin-Dong",
    booktitle = "Proceedings of the International Joint Workshop on Natural Language Processing in Biomedicine and its Applications ({NLPBA}/{B}io{NLP})",
    month = aug # " 28th and 29th",
    year = "2004",
    address = "Geneva, Switzerland",
    publisher = "COLING",
    url = "https://aclanthology.org/W04-1213",
    pages = "73--78",
}
### Contributions

Thanks to [@edugp](https://github.com/edugp) for adding this dataset.