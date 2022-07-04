---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- unknown
multilinguality:
- monolingual
pretty_name: Cats Vs. Dogs
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- image-classification
task_ids:
- multi-class-image-classification
paperswithcode_id: cats-vs-dogs
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
- **Repository:**
- **Paper:** [Asirra: A CAPTCHA that Exploits Interest-Aligned Manual Image Categorization](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/10/CCS2007.pdf)
- **Leaderboard:** [Dogs vs. Cats](https://www.kaggle.com/competitions/dogs-vs-cats)
- **Point of Contact:**

### Dataset Summary

A large set of images of cats and dogs. There are 1738 corrupted images that are dropped. This dataset is part of a now-closed Kaggle competition and represents a subset of the so-called Asirra dataset.

From the competition page:

> The Asirra data set
>
> Web services are often protected with a challenge that's supposed to be easy for people to solve, but difficult for computers. Such a challenge is often called a [CAPTCHA](http://www.captcha.net/) (Completely Automated Public Turing test to tell Computers and Humans Apart) or HIP (Human Interactive Proof). HIPs are used for many purposes, such as to reduce email and blog spam and prevent brute-force attacks on web site passwords.
>
> Asirra (Animal Species Image Recognition for Restricting Access) is a HIP that works by asking users to identify photographs of cats and dogs. This task is difficult for computers, but studies have shown that people can accomplish it quickly and accurately. Many even think it's fun! Here is an example of the Asirra interface:
>
> Asirra is unique because of its partnership with [Petfinder.com](https://www.petfinder.com/), the world's largest site devoted to finding homes for homeless pets. They've provided Microsoft Research with over three million images of cats and dogs, manually classified by people at thousands of animal shelters across the United States. Kaggle is fortunate to offer a subset of this data for fun and research. 

### Supported Tasks and Leaderboards

- `image-classification`: The goal of this task is to classify a given image as either containing a cat or a dog. The leaderboard is available [here](https://paperswithcode.com/sota/image-classification-on-cats-vs-dogs).

### Languages

English.

## Dataset Structure

### Data Instances

A sample from the training set is provided below:

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=500x375 at 0x29CEAD71780>,
  'labels': 0
}
```

### Data Fields

The data instances have the following fields:

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
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
| # of examples | 23422 |

## Dataset Creation

### Curation Rationale

This subset was to built to test whether computer vision algorithms can beat the Asirra CAPTCHA:

From the competition page:

> Image recognition attacks
>
> While random guessing is the easiest form of attack, various forms of image recognition can allow an attacker to make guesses that are better than random. There is enormous diversity in the photo database (a wide variety of backgrounds, angles, poses, lighting, etc.), making accurate automatic classification difficult. In an informal poll conducted many years ago, computer vision experts posited that a classifier with better than 60% accuracy would be difficult without a major advance in the state of the art. For reference, a 60% classifier improves the guessing probability of a 12-image HIP from 1/4096 to 1/459.

### Source Data

#### Initial Data Collection and Normalization

This dataset is a subset of the Asirra dataset.

From the competition page:

> Asirra is unique because of its partnership with Petfinder.com, the world's largest site devoted to finding homes for homeless pets. They've provided Microsoft Research with over three million images of cats and dogs, manually classified by people at thousands of animal shelters across the United States.

#### Who are the source language producers?

The users of [Petfinder.com](https://www.petfinder.com/).

### Annotations

#### Annotation process

The images were annotated by selecting a pet category on [Petfinder.com](https://www.petfinder.com/).

#### Who are the annotators?

The users of [Petfinder.com](https://www.petfinder.com/).

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

From the paper:

> Unlike many image-based CAPTCHAs which are abstract or subjective, Asirra’s challenges are concrete, inoffensive (cute, by some accounts), require no specialized or culturally biased knowledge, and have definite ground truth. This
makes Asirra less frustrating for humans. Some beta-testers found it fun. The four-year-old child of one asked several times to “play the cat and dog game again.”


### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```bibtex
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
