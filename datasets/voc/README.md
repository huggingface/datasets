---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- other-inherited-from-flickr
multilinguality:
- monolingual
pretty_name: voc
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- object-detection
task_ids:
- other-object-detection
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** http://host.robots.ox.ac.uk/pascal/VOC/index.html
- **Repository:**
- **Paper:** http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf
- **Leaderboard:** http://host.robots.ox.ac.uk/leaderboard/main_bootstrap.php
- **Point of Contact:** 

### Dataset Summary

This dataset contains the data from the PASCAL Visual Object Classes Challenge, corresponding to the Classification and Detection competitions.

In the Classification competition, the goal is to predict the set of labels contained in the image, while in the Detection competition the goal is to predict the bounding box and label of each individual object. WARNING: As per the official dataset, the test set of VOC2012 does not contain annotations.

### Supported Tasks and Leaderboards

The two tasks that this dataset supports are:

`object-detection`: For each of the classes predict the bounding boxes of each object of that class in a test image (if any).
`image-classification`: For each of the classes predict the presence/absence of at least one object of that class in a test image.

Entries to the [leaderboard](http://host.robots.ox.ac.uk/leaderboard/main_bootstrap.php) are evaluated using Mean Average Precision (mAP).


### Languages

The class labels in the dataset are in English.

## Dataset Structure

### Data Instances

A sample from the training set is provided below:

```
{
  "image": <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=500x442 at 0x7FD3A2EFA490>,
  "objects": {
    "label": [
      12,
      14
    ],
    "bbox": [
      [
        0.1968325823545456,
        0.10599999874830246,
        0.9502262473106384,
        0.9419999718666077
      ],
      [
        0.09954751282930374,
        0.3160000145435333,
        0.37782806158065796,
        0.578000009059906
      ]
    ],
    "pose": [
      2,
      4
    ],
    "is_truncated": [
      false,
      true
    ],
    "is_difficult": [
      false,
      false
    ]
  },
  "labels": [
    12,
    14
  ],
  "labels_no_difficult": [
    12,
    14
  ]
}
```

### Data Fields

The data instances have the following fields:

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.

- `objects`: A `datasets.Sequence` containing:
    - `label`: An `int` object class label.
    - `bbox`: A list of `float`. Contains an axis-aligned rectangle specifying the extent of the object visible in the image.
    - `pose`: An `int` label related to an object's pose. The different poses are `frontal', `rear', `left' or `right'. The views are subjectively marked to indicate the view of the bulk of the object. Some objects have no view specified.
    - `is_truncated`: A `bool` value. When True, it indicates that the bounding box specified for the object does not correspond to the full extent of the object (e.g. an image of a person from the waist up, or a view of a car extending outside the image.)
    - `is_difficult`: A `bool` value. When True, it indicates that the object is considered difficult to recognize, for example an object which is clearly visible but unidentifiable without substantial use of context. Objects marked as difficult are currently ignored in the evaluation of the challenge (See [Supported Tasks And Leaderboards](#supported-tasks-and-leaderboards)).

- `labels`: A list of `int` object class labels contained within the `objects` key.

- `labels_no_difficult`: A list of `int` object class labels contained within the `objects` key where `is_difficult` is True.

### Data Splits

The number of examples per dataset split is shown below, broken down by dataset configuration:

| config   |train|validation|test|
|:---------|----:|---------:|---:|
|**2012**  |5717 |5823      |10991|
|**2007**  |2501 |2510      |4952|

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

In addition to the [dataset curators](#dataset-curators), the following people were involved in annotating the dataset:

Yusuf Aytar, Lucia Ballerini, Hakan Bilen, Ken Chatfield, Mircea Cimpoi, Ali Eslami, Basura Fernando, Christoph Godau, Bertan Gunyel, Phoenix/Xuan Huang, Jyri Kivinen, Markus Mathias, Kristof Overdulve, Konstantinos Rematas, Johan Van Rompay, Gilad Sharir, Mathias Vercruysse, Vibhav Vineet, Ziming Zhang, Shuai Kyle Zheng.

### Personal and Sensitive Information

The dataset contains a class label for "person", which is the most common class in the dataset, making up 40.9% of the training instances in VOC 2012.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

1. This [study](https://homepages.inf.ed.ac.uk/ckiw/postscript/ijcv_voc09.pdf) discussed that there are an above-average number of Christmas/winter images in the `2007` configuration due to Flickr results being ranked by recency. They also noted that there appears to be a bias in flickr images where photographers appear to take many "close-up" pictures of pets.

1. There is class imbalance in the VOC dataset. For example, [this study](https://www.sciencedirect.com/science/article/pii/S1319157821002020) pointed out that the class “person” is nearly twenty times more frequent than the smallest class “sheep”.


### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The dataset curation process was organized by:

- Mark Everingham (University of Leeds)
- Luc van Gool (ETHZ, Zurich)
- Chris Williams (University of Edinburgh)
- John Winn (Microsoft Research Cambridge), john@johnwinn.org
- Andrew Zisserman (University of Oxford)

The organizers also acknowledge the following people who helped annotate the dataset:


### Licensing Information

The VOC2012 data includes images obtained from the "flickr" website. Use of these images must respect the corresponding terms of use:

- ["flickr" Terms of Use](http://www.flickr.com/terms.gne)

### Citation Information

```bibtex
@misc{pascal-voc-2007,
    author = "Everingham, M. and Van~Gool, L. and Williams, C. K. I. and Winn, J. and Zisserman, A.",
    title = "The {PASCAL} {V}isual {O}bject {C}lasses {C}hallenge 2007 {(VOC2007)} {R}esults",
    howpublished = "http://www.pascal-network.org/challenges/VOC/voc2007/workshop/index.html"}
```

### Contributions

Thanks to [@nateraw](https://github.com/nateraw) for adding this dataset.
