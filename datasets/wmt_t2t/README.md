---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- de
- en
license:
- unknown
multilinguality:
- translation
size_categories:
- 10M<n<100M
source_datasets:
- extended|europarl_bilingual
- extended|news_commentary
- extended|opus_paracrawl
- extended|un_multi
task_categories:
- translation
task_ids: []
pretty_name: WMT T2T
paperswithcode_id: null
---

# Dataset Card for "wmt_t2t"

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

- **Homepage:** [https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/data_generators/translate_ende.py](https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/data_generators/translate_ende.py)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1647.72 MB
- **Size of the generated dataset:** 1322.40 MB
- **Total amount of disk used:** 2970.12 MB

### Dataset Summary

The WMT EnDe Translate dataset used by the Tensor2Tensor library.

Translation dataset based on the data from statmt.org.

Versions exist for different years using a combination of data
sources. The base `wmt` allows you to create a custom dataset by choosing
your own data/language pair. This can be done as follows:

```python
from datasets import inspect_dataset, load_dataset_builder

inspect_dataset("wmt_t2t", "path/to/scripts")
builder = load_dataset_builder(
    "path/to/scripts/wmt_utils.py",
    language_pair=("fr", "de"),
    subsets={
        datasets.Split.TRAIN: ["commoncrawl_frde"],
        datasets.Split.VALIDATION: ["euelections_dev2019"],
    },
)

# Standard version
builder.download_and_prepare()
ds = builder.as_dataset()

# Streamable version
ds = builder.as_streaming_dataset()
```

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### de-en

- **Size of downloaded dataset files:** 1647.72 MB
- **Size of the generated dataset:** 1322.40 MB
- **Total amount of disk used:** 2970.12 MB

An example of 'validation' looks as follows.
```
{
    "translation": {
        "de": "Just a test sentence.",
        "en": "Just a test sentence."
    }
}
```

### Data Fields

The data fields are the same among all splits.

#### de-en
- `translation`: a multilingual `string` variable, with possible languages including `de`, `en`.

### Data Splits

|name | train |validation|test|
|-----|------:|---------:|---:|
|de-en|4592289|      3000|3003|

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

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```

@InProceedings{bojar-EtAl:2014:W14-33,
  author    = {Bojar, Ondrej  and  Buck, Christian  and  Federmann, Christian  and  Haddow, Barry  and  Koehn, Philipp  and  Leveling, Johannes  and  Monz, Christof  and  Pecina, Pavel  and  Post, Matt  and  Saint-Amand, Herve  and  Soricut, Radu  and  Specia, Lucia  and  Tamchyna, Ale{s}},
  title     = {Findings of the 2014 Workshop on Statistical Machine Translation},
  booktitle = {Proceedings of the Ninth Workshop on Statistical Machine Translation},
  month     = {June},
  year      = {2014},
  address   = {Baltimore, Maryland, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {12--58},
  url       = {http://www.aclweb.org/anthology/W/W14/W14-3302}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.