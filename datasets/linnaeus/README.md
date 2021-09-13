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
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
paperswithcode_id: linnaeus
pretty_name: LINNAEUS
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [linnaeus](http://linnaeus.sourceforge.net/)
- **Repository:**
- **Paper:** [BMC Bioinformatics](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-85)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

LINNAEUS is a general-purpose dictionary matching software, capable of processing multiple types of document formats in the biomedical domain (MEDLINE, PMC, BMC, OTMI, text, etc.). It can produce multiple types of output (XML, HTML, tab-separated-value file, or save to a database). It also contains methods for acting as a server (including load balancing across several servers), allowing clients to request matching over a network. A package with files for recognizing and identifying species names is available for LINNAEUS, showing 94% recall and 97% precision compared to LINNAEUS-species-corpus.

### Supported Tasks and Leaderboards

This dataset is used for species Named Entity Recognition.

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

An example from the dataset is:

```
{'id': '2',
'tokens': ['Scp160p', 'is', 'a', '160', 'kDa', 'protein', 'in', 'the', 'yeast', 'Saccharomyces', 'cerevisiae', 'that', 'contains', '14', 'repeats', 'of', 'the', 'hnRNP', 'K', '-', 'homology', '(', 'KH', ')', 'domain', ',', 'and', 'demonstrates', 'significant', 'sequence', 'homology', 'to', 'a', 'family', 'of', 'proteins', 'collectively', 'known', 'as', 'vigilins', '.'],
'ner_tags': [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
```

### Data Fields

- `id`: Sentence identifier.  
- `tokens`: Array of tokens composing a sentence.  
- `ner_tags`: Array of tags, where `0` indicates no species mentioned, `1` signals the first token of a species and `2` the subsequent tokens of the species.  

### Data Splits


|   name   |train|validation|test|
|----------|----:|---------:|---:|
| linnaeus |11936|      4079|7143|

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

```bibtex
@article{Gerner2010,
abstract = {The task of recognizing and identifying species names in biomedical literature has recently been regarded as critical for a number of applications in text and data mining, including gene name recognition, species-specific document retrieval, and semantic enrichment of biomedical articles.},
author = {Gerner, Martin and Nenadic, Goran and Bergman, Casey M},
doi = {10.1186/1471-2105-11-85},
issn = {1471-2105},
journal = {BMC Bioinformatics},
number = {1},
pages = {85},
title = {{LINNAEUS: A species name identification system for biomedical literature}},
url = {https://doi.org/10.1186/1471-2105-11-85},
volume = {11},
year = {2010}
}
```

### Contributions

Thanks to [@edugp](https://github.com/edugp) for adding this dataset.
