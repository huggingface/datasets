---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- ar
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-poetry-classification
paperswithcode_id: metrec
---

# Dataset Card for MetRec

## Table of Contents
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

- **Homepage:** [Metrec](https://github.com/zaidalyafeai/MetRec)
- **Repository:** [Metrec repository](https://github.com/zaidalyafeai/MetRec)
- **Paper:** [MetRec: A dataset for meter classification of arabic poetry](https://www.sciencedirect.com/science/article/pii/S2352340920313792)
- **Point of Contact:** [Zaid Alyafeai](mailto:alyafey22@gmail.com)

### Dataset Summary

The dataset contains the verses and their corresponding meter classes.
Meter classes are represented as numbers from 0 to 13. 
The dataset can be highly useful for further research in order to improve the field of Arabic poems’ meter classification.
The train dataset contains 47,124 records and the test dataset contains 8,316 records.

### Supported Tasks and Leaderboards

The dataset was published on this [paper](https://www.sciencedirect.com/science/article/pii/S2352340920313792). A benchmark is acheived on this [paper](https://www.sciencedirect.com/science/article/pii/S016786552030204X).

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

A typical data point comprises a label which is out of 13 classes and a verse part of poem. 

### Data Fields

[N/A]

### Data Splits

The data is split into a training and testing. The split is organized as the following 

|           | Tain   | Test |
|---------- | ------ | ---- |
|data split | 47,124 | 8,316|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

The dataset was collected from [Aldiwan](https://www.aldiwan.net/).

#### Who are the source language producers?

The poems are from different poets.

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Discussion of Social Impact and Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]

```
@article{metrec2020,
  title={MetRec: A dataset for meter classification of arabic poetry},
  author={Al-shaibani, Maged S and Alyafeai, Zaid and Ahmad, Irfan},
  journal={Data in Brief},
  year={2020},
  publisher={Elsevier}
}
```

### Contributions

Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai) for adding this dataset.