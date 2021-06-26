---
annotations_creators:
- crowdsourced
- found
language_creators:
- crowdsourced
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-nus-sms-corpus
task_categories:
- text-classification
task_ids:
- intent-classification
paperswithcode_id: sms-spam-collection-data-set
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

- **Homepage:** http://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection
- **Repository:**
- **Paper:** Almeida, T.A., Gomez Hidalgo, J.M., Yamakami, A. Contributions to the study of SMS Spam Filtering: New Collection and Results. Proceedings of the 2011 ACM Symposium on Document Engineering (ACM DOCENG'11), Mountain View, CA, USA, 2011.
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The SMS Spam Collection v.1 is a public set of SMS labeled messages that have been collected for mobile phone spam research. 
It has one collection composed by 5,574 English, real and non-enconded messages, tagged according being legitimate (ham) or spam.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- sms: the sms message
- label: indicating if the sms message is ham or spam, ham means it is not spam

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

@inproceedings{Almeida2011SpamFiltering,
  title={Contributions to the Study of SMS Spam Filtering: New Collection and Results},
  author={Tiago A. Almeida and Jose Maria Gomez Hidalgo and Akebo Yamakami},
  year={2011},
  booktitle = "Proceedings of the 2011 ACM Symposium on Document Engineering (DOCENG'11)",
}

### Contributions

Thanks to [@czabo](https://github.com/czabo) for adding this dataset.