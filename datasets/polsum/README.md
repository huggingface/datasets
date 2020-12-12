---
annotations_creators: 
- expert-generated
language_creators: 
- expert-generated
languages: 
- pl
licenses: 
- cc-by-3.0
multilinguality: 
- monolingual
size_categories: 
- n<1K
source_datasets: 
- original
task_categories: 
- conditional-text-generation
task_ids: 
- summarization
---

# Dataset Card for polsum

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

- **Homepage:** http://zil.ipipan.waw.pl/PolishSummariesCorpus
- **Repository:** http://zil.ipipan.waw.pl/PolishSummariesCorpus
- **Paper:** http://nlp.ipipan.waw.pl/Bib/ogro:kop:14:lrec.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Mateusz Kopeć](http://zil.ipipan.waw.pl/MateuszKopec)

### Dataset Summary

The Corpus contains a large number of manual summaries of news articles,
with many independently created summaries for a single text. Such approach is supposed to overcome the annotator bias, which is often described as a problem during the evaluation of the summarization algorithms against a single gold standard.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Polish

## Dataset Structure

### Data Instances

[Needs More Information]

### Data Fields

- `id`: a `string` feature.
- `date`: a `string` feature.
- `title`: a `string` feature.
- `section`: a `string` feature.
- `authors`: a `string` feature.
- `body`: a `string` feature.
- `summaries`: a dictionary feature containing:
  - `ratio`: a `string` feature.
  - `type`: a `string` feature.
  - `author`: a `string` feature.
  - `body`: a `string` feature.
  - `spans`: a dictionary feature containing:
    - `start`: a `int32` feature.
    - `end`: a `int32` feature.
    - `span_text`: a `string` feature.

### Data Splits

Single train split

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
```
@inproceedings{
    ogro:kop:14:lrec,
    author = "Ogrodniczuk, Maciej and Kopeć, Mateusz",
    pdf = "http://nlp.ipipan.waw.pl/Bib/ogro:kop:14:lrec.pdf",
    title = "The {P}olish {S}ummaries {C}orpus",
    pages = "3712--3715",
    crossref = "lrec:14"
}
@proceedings{
    lrec:14,
    editor = "Calzolari, Nicoletta and Choukri, Khalid and Declerck, Thierry and Loftsson, Hrafn and Maegaard, Bente and Mariani, Joseph and Moreno, Asuncion and Odijk, Jan and Piperidis, Stelios",
    isbn = "978-2-9517408-8-4",
    title = "Proceedings of the Ninth International {C}onference on {L}anguage {R}esources and {E}valuation, {LREC}~2014",
    url = "http://www.lrec-conf.org/proceedings/lrec2014/index.html",
    booktitle = "Proceedings of the Ninth International {C}onference on {L}anguage {R}esources and {E}valuation, {LREC}~2014",
    address = "Reykjavík, Iceland",
    key = "LREC",
    year = "2014",
    organization = "European Language Resources Association (ELRA)"
}
```