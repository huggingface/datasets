---
annotations_creators:
- expert-generated
language_creators:
- other
languages:
- pl
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- summarization
paperswithcode_id: null
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

- **Homepage:**
  http://zil.ipipan.waw.pl/PolishSummariesCorpus
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The Polish Summaries Corpus contains news articles and their summaries. We used summaries of the same article as positive pairs and sampled the most similar summaries of different articles as negatives.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Polish

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- extract_text: text to summarise
- summary_text: summary of extracted text 
- label: 1 indicates summary is similar, 0 means that it is not similar

### Data Splits

Data is splitted in train and test dataset. Test dataset doesn't have label column, so -1 is set instead.

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

CC BY-SA 3.0

### Citation Information

@inproceedings{ogro:kop:14:lrec,
title={The {P}olish {S}ummaries {C}orpus},
author={Ogrodniczuk, Maciej and Kope{\'c}, Mateusz},
booktitle = "Proceedings of the Ninth International {C}onference on {L}anguage {R}esources and {E}valuation, {LREC}~2014",
year = "2014",
}

### Contributions

Thanks to [@abecadel](https://github.com/abecadel) for adding this dataset.