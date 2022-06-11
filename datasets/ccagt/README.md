---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- cc-by-nc-3.0
multilinguality:
- monolingual
paperswithcode_id: null
pretty_name: Images of Cervical Cells with AgNOR Stain Technique
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- image-segmentation
- object-detection
task_ids:
- semantic-segmentation
- instance-segmentation
- panoptic-segmentation
---

# Dataset Card for Images of Cervical Cells with AgNOR Stain Technique

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
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** [CCAgT homepage](https://data.mendeley.com/datasets/wg4bpm33hj/)
- **Repository:** [CCAgT-utils](https://doi.org/10.5281/zenodo.6350442)
- **Paper:** [Semantic Segmentation for the Detection of Very Small Objects on Cervical Cell Samples Stained with the AgNOR Technique](https://dx.doi.org/10.2139/ssrn.4126881)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [João G. A. Amorim](mailto:joao.atkinson@posgrad.ufsc.br)

### Dataset Summary

The CCAgT dataset contains 9339 images with resolution of 1600X1200 where each pixel is 0.111µmX0.111µm from 15 different slides stained with AgNOR technique, having at least one label per image. Have more than sixty-three thousand annotations. The images from patients of Gynecology and Colonoscopy Outpatient Clinic of the Polydoro Ernani de São Thiago University Hospital of the Universidade Federal de Santa Catarina (HU-UFSC). This research was approved by the UFSC Research Ethics Committee (CEPSH), protocol number 57423616.3.0000.0121. First, all patients involved were informed about the objectives of the study, and those who agreed to participate signed an informed consent form.

### Supported Tasks and Leaderboards

- image-segmentation: The dataset can be used to train a model for semantic segmentation. Semantic segmentation consists in classify each pixel of the images; Success on this task is typically measured by achieving a high values of [mean iou](https://huggingface.co/spaces/evaluate-metric/mean_iou) or [f-score](https://huggingface.co/spaces/evaluate-metric/f1) for pixels results. 
  - For instance segmentation's or panoptic segmentation needs to convert the original dataset.instance segmentation consists in firstly do object detection, and then uses a semantic segmentation model inside detected object; panoptic segmentation is the combination of instance segmentation and semantic segmentation. For instances results,  this task is typically measured by achieving a high values of [recall](https://huggingface.co/spaces/evaluate-metric/recall),  [precision](https://huggingface.co/spaces/evaluate-metric/precision) and [f-score](https://huggingface.co/spaces/evaluate-metric/f1).

- object-detection: The dataset can be used to train a model for object detection to detect the nuclei categories, or the tiny objects (NORs), which consists of locating instances of objects and then classifying each one. This task is typically measured by achieving a high values of [recall](https://huggingface.co/spaces/evaluate-metric/recall),  [precision](https://huggingface.co/spaces/evaluate-metric/precision) and [f-score](https://huggingface.co/spaces/evaluate-metric/f1).

### languages
The class labels in the dataset are in English.

## Dataset Structure

### Data Instances

An example looks like below: 

#### For semantic segmentation
```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1200x1600 at 0x276021C5EB8>,
  'annotation': <PIL.PngImagePlugin.PngImageFile image mode=L size=1200x1600 at 0x385021C5ED7>
}
```

#### For object detection
From the dataset into COCO format we use:

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1200x1600 at 0x276021C5EB8>,
  'digits': {
    'bbox': [
      [36, 7, 13, 32],
      [50, 7, 12, 32]
    ], 
    'label': [1, 5]
  }
```

### Data Fields


#### For semantic segmentation

The data annotations have the following fields:

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.

- `annotation`: A `PIL.Image.Image` object containing the annotation mask.


#### For object detection
- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `digits`: a dictionary containing digits' bounding boxes and labels
  - `bbox`: a list of bounding boxes (in the [coco](https://albumentations.ai/docs/getting_started/bounding_boxes_augmentation/#coco) format) corresponding to the digits present on the image
  - `label`: a list of integers between 1 and 7 representing the each category.



### Data Splits

The data is random split into training, test and validation set. The training data contains 70% of the images, the testing and the validation data contains 15% of the images each.

## Dataset Creation

### Curation Rationale

CCAgT was built to provide a dataset for machines to learn how to identify nucleus and nucleolus organizer regions (NORs). The dataset was build with samples of patients of (university hospital - UFSC)[https://unihospital.ufsc.br/], who had different diagnoses in their oncological exams.

### Source Data

#### Initial Data Collection and Normalization


### Annotations

#### Annotation process

The (labelbox tool)[labelbox.com/] have been employed to annotate the instances. The satellite category has been labeled as a single dot, and the other categories were labeled as  polygons


### Personal and Sensitive Information

This research was approved by the UFSC Research Ethics Committee (CEPSH), protocol number 57423616.3.0000.0121. First, all patients involved were informed about the objectives of the study, and those who agreed to participate signed an informed consent form.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help to spread the AgNOR as a support method for cancer diagnosis, since it is not a standardized method among pathologists.


### Other Known Limitations

Satellite annotation is not as accurate for pixel-level representation due to single-point annotations.

## Additional Information

### Dataset Curators

The dataset samples was collected by member of clinical Analyses Department from Universidade Federal de Santa Catarina ((UFSC)[https://ufsc.br/]): Ane Francyne Costa, Fabiana Botelho De Miranda Onofre, and Alexandre Sherlley Casimiro Onofre

### Licensing Information

CC BY NC 3.0 license description
The files associated with this dataset are licensed under a Attribution-NonCommercial 3.0 Unported license.

What does this mean?
You are free to adapt, copy or redistribute the material, providing you attribute appropriately and do not use the material for commercial purposes.

### Citation Information

```bibtex
% Dataset oficial page
@misc{CCAgTDataset,
  doi = {10.17632/WG4BPM33HJ.2},
  url = {https://data.mendeley.com/datasets/wg4bpm33hj/2},
  author =  {Jo{\~{a}}o Gustavo Atkinson Amorim and Andr{\'{e}} Vict{\'{o}}ria Matias and Tainee Bottamedi and Vin{\'{i}}us Sanches and Ane Francyne Costa and Fabiana Botelho De Miranda Onofre and Alexandre Sherlley Casimiro Onofre and Aldo von Wangenheim},
  title = {CCAgT: Images of Cervical Cells with AgNOR Stain Technique},
  publisher = {Mendeley},
  year = {2022},
  copyright = {Attribution-NonCommercial 3.0 Unported}
}


% Dataset second version
% pre-print:
@article{AtkinsonAmorim2022,
  doi = {10.2139/ssrn.4126881},
  url = {https://doi.org/10.2139/ssrn.4126881},
  year = {2022},
  publisher = {Elsevier {BV}},
  author = {Jo{\~{a}}o Gustavo Atkinson Amorim and Andr{\'{e}} Vict{\'{o}}ria Matias and Allan Cerentini and Fabiana Botelho de Miranda Onofre and Alexandre Sherlley Casimiro Onofre and Aldo von Wangenheim},
  title = {Semantic Segmentation for the Detection of Very Small Objects on Cervical Cell Samples Stained with the {AgNOR} Technique},
  journal = {{SSRN} Electronic Journal}
}


% Dataset first version
% Link: https://arquivos.ufsc.br/d/373be2177a33426a9e6c/
% Paper:
@inproceedings{AtkinsonSegmentationAgNORCBMS2020,  
    author={Jo{\~{a}}o Gustavo Atkinson Amorim and Luiz Antonio Buschetto Macarini and Andr{\'{e}} Vict{\'{o}}ria Matias and Allan Cerentini and Fabiana Botelho De Miranda Onofre and Alexandre Sherlley Casimiro Onofre and Aldo von Wangenheim},
    booktitle={2020 IEEE 33rd International Symposium on Computer-Based Medical Systems (CBMS)},
    title={A Novel Approach on Segmentation of AgNOR-Stained Cytology Images Using Deep Learning},
    year={2020},
    pages={552-557}, 
    doi={10.1109/CBMS49503.2020.00110},
    url={https://doi.org/10.1109/CBMS49503.2020.00110}
}

```