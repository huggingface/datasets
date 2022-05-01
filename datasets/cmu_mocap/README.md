---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
pretty_name: CMU MoCap
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- other
task_ids: []
paperswithcode_id: mocap
---

# Dataset Card for CMU MoCap 

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

- **Homepage:** [CMU MoCap homepage](http://mocap.cs.cmu.edu/)
- **Repository:** [More Information Needed]
- **Paper:** [More Information Needed]
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [CMU MoCap Contact](mailto:jkh+mocap@cs.cmu.edu)

### Dataset Summary

The CMU Graphics Lab Motion Capture Database is a dataset containing motion capture recordings of people performing different actions such as walking, jumping, dancing etc. The actions have been performed by over 140 subjects. There are a total of 2605 trials in 6 categories and 23 subcategories.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

All the categories, sub-categories and descriptions use English as their primary language.

## Dataset Structure

### Data Instances

A sample from the CMU MoCap dataset is provided below:
```
{
    'subject_id': 12, 
    'categories': ['Physical Activities & Sports', 'Locomotion', 'Locomotion', 'Locomotion'], 
    'subcategories': ['martial arts', 'walking', 'walking', 'walking'], 
    'descriptions': ['tai chi', 'walk', 'walk', 'walk'], 
    'amc_files': ['~/all_asfamc/subjects/12/12_04.amc', '~/all_asfamc/subjects/12/12_01.amc', '~/all_asfamc/subjects/12/12_03.amc', '~/all_asfamc/subjects/12/12_02.amc'], 
    'asf_file': '~/all_asfamc/subjects/12/12.asf',
}
```
Depending on the file format, 'files' field would change. Check the Data Fields section for more information.

### Data Fields

The following fields are common for all file formats of the dataset.

- `subject_id`: Unique ID for each subject in the MoCap dataset.
- `categories`:  A list containing the category names of all trials.
- `subcategories`: A list containing the subcategory names of all trials.
- `descriptions`: A list containing the descriptions of all trials.

According to the file format, we have the following fields:
- `amc_files`, `c3d_files`, `mpg_files` , `avi_files` : A list containing the path to all files.

The "asf/amc" config has an additional field :

- `asf_file`: ASF file is the skeleton file, in the ASF file a base pose is defined for the skeleton that is the starting point for the motion data. More info can be found [here](https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/ASF-AMC.html).


### Data Splits

All the data is contained in training set.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

From the [CMU MoCap Info](http://mocap.cs.cmu.edu/info.php) page:
> The mocap lab contains 12 Vicon infrared MX-40 cameras, each of which is capable of recording 120 Hz with images of 4 megapixel resolution. The cameras are placed around a rectangular area, of approximately 3m x 8m, in the center of the room. Only motions that take place in this rectangle can be captured. If motion of human hands is being captured, more detail is required and the cameras are moved closer to capture a smaller space with higher resolution. To capture something, small grey markers are placed on it. Humans wear a black jumpsuit and have 41 markers taped on. The Vicon cameras see the markers in infra-red. The images that the various cameras pick up are triangulated to get 3D data.

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

[Needs More Information]

### Licensing Information

From the website:
> This data is free for use in research projects. You may include this data in commercially-sold products, but you may not resell this data directly, even in converted form.

### Citation Information

From the website:
> The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with funding from NSF EIA-0196217.

### Contributions