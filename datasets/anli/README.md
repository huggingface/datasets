---
language:
- en
paperswithcode_id: anli
pretty_name: Adversarial NLI
---

# Dataset Card for "anli"

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

- **Homepage:** [https://github.com/facebookresearch/anli/](https://github.com/facebookresearch/anli/)
- **Repository:** [https://github.com/facebookresearch/anli/](https://github.com/facebookresearch/anli/)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 17.76 MB
- **Size of the generated dataset:** 73.55 MB
- **Total amount of disk used:** 91.31 MB

### Dataset Summary

The Adversarial Natural Language Inference (ANLI) is a new large-scale NLI benchmark dataset,
The dataset is collected via an iterative, adversarial human-and-model-in-the-loop procedure.
ANLI is much more difficult than its predecessors including SNLI and MNLI.
It contains three rounds. Each round has train/dev/test splits.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

English

## Dataset Structure

### Data Instances

#### plain_text

- **Size of downloaded dataset files:** 17.76 MB
- **Size of the generated dataset:** 73.55 MB
- **Total amount of disk used:** 91.31 MB

An example of 'train_r2' looks as follows.
```
This example was too long and was cropped:

{
    "hypothesis": "Idris Sultan was born in the first month of the year preceding 1994.",
    "label": 0,
    "premise": "\"Idris Sultan (born January 1993) is a Tanzanian Actor and comedian, actor and radio host who won the Big Brother Africa-Hotshot...",
    "reason": "",
    "uid": "ed5c37ab-77c5-4dbc-ba75-8fd617b19712"
}
```

### Data Fields

The data fields are the same among all splits.

#### plain_text
- `uid`: a `string` feature.
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).
- `reason`: a `string` feature.

### Data Splits

|   name   |train_r1|dev_r1|train_r2|dev_r2|train_r3|dev_r3|test_r1|test_r2|test_r3|
|----------|-------:|-----:|-------:|-----:|-------:|-----:|------:|------:|------:|
|plain_text|   16946|  1000|   45460|  1000|  100459|  1200|   1000|   1000|   1200|

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

[cc-4 Attribution-NonCommercial](https://github.com/facebookresearch/anli/blob/main/LICENSE)

### Citation Information

```
@InProceedings{nie2019adversarial,
    title={Adversarial NLI: A New Benchmark for Natural Language Understanding},
    author={Nie, Yixin
                and Williams, Adina
                and Dinan, Emily
                and Bansal, Mohit
                and Weston, Jason
                and Kiela, Douwe},
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    year = "2020",
    publisher = "Association for Computational Linguistics",
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@easonnie](https://github.com/easonnie), [@lhoestq](https://github.com/lhoestq), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.
