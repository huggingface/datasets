---
---

# Dataset Card for "wiki_split"

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

- **Homepage:** [https://dataset-homepage/](https://dataset-homepage/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 95.63 MB
- **Size of the generated dataset:** 370.41 MB
- **Total amount of disk used:** 466.04 MB

### [Dataset Summary](#dataset-summary)

One million English sentences, each split into two sentences that together preserve the original meaning, extracted from Wikipedia
Google's WikiSplit dataset was constructed automatically from the publicly available Wikipedia revision history. Although
the dataset contains some inherent noise, it can serve as valuable training data for models that split or merge sentences.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 95.63 MB
- **Size of the generated dataset:** 370.41 MB
- **Total amount of disk used:** 466.04 MB

An example of 'train' looks as follows.
```
{
    "complex_sentence": " '' As she translates from one language to another , she tries to find the appropriate wording and context in English that would correspond to the work in Spanish her poems and stories started to have differing meanings in their respective languages .",
    "simple_sentence_1": "' '' As she translates from one language to another , she tries to find the appropriate wording and context in English that would correspond to the work in Spanish . ",
    "simple_sentence_2": " Ergo , her poems and stories started to have differing meanings in their respective languages ."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `complex_sentence`: a `string` feature.
- `simple_sentence_1`: a `string` feature.
- `simple_sentence_2`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train |validation|test|
|-------|-----:|---------:|---:|
|default|989944|      5000|5000|

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
@InProceedings{BothaEtAl2018,
  title = {{Learning To Split and Rephrase From Wikipedia Edit History}},
  author = {Botha, Jan A and Faruqui, Manaal and Alex, John and Baldridge, Jason and Das, Dipanjan},
  booktitle = {Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing},
  pages = {to appear},
  note = {arXiv preprint arXiv:1808.09468},
  year = {2018}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@albertvillanova](https://github.com/albertvillanova), [@lewtun](https://github.com/lewtun) for adding this dataset.