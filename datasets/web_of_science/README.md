---
language:
- en
paperswithcode_id: web-of-science-dataset
pretty_name: Web of Science Dataset
---

# Dataset Card for "web_of_science"

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

- **Homepage:** [https://data.mendeley.com/datasets/9rw3vkcfy4/6](https://data.mendeley.com/datasets/9rw3vkcfy4/6)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 172.30 MB
- **Size of the generated dataset:** 85.65 MB
- **Total amount of disk used:** 257.95 MB

### Dataset Summary

Copyright (c) 2017 Kamran Kowsari

Permission is hereby granted, free of charge, to any person obtaining a copy of this dataset and associated documentation files (the "Dataset"), to deal
in the dataset without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Dataset, and to permit persons to whom the dataset is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Dataset.

If you use this dataset please cite: Referenced paper: HDLTex: Hierarchical Deep Learning for Text Classification

Description of Dataset:

Here is three datasets which include WOS-11967 , WOS-46985, and WOS-5736
Each folder contains:
-X.txt
-Y.txt
-YL1.txt
-YL2.txt

X is input data that include text sequences
Y is target value
YL1 is target value of level one (parent label)
YL2 is target value of level one (child label)
Web of Science Dataset WOS-5736
                        -This dataset contains 5,736 documents with 11 categories which include 3 parents categories.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### WOS11967

- **Size of downloaded dataset files:** 57.43 MB
- **Size of the generated dataset:** 15.50 MB
- **Total amount of disk used:** 72.94 MB

An example of 'train' looks as follows.
```

```

#### WOS46985

- **Size of downloaded dataset files:** 57.43 MB
- **Size of the generated dataset:** 62.47 MB
- **Total amount of disk used:** 119.90 MB

An example of 'train' looks as follows.
```

```

#### WOS5736

- **Size of downloaded dataset files:** 57.43 MB
- **Size of the generated dataset:** 7.68 MB
- **Total amount of disk used:** 65.11 MB

An example of 'train' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### WOS11967
- `input_data`: a `string` feature.
- `label`: a `int32` feature.
- `label_level_1`: a `int32` feature.
- `label_level_2`: a `int32` feature.

#### WOS46985
- `input_data`: a `string` feature.
- `label`: a `int32` feature.
- `label_level_1`: a `int32` feature.
- `label_level_2`: a `int32` feature.

#### WOS5736
- `input_data`: a `string` feature.
- `label`: a `int32` feature.
- `label_level_1`: a `int32` feature.
- `label_level_2`: a `int32` feature.

### Data Splits

|  name  |train|
|--------|----:|
|WOS11967|11967|
|WOS46985|46985|
|WOS5736 | 5736|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@inproceedings{kowsari2017HDLTex,
title={HDLTex: Hierarchical Deep Learning for Text Classification},
author={Kowsari, Kamran and Brown, Donald E and Heidarysafa, Mojtaba and Jafari Meimandi, Kiana and and Gerber, Matthew S and Barnes, Laura E},
booktitle={Machine Learning and Applications (ICMLA), 2017 16th IEEE International Conference on},
year={2017},
organization={IEEE}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@mariamabarham](https://github.com/mariamabarham), [@lewtun](https://github.com/lewtun) for adding this dataset.
