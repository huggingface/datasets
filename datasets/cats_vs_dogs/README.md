---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
pretty_name: Cats Vs. Dogs
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-image-classification
---

# Dataset Card for Cats Vs. Dogs

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** [Cats vs Dogs Dataset](https://www.microsoft.com/en-us/download/details.aspx?id=54765)
- **Repository:** N/A
- **Paper:** [Paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/10/CCS2007.pdf)
- **Leaderboard:** N/A
- **Point of Contact:** N/A

### Dataset Summary

A large set of images of cats and dogs. There are 1738 corrupted images that are dropped.

### Supported Tasks and Leaderboards

- image-classification

### Languages

English

## Dataset Structure

### Data Instances

A sample from the training set is provided below:

```
{
  'image': '/root/.cache/huggingface/datasets/downloads/extracted/6e1e8c9052e9f3f7ecbcb4b90860668f81c1d36d86cc9606d49066f8da8bfb4f/PetImages/Cat/1.jpg',
  'label': 0
}
```

### Data Fields

The data instances have the following fields:

- `image_file_path`: a `string` filepath to an image.
- `labels`: an `int` classification label.

Class Label Mappings:

```
{
  "cat": 0,
  "dog": 1,
}
```

### Data Splits

 
|               | train |
|---------------|------:|
| # of examples | 23410 |

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```
@Inproceedings (Conference){asirra-a-captcha-that-exploits-interest-aligned-manual-image-categorization,
author = {Elson, Jeremy and Douceur, John (JD) and Howell, Jon and Saul, Jared},
title = {Asirra: A CAPTCHA that Exploits Interest-Aligned Manual Image Categorization},
booktitle = {Proceedings of 14th ACM Conference on Computer and Communications Security (CCS)},
year = {2007},
month = {October},
publisher = {Association for Computing Machinery, Inc.},
url = {https://www.microsoft.com/en-us/research/publication/asirra-a-captcha-that-exploits-interest-aligned-manual-image-categorization/},
edition = {Proceedings of 14th ACM Conference on Computer and Communications Security (CCS)},
}
```

### Contributions

Thanks to [@nateraw](https://github.com/nateraw) for adding this dataset.
