---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- cc-by-nc-nd-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-wider
task_categories:
- object-detection
task_ids:
- face-detection
paperswithcode_id: wider-face-1
pretty_name: WIDER FACE
---

# Dataset Card for WIDER FACE

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

- **Homepage:** http://shuoyang1213.me/WIDERFACE/index.html
- **Repository:**
- **Paper:** [WIDER FACE: A Face Detection Benchmark](https://arxiv.org/abs/1511.06523)
- **Leaderboard:** http://shuoyang1213.me/WIDERFACE/WiderFace_Results.html
- **Point of Contact:** shuoyang.1213@gmail.com

### Dataset Summary

WIDER FACE dataset is a face detection benchmark dataset, of which images are
selected from the publicly available WIDER dataset. We choose 32,203 images and
label 393,703 faces with a high degree of variability in scale, pose and
occlusion as depicted in the sample images. WIDER FACE dataset is organized
based on 61 event classes. For each event class, we randomly select 40%/10%/50%
data as training, validation and testing sets. We adopt the same evaluation
metric employed in the PASCAL VOC dataset. Similar to MALF and Caltech datasets,
we do not release bounding box ground truth for the test images. Users are
required to submit final prediction files, which we shall proceed to evaluate.

### Supported Tasks and Leaderboards

- `face-detection`: The dataset can be used to train a model for Face Detection. More information on evaluating the model's performance can be found [here](http://shuoyang1213.me/WIDERFACE/WiderFace_Results.html).

### Languages

English

## Dataset Structure

### Data Instances

A data point comprises an image and its face annotations.

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1024x755 at 0x19FA12186D8>, 'faces': {
    'bbox': [
      [178.0, 238.0, 55.0, 73.0],
      [248.0, 235.0, 59.0, 73.0],
      [363.0, 157.0, 59.0, 73.0],
      [468.0, 153.0, 53.0, 72.0],
      [629.0, 110.0, 56.0, 81.0],
      [745.0, 138.0, 55.0, 77.0]
    ], 
    'blur': [2, 2, 2, 2, 2, 2],
    'expression': [0, 0, 0, 0, 0, 0],
    'illumination': [0, 0, 0, 0, 0, 0],
    'occlusion': [1, 2, 1, 2, 1, 2],
    'pose': [0, 0, 0, 0, 0, 0],
    'invalid': [False, False, False, False, False, False]
  }
}
```

### Data Fields

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `faces`: a dictionary of face attributes for the faces present on the image
  - `bbox`: the bounding box of each face (in the [coco](https://albumentations.ai/docs/getting_started/bounding_boxes_augmentation/#coco) format)
  - `blur`: the blur level of each face, with possible values including `clear` (0), `normal` (1) and `heavy`
  - `expression`: the facial expression of each face, with possible values including `typical` (0) and `exaggerate` (1)
  - `illumination`: the lightning condition of each face, with possible values including `normal` (0) and `exaggerate` (1)
  - `occlusion`: the level of occlusion of each face, with possible values including `no` (0), `partial` (1) and `heavy` (2)
  - `pose`: the pose of each face, with possible values including `typical` (0) and `atypical` (1)
  - `invalid`: whether the image is valid or invalid.

### Data Splits

The data is split into training, validation and testing set. WIDER FACE dataset is organized
based on 61 event classes. For each event class, 40%/10%/50%
data is randomly selected as training, validation and testing sets. The training set contains 12880 images, the validation set 3226 images and test set 16097 images.

## Dataset Creation

### Curation Rationale

The curators state that the current face detection datasets typically contain a few thousand faces, with limited variations in pose, scale, facial expression, occlusion, and background clutters,
making it difficult to assess for real world performance. They argue that the limitations of datasets have partially contributed to the failure of some algorithms in coping
with heavy occlusion, small scale, and atypical pose.

### Source Data

#### Initial Data Collection and Normalization

WIDER FACE dataset is a subset of the WIDER dataset.
The images in WIDER were collected in the following three steps: 1) Event categories
were defined and chosen following the Large Scale Ontology for Multimedia (LSCOM) [22], which provides around 1000 concepts relevant to video event analysis. 2) Images
are retrieved using search engines like Google and Bing. For
each category, 1000-3000 images were collected. 3) The
data were cleaned by manually examining all the images
and filtering out images without human face. Then, similar
images in each event category were removed to ensure large
diversity in face appearance. A total of 32203 images are
eventually included in the WIDER FACE dataset.

#### Who are the source language producers?

The images are selected from publicly available WIDER dataset.

### Annotations

#### Annotation process

The curators label the bounding boxes for all
the recognizable faces in the WIDER FACE dataset. The
bounding box is required to tightly contain the forehead,
chin, and cheek.. If a face is occluded, they still label it with a bounding box but with an estimation on the scale of occlusion. Similar to the PASCAL VOC dataset [6], they assign an ’Ignore’ flag to the face
which is very difficult to be recognized due to low resolution and small scale (10 pixels or less). After annotating
the face bounding boxes, they further annotate the following
attributes: pose (typical, atypical) and occlusion level (partial, heavy). Each annotation is labeled by one annotator
and cross-checked by two different people.

#### Who are the annotators?

Shuo Yang, Ping Luo, Chen Change Loy and Xiaoou Tang.

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

Shuo Yang, Ping Luo, Chen Change Loy and Xiaoou Tang

### Licensing Information

[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/).

### Citation Information

```
@inproceedings{yang2016wider,
    Author = {Yang, Shuo and Luo, Ping and Loy, Chen Change and Tang, Xiaoou},
    Booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
    Title = {WIDER FACE: A Face Detection Benchmark},
    Year = {2016}}
```

### Contributions

Thanks to [@mariosasko](https://github.com/mariosasko) for adding this dataset.
