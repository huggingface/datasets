---
---

# Dataset Card for "commonsense_qa"

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

- **Homepage:** [https://www.tau-nlp.org/commonsenseqa](https://www.tau-nlp.org/commonsenseqa)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 4.46 MB
- **Size of the generated dataset:** 2.08 MB
- **Total amount of disk used:** 6.54 MB

### [Dataset Summary](#dataset-summary)

CommonsenseQA is a new multiple-choice question answering dataset that requires different types of commonsense knowledge
 to predict the correct answers . It contains 12,102 questions with one correct answer and four distractor answers.
 The dataset is provided in two major training/validation/testing set splits: "Random split" which is the main evaluation
  split, and "Question token split", see paper for details.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 4.46 MB
- **Size of the generated dataset:** 2.08 MB
- **Total amount of disk used:** 6.54 MB

An example of 'train' looks as follows.
```
{
    "answerKey": "B",
    "choices": {
        "label": ["A", "B", "C", "D", "E"],
        "text": ["mildred's coffee shop", "mexico", "diner", "kitchen", "canteen"]
    },
    "question": "In what Spanish speaking North American country can you get a great cup of coffee?"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `answerKey`: a `string` feature.
- `question`: a `string` feature.
- `choices`: a dictionary feature containing:
  - `label`: a `string` feature.
  - `text`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default| 9741|      1221|1140|

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
@InProceedings{commonsense_QA,
title={COMMONSENSEQA: A Question Answering Challenge Targeting Commonsense Knowledge},
author={Alon, Talmor and Jonathan, Herzig and Nicholas, Lourie and Jonathan ,Berant},
journal={arXiv preprint arXiv:1811.00937v2},
year={2019}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@albertvillanova](https://github.com/albertvillanova), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.