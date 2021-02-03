---
---

# Dataset Card for "winogrande"

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

- **Homepage:** [https://leaderboard.allenai.org/winogrande/submissions/get-started](https://leaderboard.allenai.org/winogrande/submissions/get-started)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 19.43 MB
- **Size of the generated dataset:** 10.01 MB
- **Total amount of disk used:** 29.44 MB

### [Dataset Summary](#dataset-summary)

WinoGrande is a new collection of 44k problems, inspired by Winograd Schema Challenge (Levesque, Davis, and Morgenstern
 2011), but adjusted to improve the scale and robustness against the dataset-specific bias. Formulated as a
fill-in-a-blank task with binary options, the goal is to choose the right option for a given sentence which requires
commonsense reasoning.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### winogrande_debiased

- **Size of downloaded dataset files:** 3.24 MB
- **Size of the generated dataset:** 1.52 MB
- **Total amount of disk used:** 4.76 MB

An example of 'train' looks as follows.
```

```

#### winogrande_l

- **Size of downloaded dataset files:** 3.24 MB
- **Size of the generated dataset:** 1.63 MB
- **Total amount of disk used:** 4.87 MB

An example of 'validation' looks as follows.
```

```

#### winogrande_m

- **Size of downloaded dataset files:** 3.24 MB
- **Size of the generated dataset:** 0.69 MB
- **Total amount of disk used:** 3.93 MB

An example of 'validation' looks as follows.
```

```

#### winogrande_s

- **Size of downloaded dataset files:** 3.24 MB
- **Size of the generated dataset:** 0.45 MB
- **Total amount of disk used:** 3.69 MB

An example of 'validation' looks as follows.
```

```

#### winogrande_xl

- **Size of downloaded dataset files:** 3.24 MB
- **Size of the generated dataset:** 5.32 MB
- **Total amount of disk used:** 8.56 MB

An example of 'train' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### winogrande_debiased
- `sentence`: a `string` feature.
- `option1`: a `string` feature.
- `option2`: a `string` feature.
- `answer`: a `string` feature.

#### winogrande_l
- `sentence`: a `string` feature.
- `option1`: a `string` feature.
- `option2`: a `string` feature.
- `answer`: a `string` feature.

#### winogrande_m
- `sentence`: a `string` feature.
- `option1`: a `string` feature.
- `option2`: a `string` feature.
- `answer`: a `string` feature.

#### winogrande_s
- `sentence`: a `string` feature.
- `option1`: a `string` feature.
- `option2`: a `string` feature.
- `answer`: a `string` feature.

#### winogrande_xl
- `sentence`: a `string` feature.
- `option1`: a `string` feature.
- `option2`: a `string` feature.
- `answer`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|       name        |train|validation|test|
|-------------------|----:|---------:|---:|
|winogrande_debiased| 9248|      1267|1767|
|winogrande_l       |10234|      1267|1767|
|winogrande_m       | 2558|      1267|1767|
|winogrande_s       |  640|      1267|1767|
|winogrande_xl      |40398|      1267|1767|

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
@InProceedings{ai2:winogrande,
title = {WinoGrande: An Adversarial Winograd Schema Challenge at Scale},
authors={Keisuke, Sakaguchi and Ronan, Le Bras and Chandra, Bhagavatula and Yejin, Choi
},
year={2019}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@TevenLeScao](https://github.com/TevenLeScao), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun) for adding this dataset.