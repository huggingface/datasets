---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- other
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|iit_cdip
task_categories:
- image-classification
task_ids:
- multi-class-image-classification
paperswithcode_id: rvl-cdip
pretty_name: RVL-CDIP
---

# Dataset Card for RVL-CDIP

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** [The RVL-CDIP Dataset](https://www.cs.cmu.edu/~aharley/rvl-cdip/)
- **Repository:**
- **Paper:** [Evaluation of Deep Convolutional Nets for Document Image Classification and Retrieval](https://arxiv.org/abs/1502.07058)
- **Leaderboard:** [RVL-CDIP leaderboard](https://paperswithcode.com/dataset/rvl-cdip)
- **Point of Contact:** [Adam W. Harley](mailto:aharley@cmu.edu)

### Dataset Summary

The RVL-CDIP (Ryerson Vision Lab Complex Document Information Processing) dataset consists of 400,000 grayscale images in 16 classes, with 25,000 images per class. There are 320,000 training images, 40,000 validation images, and 40,000 test images. The images are sized so their largest dimension does not exceed 1000 pixels.

### Supported Tasks and Leaderboards

- `image-classification`: The goal of this task is to classify a given document into one of 16 classes representing document types (letter, form, etc.). The leaderboard for this task is available [here](https://paperswithcode.com/sota/document-image-classification-on-rvl-cdip).

### Languages

All the classes and documents use English as their primary language.

## Dataset Structure

### Data Instances

A sample from the training set is provided below :
```
{
    'image': <PIL.TiffImagePlugin.TiffImageFile image mode=L size=754x1000 at 0x7F9A5E92CA90>,
    'label': 15
}
```

### Data Fields

- `image`: A `PIL.Image.Image` object containing a document.
- `label`: an `int` classification label.

<details>
  <summary>Class Label Mappings</summary>

```json
{
  "0": "letter",
  "1": "form",
  "2": "email",
  "3": "handwritten",
  "4": "advertisement",
  "5": "scientific report",
  "6": "scientific publication",
  "7": "specification",
  "8": "file folder",
  "9": "news article",
  "10": "budget",
  "11": "invoice",
  "12": "presentation",
  "13": "questionnaire",
  "14": "resume",
  "15": "memo"
}
```

</details>

### Data Splits

|   |train|test|validation|
|----------|----:|----:|---------:|
|# of examples|320000|40000|40000|

The dataset was split in proportions similar to those of ImageNet.
- 320000 images were used for training,
- 40000 images for validation, and 
- 40000 images for testing. 

## Dataset Creation

### Curation Rationale

From the paper:
> This work makes available a new labelled subset of the IIT-CDIP collection, containing 400,000
document images across 16 categories, useful for training new CNNs for document analysis.

### Source Data

#### Initial Data Collection and Normalization

The same as in the IIT-CDIP collection.

#### Who are the source language producers?

The same as in the IIT-CDIP collection.

### Annotations

#### Annotation process

The same as in the IIT-CDIP collection.

#### Who are the annotators?

The same as in the IIT-CDIP collection.

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

The dataset was curated by the authors - Adam W. Harley, Alex Ufkes, and Konstantinos G. Derpanis.

### Licensing Information

RVL-CDIP is a subset of IIT-CDIP, which came from the [Legacy Tobacco Document Library](https://www.industrydocuments.ucsf.edu/tobacco/), for which license information can be found [here](https://www.industrydocuments.ucsf.edu/help/copyright/).

### Citation Information

```bibtex
@inproceedings{harley2015icdar,
    title = {Evaluation of Deep Convolutional Nets for Document Image Classification and Retrieval},
    author = {Adam W Harley and Alex Ufkes and Konstantinos G Derpanis},
    booktitle = {International Conference on Document Analysis and Recognition ({ICDAR})}},
    year = {2015}
}
```

### Contributions

Thanks to [@dnaveenr](https://github.com/dnaveenr) for adding this dataset.
