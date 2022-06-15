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
- 1K<n<10K
source_datasets:
- original
task_categories:
- image-segmentation
- object-detection
task_ids:
- semantic-segmentation
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

The CCAgT (Images of Cervical Cells with AgNOR Stain Technique) dataset contains 9339 images (1600x1200 resolution where each pixel is 0.111µmX0.111µm) from 15 different slides stained using the AgNOR technique. Each image has at least one label. In total, this dataset has more than 63K instances of annotated object. The images are from the patients of the Gynecology and Colonoscopy Outpatient Clinic of the [Polydoro Ernani de São Thiago University Hospital of the Universidade Federal de Santa Catarina (HU-UFSC)](https://unihospital.ufsc.br/).

### Supported Tasks and Leaderboards

- `image-segmentation`: The dataset can be used to train a model for semantic segmentation. Semantic segmentation consists in classifying each pixel of the image. Success on this task is typically measured by achieving high values of [mean iou](https://huggingface.co/spaces/evaluate-metric/mean_iou) or [f-score](https://huggingface.co/spaces/evaluate-metric/f1) for pixels results. 
  - Instance segmentation and panoptic segmentation require an additional conversion of the original dataset. Instance segmentation consists of doing object detection first and then using a semantic segmentation model inside detected objects. Panoptic segmentation is the combination of instance segmentation and semantic segmentation. For instances results, this task is typically measured by achieving high values of [recall](https://huggingface.co/spaces/evaluate-metric/recall), [precision](https://huggingface.co/spaces/evaluate-metric/precision) and [f-score](https://huggingface.co/spaces/evaluate-metric/f1).

- `object-detection`: The dataset can be used to train a model for object detection to detect the nuclei categories or the nucleolus organizer regions (NORs), which consists of locating instances of objects and then classifying each one. This task is typically measured by achieving a high values of [recall](https://huggingface.co/spaces/evaluate-metric/recall), [precision](https://huggingface.co/spaces/evaluate-metric/precision) and [f-score](https://huggingface.co/spaces/evaluate-metric/f1).


### Languages

The class labels in the dataset are in English.

## Dataset Structure

### Data Instances

An example looks like the one below:

#### `semantic segmentation` (default configuration)

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1200x1600 at 0x276021C5EB8>,
  'annotation': <PIL.PngImagePlugin.PngImageFile image mode=L size=1200x1600 at 0x385021C5ED7>
}
```

#### `object detection`

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1200x1600 at 0x276021C5EB8>,
  'objects': {
    'bbox': [
      [36, 7, 13, 32],
      [50, 7, 12, 32]
    ], 
    'label': [1, 5]
  }
```

### Data Fields

The data annotations have the following fields:

#### `semantic segmentation` (default configuration)

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `annotation`: A `PIL.Image.Image` object containing the annotation mask.

#### `object detection`

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `objects`: a dictionary containing bounding boxes and labels of the cell objects 
  - `bbox`: a list of bounding boxes (in the [coco](https://albumentations.ai/docs/getting_started/bounding_boxes_augmentation/#coco) format) corresponding to the objects present on the image
  - `label`: a list of integers representing the category (7 categories to describe the objects in total; two to differentiate nucleolus organizer regions), with the possible values including `NUCLEUS` (1), `CLUSTER` (2), `SATELLITE` (3), `NUCLEUS_OUT_OF_FOCUS` (4), `OVERLAPPED_NUCLEI` (5), `NON_VIABLE_NUCLEUS` (6) and `LEUKOCYTE_NUCLEUS` (7).


### Data Splits

The data is split randomly using the fixed seed into training, test and validation set. The training data contains 70% of the images and the testing and the validation data contain 15% of the images each. In total, the training set contains 6533 images and the testing and the validation set 1403 images each.

<details>
  <summary>
  Click here to see additional statistics:
  </summary>

  | Slide id  | Diagnostics | images | annotations | NUCLEUS | CLUSTER | SATELLITE | NUCLEUS_OUT_OF_FOCUS | OVERLAPPED_NUCLEI | NON_VIABLE_NUCLEUS | LEUKOCYTE_NUCLEUS |
  | :-------: | :---------: | :----: | :---------: | :-----: | :------: | :-------: | :------------------: | :---------------: | :---------------: | :-------: |
  |     A     |    CIN 3    |  1311  |    3164     |   763   |   1038   |    922    |         381          |        46         |        14         |     0     |
  |     B     |     SCC     |  561   |     911     |   224   |   307    |    112    |         132          |         5         |         1         |    130    |
  |     C     |     AC      |  385   |    11420    |  2420   |   3584   |   1112    |         1692         |        228        |        477        |   1907    |
  |     D     |    CIN 3    |  2125  |    1258     |   233   |   337    |    107    |         149          |        12         |         8         |    412    |
  |     E     |    CIN 3    |  506   |    11131    |  2611   |   6249   |   1648    |         476          |        113        |        34         |     0     |
  |     F     |    CIN 1    |  318   |    3365     |   954   |   1406   |    204    |         354          |        51         |        326        |    70     |
  |     G     |    CIN 2    |  249   |    2759     |   691   |   1279   |    336    |         268          |        49         |        51         |    85     |
  |     H     |    CIN 2    |  650   |    5216     |   993   |   983    |    425    |         2562         |        38         |        214        |     1     |
  |     I     |  No lesion  |  309   |     474     |   56    |    55    |    19     |         170          |         2         |        23         |    149    |
  |     J     |    CIN 1    |  261   |    1786     |   355   |   304    |    174    |         743          |        18         |        33         |    159    |
  |     K     |  No lesion  |  1503  |    13102    |  2464   |   6669   |    638    |         620          |        670        |        138        |   1903    |
  |     L     |    CIN 2    |  396   |    3289     |   842   |   796    |    387    |         1209         |        27         |        23         |     5     |
  |     M     |    CIN 2    |  254   |    1500     |   357   |   752    |    99     |         245          |        16         |        12         |    19     |
  |     N     |    CIN 3    |  248   |     911     |   258   |   402    |    67     |         136          |        10         |         6         |    32     |
  |     O     |     AC      |  262   |    2904     |   792   |   1549   |    228    |         133          |        88         |        52         |    62     |
  | **Total** |      -      |  9339  |    63190    |  14013  |  25710   |   6478    |         9270         |       1373        |       1412        |   4934    |

  Lision types:
  - Cervical intraepithelial neoplasia 1 - CIN 1
  - Cervical intraepithelial neoplasia 2 - CIN 2
  - Cervical intraepithelial neoplasia 3 - CIN 3
  - Squamous cell carcinoma - SCC
  - Adenocarcinoma - AC
  - No lesion

</details>

## Dataset Creation

### Curation Rationale

CCAgT was built to provide a dataset for machines to learn how to identify nucleus and nucleolus organizer regions (NORs).

### Source Data

#### Initial Data Collection and Normalization

The images are collected as patches/tiles of whole slide images (WSIs) from cervical samples stained with AgNOR technique to allow the detection of nucleolus organizer regions (NORs). NORs are DNA loops containing genes responsible for the transcription of ribosomal RNA located in the cell nucleolus. They contain a set of argyrophilic proteins, selectively stained by silver nitrate, which can be identified as black dots located throughout the nucleoli area and called AgNORs.

#### Who are the source language producers?

The dataset was built using images from examinations (a gynecological exam, colposcopy and biopsy) of 15 women patients who were treated at the Gynecology and Colposcopy Outpatient Clinic of the [University Hospital Professor Polydoro Ernani de São Thiago of Federal University of Santa Catarina (HU-UFSC)](https://unihospital.ufsc.br/) and had 6 different diagnoses in their oncological exams. The samples were collected by the members of the Clinical Analyses Department: Ane Francyne Costa, Fabiana Botelho De Miranda Onofre, and Alexandre Sherlley Casimiro Onofre.

### Annotations

#### Annotation process

The instances were annotated using the [labelbox](https://labelbox.com/) tool. The satellite category was labeled as a single dot, and the other categories were labeled as polygons. After the annotation process, all annotations was reviewed.

#### Who are the annotators?

Members of the Clinical Analyses Department and the Image Processing and Computer Graphics Lab. — LAPiX from [Universidade Federal de Santa Catarina (UFSC)](https://en.ufsc.br/). 

- Tainee Bottamedi
- Vinícius Sanches
- João H. Telles de Carvalho
- Ricardo Thisted

### Personal and Sensitive Information

This research was approved by the UFSC Research Ethics Committee (CEPSH), protocol number 57423616.3.0000.0121. All involved patients were informed about the study's objectives, and those who agreed to participate signed an informed consent form.

## Considerations for Using the Data

### Social Impact of Dataset

This dataset's purpose is to help spread the AgNOR as a support method for cancer diagnosis since this method is not standardized among pathologists.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Satellite annotation is not as accurate for pixel-level representation due to single-point annotations.

## Additional Information

### Dataset Curators

Members of the Clinical Analyses Department from [Universidade Federal de Santa Catarina (UFSC)](https://en.ufsc.br/) collected the dataset samples: Ane Francyne Costa, Fabiana Botelho De Miranda Onofre, and Alexandre Sherlley Casimiro Onofre.

### Licensing Information

The files associated with this dataset are licensed under an [Attribution-NonCommercial 3.0 Unported](https://creativecommons.org/licenses/by-nc/3.0/) license.

Users are free to adapt, copy or redistribute the material as long as they attribute it appropriately and do not use it for commercial purposes.

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

### Contributions

Thanks to [@johnnv1](https://github.com/johnnv1) for adding this dataset.
