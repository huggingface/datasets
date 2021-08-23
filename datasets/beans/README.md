---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
pretty_name: Beans
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-image-classification
---

# Dataset Card for Beans

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

- **Homepage:**[Beans Homepage](https://github.com/AI-Lab-Makerere/ibean/)
- **Repository:**[AI-Lab-Makerere/ibean](https://github.com/AI-Lab-Makerere/ibean/)
- **Paper:** N/A
- **Leaderboard:** N/A
- **Point of Contact:** N/A

### Dataset Summary

Beans leaf dataset with images of diseased and health leaves.

### Supported Tasks and Leaderboards

- image-classification

### Languages

English

## Dataset Structure

### Data Instances

A sample from the training set is provided below:

```
{
    'image_file_path': '/root/.cache/huggingface/datasets/downloads/extracted/0aaa78294d4bf5114f58547e48d91b7826649919505379a167decb629aa92b0a/train/bean_rust/bean_rust_train.109.jpg',
    'labels': 1
}
```

### Data Fields

The data instances have the following fields:

- `image_file_path`: a `string` filepath to an image.
- `labels`: an `int` classification label.

### Data Splits

 
|   name   |train|validation|test|
|----------|----:|----:|----:|
|beans|1034|133|128|

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
@ONLINE {beansdata,
    author="Makerere AI Lab",
    title="Bean disease dataset",
    month="January",
    year="2020",
    url="https://github.com/AI-Lab-Makerere/ibean/"
}
```

### Contributions

Thanks to [@nateraw](https://github.com/nateraw) for adding this dataset.
