---
---

# Dataset Card for "guardian_authorship"

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

- **Homepage:** [http://www.icsd.aegean.gr/lecturers/stamatatos/papers/JLP2013.pdf](http://www.icsd.aegean.gr/lecturers/stamatatos/papers/JLP2013.pdf)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 47.31 MB
- **Size of the generated dataset:** 37.17 MB
- **Total amount of disk used:** 84.49 MB

### [Dataset Summary](#dataset-summary)

A dataset cross-topic authorship attribution. The dataset is provided by Stamatatos 2013.
1- The cross-topic scenarios are based on Table-4 in Stamatatos 2017 (Ex. cross_topic_1 => row 1:P S U&W ).
2- The cross-genre scenarios are based on Table-5 in the same paper. (Ex. cross_genre_1 => row 1:B P S&U&W).

3- The same-topic/genre scenario is created by grouping all the datasts as follows.
For ex., to use same_topic and split the data 60-40 use:
train_ds = load_dataset('guardian_authorship', name="cross_topic_<<#>>",
                        split='train[:60%]+validation[:60%]+test[:60%]')
tests_ds = load_dataset('guardian_authorship', name="cross_topic_<<#>>",
                        split='train[-40%:]+validation[-40%:]+test[-40%:]')

IMPORTANT: train+validation+test[:60%] will generate the wrong splits becasue the data is imbalanced

* See https://huggingface.co/docs/datasets/splits.html for detailed/more examples

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### cross_genre_1

- **Size of downloaded dataset files:** 2.96 MB
- **Size of the generated dataset:** 2.61 MB
- **Total amount of disk used:** 5.57 MB

An example of 'train' looks as follows.
```
{
    "article": "File 1a\n",
    "author": 0,
    "topic": 4
}
```

#### cross_genre_2

- **Size of downloaded dataset files:** 2.96 MB
- **Size of the generated dataset:** 2.61 MB
- **Total amount of disk used:** 5.57 MB

An example of 'validation' looks as follows.
```
{
    "article": "File 1a\n",
    "author": 0,
    "topic": 1
}
```

#### cross_genre_3

- **Size of downloaded dataset files:** 2.96 MB
- **Size of the generated dataset:** 2.61 MB
- **Total amount of disk used:** 5.57 MB

An example of 'validation' looks as follows.
```
{
    "article": "File 1a\n",
    "author": 0,
    "topic": 2
}
```

#### cross_genre_4

- **Size of downloaded dataset files:** 2.96 MB
- **Size of the generated dataset:** 2.61 MB
- **Total amount of disk used:** 5.57 MB

An example of 'validation' looks as follows.
```
{
    "article": "File 1a\n",
    "author": 0,
    "topic": 3
}
```

#### cross_topic_1

- **Size of downloaded dataset files:** 2.96 MB
- **Size of the generated dataset:** 2.23 MB
- **Total amount of disk used:** 5.18 MB

An example of 'validation' looks as follows.
```
{
    "article": "File 1a\n",
    "author": 0,
    "topic": 1
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### cross_genre_1
- `author`: a classification label, with possible values including `catherinebennett` (0), `georgemonbiot` (1), `hugoyoung` (2), `jonathanfreedland` (3), `martinkettle` (4).
- `topic`: a classification label, with possible values including `Politics` (0), `Society` (1), `UK` (2), `World` (3), `Books` (4).
- `article`: a `string` feature.

#### cross_genre_2
- `author`: a classification label, with possible values including `catherinebennett` (0), `georgemonbiot` (1), `hugoyoung` (2), `jonathanfreedland` (3), `martinkettle` (4).
- `topic`: a classification label, with possible values including `Politics` (0), `Society` (1), `UK` (2), `World` (3), `Books` (4).
- `article`: a `string` feature.

#### cross_genre_3
- `author`: a classification label, with possible values including `catherinebennett` (0), `georgemonbiot` (1), `hugoyoung` (2), `jonathanfreedland` (3), `martinkettle` (4).
- `topic`: a classification label, with possible values including `Politics` (0), `Society` (1), `UK` (2), `World` (3), `Books` (4).
- `article`: a `string` feature.

#### cross_genre_4
- `author`: a classification label, with possible values including `catherinebennett` (0), `georgemonbiot` (1), `hugoyoung` (2), `jonathanfreedland` (3), `martinkettle` (4).
- `topic`: a classification label, with possible values including `Politics` (0), `Society` (1), `UK` (2), `World` (3), `Books` (4).
- `article`: a `string` feature.

#### cross_topic_1
- `author`: a classification label, with possible values including `catherinebennett` (0), `georgemonbiot` (1), `hugoyoung` (2), `jonathanfreedland` (3), `martinkettle` (4).
- `topic`: a classification label, with possible values including `Politics` (0), `Society` (1), `UK` (2), `World` (3), `Books` (4).
- `article`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|    name     |train|validation|test|
|-------------|----:|---------:|---:|
|cross_genre_1|   63|       112| 269|
|cross_genre_2|   63|        62| 319|
|cross_genre_3|   63|        90| 291|
|cross_genre_4|   63|       117| 264|
|cross_topic_1|  112|        62| 207|

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
@article{article,
    author = {Stamatatos, Efstathios},
    year = {2013},
    month = {01},
    pages = {421-439},
    title = {On the robustness of authorship attribution based on character n-gram features},
    volume = {21},
    journal = {Journal of Law and Policy}
}

@inproceedings{stamatatos2017authorship,
    title={Authorship attribution using text distortion},
    author={Stamatatos, Efstathios},
    booktitle={Proc. of the 15th Conf. of the European Chapter of the Association for Computational Linguistics},
    volume={1}
    pages={1138--1149},
    year={2017}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@eltoto1219](https://github.com/eltoto1219), [@malikaltakrori](https://github.com/malikaltakrori) for adding this dataset.