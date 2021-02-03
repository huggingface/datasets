---
---

# Dataset Card for "discofuse"

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

- **Homepage:** [https://github.com/google-research-datasets/discofuse](https://github.com/google-research-datasets/discofuse)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 5764.06 MB
- **Size of the generated dataset:** 20547.64 MB
- **Total amount of disk used:** 26311.70 MB

### [Dataset Summary](#dataset-summary)

 DISCOFUSE is a large scale dataset for discourse-based sentence fusion.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### discofuse-sport

- **Size of downloaded dataset files:** 4126.20 MB
- **Size of the generated dataset:** 14341.49 MB
- **Total amount of disk used:** 18467.70 MB

An example of 'train' looks as follows.
```
{
    "coherent_first_sentence": "Four LPr and three LC2000r HP Netservers handle customer management and web server functions .",
    "coherent_second_sentence": "Finally , an HP Netserver LT6000r hosts i2 Demand Planner and i2 Collaboration Planner .",
    "connective_string": "finally ,",
    "discourse_type": "PAIR_CONN",
    "has_coref_type_nominal": 0.0,
    "has_coref_type_pronoun": 0.0,
    "incoherent_first_sentence": "Four LPr and three LC2000r HP Netservers handle customer management and web server functions .",
    "incoherent_second_sentence": "An HP Netserver LT6000r hosts i2 Demand Planner and i2 Collaboration Planner ."
}
```

#### discofuse-wikipedia

- **Size of downloaded dataset files:** 1637.86 MB
- **Size of the generated dataset:** 6206.14 MB
- **Total amount of disk used:** 7844.01 MB

An example of 'validation' looks as follows.
```
{
    "coherent_first_sentence": "Four LPr and three LC2000r HP Netservers handle customer management and web server functions .",
    "coherent_second_sentence": "Finally , an HP Netserver LT6000r hosts i2 Demand Planner and i2 Collaboration Planner .",
    "connective_string": "finally ,",
    "discourse_type": "PAIR_CONN",
    "has_coref_type_nominal": 0.0,
    "has_coref_type_pronoun": 0.0,
    "incoherent_first_sentence": "Four LPr and three LC2000r HP Netservers handle customer management and web server functions .",
    "incoherent_second_sentence": "An HP Netserver LT6000r hosts i2 Demand Planner and i2 Collaboration Planner ."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### discofuse-sport
- `connective_string`: a `string` feature.
- `discourse_type`: a `string` feature.
- `coherent_second_sentence`: a `string` feature.
- `has_coref_type_pronoun`: a `float32` feature.
- `incoherent_first_sentence`: a `string` feature.
- `incoherent_second_sentence`: a `string` feature.
- `has_coref_type_nominal`: a `float32` feature.
- `coherent_first_sentence`: a `string` feature.

#### discofuse-wikipedia
- `connective_string`: a `string` feature.
- `discourse_type`: a `string` feature.
- `coherent_second_sentence`: a `string` feature.
- `has_coref_type_pronoun`: a `float32` feature.
- `incoherent_first_sentence`: a `string` feature.
- `incoherent_second_sentence`: a `string` feature.
- `has_coref_type_nominal`: a `float32` feature.
- `coherent_first_sentence`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|       name        | train  |validation| test |
|-------------------|-------:|---------:|-----:|
|discofuse-sport    |43291020|    440902|445521|
|discofuse-wikipedia|16310585|    168081|163657|

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
@InProceedings{GevaEtAl2019,
  title = {DiscoFuse: A Large-Scale Dataset for Discourse-Based Sentence Fusion},
  author = {Geva, Mor and Malmi, Eric and Szpektor, Idan and Berant, Jonathan},
  booktitle = {Proceedings of the 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics},
  note = {arXiv preprint arXiv:1902.10526},
  year = {2019}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham), [@lewtun](https://github.com/lewtun) for adding this dataset.