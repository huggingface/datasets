---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- code
licenses:
- other-C-UDA
multilinguality:
- other-programming-languages
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- conditional-text-generation-other-debugging
---

# Dataset Card for "code_x_glue_cc_code_refinement"

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

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-refinement

### [Dataset Summary](#dataset-summary)

CodeXGLUE code-refinement dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-refinement

We use the dataset released by this paper(https://arxiv.org/pdf/1812.08693.pdf). The source side is a Java function with bugs and the target side is the refined one. All the function and variable names are normalized. Their dataset contains two subsets ( i.e.small and medium) based on the function length.

### [Supported Tasks](#supported-tasks)

[More Information Needed]

## [Dataset Structure](#dataset-structure)

### [Data Instances](#data-instances)

#### medium

An example of 'train' looks as follows.
```
{
    "buggy": "public static TYPE_1 init ( java.lang.String name , java.util.Date date ) { TYPE_1 VAR_1 = new TYPE_1 ( ) ; VAR_1 . METHOD_1 ( name ) ; java.util.Calendar VAR_2 = java.util.Calendar.getInstance ( ) ; VAR_2 . METHOD_2 ( date ) ; VAR_1 . METHOD_3 ( VAR_2 ) ; return VAR_1 ; }\n",
    "fixed": "public static TYPE_1 init ( java.lang.String name , java.util.Date date ) { TYPE_1 VAR_1 = new TYPE_1 ( ) ; VAR_1 . METHOD_1 ( name ) ; java.util.Calendar VAR_2 = null ; if ( date != null ) { VAR_2 = java.util.Calendar.getInstance ( ) ; VAR_2 . METHOD_2 ( date ) ; } VAR_1 . METHOD_3 ( VAR_2 ) ; return VAR_1 ; }\n",
    "id": 0
}
```

#### small

An example of 'test' looks as follows.
```
{
    "buggy": "private TYPE_1 getType ( TYPE_2 VAR_1 ) { TYPE_3 VAR_2 = new TYPE_3 ( STRING_1 ) ; return new TYPE_1 ( VAR_2 , VAR_2 ) ; } \n",
    "fixed": "private TYPE_1 getType ( TYPE_2 VAR_1 ) { TYPE_3 VAR_2 = new TYPE_3 ( STRING_1 ) ; return new TYPE_1 ( VAR_2 , VAR_2 , this , VAR_1 ) ; } \n",
    "id": 0
}
```

### [Data Fields](#data-fields)

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### medium, small

|field name| type |          description           |
|----------|------|--------------------------------|
|id        |int32 | Index of the sample            |
|buggy     |string| The buggy version of the code  |
|fixed     |string| The correct version of the code|

### [Data Splits](#data-splits)

| name |train|validation|test|
|------|----:|---------:|---:|
|medium|52364|      6546|6545|
|small |46680|      5835|5835|

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
@article{CodeXGLUE,
         title={CodeXGLUE: A Benchmark Dataset and Open Challenge for Code Intelligence},
         year={2020},}
```

