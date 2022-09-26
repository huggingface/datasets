---
annotations_creators:
- found
language:
- en
language_creators:
- found
license:
- unknown
multilinguality:
- monolingual
pretty_name: 20 Newsgroups
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
paperswithcode_id: 20-newsgroups
---

# Dataset Card for "newsgroup"

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

- **Homepage:** [http://qwone.com/~jason/20Newsgroups/](http://qwone.com/~jason/20Newsgroups/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [NewsWeeder: Learning to Filter Netnews](https://doi.org/10.1016/B978-1-55860-377-6.50048-7)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 886.22 MB
- **Size of the generated dataset:** 118.65 MB
- **Total amount of disk used:** 1004.87 MB

### Dataset Summary

The 20 Newsgroups data set is a collection of approximately 20,000 newsgroup documents, partitioned (nearly) evenly across
20 different newsgroups. To the best of my knowledge, it was originally collected by Ken Lang, probably for his Newsweeder:
Learning to filter netnews paper, though he does not explicitly mention this collection. The 20 newsgroups collection has become
a popular data set for experiments in text applications of machine learning techniques, such as text classification and text clustering.

does not include cross-posts and includes only the "From" and "Subject" headers.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### 18828_alt.atheism

- **Size of downloaded dataset files:** 13.99 MB
- **Size of the generated dataset:** 1.59 MB
- **Total amount of disk used:** 15.58 MB

An example of 'train' looks as follows.
```

```

#### 18828_comp.graphics

- **Size of downloaded dataset files:** 13.99 MB
- **Size of the generated dataset:** 1.58 MB
- **Total amount of disk used:** 15.57 MB

An example of 'train' looks as follows.
```

```

#### 18828_comp.os.ms-windows.misc

- **Size of downloaded dataset files:** 13.99 MB
- **Size of the generated dataset:** 2.27 MB
- **Total amount of disk used:** 16.26 MB

An example of 'train' looks as follows.
```

```

#### 18828_comp.sys.ibm.pc.hardware

- **Size of downloaded dataset files:** 13.99 MB
- **Size of the generated dataset:** 1.13 MB
- **Total amount of disk used:** 15.12 MB

An example of 'train' looks as follows.
```

```

#### 18828_comp.sys.mac.hardware

- **Size of downloaded dataset files:** 13.99 MB
- **Size of the generated dataset:** 1.01 MB
- **Total amount of disk used:** 15.00 MB

An example of 'train' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### 18828_alt.atheism
- `text`: a `string` feature.

#### 18828_comp.graphics
- `text`: a `string` feature.

#### 18828_comp.os.ms-windows.misc
- `text`: a `string` feature.

#### 18828_comp.sys.ibm.pc.hardware
- `text`: a `string` feature.

#### 18828_comp.sys.mac.hardware
- `text`: a `string` feature.

### Data Splits

|             name             |train|
|------------------------------|----:|
|18828_alt.atheism             |  799|
|18828_comp.graphics           |  973|
|18828_comp.os.ms-windows.misc |  985|
|18828_comp.sys.ibm.pc.hardware|  982|
|18828_comp.sys.mac.hardware   |  961|

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
@incollection{LANG1995331,
title = {NewsWeeder: Learning to Filter Netnews},
editor = {Armand Prieditis and Stuart Russell},
booktitle = {Machine Learning Proceedings 1995},
publisher = {Morgan Kaufmann},
address = {San Francisco (CA)},
pages = {331-339},
year = {1995},
isbn = {978-1-55860-377-6},
doi = {https://doi.org/10.1016/B978-1-55860-377-6.50048-7},
url = {https://www.sciencedirect.com/science/article/pii/B9781558603776500487},
author = {Ken Lang},
}
```

### Contributions

Thanks to [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
