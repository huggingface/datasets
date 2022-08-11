---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- en
license:
- mit
multilinguality:
- monolingual
pretty_name: OpenWebText2
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
- text-classification
task_ids:
- language-modeling
- masked-language-modeling
- text-scoring
---

# Dataset Card for the_pile_openwebtext2

## Table of Contents
- [Dataset Card for the_pile_openwebtext2](#dataset-card-for-the_pile_openwebtext2)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
    - [Languages](#languages)
  - [Dataset Structure](#dataset-structure)
    - [Data Instances](#data-instances)
    - [Data Fields](#data-fields)
    - [Data Splits](#data-splits)
  - [|split|num examples|](#splitnum-examples)
  - [Dataset Creation](#dataset-creation)
    - [Curation Rationale](#curation-rationale)
    - [Source Data](#source-data)
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** https://openwebtext2.readthedocs.io/en/latest/
- **Repository:** [GitHub](https://github.com/EleutherAI/openwebtext2)
- **Paper:** https://arxiv.org/abs/2101.00027
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

OpenWebText2 is part of EleutherAi/The Pile dataset and is an enhanced version of the original OpenWebTextCorpus covering all Reddit submissions from 2005 up until April 2020, with further months becoming available after the corresponding PushShift dump files are released.

|download_size|27.3 Gib|
|dataset_size|63.8 Gib|

### Supported Tasks and Leaderboards

This dataset is used for Language Modeling.

### Languages

This dataset is in English.

## Dataset Structure

### Data Instances

```
This example was too long and was cropped:

{'title': Xiaomi Mi Note 10 Gearbest Coupon Promo Code [6+128GB] [France Warehouse],
'text': '27% off Xiaomi Mi Note 10 (CC9 Pro) 108MP Penta Camera Mobile Phone Global Version Online Smartphone – Black Gearbest Coupon Promo Code\n\nGearbest Coupon Price :$439.99\n\nRegular Price : $603.19 Your Save : $163.20 Coupon Limit: 100 times Warehouse: France Expires : September 30, 2020 Coupon Valid for...',
'reddit_scores': [6],}
```

### Data Fields

- `title`: title of the web page
- `text`: text content of the web page
- `reddit_scores`: scores of the reddit submissions that mention this web page, as a list of integers

### Data Splits

|split|num examples|
--------------------------------
|train|17103059|

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

```
@article{pile,
    title={The {P}ile: An 800GB Dataset of Diverse Text for Language Modeling},
    author={Gao, Leo and Biderman, Stella and Black, Sid and Golding, Laurence and Hoppe, Travis and Foster, Charles and Phang, Jason and He, Horace and Thite, Anish and Nabeshima, Noa and Presser, Shawn and Leahy, Connor},
    journal={arXiv preprint arXiv:2101.00027},
    year={2020}
}
```

### Contributions

[researcher2](https://github.com/researcher2) Wrote much of this code, with inspiration and some straight copying of the scraping code found [here](https://github.com/yet-another-account/openwebtext/).<br/>
[sdtblck](https://github.com/sdtblck/) kindly put together the Colab notebook, and performed a chunk of the scraping. <br/>
[leogao2](https://github.com/leogao2/) provided overall design guidance, lm_dataformat, and performed another chunk of scraping. <br />
[Colaboratory](https://colab.research.google.com/) VMs helped with about 10% of our overall scraping. <br />
[The Eye](http://the-eye.eu/) host the processed datasets.<br />
[Read The Docs](https://readthedocs.org/) host our documentation.<br />

[@richarddwang](https://github.com/richarddwang) added this dataset to HF/datasets.