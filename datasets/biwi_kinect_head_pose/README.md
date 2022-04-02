---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- other
multilinguality:
- monolingual
pretty_name: Biwi Kinect Head Pose
size_categories:
- unknown
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-head-pose-estimation
paperswithcode_id: biwi
---

# Dataset Card for Biwi Kinect Head Pose Database

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

- **Homepage:** [Biwi Kinect Head Pose homepage](https://icu.ee.ethz.ch/research/datsets.html)
- **Repository:** [Needs More Information]
- **Paper:** [Biwi Kinect Head Pose paper](https://link.springer.com/article/10.1007/s11263-012-0549-0)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Gabriele Fanelli](mailto:gabriele.fanelli@gmail.com)

### Dataset Summary

The Biwi Kinect Head Pose Database is acquired with the Microsoft Kinect sensor, a structured IR light device.It contains 15K images of 20 people with 6 females and 14 males where 4 people were recorded twice.

For each frame, there is :
- a depth image,
- a corresponding rgb image (both 640x480 pixels),
- annotation

The head pose range covers about +-75 degrees yaw and +-60 degrees pitch. The ground truth is the 3D location of the head and its rotation.

### Supported Tasks and Leaderboards

Biwi Kinect Head Pose Database supports the following tasks :
- Head pose estimation
- Pose estimation
- Face verification

### Languages

[Needs More Information]

## Dataset Structure

### Data Instances

A sample from the Biwi Kinect Head Pose dataset is provided below:

```
{
    'sequence_number': '12', 
    'subject_id': 'M06', 
    'rgb': [<PIL.PngImagePlugin.PngImageFile image mode=RGB size=640x480 at 0x7F53A6446C10>,.....],
    'rgb_cal': 
        {
            'intrisic_mat': [[517.679, 0.0, 320.0], [0.0, 517.679, 240.5], [0.0, 0.0, 1.0]],
            'extrinsic_mat': 
            {
                'rotation': [[0.999947, 0.00432361, 0.00929419], [-0.00446314, 0.999877, 0.0150443], [-0.009228, -0.015085, 0.999844]], 
                'translation': [-24.0198, 5.8896, -13.2308]
            }
        }
    'depth': ['../hpdb/12/frame_00003_depth.bin', .....],
    'depth_cal': 
        {
            'intrisic_mat': [[575.816, 0.0, 320.0], [0.0, 575.816, 240.0], [0.0, 0.0, 1.0]],
            'extrinsic_mat': 
            {
                'rotation': [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], 
                'translation': [0.0, 0.0, 0.0]
            }
        }
    'head_pose_gt': 
        {
            'center': [[43.4019, -30.7038, 906.864], [43.0202, -30.8683, 906.94], [43.0255, -30.5611, 906.659], .....],
            'rotation': [[[0.980639, 0.109899, 0.162077], [-0.11023, 0.993882, -0.00697376], [-0.161851, -0.011027, 0.986754]], ......]
        }
}
```

### Data Fields

- `sequence_number` : This refers to the sequence number in the dataset. There are a total of 24 sequences.
- `subject_id` : This refers to the subjects in the dataset. There are a total of 20 people with 6 females and 14 males where 4 people were recorded twice.
- `rgb` : List of png frames containing the poses.
- `rgb_cal`: Contains calibration information for the color camera which includes intrinsic matrix, 
global rotation and translation.
- `depth` : List of depth frames for the poses.
- `depth_cal`: Contains calibration information for the depth camera which includes intrinsic matrix, global rotation and translation.
- `head_pose_gt` : Contains ground truth information, i.e., the location of the center of the head in 3D and the head rotation, encoded as a 3x3 rotation matrix.


### Data Splits

All the data is contained in the training set.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The Biwi Kinect Head Pose Database is acquired with the Microsoft Kinect sensor, a structured IR light device.
#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

From Dataset's README : 
> The database contains 24 sequences acquired with a Kinect sensor. 20 people (some were recorded twice - 6 women and 14 men) were recorded while turning their heads, sitting in front of the sensor, at roughly one meter of distance.

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

[Needs More Information]

### Licensing Information

From Dataset's README : 
> This database is made available for non-commercial use such as university research and education.

### Citation Information

```bibtex
@article{fanelli_IJCV,
  author = {Fanelli, Gabriele and Dantone, Matthias and Gall, Juergen and Fossati, Andrea and Van Gool, Luc},
  title = {Random Forests for Real Time 3D Face Analysis},
  journal = {Int. J. Comput. Vision},
  year = {2013},
  month = {February},
  volume = {101},
  number = {3},
  pages = {437--458}
}
```