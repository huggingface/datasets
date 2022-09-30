---
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- object-detection
task_ids:
- object-detection-other-medical-personal-protective-equipment-detection
paperswithcode_id: cppe-5
pretty_name: CPPE - 5
---

# Dataset Card for CPPE - 5

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

- **Homepage:**
- **Repository:** https://github.com/Rishit-dagli/CPPE-Dataset
- **Paper:** [CPPE-5: Medical Personal Protective Equipment Dataset](https://arxiv.org/abs/2112.09569)
- **Leaderboard:** https://paperswithcode.com/sota/object-detection-on-cppe-5
- **Point of Contact:** rishit.dagli@gmail.com

### Dataset Summary

CPPE - 5 (Medical Personal Protective Equipment) is a new challenging dataset with the goal to allow the study of subordinate categorization of medical personal protective equipments, which is not possible with other popular data sets that focus on broad level categories.

Some features of this dataset are:

* high quality images and annotations (~4.6 bounding boxes per image)
* real-life images unlike any current such dataset
* majority of non-iconic images (allowing easy deployment to real-world environments)

### Supported Tasks and Leaderboards

- `object-detection`: The dataset can be used to train a model for Object Detection. This task has an active leaderboard which can be found at https://paperswithcode.com/sota/object-detection-on-cppe-5. The metrics for this task are adopted from the COCO detection evaluation criteria, and include the mean Average Precision (AP) across IoU thresholds ranging from 0.50 to 0.95 at different scales.

### Languages

English

## Dataset Structure

### Data Instances

A data point comprises an image and its object annotations.

```
{
  'image_id': 15,
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=943x663 at 0x2373B065C18>,
  'width': 943,
  'height': 663,
  'objects': {
    'id': [114, 115, 116, 117], 
    'area': [3796, 1596, 152768, 81002],
    'bbox': [
      [302.0, 109.0, 73.0, 52.0],
      [810.0, 100.0, 57.0, 28.0],
      [160.0, 31.0, 248.0, 616.0],
      [741.0, 68.0, 202.0, 401.0]
    ], 
    'category': [4, 4, 0, 0]
  }
}
```

### Data Fields

- `image`: the image id
- `image`: `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `width`: the image width
- `height`: the image height
- `objects`: a dictionary containing bounding box metadata for the objects present on the image
  - `id`: the annotation id
  - `area`: the area of the bounding box
  - `bbox`: the object's bounding box (in the [coco](https://albumentations.ai/docs/getting_started/bounding_boxes_augmentation/#coco) format)
  - `category`: the object's category, with possible values including `Coverall` (0),`Face_Shield` (1),`Gloves` (2),`Goggles` (3) and `Mask` (4)

### Data Splits

The data is split into training and testing set. The training set contains 1000 images and test set 29 images.

## Dataset Creation

### Curation Rationale

From the paper:
> With CPPE-5 dataset, we hope to facilitate research and use in applications at multiple public places to autonomously identify if a PPE (Personal Protective Equipment) kit has been worn and also which part of the PPE kit has been worn. One of the main aims with this dataset was to also capture a higher ratio of non-iconic images or non-canonical perspectives [5] of the objects in this dataset. We further hope to see high use of this dataset to aid in medical scenarios which would have a huge effect
worldwide.

### Source Data

#### Initial Data Collection and Normalization

The images in the CPPE-5 dataset were collected using the following process:
* Obtain Images from Flickr: Following the object categories we identified earlier, we first download images from Flickr and save them at the "Original" size. On Flickr, images are served at multiple different sizes (Square 75, Small 240, Large 1024, X-Large 4K etc.), the "Original" size is an exact copy of the image uploaded by author.
* Extract relevant metadata: Flickr contains images each with searchable metadata, we extract the following relevant
metadata:
  * A direct link to the original image on Flickr
  * Width and height of the image
  * Title given to the image by the author
  * Date and time the image was uploaded on
  * Flickr username of the author of the image
  * Flickr Name of the author of the image
  * Flickr profile of the author of the image
  * The License image is licensed under
  * MD5 hash of the original image
* Obtain Images from Google Images: Due to the reasons we mention earlier, we only collect a very small proportion
of images from Google Images. For these set of images we extract the following metadata:
  * A direct link to the original image
  * Width and height of the image
  * MD5 hash of the original image
* Filter inappropriate images: Though very rare in the collected images, we also remove images containing inappropriate content using the safety filters on Flickr and Google Safe Search.
* Filter near-similar images: We then remove near-duplicate images in the dataset using GIST descriptors

#### Who are the source language producers?

The images for this dataset were collected from Flickr and Google Images.

### Annotations

#### Annotation process

The dataset was labelled in two phases: the first phase included labelling 416 images and the second phase included labelling 613 images. For all the images in the dataset volunteers were provided the following table:

|Item        |Description                                                              |
|------------|---------------------------------------------------------------------    | 
|coveralls | Coveralls are hospital gowns worn by medical professionals as in order to provide a barrier between patient and professional, these usually cover most of the exposed skin surfaces of the professional medics.|
|mask | Mask prevents airborne transmission of infections between patients and/or treating personnel by blocking the movement of pathogens (primarily bacteria and viruses) shed in respiratory droplets and aerosols into and from the wearer’s mouth and nose.|
face shield | Face shield aims to protect the wearer’s entire face (or part of it) from hazards such as flying objects and road debris, chemical splashes (in laboratories or in industry), or potentially infectious materials (in medical and laboratory environments).|
gloves | Gloves are used during medical examinations and procedures to help prevent cross-contamination between caregivers and patients.|
|goggles | Goggles, or safety glasses, are forms of protective eye wear that usually enclose or protect the area surrounding the eye in order to prevent particulates, water or chemicals from striking the eyes.|

as well as examples of: correctly labelled images, incorrectly labelled images, and not applicable images. Before the labelling task, each volunteer was provided with an exercise to verify if the volunteer was able to correctly identify categories as well as identify if an annotated image is correctly labelled, incorrectly labelled, or not applicable. The labelling process first involved two volunteers independently labelling an image from the dataset. In any of the cases that: the number of bounding boxes are different, the labels for on or more of the bounding boxes are different or two volunteer annotations are sufficiently different; a third volunteer compiles the result from the two annotations to come up with a correctly labelled image. After this step, a volunteer verifies the bounding box annotations. Following this method of labelling the dataset we ensured that all images were labelled accurately and contained exhaustive
annotations. As a result of this, our dataset consists of 1029 high-quality, majorly non-iconic, and accurately annotated images.

#### Who are the annotators?

In both the phases crowd-sourcing techniques were used with multiple volunteers labelling the dataset using the open-source tool LabelImg.

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

Dagli, Rishit, and Ali Mustufa Shaikh.

### Licensing Information

[More Information Needed]

### Citation Information

```
@misc{dagli2021cppe5,
      title={CPPE-5: Medical Personal Protective Equipment Dataset},
      author={Rishit Dagli and Ali Mustufa Shaikh},
      year={2021},
      eprint={2112.09569},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

### Contributions

Thanks to [@mariosasko](https://github.com/mariosasko) for adding this dataset.
