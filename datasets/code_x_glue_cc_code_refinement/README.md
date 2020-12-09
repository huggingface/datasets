---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- java
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
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)



## [Dataset Description](#dataset-description)

 
- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-refinement

 

### [Dataset Summary](#dataset-summary)


CodeXGLUE code-refinement dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-refinement

We use the dataset released by this paper(https://arxiv.org/pdf/1812.08693.pdf). The source side is a Java function with bugs and the target side is the refined one. All the function and variable names are normalized. Their dataset contains two subsets ( i.e.small and medium) based on the function length.


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

An example of 'validation' looks as follows.
```
{
    "buggy": "public java.util.List < TYPE_1 > METHOD_1 ( ) { java.util.ArrayList < TYPE_1 > VAR_1 = new java.util.ArrayList < TYPE_1 > ( ) ; for ( TYPE_2 VAR_2 : VAR_3 ) { VAR_1 . METHOD_2 ( VAR_2 . METHOD_1 ( ) ) ; } return VAR_1 ; } \n", 
    "fixed": "public java.util.List < TYPE_1 > METHOD_1 ( ) { return VAR_1 ; } \n", 
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




