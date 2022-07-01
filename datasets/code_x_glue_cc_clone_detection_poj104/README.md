---
pretty_name: CodeXGlueCcCloneDetectionPoj104
annotations_creators:
- found
language_creators:
- found
language:
- code
license:
- c-uda
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

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-POJ-104

### Dataset Summary

CodeXGLUE Clone-detection-POJ-104 dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-POJ-104

Given a code and a collection of candidates as the input, the task is to return Top K codes with the same semantic. Models are evaluated by MAP score.
We use POJ-104 dataset on this task.

### Supported Tasks and Leaderboards

- `document-retrieval`: The dataset can be used to train a model for retrieving top-k codes with the same semantics.

### Languages

- C++ **programming** language

## Dataset Structure

### Data Instances

An example of 'train' looks as follows.
```
{
    "code": "\nint f(int shu,int min)\n{ \n  int k=1;\n  if(shu < min)\n  { \n    k= 0; \n   return k;\n  } \n  else\n {\n  for(int i = min;i<shu;i++)\n  { \n    if(shu%i == 0)\n    { \n         k=k+ f(shu/i,i); \n    } \n  \n    \n  } \n    return k; \n}\n} \n\nmain()\n{\n      int n,i,a;\n      scanf(\"%d\",&n);\n      \n      for(i=0;i<n;i++)\n      {\n          scanf(\"%d\",&a);\n          \n          if(i!=n-1)                                                        \n           printf(\"%d\\n\",f(a,2));\n           else\n           printf(\"%d\",f(a,2));                           \n                                      \n                     \n                      \n      }              \n                     \n                      \n                      }", 
    "id": 0, 
    "label": "home"
}
```

### Data Fields

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name| type |                 description                  |
|----------|------|----------------------------------------------|
|id        |int32 | Index of the sample                          |
|code      |string| The full text of the function                |
|label     |string| The id of problem that the source code solves|

### Data Splits

| name  |train|validation|test |
|-------|----:|---------:|----:|
|default|32000|      8000|12000|

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
@inproceedings{mou2016convolutional,
  title={Convolutional neural networks over tree structures for programming language processing},
  author={Mou, Lili and Li, Ge and Zhang, Lu and Wang, Tao and Jin, Zhi},
  booktitle={Proceedings of the Thirtieth AAAI Conference on Artificial Intelligence},
  pages={1287--1293},
  year={2016}
}
```

### Contributions

Thanks to @madlag (and partly also @ncoop57) for adding this dataset.
