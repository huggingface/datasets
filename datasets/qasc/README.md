---
---

# Dataset Card for "qasc"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://allenai.org/data/qasc](https://allenai.org/data/qasc)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1.54 MB
- **Size of the generated dataset:** 5.60 MB
- **Total amount of disk used:** 7.14 MB

### [Dataset Summary](#dataset-summary)

QASC is a question-answering dataset with a focus on sentence composition. It consists of 9,980 8-way multiple-choice
questions about grade school science (8,134 train, 926 dev, 920 test), and comes with a corpus of 17M sentences.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 1.54 MB
- **Size of the generated dataset:** 5.60 MB
- **Total amount of disk used:** 7.14 MB

An example of 'validation' looks as follows.
```
{
    "answerKey": "F",
    "choices": {
        "label": ["A", "B", "C", "D", "E", "F", "G", "H"],
        "text": ["sand", "occurs over a wide range", "forests", "Global warming", "rapid changes occur", "local weather conditions", "measure of motion", "city life"]
    },
    "combinedfact": "Climate is generally described in terms of local weather conditions",
    "fact1": "Climate is generally described in terms of temperature and moisture.",
    "fact2": "Fire behavior is driven by local weather conditions such as winds, temperature and moisture.",
    "formatted_question": "Climate is generally described in terms of what? (A) sand (B) occurs over a wide range (C) forests (D) Global warming (E) rapid changes occur (F) local weather conditions (G) measure of motion (H) city life",
    "id": "3NGI5ARFTT4HNGVWXAMLNBMFA0U1PG",
    "question": "Climate is generally described in terms of what?"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `id`: a `string` feature.
- `question`: a `string` feature.
- `choices`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `label`: a `string` feature.
- `answerKey`: a `string` feature.
- `fact1`: a `string` feature.
- `fact2`: a `string` feature.
- `combinedfact`: a `string` feature.
- `formatted_question`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default| 8134|       926| 920|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

```
@article{allenai:qasc,
      author    = {Tushar Khot and Peter Clark and Michal Guerquin and Peter Jansen and Ashish Sabharwal},
      title     = {QASC: A Dataset for Question Answering via Sentence Composition},
      journal   = {arXiv:1910.11473v2},
      year      = {2020},
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun) for adding this dataset.