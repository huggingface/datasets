---
---

# Dataset Card for "art"

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

- **Homepage:** [https://leaderboard.allenai.org/anli/submissions/get-started](https://leaderboard.allenai.org/anli/submissions/get-started)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 4.88 MB
- **Size of the generated dataset:** 32.77 MB
- **Total amount of disk used:** 37.65 MB

### [Dataset Summary](#dataset-summary)

the Abductive Natural Language Inference Dataset from AI2

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### anli

- **Size of downloaded dataset files:** 4.88 MB
- **Size of the generated dataset:** 32.77 MB
- **Total amount of disk used:** 37.65 MB

An example of 'train' looks as follows.
```
{
    "hypothesis_1": "Chad's car had all sorts of other problems besides alignment.",
    "hypothesis_2": "Chad's car had all sorts of benefits other than being sexy.",
    "label": 1,
    "observation_1": "Chad went to get the wheel alignment measured on his car.",
    "observation_2": "The mechanic provided a working alignment with new body work."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### anli
- `observation_1`: a `string` feature.
- `observation_2`: a `string` feature.
- `hypothesis_1`: a `string` feature.
- `hypothesis_2`: a `string` feature.
- `label`: a classification label, with possible values including `0` (0), `1` (1), `2` (2).

### [Data Splits Sample Size](#data-splits-sample-size)

|name|train |validation|
|----|-----:|---------:|
|anli|169654|      1532|

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
@InProceedings{anli,
  author = "Chandra, Bhagavatula
    and Ronan, Le Bras
    and Chaitanya, Malaviya
    and Keisuke, Sakaguchi
    and Ari, Holtzman
    and Hannah, Rashkin
    and Doug, Downey
    and Scott, Wen-tau Yih
    and Yejin, Choi",
  title = "Abductive Commonsense Reasoning",
  year = "2020",
}
```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham), [@lewtun](https://github.com/lewtun), [@lhoestq](https://github.com/lhoestq) for adding this dataset.