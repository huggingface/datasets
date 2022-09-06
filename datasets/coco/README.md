---
licenses: 
- cc-by-4.0
pretty_name: COCO
task_categories: 
- object-detection
- image-segmentation
- image-to-text
- image-classification
---

# Dataset Card for [Dataset Name]

## Table of Contents
- [Dataset Card for [Dataset Name]](#dataset-card-for-dataset-name)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Dataset Structure](#dataset-structure)
    - [Data Instances and Annotations](#data-instances)
    - [Data Splits](#data-splits)
  - [Dataset Creation](#dataset-creation)
    - [Curation Rationale](#curation-rationale)
  - [Additional Information](#additional-information)
    - [Dataset Curators](#dataset-curators)
    - [Licensing Information](#licensing-information)
    - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** https://cocodataset.org/#home
- **Repository:** https://github.com/cocodataset
- **Paper:** Microsoft COCO: Common Objects in Context
- **Leaderboard:** https://paperswithcode.com/sota/object-detection-on-coco
- **Point of Contact:** info@cocodataset.org

### Dataset Summary

COCO (Common Objects in Context) is a large-scale object detection, segmentation, and captioning dataset.

### Supported Tasks and Leaderboards

- Object Detection
- Keypoint Detection
- Semantic Segmentation
- Panoptic Segmentation
- Dense Pose Estimation

## Dataset Structure
### Data Instances and Annotations

COCO has several annotation types across different tasks,for object detection, keypoint detection, stuff segmentation, panoptic segmentation, densepose, and image captioning. The annotations are stored using JSON. 
All annotations share the following common part:
```
{
"info": info, "images": [image], "annotations": [annotation], "licenses": [license],
}

info{
"year": int, "version": str, "description": str, "contributor": str, "url": str, "date_created": datetime,
}

image{
"id": int, "width": int, "height": int, "file_name": str, "license": int, "flickr_url": str, "coco_url": str, "date_captured": datetime,
}

license{
"id": int, "name": str, "url": str,
}
```

Instances in object detection split contains segmentation mask of the object. `iscrowd` is 0 for single objects and 1 for crowd annotations. Box coordinates are measured from the top left image corner and 0-indexed.
```
annotation{
"id": int, "image_id": int, "category_id": int, "segmentation": RLE or [polygon], "area": float, "bbox": [x,y,width,height], "iscrowd": 0 or 1,
}

categories[{
"id": int, "name": str, "supercategory": str,
}]
```

A keypoint annotation contains all the data of the object annotation. First, `keypoints` is a length 3k array where k is the total number of keypoints defined for the category. Each keypoint has a 0-indexed location x,y and a visibility flag v defined as:

- v=0: not labeled (in which case x=y=0),
- v=1: labeled but not visible,
- v=2: labeled and visible. 

A keypoint is considered visible if it falls inside the object segment. `num_keypoints` indicates the number of labeled keypoints (v>0) for a given object. Finally, for each category, the categories struct has two additional fields: `keypoints` which is a length k array of keypoint names, and `skeleton`, which defines connectivity via a list of keypoint edge pairs and is used for visualization. Currently keypoints are only labeled for the person category (for most medium/large non-crowd person instances).
```
annotation{
"keypoints": [x1,y1,v1,...], 
"num_keypoints": int, 
"[cloned]": ...,
}

categories[{
"keypoints": [str], 
"skeleton": [edge], 
"[cloned]": ...,
}]
```
Annotation format for stuff segmentation is identical and fully compatible to the object detection format above (except iscrowd is unnecessary and set to 0 by default).  The category_id represents the id of the current stuff category. 
In panoptic segmentation task, each annotation struct is a per-image annotation rather than a per-object annotation. Each per-image annotation has two parts: 
- a PNG that stores the class-agnostic image segmentation
- a JSON struct that stores the semantic information for each image segment. 

To match an annotation with an image, use the `image_id` field (that is `annotation.image_id==image.id`).
For each annotation, per-pixel segment ids are stored as a single PNG at `annotation.file_name`. The PNGs are in a folder with the same name as the JSON, i.e., `annotations/name/` for `annotations/name.json`. Each segment (whether it's a stuff or thing segment) is assigned a unique id. Unlabeled pixels (void) are assigned a value of 0. Note that when you load the PNG as an RGB image, you will need to compute the ids via ids=R+G*256+B*256^2.
For each annotation, per-segment info is stored in `annotation.segments_info`. `segment_info.id` stores the unique id of the segment and is used to retrieve the corresponding mask from the PNG (`ids==segment_info.id`). `category_id` gives the semantic category and iscrowd indicates the segment encompasses a group of objects (relevant for thing categories only). The bbox and area fields provide additional info about the segment.
The COCO panoptic task has the same thing categories as the detection task, whereas the stuff categories differ from those in the stuff task (for details see the panoptic evaluation page).
Finally, each category struct has two additional fields:

- isthing that distinguishes stuff and thing categories,
- color that is useful for consistent visualization.

```
annotation{
"image_id": int, 
"file_name": str, 
"segments_info": [segment_info],
}

segment_info{
"id": int,. 
"category_id": int, 
"area": int, 
"bbox": [x,y,width,height], 
"iscrowd": 0 or 1,
}

categories[{
"id": int, 
"name": str, 
"supercategory": str, 
"isthing": 0 or 1, 
"color": [R,G,B],
}]
```
For image segmentation task, each caption describes the specified image and each image has at least 5 captions (some images have more). The format is as follows:
```
annotation{
"id": int, "image_id": int, "caption": str,
}
```
DensePose task annotation format contains a series of fields, including category id, bounding box, body part masks and parametrization data for selected points, which are detailed below. Crowd annotations (`iscrowd=1`) are used to label large groups of objects. An enclosing bounding box is provided for each person (box coordinates are measured from the top left image corner and are 0-indexed). The categories field of the annotation structure stores the mapping of category id to category and supercategory names.
DensePose annotations are stored in dp_* fields:
Annotated masks:

- dp_masks: RLE encoded dense masks. All part masks are of size 256x256. They correspond to 14 semantically meaningful parts of the body: Torso, Right Hand, Left Hand, Left Foot, Right Foot, Upper Leg Right, Upper Leg Left, Lower Leg Right, Lower Leg Left, Upper Arm Left, Upper Arm Right, Lower Arm Left, Lower Arm Right, Head;
Annotated points:

- dp_x, dp_y: spatial coordinates of collected points on the image. The coordinates are scaled such that the bounding box size is 256x256;
- dp_I: The patch index that indicates which of the 24 surface patches the point is on. Patches correspond to the body parts described above. Some body parts are split into 2 patches: 1, 2 = Torso, 3 = Right Hand, 4 = Left Hand, 5 = Left Foot, 6 = Right Foot, 7, 9 = Upper Leg Right, 8, 10 = Upper Leg Left, 11, 13 = Lower Leg Right, 12, 14 = Lower Leg Left, 15, 17 = Upper Arm Left, 16, 18 = Upper Arm Right, 19, 21 = Lower Arm Left, 20, 22 = Lower Arm Right, 23, 24 = Head;
- dp_U, dp_V: Coordinates in the UV space. Each surface patch has a separate 2D parameterization.

### Data Splits
COCO has three configurations, including: 
- 2014 configuration that contains images for object detection, image captioning, keypoint detection and dense estimation of human pose. It has three splits, train, test and validation.
- 2015 configuration that consists of one test split only, for object detection, semantic segmentation, panoptic segmentation  and keypoint detection.
- 2017 configuration that contains images for object detection, image captioning, panoptic segmentation, semantic segmentation and keypoint detection.
```
annotation{
"id": int, 
"image_id": int, 
"category_id": int, 
"is_crowd": 0 or 1, 
"area": int, 
"bbox": [x,y,width,height], 
"dp_I": [float], 
"dp_U": [float], 
"dp_V": [float], 
"dp_x": [float], 
"dp_y": [float], 
"dp_masks": [RLE],
}
```
## Dataset Creation

### Curation Rationale

This dataset addresses three problems in scene understanding:
- Detecting non-iconic views (or non-canonical perspectives) of objects,
- contextual reasoning between objects
- the precise 2D localization of objects.

MS COCO contains 91 common object categories with 82 of them having more than 5000 labeled instances, and total dataset has 2.5M labeled instances in 328,000 images. 

## Additional Information

### Dataset Curators

The dataset is created by [the COCO Consortium](https://cocodataset.org/#people).

### Licensing Information

The annotations in this dataset belong to the COCO Consortium and are licensed under a Creative Commons Attribution 4.0 License. The COCO Consortium does not own the copyright of the images. Use of the images must abide by the [Flickr Terms of Use](https://www.flickr.com/creativecommons/). The users of the images accept full responsibility for the use of the dataset, including but not limited to the use of any copies of copyrighted images that they may create from the dataset.

### Citation Information

@article{DBLP:journals/corr/LinMBHPRDZ14,
  author    = {Tsung{-}Yi Lin and
               Michael Maire and
               Serge J. Belongie and
               Lubomir D. Bourdev and
               Ross B. Girshick and
               James Hays and
               Pietro Perona and
               Deva Ramanan and
               Piotr Doll{'{a} }r and
               C. Lawrence Zitnick},
  title     = {Microsoft {COCO:} Common Objects in Context},
  journal   = {CoRR},
  volume    = {abs/1405.0312},
  year      = {2014},
  url       = {http://arxiv.org/abs/1405.0312},
  archivePrefix = {arXiv},
  eprint    = {1405.0312},
  timestamp = {Mon, 13 Aug 2018 16:48:13 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/LinMBHPRDZ14},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}