---
paperswithcode_id: dailydialog
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
- text-classification-other-emotion-classification
- text-classification-other-dialog-act-classification
pretty_name: DailyDialog
---

# Dataset Card for "daily_dialog"

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

- **Homepage:** [http://yanran.li/dailydialog](http://yanran.li/dailydialog)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 4.27 MB
- **Size of the generated dataset:** 8.23 MB
- **Total amount of disk used:** 12.50 MB

### Dataset Summary

We develop a high-quality multi-turn dialog dataset, DailyDialog, which is intriguing in several aspects.
The language is human-written and less noisy. The dialogues in the dataset reflect our daily communication way
and cover various topics about our daily life. We also manually label the developed dataset with communication
intention and emotion information. Then, we evaluate existing approaches on DailyDialog dataset and hope it
benefit the research field of dialog systems.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 4.27 MB
- **Size of the generated dataset:** 8.23 MB
- **Total amount of disk used:** 12.50 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "act": [2, 1, 1, 1, 1, 2, 3, 2, 3, 4],
    "dialog": "[\"Good afternoon . This is Michelle Li speaking , calling on behalf of IBA . Is Mr Meng available at all ? \", \" This is Mr Meng ...",
    "emotion": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `dialog`: a `list` of `string` features.
- `act`: a `list` of classification labels, with possible values including `__dummy__` (0), `inform` (1), `question` (2), `directive` (3), `commissive` (4).
- `emotion`: a `list` of classification labels, with possible values including `no emotion` (0), `anger` (1), `disgust` (2), `fear` (3), `happiness` (4).

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|11118|      1000|1000|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

Dataset provided for research purposes only. Please check dataset license for additional information.

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

DailyDialog dataset is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### Citation Information

```
@InProceedings{li2017dailydialog,
    author = {Li, Yanran and Su, Hui and Shen, Xiaoyu and Li, Wenjie and Cao, Ziqiang and Niu, Shuzi},
    title = {DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset},
    booktitle = {Proceedings of The 8th International Joint Conference on Natural Language Processing (IJCNLP 2017)},
    year = {2017}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@julien-c](https://github.com/julien-c) for adding this dataset.
