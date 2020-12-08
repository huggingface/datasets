---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
  ca:
  - ca
  eu:
  - eu
licenses:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
---

# Dataset Card for MultiBooked

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

- **Homepage:** http://hdl.handle.net/10230/33928
- **Repository:** https://github.com/jerbarnes/multibooked
- **Paper:** https://arxiv.org/abs/1803.08614
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

MultiBooked is a corpus of Basque and Catalan Hotel Reviews Annotated for Aspect-level Sentiment Classification.

The corpora are compiled from hotel reviews taken mainly from booking.com. The corpora are in Kaf/Naf format, which is
an xml-style stand-off format that allows for multiple layers of annotation. Each review was sentence- and
word-tokenized and lemmatized using Freeling for Catalan and ixa-pipes for Basque. Finally, for each language two
annotators annotated opinion holders, opinion targets, and opinion expressions for each review, following the
guidelines set out in the OpeNER project.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Each sub-dataset is monolingual in the languages:
- ca: Catalan
- eu: Basque

## Dataset Structure

### Data Instances

[More Information Needed]

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

Dataset is under the [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license.

### Citation Information

```
@inproceedings{Barnes2018multibooked,
    author={Barnes, Jeremy and Lambert, Patrik and Badia, Toni},
    title={MultiBooked: A corpus of Basque and Catalan Hotel Reviews Annotated for Aspect-level Sentiment Classification},
    booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC'18)},
    year = {2018},
    month = {May},
    date = {7-12},
    address = {Miyazaki, Japan},
    publisher = {European Language Resources Association (ELRA)},
    language = {english}
}
```
