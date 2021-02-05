---
annotations_creators:
- crowdsourced
language_creators:
- found
languages: []
licenses:
- unknown
multilinguality: []
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-80-Million-Tiny-Images
task_categories:
- other
task_ids:
- other-other-image-classification
---
 
# Dataset Card for CIFAR-10
 
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
 
- **Homepage:** [CIFAR Datasets](https://www.cs.toronto.edu/~kriz/cifar.html)
- **Repository:** 
- **Paper:** [Paper](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf)
- **Leaderboard:**
- **Point of Contact:**
 
### Dataset Summary
 
The CIFAR-100 dataset consists of 60000 32x32 colour images in 100 classes, with 600 images
per class. There are 500 training images and 100 testing images per class. There are 50000 training images and 10000 test images. The 100 classes are grouped into 20 superclasses. 
There are two labels per image - fine label (actual class) and coarse label (superclass).
 
### Supported Tasks and Leaderboards
 
[More Information Needed]
 
### Languages
 
English
 
## Dataset Structure
 
### Data Instances

### Data Fields
 
- `img`:  32x32x3 image
- `fine_label`: a classification label, with possible values including `apple`, `aquarium_fish`, `baby`, `bear`, `beaver` and more.
- `coarse_label`: a classification label, with possible values including `aquatic_mammals`, `fish`, `flowers`, `food_containers`, `fruit_and_vegetables` and more.
 
### Data Splits
 
|   name   |train|test|
|----------|----:|---------:|
|cifar100|50000|     10000|
 
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
 
[More Information Needed]
 
### Licensing Information
 
[More Information Needed]
 
### Citation Information
 
```
@TECHREPORT{Krizhevsky09learningmultiple,
    author = {Alex Krizhevsky},
    title = {Learning multiple layers of features from tiny images},
    institution = {},
    year = {2009}
}
```