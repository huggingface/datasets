---
annotations_creators:
- found
language_creators:
- found
languages:
  ar-en:
  - ar
  - en
  ar-es:
  - ar
  - es
  ar-fr:
  - ar
  - fr
  ar-ru:
  - ar
  - ru
  ar-zh:
  - ar
  - zh
  en-es:
  - en
  - es
  en-fr:
  - en
  - fr
  en-ru:
  - en
  - ru
  en-zh:
  - en
  - zh
  es-fr:
  - es
  - fr
  es-ru:
  - es
  - ru
  es-zh:
  - es
  - zh
  fr-ru:
  - fr
  - ru
  fr-zh:
  - fr
  - zh
  ru-zh:
  - ru
  - zh
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: united-nations-parallel-corpus
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

- **Homepage:**[UNPC](http://opus.nlpl.eu/UNPC.php)
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

This parallel corpus consists of manually translated UN documents from the last 25 years (1990 to 2014) \
for the six official UN languages, Arabic, Chinese, English, French, Russian, and Spanish.
6 languages, 15 bitexts

### Supported Tasks and Leaderboards

The underlying task is machine translation.

### Languages

[More Information Needed]

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

[More Information Needed]

### Citation Information

```
@inproceedings{ziemski-etal-2016-united,
    title = "The {U}nited {N}ations Parallel Corpus v1.0",
    author = "Ziemski, Micha{\\l}  and
      Junczys-Dowmunt, Marcin  and
      Pouliquen, Bruno",
    booktitle = "Proceedings of the Tenth International Conference on Language Resources and Evaluation ({LREC}'16)",
    month = may,
    year = "2016",
    address = "Portoro{\v{z}}, Slovenia",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://www.aclweb.org/anthology/L16-1561",
    pages = "3530--3534",
    abstract = "This paper describes the creation process and statistics of the official United Nations Parallel Corpus, the first parallel corpus composed from United Nations documents published by the original data creator. The parallel corpus presented consists of manually translated UN documents from the last 25 years (1990 to 2014) for the six official UN languages, Arabic, Chinese, English, French, Russian, and Spanish. The corpus is freely available for download under a liberal license. Apart from the pairwise aligned documents, a fully aligned subcorpus for the six official UN languages is distributed. We provide baseline BLEU scores of our Moses-based SMT systems trained with the full data of language pairs involving English and for all possible translation directions of the six-way subcorpus.",
}
```
### Contributions

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.