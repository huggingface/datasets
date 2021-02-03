---
---

# Dataset Card for "docred"

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

- **Homepage:** [https://github.com/thunlp/DocRED](https://github.com/thunlp/DocRED)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 20.03 MB
- **Size of the generated dataset:** 19.19 MB
- **Total amount of disk used:** 39.23 MB

### [Dataset Summary](#dataset-summary)

Multiple entities in a document generally exhibit complex inter-sentence relations, and cannot be well handled by existing relation extraction (RE) methods that typically focus on extracting intra-sentence relations for single entity pairs. In order to accelerate the research on document-level RE, we introduce DocRED, a new dataset constructed from Wikipedia and Wikidata with three features:
    - DocRED annotates both named entities and relations, and is the largest human-annotated dataset for document-level RE from plain text.
    - DocRED requires reading multiple sentences in a document to extract entities and infer their relations by synthesizing all information of the document.
    - Along with the human-annotated data, we also offer large-scale distantly supervised data, which enables DocRED to be adopted for both supervised and weakly supervised scenarios.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 20.03 MB
- **Size of the generated dataset:** 19.19 MB
- **Total amount of disk used:** 39.23 MB

An example of 'train_annotated' looks as follows.
```
{
    "labels": {
        "evidence": [[0]],
        "head": [0],
        "relation_id": ["P1"],
        "relation_text": ["is_a"],
        "tail": [0]
    },
    "sents": [["This", "is", "a", "sentence"], ["This", "is", "another", "sentence"]],
    "title": "Title of the document",
    "vertexSet": [[{
        "name": "sentence",
        "pos": [3],
        "sent_id": 0,
        "type": "NN"
    }, {
        "name": "sentence",
        "pos": [3],
        "sent_id": 1,
        "type": "NN"
    }], [{
        "name": "This",
        "pos": [0],
        "sent_id": 0,
        "type": "NN"
    }]]
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `title`: a `string` feature.
- `sents`: a dictionary feature containing:
  - `feature`: a `string` feature.
- `name`: a `string` feature.
- `sent_id`: a `int32` feature.
- `pos`: a `list` of `int32` features.
- `type`: a `string` feature.
- `labels`: a dictionary feature containing:
  - `head`: a `int32` feature.
  - `tail`: a `int32` feature.
  - `relation_id`: a `string` feature.
  - `relation_text`: a `string` feature.
  - `evidence`: a `list` of `int32` features.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train_annotated|train_distant|validation|test|
|-------|--------------:|------------:|---------:|---:|
|default|           3053|         1000|      1000|1000|

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
@inproceedings{yao2019DocRED,
  title={{DocRED}: A Large-Scale Document-Level Relation Extraction Dataset},
  author={Yao, Yuan and Ye, Deming and Li, Peng and Han, Xu and Lin, Yankai and Liu, Zhenghao and Liu,   Zhiyuan and Huang, Lixin and Zhou, Jie and Sun, Maosong},
  booktitle={Proceedings of ACL 2019},
  year={2019}
}

```


### Contributions

Thanks to [@ghomasHudson](https://github.com/ghomasHudson), [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq) for adding this dataset.