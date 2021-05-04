---
annotations_creators: []
language_creators: []
languages:
- de
licenses:
- other-ASL 2.0
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
---

# Dataset Card Creation Guide

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** None
- **Repository:** https://github.com/tudarmstadt-lt/GermaNER
- **Paper:** https://pdfs.semanticscholar.org/b250/3144ed2152830f6c64a9f797ab3c5a34fee5.pdf
- **Leaderboard:** [If the dataset supports an active leaderboard, add link here]()
- **Point of Contact:** Darina Benikova (benikova@aiphes.tu-darmstadt.de,)

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

German

## Dataset Structure

### Data Instances

An example instance looks as follows:

```
{
  'id': '3', 
  'ner_tags': [1, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], 
  'tokens': ['Bayern', 'München', 'ist', 'wieder', 'alleiniger', 'Top-', 'Favorit', 'auf', 'den', 'Gewinn', 'der', 'deutschen', 'Fußball-Meisterschaft', '.']
}
```

### Data Fields

Each instance in the dataset has:
- an id
- sequence of tokens
- NER tags for each token (encoded as IOB)

NER tags can be: 'B-LOC', 'B-ORG', 'B-OTH', 'B-PER', 'I-LOC', 'I-ORG', 'I-OTH', 'I-PER', 'O'

### Data Splits

Dataset provides only train part (26200 data instances).

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

[More Information Needed]
### Contributions

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.
