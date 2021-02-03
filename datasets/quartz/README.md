---
---

# Dataset Card for "quartz"

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

- **Homepage:** [https://allenai.org/data/quartz](https://allenai.org/data/quartz)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.47 MB
- **Size of the generated dataset:** 1.64 MB
- **Total amount of disk used:** 2.12 MB

### [Dataset Summary](#dataset-summary)

QuaRTz is a crowdsourced dataset of 3864 multiple-choice questions about open domain qualitative relationships. Each
question is paired with one of 405 different background sentences (sometimes short paragraphs).
The QuaRTz dataset V1 contains 3864 questions about open domain qualitative relationships. Each question is paired with
one of 405 different background sentences (sometimes short paragraphs).

The dataset is split into train (2696), dev (384) and test (784). A background sentence will only appear in a single split.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 0.47 MB
- **Size of the generated dataset:** 1.64 MB
- **Total amount of disk used:** 2.12 MB

An example of 'train' looks as follows.
```
{
    "answerKey": "A",
    "choices": {
        "label": ["A", "B"],
        "text": ["higher", "lower"]
    },
    "id": "QRQA-10116-3",
    "para": "Electrons at lower energy levels, which are closer to the nucleus, have less energy.",
    "para_anno": {
        "cause_dir_sign": "LESS",
        "cause_dir_str": "closer",
        "cause_prop": "distance from a nucleus",
        "effect_dir_sign": "LESS",
        "effect_dir_str": "less",
        "effect_prop": "energy"
    },
    "para_id": "QRSent-10116",
    "question": "Electrons further away from a nucleus have _____ energy levels than close ones.",
    "question_anno": {
        "less_cause_dir": "electron energy levels",
        "less_cause_prop": "nucleus",
        "less_effect_dir": "lower",
        "less_effect_prop": "electron energy levels",
        "more_effect_dir": "higher",
        "more_effect_prop": "electron energy levels"
    }
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
- `para`: a `string` feature.
- `para_id`: a `string` feature.
- `effect_prop`: a `string` feature.
- `cause_dir_str`: a `string` feature.
- `effect_dir_str`: a `string` feature.
- `cause_dir_sign`: a `string` feature.
- `effect_dir_sign`: a `string` feature.
- `cause_prop`: a `string` feature.
- `more_effect_dir`: a `string` feature.
- `less_effect_dir`: a `string` feature.
- `less_cause_prop`: a `string` feature.
- `more_effect_prop`: a `string` feature.
- `less_effect_prop`: a `string` feature.
- `less_cause_dir`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default| 2696|       384| 784|

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
@InProceedings{quartz,
  author = {Oyvind Tafjord and Matt Gardner and Kevin Lin and Peter Clark},
  title = {"QUARTZ: An Open-Domain Dataset of Qualitative Relationship
Questions"},

  year = {"2019"},
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf) for adding this dataset.