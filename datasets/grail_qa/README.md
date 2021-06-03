---
annotations_creators:
- crowdsourced
language_creators:
- found
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
- question-answering
task_ids:
- question-answering-other-knowledge-base-qa
paperswithcode_id: null
---

# Dataset Card for Grail QA

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

- **Homepage: [Grail QA](https://dki-lab.github.io/GrailQA/)**
- **Repository:**
- **Paper:[GrailQA paper (Gu et al. '20)](https://arxiv.org/abs/2011.07743)**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

#### What is GrailQA?

Strongly Generalizable Question Answering (GrailQA) is a new large-scale, high-quality dataset for question answering on knowledge bases (KBQA) on Freebase with 64,331 questions annotated with both answers and corresponding logical forms in different syntax (i.e., SPARQL, S-expression, etc.). It can be used to test three levels of generalization in KBQA: i.i.d., compositional, and zero-shot.

#### Why GrailQA?

GrailQA is by far the largest crowdsourced KBQA dataset with questions of high diversity (i.e., questions in GrailQA can have up to 4 relations and optionally have a function from counting, superlatives and comparatives). It also has the highest coverage over Freebase; it widely covers 3,720 relations and 86 domains from Freebase. Last but not least, our meticulous data split allows GrailQA to test not only i.i.d. generalization, but also compositional generalization and zero-shot generalization, which are critical for practical KBQA systems.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English and Graph query

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- `qid` (`str`)
- `question` (`str`)
- `answer` (`List`): Defaults to `[]` in test split.
  - `answer_type` (`str`)
  - `answer_argument` (`str`)
  - `entity_name` (`str`): Defauts to `""` if `answer_type` is not `Entity`.
- `function` (`string`): Defaults to `""` in test split.
- `num_node` (`int`): Defaults to `-1` in test split.
- `num_edge` (`int`): Defaults to `-1` in test split.
- `graph_query` (`Dict`)
  - `nodes` (`List`): Defaults to `[]` in test split.
    - `nid` (`int`)
    - `node_type` (`str`)
    - `id` (`str`)
    - `class` (`str`)
    - `friendly_name` (`str`)
    - `question_node` (`int`)
    - `function` (`str`)
  - `edges` (`List`): Defaults to `[]` in test split.
    - `start` (`int`)
    - `end` (`int`)
    - `relation` (`str`)
    - `friendly_name` (`str`)
- `sqarql_query` (`str`): Defaults to `""` in test split.
- `domains` (`List[str]`): Defaults to `[]` in test split.
- `level` (`str`): Only available in validation split. Defaults to `""` in others.
- `s_expression` (`str`): Defaults to `""` in test split.

**Notes:** Only `qid` and `question` available in test split.

### Data Splits

Dataset Split | Number of Instances in Split
--------------|--------------------------------------------
Train | 44,337
Validation | 6,763
Test | 13,231

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

[More Information Needed]

### Contributions

Thanks to [@mattbui](https://github.com/mattbui) for adding this dataset.