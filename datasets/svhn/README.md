---
annotations_creators:
- machine-generated
- expert-generated
language_creators:
- machine-generated
language:
- en
license:
- other
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- image-classification
- object-detection
task_ids: []
paperswithcode_id: svhn
pretty_name: Street View House Numbers
---

# Dataset Card for Street View House Numbers

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

- **Homepage:** http://ufldl.stanford.edu/housenumbers
- **Repository:**
- **Paper:** [Reading Digits in Natural Images with Unsupervised Feature Learning](http://ufldl.stanford.edu/housenumbers/nips2011_housenumbers.pdf)
- **Leaderboard:** https://paperswithcode.com/sota/image-classification-on-svhn
- **Point of Contact:** streetviewhousenumbers@gmail.com

### Dataset Summary

SVHN is a real-world image dataset for developing machine learning and object recognition algorithms with minimal requirement on data preprocessing and formatting. It can be seen as similar in flavor to MNIST (e.g., the images are of small cropped digits), but incorporates an order of magnitude more labeled data (over 600,000 digit images) and comes from a significantly harder, unsolved, real world problem (recognizing digits and numbers in natural scene images). SVHN is obtained from house numbers in Google Street View images. The dataset comes in two formats:
1. Original images with character level bounding boxes.
2. MNIST-like 32-by-32 images centered around a single character (many of the images do contain some distractors at the sides).

### Supported Tasks and Leaderboards

- `object-detection`: The dataset can be used to train a model for digit detection.
- `image-classification`: The dataset can be used to train a model for Image Classification where the task is to predict a correct digit on the image. The leaderboard for this task is available at:
https://paperswithcode.com/sota/image-classification-on-svhn

### Languages

English

## Dataset Structure

### Data Instances

#### full_numbers

The original, variable-resolution, color house-number images with character level bounding boxes.

```
{
  'image': <PIL.PngImagePlugin.PngImageFile image mode=RGB size=98x48 at 0x259E3F01780>,
  'digits': {
    'bbox': [
      [36, 7, 13, 32],
      [50, 7, 12, 32]
    ], 
    'label': [6, 9]
  }
}
```

#### cropped_digits

Character level ground truth in an MNIST-like format. All digits have been resized to a fixed resolution of 32-by-32 pixels. The original character bounding boxes are extended in the appropriate dimension to become square windows, so that resizing them to 32-by-32 pixels does not introduce aspect ratio distortions. Nevertheless this preprocessing introduces some distracting digits to the sides of the digit of interest.

```
{
  'image': <PIL.PngImagePlugin.PngImageFile image mode=RGB size=32x32 at 0x25A89494780>,
  'label': 1
}
```

### Data Fields

#### full_numbers

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `digits`: a dictionary containing digits' bounding boxes and labels
  - `bbox`: a list of bounding boxes (in the [coco](https://albumentations.ai/docs/getting_started/bounding_boxes_augmentation/#coco) format) corresponding to the digits present on the image
  - `label`: a list of integers between 0 and 9 representing the digit.

#### cropped_digits

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `digit`: an integer between 0 and 9 representing the digit.

### Data Splits

#### full_numbers

The data is split into training, test and extra set. The training set contains 33402 images, test set 13068 and the extra set 202353 images.

#### cropped_digits

The data is split into training, test and extra set. The training set contains 73257 images, test set 26032 and the extra set 531131 images.

The extra set can be used as extra training data. The extra set was obtained in a similar manner to the training and test set, but with the increased detection threshold in order to generate this large amount of labeled data. The SVHN extra subset is thus somewhat biased toward less difficult detections, and is thus easier than SVHN train/SVHN test.

## Dataset Creation

### Curation Rationale

From the paper:
> As mentioned above, the venerable MNIST dataset has been a valuable goal post for researchers seeking to build better learning systems whose benchmark performance could be expected to translate into improved performance on realistic applications. However, computers have now reached essentially human levels of performance on this problem—a testament to progress in machine learning and computer vision. The Street View House Numbers (SVHN) digit database that we provide can be seen as similar in flavor to MNIST (e.g., the images are of small cropped characters), but the SVHN dataset incorporates an order of magnitude more labeled data and comes from a significantly harder, unsolved, real world problem. Here the gap between human performance and state of the art feature representations is significant. Going forward, we expect that this dataset may fulfill a similar role for modern feature learning algorithms: it provides a new and difficult benchmark where increased performance can be expected to translate into tangible gains on a realistic application.

### Source Data

#### Initial Data Collection and Normalization

From the paper:
> The SVHN dataset was obtained from a large number of Street View images using a combination
of automated algorithms and the Amazon Mechanical Turk (AMT) framework, which was
used to localize and transcribe the single digits. We downloaded a very large set of images from
urban areas in various countries.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

From the paper:
> From these randomly selected images, the house-number patches were extracted using a dedicated sliding window house-numbers detector using a low threshold on the detector’s confidence score in order to get a varied, unbiased dataset of house-number signs. These low precision detections were screened and transcribed by AMT workers.

#### Who are the annotators?

The AMT workers.

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

Yuval Netzer, Tao Wang, Adam Coates, Alessandro Bissacco, Bo Wu and Andrew Y. Ng 

### Licensing Information

Non-commerical use only.

### Citation Information

```
@article{netzer2011reading,
  title={Reading digits in natural images with unsupervised feature learning},
  author={Netzer, Yuval and Wang, Tao and Coates, Adam and Bissacco, Alessandro and Wu, Bo and Ng, Andrew Y},
  year={2011}
}
```

### Contributions

Thanks to [@mariosasko](https://github.com/mariosasko) for adding this dataset.