---
paperswithcode_id: matinf
pretty_name: Maternal and Infant Dataset
---

# Dataset Card for "matinf"

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

- **Homepage:** [https://github.com/WHUIR/MATINF](https://github.com/WHUIR/MATINF)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 758.17 MB
- **Total amount of disk used:** 758.17 MB

### Dataset Summary

MATINF is the first jointly labeled large-scale dataset for classification, question answering and summarization.
MATINF contains 1.07 million question-answer pairs with human-labeled categories and user-generated question
descriptions. Based on such rich information, MATINF is applicable for three major NLP tasks, including classification,
question answering, and summarization. We benchmark existing methods and a novel multi-task baseline over MATINF to
inspire further research. Our comprehensive comparison and experiments over MATINF and other datasets demonstrate the
merits held by MATINF.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### age_classification

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 46.15 MB
- **Total amount of disk used:** 46.15 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "description": "\"6个月的时候去儿宝检查，医生说宝宝的分胯动作做的不好，说最好去儿童医院看看，但我家宝宝很好，感觉没有什么不正常啊，请教一下，分胯做的不好，有什么不好吗？\"...",
    "id": 88016,
    "label": 0,
    "question": "医生说宝宝的分胯动作不好"
}
```

#### qa

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 256.24 MB
- **Total amount of disk used:** 256.24 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answer": "\"我一个同学的孩子就是发现了肾积水，治疗了一段时间，结果还是越来越多，没办法就打掉了。虽然舍不得，但是还是要忍痛割爱，不然以后孩子真的有问题，大人和孩子都受罪。不过，这个最后的决定还要你自己做，毕竟是你的宝宝。，、、、、\"...",
    "id": 536714,
    "question": "孕5个月检查右侧肾积水孩子能要吗？"
}
```

#### summarization

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 246.89 MB
- **Total amount of disk used:** 246.89 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "description": "\"宝宝有中度HIE，但原因未查明，这是他出生后脸上红的几道，嘴唇深红近紫，请问这是像缺氧的表现吗？\"...",
    "id": 173649,
    "question": "宝宝脸上红的几道嘴唇深红近紫是像缺氧的表现吗？"
}
```

#### topic_classification

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 208.89 MB
- **Total amount of disk used:** 208.89 MB

An example of 'train' looks as follows.
```
{
    "description": "媳妇怀孕五个月了经检查右侧肾积水、过了半月左侧也出现肾积水、她要拿掉孩子、怎么办？",
    "id": 536714,
    "label": 8,
    "question": "孕5个月检查右侧肾积水孩子能要吗？"
}
```

### Data Fields

The data fields are the same among all splits.

#### age_classification
- `question`: a `string` feature.
- `description`: a `string` feature.
- `label`: a classification label, with possible values including `0-1岁` (0), `1-2岁` (1), `2-3岁` (2).
- `id`: a `int32` feature.

#### qa
- `question`: a `string` feature.
- `answer`: a `string` feature.
- `id`: a `int32` feature.

#### summarization
- `description`: a `string` feature.
- `question`: a `string` feature.
- `id`: a `int32` feature.

#### topic_classification
- `question`: a `string` feature.
- `description`: a `string` feature.
- `label`: a classification label, with possible values including `产褥期保健` (0), `儿童过敏` (1), `动作发育` (2), `婴幼保健` (3), `婴幼心理` (4).
- `id`: a `int32` feature.

### Data Splits

|        name        |train |validation| test |
|--------------------|-----:|---------:|-----:|
|age_classification  |134852|     19323| 38318|
|qa                  |747888|    106842|213681|
|summarization       |747888|    106842|213681|
|topic_classification|613036|     87519|175363|

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

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@inproceedings{xu-etal-2020-matinf,
    title = "{MATINF}: A Jointly Labeled Large-Scale Dataset for Classification, Question Answering and Summarization",
    author = "Xu, Canwen  and
      Pei, Jiaxin  and
      Wu, Hongtao  and
      Liu, Yiyu  and
      Li, Chenliang",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.330",
    pages = "3586--3596",
}

```


### Contributions

Thanks to [@JetRunner](https://github.com/JetRunner) for adding this dataset.
