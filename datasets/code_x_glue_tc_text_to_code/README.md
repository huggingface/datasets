---
annotations_creators:
- found
language_creators:
- found
languages:
- en
- java
licenses:
- other-C-UDA
multilinguality:
- other-programming-languages
size_categories:
- 100K<n<1M
source_datasets: []
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
---
# Dataset Card for "code_x_glue_tc_text_to_code"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)



## [Dataset Description](#dataset-description)

 
- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code

 

### [Dataset Summary](#dataset-summary)


CodeXGLUE text-to-code dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code

The dataset we use is crawled and filtered from Microsoft Documentation, whose document located at https://github.com/MicrosoftDocs/.


## [Dataset Structure](#dataset-structure)
 

### [Data Instances](#data-instances)

 

 

An example of 'train' looks as follows.
```
{
    "code": "boolean function ( ) { return isParsed ; }", 
    "id": 0, 
    "nl": "check if details are parsed . concode_field_sep Container parent concode_elem_sep boolean isParsed concode_elem_sep long offset concode_elem_sep long contentStartPosition concode_elem_sep ByteBuffer deadBytes concode_elem_sep boolean isRead concode_elem_sep long memMapSize concode_elem_sep Logger LOG concode_elem_sep byte[] userType concode_elem_sep String type concode_elem_sep ByteBuffer content concode_elem_sep FileChannel fileChannel concode_field_sep Container getParent concode_elem_sep byte[] getUserType concode_elem_sep void readContent concode_elem_sep long getOffset concode_elem_sep long getContentSize concode_elem_sep void getContent concode_elem_sep void setDeadBytes concode_elem_sep void parse concode_elem_sep void getHeader concode_elem_sep long getSize concode_elem_sep void parseDetails concode_elem_sep String getType concode_elem_sep void _parseDetails concode_elem_sep String getPath concode_elem_sep boolean verify concode_elem_sep void setParent concode_elem_sep void getBox concode_elem_sep boolean isSmallBox"
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




