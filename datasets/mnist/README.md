---
annotations_creators:
- experts
language_creators:
- found
languages: []
licenses:
- MIT
multilinguality: []
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-nist
task_categories:
- other
task_ids:
- other-other-image-classification
paperswithcode_id: mnist
---

# Dataset Card for MNIST

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

- **Homepage:** http://yann.lecun.com/exdb/mnist/
- **Repository:** 
- **Paper:** MNIST handwritten digit database by Yann LeCun, Corinna Cortes, and CJ Burges
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The MNIST dataset consists of 70,000 28x28 black-and-white images of handwritten digits extracted from two NIST databases. There are 60,000 images in the training dataset and 10,000 images in the validation dataset, one class per digit so a total of 10 classes, with 7,000 images (6,000 train images and 1,000 test images) per class.
Half of the image were drawn by Census Bureau employees and the other half by high school students (this split is evenly distributed in the training and testing sets).

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

A data point comprises an image and its label:

```
{
  'image': <PIL.PngImagePlugin.PngImageFile image mode=L size=28x28 at 0x276021F6DD8>,
  'label': 5
}
```

### Data Fields

- `image`: A `PIL.Image.Image` object containing the 28x28 image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `label`: an integer between 0 and 9 representing the digit.

### Data Splits

The data is split into training and test set. All the images in the test set were drawn by different individuals than the images in the training set. The training set contains 60,000 images and the test set 10,000 images. 

## Dataset Creation

### Curation Rationale

The MNIST database was created to provide a testbed for people wanting to try pattern recognition methods or machine learning algorithms while spending minimal efforts on preprocessing and formatting. Images of the original dataset (NIST) were  in two groups, one consisting of images drawn by Census Bureau employees and one consisting of images drawn by high school students. In NIST, the training set was built by grouping all the images of the Census Bureau employees, and the test set was built by grouping the images form the high school students.
The goal in building MNIST was to have a training and test set following the same distributions, so the training set contains 30,000 images drawn by Census Bureau employees and 30,000 images drawn by high school students, and the test set contains 5,000 images of each group. The curators took care to make sure all the images in the test set were drawn by different individuals than the images in the training set. 

### Source Data

#### Initial Data Collection and Normalization

The original images from NIST were size normalized to fit a 20x20 pixel box while preserving their aspect ratio. The resulting images contain grey levels (i.e., pixels don't simply have a value of black and white, but a level of greyness from 0 to 255) as a result of the anti-aliasing technique used by the normalization algorithm. The images were then centered in a 28x28 image by computing the center of mass of the pixels, and translating the image so as to position this point at the center of the 28x28 field.

#### Who are the source image producers?

Half of the source images were drawn by Census Bureau employees, half by high school students. According to the dataset curator, the images from the first group are more easily recognizable.

### Annotations

#### Annotation process

The images were not annotated after their creation: the image creators annotated their images with the corresponding label after drawing them.

#### Who are the annotators?

Same as the source data creators.

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

Chris Burges, Corinna Cortes and Yann LeCun

### Licensing Information

MIT Licence

### Citation Information

```
@article{lecun2010mnist,
  title={MNIST handwritten digit database},
  author={LeCun, Yann and Cortes, Corinna and Burges, CJ},
  journal={ATT Labs [Online]. Available: http://yann.lecun.com/exdb/mnist},
  volume={2},
  year={2010}
}
```

### Contributions

Thanks to [@sgugger](https://github.com/sgugger) for adding this dataset.