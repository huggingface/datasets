---
annotations_creators: []
language_creators: []
languages:
- zh
- de
- es
- fr
- it
- ja
- pt'
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- multilingual
pretty_name: xfun
size_categories:
- unknown
source_datasets:
- original
task_categories:
- other
task_ids: []
---

# Dataset Card for XFUN

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage: https://github.com/doc-analysis/XFUND**
- **Repository: https://github.com/doc-analysis/XFUND**
- **Paper: https://arxiv.org/abs/2104.08836**
- **Leaderboard:**
- **Point of Contact: Lei Cui (`lecu@microsoft.com`) or Furu Wei (`fuwei@microsoft.com`)**

### Dataset Summary

XFUND is a multilingual form understanding benchmark dataset that includes human-labeled forms with key-value pairs in 7 languages (Chinese, Japanese, Spanish, French, Italian, German, Portuguese).

### Supported Tasks and Leaderboards

Key-value pair relation-extraction.

### Languages

Chinese, Japanese, Spanish, French, Italian, German, Portuguese

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields


- `id`: a `string` feature.
- `input_ids`: a sequence feature containing `int64` features.
- `bbox`: a sequence feature containing:
  - a sequence feature containing:
    -  a `int64` feature.
- `labels`: a sequence feature containing:
  - a `ClassLabel` feature representing one of `O`, `B-QUESTION`, `B-ANSWER`, `B-HEADER`, `I-ANSWER`, `I-QUESTION`, and `I-HEADER` class.
- `image`: a `Array3D` feature with shape (3, 224, 224) and dtype `uint8`.
- `entities`: a sequence feature containing:
  - a dictionary feature containing:
    - `start`: a `int64` feature.
    - `end`: a `int64` feature.
    - `label`: a `ClassLabel` feature with one of `HEADER`, `QUESTION`, and `ANSWER` class.    
- `relations`: a sequence feature containing:
  - a dictionary feature containing:
    - `head`: a `int64` feature.
    - `tail`: a `int64` feature.
    - `start_index`: a `int64` feature.
    - `end_index`: a `int64` feature.


### Data Splits

| config  | split    | header | question | answer | other | total  |
| ------- | -------- | ------ | -------- | ------ | ----- | ------ |
| xfun.zh | training | 441    | 3,266    | 2,808  | 896   | 7,411  |
|         | testing  | 122    | 1,077    | 821    | 312   | 2,332  |
| xfun.ja | training | 229    | 3,692    | 4,641  | 1,666 | 10,228 |
|         | testing  | 58     | 1,253    | 1,732  | 586   | 3,629  |
| xfun.es | training | 253    | 3,013    | 4,254  | 3,929 | 11,449 |
|         | testing  | 90     | 909      | 1,218  | 1,196 | 3,413  |
| xfun.fr | training | 183    | 2,497    | 3,427  | 2,709 | 8,816  |
|         | testing  | 66     | 1,023    | 1,281  | 1,131 | 3,501  |
| xfun.it | training | 166    | 3,762    | 4,932  | 3,355 | 12,215 |
|         | testing  | 65     | 1,230    | 1,599  | 1,135 | 4,029  |
| xfun.de | training | 155    | 2,609    | 3,992  | 1,876 | 8,632  |
|         | testing  | 59     | 858      | 1,322  | 650   | 2,889  |
| xfun.pt | training | 185    | 3,510    | 5,428  | 2,531 | 11,654 |
|         | testing  | 59     | 1,288    | 1,940  | 882   | 4,169  |

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

Yiheng Xu, Tengchao Lv, Lei Cui, Guoxin Wang, Yijuan Lu, Dinei Florencio, Cha Zhang, Furu Wei

### Licensing Information

The content of this project itself is licensed under the [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
Portions of the source code are based on the [transformers](https://github.com/huggingface/transformers) project.
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct)

### Citation Information

```
@article{Xu2020LayoutXLMMP,
  title         = {LayoutXLM: Multimodal Pre-training for Multilingual Visually-rich Document Understanding},
  author        = {Yiheng Xu and Tengchao Lv and Lei Cui and Guoxin Wang and Yijuan Lu and Dinei Florencio and Cha Zhang and Furu Wei},
  year          = {2021},
  eprint        = {2104.08836},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CL}
}
```

### Contributions

Thanks to [@qqaatw](https://github.com/qqaatw) for adding this dataset.
