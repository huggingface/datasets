---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- th
licenses:
- cc-by-nc-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-thaiqa
task_categories:
- question-answering
task_ids:
- extractive-qa
- open-domain-qa
---

# Dataset Card for `thaiqa-squad`

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

- **Homepage:** http://github.com/pythainlp/thaiqa_squad (original `thaiqa` at https://aiforthai.in.th/)
- **Repository:** http://github.com/pythainlp/thaiqa_squad
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**http://github.com/pythainlp/ (original `thaiqa` at https://aiforthai.in.th/)

### Dataset Summary

`thaiqa_squad` is an open-domain, extractive question answering dataset (4,000 questions in `train` and 74 questions in `dev`) in [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) format, originally created by [NECTEC](https://www.nectec.or.th/en/) from Wikipedia articles and adapted to [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) format by [PyThaiNLP](https://github.com/PyThaiNLP/).

### Supported Tasks and Leaderboards

extractive question answering

### Languages

Thai

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

|                         | train       | valid       |
|-------------------------|-------------|-------------|
| # questions             | 4000        | 74          |
| # avg words in context  | 1186.740750 | 1016.459459 |
| # avg words in question | 14.325500   | 12.743243   |
| # avg words in answer   | 3.279750    | 4.608108    |

## Dataset Creation

### Curation Rationale

[PyThaiNLP](https://github.com/PyThaiNLP/) created `thaiqa_squad` as a [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) version of [thaiqa](http://copycatch.in.th/thai-qa-task.html). [thaiqa](https://aiforthai.in.th/corpus.php) is part of [The 2nd Question answering program from Thai Wikipedia](http://copycatch.in.th/thai-qa-task.html) of [National Software Contest 2020](http://nsc.siit.tu.ac.th/GENA2/login.php).

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Wikipedia authors for contexts and [NECTEC](https://www.nectec.or.th/en/) for questions and answer annotations

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[NECTEC](https://www.nectec.or.th/en/)

### Personal and Sensitive Information

All contents are from Wikipedia. No personal and sensitive information is expected to be included.

## Considerations for Using the Data

### Social Impact of Dataset

- open-domain, extractive question answering in Thai

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

- The contexts include `<doc>` tags at start and at the end

## Additional Information

### Dataset Curators

[NECTEC](https://www.nectec.or.th/en/) for original [thaiqa](https://aiforthai.in.th/corpus.php). SQuAD formattting by [PyThaiNLP](https://github.com/PyThaiNLP/).

### Licensing Information

CC-BY-NC-SA 3.0

### Citation Information

[More Information Needed]
