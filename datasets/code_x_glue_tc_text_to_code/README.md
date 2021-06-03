---
annotations_creators:
- found
language_creators:
- found
languages:
- code
- en
licenses:
- other-C-UDA
multilinguality:
- other-programming-languages
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
---
# Dataset Card for "code_x_glue_tc_text_to_code"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
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

## [Dataset Description](#dataset-description)

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code

### [Dataset Summary](#dataset-summary)

CodeXGLUE text-to-code dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code

The dataset we use is crawled and filtered from Microsoft Documentation, whose document located at https://github.com/MicrosoftDocs/.

### [Supported Tasks](#supported-tasks)

[More Information Needed]

## [Dataset Structure](#dataset-structure)

### [Data Instances](#data-instances)

An example of 'validation' looks as follows.
```
{
    "code": "int function ( ) { _total = extractList ( ) . size ( ) ; return _total ; }",
    "id": 0,
    "nl": "actually walks the bag to make sure the count is correct and resets the running total concode_field_sep Object _current concode_elem_sep int _total concode_elem_sep DefaultMapBag _parent concode_elem_sep Map _map concode_elem_sep int _mods concode_elem_sep Iterator _support concode_field_sep boolean add concode_elem_sep boolean add concode_elem_sep Object next concode_elem_sep boolean containsAll concode_elem_sep boolean containsAll concode_elem_sep void clear concode_elem_sep boolean isEmpty concode_elem_sep boolean hasNext concode_elem_sep void remove concode_elem_sep boolean remove concode_elem_sep boolean remove concode_elem_sep Map getMap concode_elem_sep int modCount concode_elem_sep boolean contains concode_elem_sep Iterator iterator concode_elem_sep boolean removeAll concode_elem_sep int size concode_elem_sep boolean addAll concode_elem_sep int hashCode concode_elem_sep boolean equals concode_elem_sep Object[] toArray concode_elem_sep Object[] toArray concode_elem_sep Set uniqueSet concode_elem_sep void setMap concode_elem_sep String toString concode_elem_sep int getCount concode_elem_sep List extractList concode_elem_sep boolean retainAll concode_elem_sep boolean retainAll"
}
```

### [Data Fields](#data-fields)

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name| type |                 description                 |
|----------|------|---------------------------------------------|
|id        |int32 | Index of the sample                         |
|nl        |string| The natural language description of the task|
|code      |string| The programming source code for the task    |

### [Data Splits](#data-splits)

| name  |train |validation|test|
|-------|-----:|---------:|---:|
|default|100000|      2000|2000|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed]

### [Source Data](#source-data)

[More Information Needed]

### [Annotations](#annotations)

[More Information Needed]

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed]

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed]

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed]

### [Other Known Limitations](#other-known-limitations)

[More Information Needed]

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

https://github.com/microsoft, https://github.com/madlag

### [Licensing Information](#licensing-information)

Computational Use of Data Agreement (C-UDA) License.

### [Citation Information](#citation-information)

```
@article{iyer2018mapping,
  title={Mapping language to code in programmatic context},
  author={Iyer, Srinivasan and Konstas, Ioannis and Cheung, Alvin and Zettlemoyer, Luke},
  journal={arXiv preprint arXiv:1808.09588},
  year={2018}
}
```

