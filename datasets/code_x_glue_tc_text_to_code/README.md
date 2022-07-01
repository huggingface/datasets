---
annotations_creators:
- found
language_creators:
- found
language:
- en
- code
license:
- c-uda
multilinguality:
- other-programming-languages
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- translation
task_ids:
- translation-other-text-to-code
pretty_name: CodeXGlueTcTextToCode
---
# Dataset Card for "code_x_glue_tc_text_to_code"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits-sample-size)
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

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code

### Dataset Summary

CodeXGLUE text-to-code dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code

The dataset we use is crawled and filtered from Microsoft Documentation, whose document located at https://github.com/MicrosoftDocs/.

### Supported Tasks and Leaderboards

- `machine-translation`: The dataset can be used to train a model for generating Java code from an **English** natural language description.

### Languages

- Java **programming** language

## Dataset Structure

### Data Instances

An example of 'train' looks as follows.
```
{
    "code": "boolean function ( ) { return isParsed ; }", 
    "id": 0, 
    "nl": "check if details are parsed . concode_field_sep Container parent concode_elem_sep boolean isParsed concode_elem_sep long offset concode_elem_sep long contentStartPosition concode_elem_sep ByteBuffer deadBytes concode_elem_sep boolean isRead concode_elem_sep long memMapSize concode_elem_sep Logger LOG concode_elem_sep byte[] userType concode_elem_sep String type concode_elem_sep ByteBuffer content concode_elem_sep FileChannel fileChannel concode_field_sep Container getParent concode_elem_sep byte[] getUserType concode_elem_sep void readContent concode_elem_sep long getOffset concode_elem_sep long getContentSize concode_elem_sep void getContent concode_elem_sep void setDeadBytes concode_elem_sep void parse concode_elem_sep void getHeader concode_elem_sep long getSize concode_elem_sep void parseDetails concode_elem_sep String getType concode_elem_sep void _parseDetails concode_elem_sep String getPath concode_elem_sep boolean verify concode_elem_sep void setParent concode_elem_sep void getBox concode_elem_sep boolean isSmallBox"
}
```

### Data Fields

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name| type |                 description                 |
|----------|------|---------------------------------------------|
|id        |int32 | Index of the sample                         |
|nl        |string| The natural language description of the task|
|code      |string| The programming source code for the task    |

### Data Splits

| name  |train |validation|test|
|-------|-----:|---------:|---:|
|default|100000|      2000|2000|

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

https://github.com/microsoft, https://github.com/madlag

### Licensing Information

Computational Use of Data Agreement (C-UDA) License.

### Citation Information

```
@article{iyer2018mapping,
  title={Mapping language to code in programmatic context},
  author={Iyer, Srinivasan and Konstas, Ioannis and Cheung, Alvin and Zettlemoyer, Luke},
  journal={arXiv preprint arXiv:1808.09588},
  year={2018}
}
```

### Contributions

Thanks to @madlag (and partly also @ncoop57) for adding this dataset.
