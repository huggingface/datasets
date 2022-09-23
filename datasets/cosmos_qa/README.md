---
annotations_creators:
- crowdsourced
language:
- en
language_creators:
- found
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: CosmosQA
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- multiple-choice
task_ids:
- multiple-choice-qa
paperswithcode_id: cosmosqa
dataset_info:
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answer0
    dtype: string
  - name: answer1
    dtype: string
  - name: answer2
    dtype: string
  - name: answer3
    dtype: string
  - name: label
    dtype: int32
  splits:
  - name: test
    num_bytes: 5121479
    num_examples: 6963
  - name: train
    num_bytes: 17159918
    num_examples: 25262
  - name: validation
    num_bytes: 2186987
    num_examples: 2985
  download_size: 24399475
  dataset_size: 24468384
---

# Dataset Card for "cosmos_qa"

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

- **Homepage:** [https://wilburone.github.io/cosmos/](https://wilburone.github.io/cosmos/)
- **Repository:** https://github.com/wilburOne/cosmosqa/
- **Paper:** [Cosmos QA: Machine Reading Comprehension with Contextual Commonsense Reasoning](https://arxiv.org/abs/1909.00277)
- **Point of Contact:** [Lifu Huang](mailto:warrior.fu@gmail.com)
- **Size of downloaded dataset files:** 23.27 MB
- **Size of the generated dataset:** 23.37 MB
- **Total amount of disk used:** 46.64 MB

### Dataset Summary

Cosmos QA is a large-scale dataset of 35.6K problems that require commonsense-based reading comprehension, formulated as multiple-choice questions. It focuses on reading between the lines over a diverse collection of people's everyday narratives, asking questions concerning on the likely causes or effects of events that require reasoning beyond the exact text spans in the context

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 23.27 MB
- **Size of the generated dataset:** 23.37 MB
- **Total amount of disk used:** 46.64 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answer0": "If he gets married in the church he wo nt have to get a divorce .",
    "answer1": "He wants to get married to a different person .",
    "answer2": "He wants to know if he does nt like this girl can he divorce her ?",
    "answer3": "None of the above choices .",
    "context": "\"Do i need to go for a legal divorce ? I wanted to marry a woman but she is not in the same religion , so i am not concern of th...",
    "id": "3BFF0DJK8XA7YNK4QYIGCOG1A95STE##3180JW2OT5AF02OISBX66RFOCTG5J7##A2LTOS0AZ3B28A##Blog_56156##q1_a1##378G7J1SJNCDAAIN46FM2P7T6KZEW2",
    "label": 1,
    "question": "Why is this person asking about divorce ?"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `id`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answer0`: a `string` feature.
- `answer1`: a `string` feature.
- `answer2`: a `string` feature.
- `answer3`: a `string` feature.
- `label`: a `int32` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|25262|      2985|6963|

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

As reported via email by Yejin Choi, the dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

### Citation Information

```
@inproceedings{huang-etal-2019-cosmos,
    title = "Cosmos {QA}: Machine Reading Comprehension with Contextual Commonsense Reasoning",
    author = "Huang, Lifu  and
      Le Bras, Ronan  and
      Bhagavatula, Chandra  and
      Choi, Yejin",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-1243",
    doi = "10.18653/v1/D19-1243",
    pages = "2391--2401",
}
```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@albertvillanova](https://github.com/albertvillanova), [@thomwolf](https://github.com/thomwolf) for adding this dataset.