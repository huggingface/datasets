---
annotations_creators:
- found
language_creators:
- found
languages:
- C
licenses:
- other-C-UDA
multilinguality:
- other-programming-languages
size_categories:
- 10K<n<100K
source_datasets: []
task_categories:
- text-classification
task_ids:
- multi-class-classification
---
# Dataset Card for "code_x_glue_cc_defect_detection"

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

 
- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection

 

### [Dataset Summary](#dataset-summary)


CodeXGLUE Defect-detection dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection

Given a source code, the task is to identify whether it is an insecure code that may attack software systems, such as resource leaks, use-after-free vulnerabilities and DoS attack. We treat the task as binary classification (0/1), where 1 stands for insecure code and 0 for secure code.
The dataset we use comes from the paper Devign: Effective Vulnerability Identification by Learning Comprehensive Program Semantics via Graph Neural Networks. We combine all projects and split 80%/10%/10% for training/dev/test.


## [Dataset Structure](#dataset-structure)
 

### [Data Instances](#data-instances)

 

 

An example of 'validation' looks as follows.
```
{
    "commit_id": "aa1530dec499f7525d2ccaa0e3a876dc8089ed1e", 
    "func": "static void filter_mirror_setup(NetFilterState *nf, Error **errp)\n{\n    MirrorState *s = FILTER_MIRROR(nf);\n    Chardev *chr;\n    chr = qemu_chr_find(s->outdev);\n    if (chr == NULL) {\n        error_set(errp, ERROR_CLASS_DEVICE_NOT_FOUND,\n                  \"Device '%s' not found\", s->outdev);\n    qemu_chr_fe_init(&s->chr_out, chr, errp);", 
    "id": 8, 
    "project": "qemu", 
    "target": true
}
```
 



### [Data Fields](#data-fields)

 
In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name| type |               description                |
|----------|------|------------------------------------------|
|id        |int32 | Index of the sample                      |
|func      |string| The source code                          |
|target    |bool  | 0 or 1 (vulnerability or not)            |
|project   |string| Original project that contains this code |
|commit_id |string| Commit identifier in the original project|






### [Data Splits](#data-splits)

 


| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|21854|      2732|2732|







## [Additional Information](#additional-information)
 

### [Dataset Curators](#dataset-curators)


https://github.com/microsoft, https://github.com/madlag


### [Licensing Information](#licensing-information)


Computational Use of Data Agreement (C-UDA) License.


### [Citation Information](#citation-information)


```
@inproceedings{zhou2019devign,
title={Devign: Effective vulnerability identification by learning comprehensive program semantics via graph neural networks},
author={Zhou, Yaqin and Liu, Shangqing and Siow, Jingkai and Du, Xiaoning and Liu, Yang},
booktitle={Advances in Neural Information Processing Systems},
pages={10197--10207}, year={2019}
```




