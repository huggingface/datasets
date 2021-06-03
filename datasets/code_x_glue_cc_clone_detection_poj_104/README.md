---
annotations_creators:
- found
language_creators:
- found
languages:
- code
- licenses:
- other-C-UDA
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-retrieval
task_ids:
- document-retrieval
---
# Dataset Card for "code_x_glue_cc_clone_detection_poj_104"

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

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-POJ-104

### [Dataset Summary](#dataset-summary)

CodeXGLUE Clone-detection-POJ-104 dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-POJ-104

Given a code and a collection of candidates as the input, the task is to return Top K codes with the same semantic. Models are evaluated by MAP score.
We use POJ-104 dataset on this task.

### [Supported Tasks](#supported-tasks)

[More Information Needed]

## [Dataset Structure](#dataset-structure)

### [Data Instances](#data-instances)

An example of 'validation' looks as follows.
```
{
    "code": " \nmain()\n{\n      int n,i,j, c,d;\n      int a=0,b=0;\n      scanf(\"%d\",&n);\n     for(i=0;i<n;i++)\n     {\n      scanf(\"%d%d\",&c,&d);\n      if(c==0&&d==1)a++;\n   if(c==0&&d==2)b++;\n       if(c==1)\n     {if(d==0)b++;\n     else if(d==2)a++;\n     }\n    else  if(c==2)\n     {if(d==0)a++;\n     if(d==1)b++;}\n                          \n     }\n                          if(a>b)printf(\"A\");\n                          else if(a<b)printf(\"B\");\n                          else printf(\"Tie\");\n       }\n\n",
    "id": 32000,
    "label": "home"
}
```

### [Data Fields](#data-fields)

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name| type |                 description                  |
|----------|------|----------------------------------------------|
|id        |int32 | Index of the sample                          |
|code      |string| The full text of the function                |
|label     |string| The id of problem that the source code solves|

### [Data Splits](#data-splits)

| name  |train|validation|test |
|-------|----:|---------:|----:|
|default|32000|      8000|12000|

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
@inproceedings{mou2016convolutional,
  title={Convolutional neural networks over tree structures for programming language processing},
  author={Mou, Lili and Li, Ge and Zhang, Lu and Wang, Tao and Jin, Zhi},
  booktitle={Proceedings of the Thirtieth AAAI Conference on Artificial Intelligence},
  pages={1287--1293},
  year={2016}
}
```

