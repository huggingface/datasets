---
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
paperswithcode_id: null
pretty_name: WikiTableQuestions
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- question-answering-other-table-question-answering
---

# Dataset Card for WikiTableQuestions

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

- **Homepage:** [WikiTableQuestions homepage](https://nlp.stanford.edu/software/sempre/wikitable)
- **Repository:** [WikiTableQuestions repository](https://github.com/ppasupat/WikiTableQuestions)
- **Paper:** [Compositional Semantic Parsing on Semi-Structured Tables](https://arxiv.org/abs/1508.00305)
- **Leaderboard:** [WikiTableQuestions leaderboard on PaperWithCode](https://paperswithcode.com/dataset/wikitablequestions)
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The WikiTableQuestions dataset is a large-scale dataset for the task of question answering on semi-structured tables.

### Supported Tasks and Leaderboards

question-answering, table-question-answering

### Languages

en

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 27.91 MB
- **Size of the generated dataset:** 45.68 MB
- **Total amount of disk used:** 73.60 MB

An example of 'validation' looks as follows:
```
{
    "id": "nt-0",
    "question": "what was the last year where this team was a part of the usl a-league?",
    "answers": ["2004"],
    "table": {
        "header": ["Year", "Division", "League", ...], 
        "name": "csv/204-csv/590.csv", 
        "rows": [
           ["2001", "2", "USL A-League", ...],
           ["2002", "2", "USL A-League", ...], 
           ...
        ]
    }
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `id`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a `list` of `string` feature.
- `table`: a dictionary feature containing:
  - `header`: a `list` of `string` features.
  - `rows`: a `list` of `list` of `string` features:
  - `name`: a `string` feature.

### Data Splits

| name  |train|validation|test |
|-------|----:|---------:|----:|
|default|11321|      2831|4344|

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

Panupong Pasupat and Percy Liang

### Licensing Information

Creative Commons Attribution Share Alike 4.0 International

### Citation Information

```
@inproceedings{pasupat-liang-2015-compositional,
    title = "Compositional Semantic Parsing on Semi-Structured Tables",
    author = "Pasupat, Panupong and Liang, Percy",
    booktitle = "Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",
    month = jul,
    year = "2015",
    address = "Beijing, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P15-1142",
    doi = "10.3115/v1/P15-1142",
    pages = "1470--1480",
}
```

### Contributions

Thanks to [@SivilTaram](https://github.com/SivilTaram) for adding this dataset.
