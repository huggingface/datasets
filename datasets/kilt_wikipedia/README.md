---
paperswithcode_id: null
pretty_name: KiltWikipedia
---

# Dataset Card for "kilt_wikipedia"

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

- **Homepage:** [https://github.com/facebookresearch/KILT](https://github.com/facebookresearch/KILT)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 35590.05 MB
- **Size of the generated dataset:** 28011.83 MB
- **Total amount of disk used:** 63601.89 MB

### Dataset Summary

KILT-Wikipedia: Wikipedia pre-processed for KILT.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### 2019-08-01

- **Size of downloaded dataset files:** 35590.05 MB
- **Size of the generated dataset:** 28011.83 MB
- **Total amount of disk used:** 63601.89 MB

An example of 'full' looks as follows.
```
{
    "anchors": {
        "end": [],
        "href": [],
        "paragraph_id": [],
        "start": [],
        "text": [],
        "wikipedia_id": [],
        "wikipedia_title": []
    },
    "categories": "",
    "history": {
        "pageid": 0,
        "parentid": 0,
        "pre_dump": true,
        "revid": 0,
        "timestamp": "",
        "url": ""
    },
    "kilt_id": "",
    "text": {
        "paragraph": []
    },
    "wikidata_info": {
        "aliases": {
            "alias": []
        },
        "description": "",
        "enwikiquote_title": "",
        "wikidata_id": "",
        "wikidata_label": "",
        "wikipedia_title": ""
    },
    "wikipedia_id": "",
    "wikipedia_title": ""
}
```

### Data Fields

The data fields are the same among all splits.

#### 2019-08-01
- `kilt_id`: a `string` feature.
- `wikipedia_id`: a `string` feature.
- `wikipedia_title`: a `string` feature.
- `text`: a dictionary feature containing:
  - `paragraph`: a `string` feature.
- `anchors`: a dictionary feature containing:
  - `paragraph_id`: a `int32` feature.
  - `start`: a `int32` feature.
  - `end`: a `int32` feature.
  - `text`: a `string` feature.
  - `href`: a `string` feature.
  - `wikipedia_title`: a `string` feature.
  - `wikipedia_id`: a `string` feature.
- `categories`: a `string` feature.
- `description`: a `string` feature.
- `enwikiquote_title`: a `string` feature.
- `wikidata_id`: a `string` feature.
- `wikidata_label`: a `string` feature.
- `wikipedia_title`: a `string` feature.
- `aliases`: a dictionary feature containing:
  - `alias`: a `string` feature.
- `pageid`: a `int32` feature.
- `parentid`: a `int32` feature.
- `revid`: a `int32` feature.
- `pre_dump`: a `bool` feature.
- `timestamp`: a `string` feature.
- `url`: a `string` feature.

### Data Splits

|   name   | full  |
|----------|------:|
|2019-08-01|5903530|

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
@inproceedings{fb_kilt,
    author    = {Fabio Petroni and
                 Aleksandra Piktus and
                 Angela Fan and
                 Patrick Lewis and
                 Majid Yazdani and
                 Nicola De Cao and
                 James Thorne and
                 Yacine Jernite and
                 Vassilis Plachouras and
                 Tim Rockt"aschel and
                 Sebastian Riedel},
    title     = {{KILT:} a {B}enchmark for {K}nowledge {I}ntensive {L}anguage {T}asks},
    journal   = {CoRR},
    archivePrefix = {arXiv},
    year      = {2020},

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@yjernite](https://github.com/yjernite) for adding this dataset.
