---
language:
- en
paperswithcode_id: wiqa
pretty_name: What-If Question Answering
---

# Dataset Card for "wiqa"

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

- **Homepage:** [https://allenai.org/data/wiqa](https://allenai.org/data/wiqa)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 5.00 MB
- **Size of the generated dataset:** 21.36 MB
- **Total amount of disk used:** 26.37 MB

### Dataset Summary

The WIQA dataset V1 has 39705 questions containing a perturbation and a possible effect in the context of a paragraph.
The dataset is split into 29808 train questions, 6894 dev questions and 3003 test questions.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 5.00 MB
- **Size of the generated dataset:** 21.36 MB
- **Total amount of disk used:** 26.37 MB

An example of 'validation' looks as follows.
```
{
    "answer_label": "more",
    "answer_label_as_choice": "A",
    "choices": {
        "label": ["A", "B", "C"],
        "text": ["more", "less", "no effect"]
    },
    "metadata_graph_id": "481",
    "metadata_para_id": "528",
    "metadata_path_len": 3,
    "metadata_question_id": "influence_graph:528:481:77#0",
    "metadata_question_type": "INPARA_EFFECT",
    "question_para_step": ["A male and female rabbit mate", "The female rabbit becomes pregnant", "Baby rabbits form inside of the mother rabbit", "The female rabbit gives birth to a litter", "The newborn rabbits grow up to become adults", "The adult rabbits find mates."],
    "question_stem": "suppose the female is sterile happens, how will it affect LESS rabbits."
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `question_stem`: a `string` feature.
- `question_para_step`: a `list` of `string` features.
- `answer_label`: a `string` feature.
- `answer_label_as_choice`: a `string` feature.
- `choices`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `label`: a `string` feature.
- `metadata_question_id`: a `string` feature.
- `metadata_graph_id`: a `string` feature.
- `metadata_para_id`: a `string` feature.
- `metadata_question_type`: a `string` feature.
- `metadata_path_len`: a `int32` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|29808|      6894|3003|

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
@article{wiqa,
      author    = {Niket Tandon and Bhavana Dalvi Mishra and Keisuke Sakaguchi and Antoine Bosselut and Peter Clark}
      title     = {WIQA: A dataset for "What if..." reasoning over procedural text},
      journal   = {arXiv:1909.04739v1},
      year      = {2019},
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
