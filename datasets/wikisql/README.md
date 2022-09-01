---
language:
- en
paperswithcode_id: wikisql
pretty_name: WikiSQL
---

# Dataset Card for "wikisql"

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

- **Homepage:** [https://github.com/salesforce/WikiSQL](https://github.com/salesforce/WikiSQL)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 24.95 MB
- **Size of the generated dataset:** 147.57 MB
- **Total amount of disk used:** 172.52 MB

### Dataset Summary

A large crowd-sourced dataset for developing natural language interfaces for relational databases

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 24.95 MB
- **Size of the generated dataset:** 147.57 MB
- **Total amount of disk used:** 172.52 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "phase": 1,
    "question": "How would you answer a second test question?",
    "sql": {
        "agg": 0,
        "conds": {
            "column_index": [2],
            "condition": ["Some Entity"],
            "operator_index": [0]
        },
        "human_readable": "SELECT Header1 FROM table WHERE Another Header = Some Entity",
        "sel": 0
    },
    "table": "{\"caption\": \"L\", \"header\": [\"Header1\", \"Header 2\", \"Another Header\"], \"id\": \"1-10015132-9\", \"name\": \"table_10015132_11\", \"page_i..."
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `phase`: a `int32` feature.
- `question`: a `string` feature.
- `header`: a `list` of `string` features.
- `page_title`: a `string` feature.
- `page_id`: a `string` feature.
- `types`: a `list` of `string` features.
- `id`: a `string` feature.
- `section_title`: a `string` feature.
- `caption`: a `string` feature.
- `rows`: a dictionary feature containing:
  - `feature`: a `string` feature.
- `name`: a `string` feature.
- `human_readable`: a `string` feature.
- `sel`: a `int32` feature.
- `agg`: a `int32` feature.
- `conds`: a dictionary feature containing:
  - `column_index`: a `int32` feature.
  - `operator_index`: a `int32` feature.
  - `condition`: a `string` feature.

### Data Splits

| name  |train|validation|test |
|-------|----:|---------:|----:|
|default|56355|      8421|15878|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@article{zhongSeq2SQL2017,
  author    = {Victor Zhong and
               Caiming Xiong and
               Richard Socher},
  title     = {Seq2SQL: Generating Structured Queries from Natural Language using
               Reinforcement Learning},
  journal   = {CoRR},
  volume    = {abs/1709.00103},
  year      = {2017}
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@ghomasHudson](https://github.com/ghomasHudson), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
