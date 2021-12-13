---
pretty_name: Cifar10
annotations_creators:
- crowdsourced
language_creators:
- found
languages: []
licenses:
- unknown
multilinguality: []
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-80-Million-Tiny-Images
task_categories:
- other
task_ids:
- other-other-image-classification
paperswithcode_id: cifar-10
---

# Dataset Card for CIFAR-10

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

- **Homepage:** https://www.cs.toronto.edu/~kriz/cifar.html
- **Repository:** 
- **Paper:** Learning Multiple Layers of Features from Tiny Images by Alex Krizhevsky
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The CIFAR-10 dataset consists of 60000 32x32 colour images in 10 classes, with 6000 images per class. There are 50000 training images and 10000 test images.
The dataset is divided into five training batches and one test batch, each with 10000 images. The test batch contains exactly 1000 randomly-selected images from each class. The training batches contain the remaining images in random order, but some training batches may contain more images from one class than another. Between them, the training batches contain exactly 5000 images from each class.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

A sample from the training set is provided below:

```
{
  'img': <PIL.PngImagePlugin.PngImageFile image mode=RGB size=32x32 at 0x201FA6EE748>,
  'label': 0
}
```

### Data Fields

- img: A `PIL.Image.Image` object containing the 32x32 image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- label: 0-9 with the following correspondence
         0 airplane
         1 automobile
         2 bird
         3 cat
         4 deer
         5 dog
         6 frog
         7 horse
         8 ship
         9 truck

### Data Splits

Train and Test

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
@TECHREPORT{Krizhevsky09learningmultiple,
    author = {Alex Krizhevsky},
    title = {Learning multiple layers of features from tiny images},
    institution = {},
    year = {2009}
}
```

### Contributions

Thanks to [@czabo](https://github.com/czabo) for adding this dataset.