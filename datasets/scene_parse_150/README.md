---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- bsd-3-clause
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|ade20k
task_categories:
- image-segmentation
task_ids:
- instance-segmentation
- other-scene-parsing
paperswithcode_id: null
pretty_name: MIT Scene Parsing Benchmark
---

# Dataset Card for MIT Scene Parsing Benchmark

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

- **Homepage:** [MIT Scene Parsing Benchmark homepage](https://www.robots.ox.ac.uk/~vgg/research/pass/)
- **Repository:** [Scene Parsing repository (Caffe/Torch7)](https://github.com/CSAILVision/sceneparsing),[Scene Parsing repository (PyTorch)](https://github.com/CSAILVision/semantic-segmentation-pytorch) and [Instance Segmentation repository](https://github.com/CSAILVision/placeschallenge/tree/master/instancesegmentation)
- **Paper:** [Scene Parsing through ADE20K Dataset.](http://people.csail.mit.edu/bzhou/publication/scene-parse-camera-ready.pdf) and [Semantic Understanding of Scenes through ADE20K Datase](https://arxiv.org/abs/1608.05442)
- **Leaderboard:** [MIT Scene Parsing Benchmark leaderboard](http://sceneparsing.csail.mit.edu/#:~:text=twice%20per%20week.-,leaderboard,-Organizers)
- **Point of Contact:** [Bolei Zhou](mailto:bzhou@ie.cuhk.edu.hk)

### Dataset Summary

Scene parsing is the task of segmenting and parsing an image into different image regions associated with semantic categories, such as sky, road, person, and bed. MIT Scene Parsing Benchmark (SceneParse150) provides a standard training and evaluation platform for the algorithms of scene parsing. The data for this benchmark comes from ADE20K Dataset which contains more than 20K scene-centric images exhaustively annotated with objects and object parts. Specifically, the benchmark is divided into 20K images for training, 2K images for validation, and another batch of held-out images for testing. There are in total 150 semantic categories included for evaluation, which include e.g. sky, road, grass, and discrete objects like person, car, bed. Note that there are non-uniform distribution of objects occuring in the images, mimicking a more natural object occurrence in daily scene.

The goal of this benchmark is to segment and parse an image into different image regions associated with semantic categories, such as sky, road, person, and bedThis benchamark is similar to semantic segmentation tasks in COCO and Pascal Dataset, but the data is more scene-centric and with a diverse range of object categories. The data for this benchmark comes from ADE20K Dataset which contains more than 20K scene-centric images exhaustively annotated with objects and object parts.

### Supported Tasks and Leaderboards

- `scene-parsing`: The goal of this task is to segment the whole image densely into semantic classes (image regions), where each pixel is assigned a class label such as the region of *tree* and the region of *building*.
[The leaderboard](http://sceneparsing.csail.mit.edu/#:~:text=twice%20per%20week.-,leaderboard,-Organizers) for this task ranks the models by considering the mean of the pixel-wise accuracy and class-wise IoU as the final score. Pixel-wise accuracy indicates the ratio of pixels which are correctly predicted, while class-wise IoU indicates the Intersection of Union of pixels averaged over all the 150 semantic categories. Refer to the [Development Kit](https://github.com/CSAILVision/sceneparsing) for the detail.

- `instance-segmentation`: The goal of this task is to detect the object instances inside an image and further generate the precise segmentation masks of the objects. Its difference compared to the task of scene parsing is that in scene parsing there is no instance concept for the segmented regions, instead in instance segmentation if there are three persons in the scene, the network is required to segment each one of the person regions. This task doesn't have an active leaderboard. The performance of the instance segmentation algorithms is evaluated by Average Precision (AP, or mAP), following COCO evaluation metrics. For each image, at most 255 top-scoring instance masks are taken across all categories. Each instance mask prediction is only considered if its IoU with ground truth is above a certain threshold. There are 10 IoU thresholds of 0.50:0.05:0.95 for evaluation. The final AP is averaged across 10 IoU thresholds and 100 categories. You can refer to COCO evaluation page for more explanation: http://mscoco.org/dataset/#detections-eval

### Languages

English.

## Dataset Structure

### Data Instances

A data point comprises an image and its annotation mask, which is `None` in the testing set. The `scene_parsing` configuration has an additional `scene_category` field.

#### `scene_parsing`

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=683x512 at 0x1FF32A3EDA0>,
  'annotation': <PIL.PngImagePlugin.PngImageFile image mode=L size=683x512 at 0x1FF32E5B978>,
  'scene_category': 0
}
```

#### `instance_segmentation`

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=256x256 at 0x20B51B5C400>,
  'annotation': <PIL.PngImagePlugin.PngImageFile image mode=RGB size=256x256 at 0x20B57051B38>
}
```

### Data Fields

#### `scene_parsing`

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `annotation`: A `PIL.Image.Image` object containing the annotation mask.
- `scene_category`: A scene category for the image (e.g. `airport_terminal`, `canyon`, `mobile_home`).

> **Note**: annotation masks contain labels ranging from 0 to 150, where 0 refers to "other objects". Those pixels are not considered in the official evaluation. Refer to [this file](https://github.com/CSAILVision/sceneparsing/blob/master/objectInfo150.csv) for the information about the labels of the 150 semantic categories, including indices, pixel ratios and names.

#### `instance_segmentation`

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `annotation`: A `PIL.Image.Image` object containing the annotation mask.

> **Note**: in the instance annotation masks, the R(ed) channel encodes category ID, and the G(reen) channel encodes instance ID. Each object instance has a unique instance ID regardless of its category ID. In the dataset, all images have <256 object instances. Refer to [this file (train split)](https://github.com/CSAILVision/placeschallenge/blob/master/instancesegmentation/instanceInfo100_train.txt) and to [this file (validation split)](https://github.com/CSAILVision/placeschallenge/blob/master/instancesegmentation/instanceInfo100_val.txt) for the information about the labels of the 100 semantic categories. To find the mapping between the semantic categories for `instance_segmentation` and `scene_parsing`, refer to [this file](https://github.com/CSAILVision/placeschallenge/blob/master/instancesegmentation/categoryMapping.txt).

### Data Splits

The data is split into training, test and validation set. The training data contains 20210 images, the testing data contains 3352 images and the validation data contains 2000 images.

## Dataset Creation

### Curation Rationale

The rationale from the paper for the ADE20K dataset from which this benchmark originates:

> Semantic understanding of visual scenes is one of the holy grails of computer vision. Despite efforts of the community in data collection, there are still few image datasets covering a wide range of scenes and object categories with pixel-wise annotations for scene understanding. In this work, we present a densely annotated dataset ADE20K, which spans diverse annotations of scenes, objects, parts of objects, and
in some cases even parts of parts.

> The motivation of this work is to collect a dataset that has densely annotated images (every pixel has a semantic label) with a large and an unrestricted open vocabulary. The
images in our dataset are manually segmented in great detail, covering a diverse set of scenes, object and object part categories. The challenge for collecting such annotations is finding reliable annotators, as well as the fact that labeling is difficult if the class list is not defined in advance. On the other hand, open vocabulary naming also suffers from naming inconsistencies across different annotators. In contrast,
our dataset was annotated by a single expert annotator, providing extremely detailed and exhaustive image annotations. On average, our annotator labeled 29 annotation segments per image, compared to the 16 segments per image labeled by external annotators (like workers from Amazon Mechanical Turk). Furthermore, the data consistency and quality are much higher than that of external annotators.

### Source Data

#### Initial Data Collection and Normalization

Images come from the LabelMe, SUN datasets, and Places and were selected to cover the 900 scene categories defined in the SUN database.

This benchmark was built by selecting the top 150 objects ranked by their total pixel ratios from the ADE20K dataset. As the original images in the ADE20K dataset have various sizes, for simplicity those large-sized images were rescaled to make their minimum heights or widths as 512. Among the 150 objects, there are 35 stuff classes (i.e., wall, sky, road) and 115 discrete objects (i.e., car, person, table). The annotated pixels of the 150 objects occupy 92.75% of all the pixels in the dataset, where the stuff classes occupy 60.92%, and discrete objects occupy 31.83%.

#### Who are the source language producers?

The same as in the LabelMe, SUN datasets, and Places datasets.

### Annotations

#### Annotation process

Annotation process for the ADE20K dataset:

> **Image Annotation.** For our dataset, we are interested in having a diverse set of scenes with dense annotations of all the objects present. Images come from the LabelMe, SUN datasets, and Places and were selected to cover the 900 scene categories defined in the SUN database. Images were annotated by a single expert worker using the LabelMe interface. Fig. 2 shows a snapshot of the annotation interface and one fully segmented image. The worker provided three types of annotations: object segments with names, object parts, and attributes. All object instances are segmented independently so that the dataset could be used to train and evaluate detection or segmentation algorithms. Datasets such as COCO, Pascal or Cityscape start by defining a set of object categories of interest. However, when labeling all the objects in a scene, working with a predefined list of objects is not possible as new categories
appear frequently (see fig. 5.d). Here, the annotator created a dictionary of visual concepts where new classes were added constantly to ensure consistency in object naming. Object parts are associated with object instances. Note that parts can have parts too, and we label these associations as well. For example, the ‘rim’ is a part of a ‘wheel’, which in turn is part of a ‘car’. A ‘knob’ is a part of a ‘door’
that can be part of a ‘cabinet’. The total part hierarchy has a depth of 3. The object and part hierarchy is in the supplementary materials.

> **Annotation Consistency.** Defining a labeling protocol is relatively easy when the labeling task is restricted to a fixed list of object classes, however it becomes challenging when the class list is openended. As the goal is to label all the objects within each image, the list of classes grows unbounded. >Many object classes appear only a few times across the entire collection of images. However, those rare >object classes cannot be ignored as they might be important elements for the interpretation of the scene. >Labeling in these conditions becomes difficult because we need to keep a growing list of all the object >classes in order to have a consistent naming across the entire dataset. Despite the annotator’s best effort, >the process is not free of noise. To analyze the annotation consistency we took a subset of 61 randomly >chosen images from the validation set, then asked our annotator to annotate them again (there is a time difference of six months). One expects that there are some differences between the two annotations. A few examples are shown in Fig 3. On average, 82.4% of the pixels got the same label. The remaining 17.6% of pixels had some errors for which we grouped into three error types as follows:
>
>    • Segmentation quality: Variations in the quality of segmentation and outlining of the object boundary.  One typical source of error arises when segmenting complex objects such as buildings and trees, which can be segmented with different degrees of precision. 5.7% of the pixels had this type of error.
>
>    • Object naming: Differences in object naming (due to ambiguity or similarity between concepts, for instance calling a big car a ‘car’ in one segmentation and a ‘truck’ in the another one, or a ‘palm tree’ a‘tree’. 6.0% of the pixels had naming issues. These errors can be reduced by defining a very precise terminology, but this becomes much harder with a large growing vocabulary.
>
>    • Segmentation quantity: Missing objects in one of the two segmentations. There is a very large number of objects in each image and some images might be annotated more thoroughly than others. For example, in the third column of Fig 3 the annotator missed some small objects in different annotations. 5.9% of the pixels are due to missing labels. A similar issue existed in segmentation datasets such as the Berkeley Image segmentation dataset.
>
> The median error values for the three error types are: 4.8%, 0.3% and 2.6% showing that the mean value is dominated by a few images, and that the most common type of error is segmentation quality.
To further compare the annotation done by our single expert annotator and the AMT-like annotators, 20 images
from the validation set are annotated by two invited external annotators, both with prior experience in image labeling. The first external annotator had 58.5% of inconsistent pixels compared to the segmentation provided by our annotator, and the second external annotator had 75% of the inconsistent pixels. Many of these inconsistencies are due to the poor quality of the segmentations provided by external annotators (as it has been observed with AMT which requires multiple verification steps for quality control). For the
best external annotator (the first one), 7.9% of pixels have inconsistent segmentations (just slightly worse than our annotator), 14.9% have inconsistent object naming and 35.8% of the pixels correspond to missing objects, which is due to the much smaller number of objects annotated by the external annotator in comparison with the ones annotated by our expert annotator. The external annotators labeled on average 16 segments per image while our annotator provided 29 segments per image.

#### Who are the annotators?

Three expert annotators and the AMT-like annotators.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Refer to the `Annotation Consistency` subsection of `Annotation Process`.

## Additional Information

### Dataset Curators

Bolei Zhou, Hang Zhao, Xavier Puig, Sanja Fidler, Adela Barriuso and Antonio Torralba.

### Licensing Information

The MIT Scene Parsing Benchmark dataset is licensed under a [BSD 3-Clause License](https://github.com/CSAILVision/sceneparsing/blob/master/LICENSE).

### Citation Information

```bibtex
@inproceedings{zhou2017scene,
    title={Scene Parsing through ADE20K Dataset},
    author={Zhou, Bolei and Zhao, Hang and Puig, Xavier and Fidler, Sanja and Barriuso, Adela and Torralba, Antonio},
    booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
    year={2017}
}

@article{zhou2016semantic,
  title={Semantic understanding of scenes through the ade20k dataset},
  author={Zhou, Bolei and Zhao, Hang and Puig, Xavier and Fidler, Sanja and Barriuso, Adela and Torralba, Antonio},
  journal={arXiv preprint arXiv:1608.05442},
  year={2016}
}
```

### Contributions

Thanks to [@mariosasko](https://github.com/mariosasko) for adding this dataset.